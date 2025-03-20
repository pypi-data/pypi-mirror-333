import subprocess
import re

from abc import ABC, abstractmethod
from enum import Enum
from git import Repo
from git.exc import (
    GitCommandError,
    InvalidGitRepositoryError
)
from logging import getLogger
from pathlib import Path
from shutil import rmtree
from typing import Iterator

from phystool.config import config
from phystool.pdbfile import PDBFile
from phystool.helper import (
    terminal_yes_no,
    silent_keyboard_interrupt
)

logger = getLogger(__name__)


class GitFile(ABC):
    class Status(Enum):
        NEW = 0
        MODIFIED = 1
        REMOVED = 2

    def __init__(self, status: Status, path: Path):
        self._files: dict[str, str] = {}
        self.uuid = path.stem
        self.status = status
        self.title = ""
        self.add(path)

    @abstractmethod
    def add(self, path: Path) -> None:
        ...

    def message(self) -> str:
        exts = "/".join(
            [
                suffix
                for suffix, path in self._files.items()
                if path
            ]
        )
        return f"{self.status.name[0]}: {self.uuid} {exts}"

    def _commands(self) -> Iterator[str]:
        for suffix, path in self._files.items():
            if path:
                if self.status == self.Status.NEW:
                    yield f"bat --color always -l {suffix} {path}"
                elif self.status == self.Status.MODIFIED:
                    yield f"git diff {path} | delta {config.PDB_DELTA_THEME}"
                else:
                    yield f"git show HEAD:{path} | bat --color always -l {suffix}"  # noqa

    def get_files(self) -> list[str]:
        return list(self._files.values())

    def get_diff(self) -> str:
        out = ""
        for cmd in self._commands():
            tmp = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                shell=True,
                cwd=config.PDB_DB_DIR
            )
            if tmp.returncode == 0:
                out += tmp.stdout
            else:
                logger.warning(f"git diff failed ({tmp.returncode})")
                logger.warning(tmp.stderr)
        return out

    def display_diff(self) -> None:
        for cmd in self._commands():
            subprocess.run(
                cmd,
                shell=True,
                cwd=config.PDB_DB_DIR
            )


class GitPDBFile(GitFile):
    def __init__(self, status: GitFile.Status, path: Path):
        self.n = 0
        super().__init__(status, path)

    def add(self, path: Path) -> None:
        if path.stem != self.uuid:
            logger.error(f"Non matching uuids ({path.stem} != {self.uuid})")
            raise ValueError(f"{path.stem} != {self.uuid}")

        self._files[path.suffix[1:]] = str(path.relative_to(config.PDB_DB_DIR))
        if not self.n:
            self.n += 1

        if self.status == self.Status.REMOVED:
            self.title = self.uuid
        else:
            pdb_file = PDBFile.open(path.stem)
            self.title = pdb_file.title


class GitTexFile(GitFile):
    def add(self, path: Path) -> None:
        self._files[path.suffix[1:]] = str(path.relative_to(config.PDB_DB_DIR))
        self.title = path.name


class PhysGit:
    def __init__(self) -> None:
        """
        Helper class to manage PDBFile stored in config.PDB_DB_DIR. If the
        directory is not a valid git repository it raises
        InvalidGitRepositoryError. To properly initialize the repository, use
        setup_git_repository(remote_url: str) where remote_url points to an
        empty remote repository.

        Takes a set of .tex/.json paths as input and returns the number of
        checked files with a list containing information about those files.
        That list contains the list of modified files (.tex and/or .json) for
        each selected pdb_file.

        To have a nicer git diff experience, this helper class uses bat and
        delta (named git-delta in debian package manager).
        """
        self._repo = Repo(config.PDB_DB_DIR)

        self._git_map: dict[str, GitFile] = {}
        self._check_status(
            GitPDBFile,
            set(config.PDB_DB_DIR.glob("*.tex"))
            | set(config.PDB_DB_DIR.glob("*.json"))
        )
        self._check_status(
            GitTexFile,
            set(config.PDB_LATEX_ENV._source.glob("*.cls"))
            | set(config.PDB_LATEX_ENV._source.glob("*.sty"))
        )
        self._staged: dict[GitFile.Status, tuple[list[GitFile], int]] = {
            status: ([], 0)
            for status in GitFile.Status
        }

    def __len__(self) -> int:
        return len(self._git_map)

    def __getitem__(self, uuid: str) -> GitFile:
        return self._git_map[uuid]

    def __iter__(self) -> Iterator[tuple[str, GitFile]]:
        return iter(self._git_map.items())

    def _check_status(
        self,
        git_file_class: type[GitFile],
        trackable: set[Path]
    ) -> None:
        self._add_to_status(
            git_file_class,
            GitFile.Status.NEW,
            (
                {
                    config.PDB_DB_DIR / item
                    for item in self._repo.untracked_files
                } & trackable
            )
        )
        self._add_to_status(
            git_file_class,
            GitFile.Status.MODIFIED,
            (
                {
                    config.PDB_DB_DIR / item.a_path
                    for item in self._repo.index.diff(None)
                } & trackable
            )
        )
        self._add_to_status(
            git_file_class,
            GitFile.Status.REMOVED,
            {
                config.PDB_DB_DIR / item.a_path
                for item in self._repo.index.diff(None)
                if item.deleted_file
            },
        )

    def _add_to_status(
        self,
        git_file_class: type[GitFile],
        status: GitFile.Status,
        paths: set[Path]
    ) -> None:
        for path in paths:
            if gpdb := self._git_map.get(path.stem, None):
                gpdb.add(path)
            else:
                self._git_map[path.stem] = git_file_class(status, path)

    def _get_git_message(self) -> str:
        return "{}\n\n{}".format(
            ", ".join(
                [
                    f"{len(list_staged)} ({n}) {status.name}"
                    for status, (list_staged, n) in self._staged.items()
                    if n
                ]
            ),
            "\n".join(
                git_pdb_file.message()
                for list_staged, _ in self._staged.values()
                for git_pdb_file in list_staged
            )
        )

    @silent_keyboard_interrupt
    def interactive_staging(self) -> None:
        by_status: dict[GitFile.Status, list[GitFile]] = {
            status: []
            for status in GitFile.Status
        }
        maxlen = 0
        for _, git_pdb_file in self:
            by_status[git_pdb_file.status].append(git_pdb_file)
            if len(git_pdb_file.title) > maxlen:
                maxlen = len(git_pdb_file.title)

        for status, list_sorted in by_status.items():
            for git_pdb_file in list_sorted:
                git_pdb_file.display_diff()
                if terminal_yes_no(
                    f"{git_pdb_file.title: <{maxlen}} -> stage {status.name}?"
                ):
                    self.stage(git_pdb_file.uuid)

    def stage(self, uuid: str) -> None:
        git_pdb_file = self[uuid]
        list_staged, n = self._staged[git_pdb_file.status]
        list_staged.append(git_pdb_file)
        self._staged[git_pdb_file.status] = list_staged, n+1

    def commit(self, for_terminal: bool) -> None:
        if not any([k[0] for k in self._staged.values()]):
            logger.info("Nothing was staged, git is left untouched")
            return

        git_msg = self._get_git_message()
        logger.info("Review Git actions")
        logger.info(git_msg)
        if for_terminal and not terminal_yes_no("Commit those changes?"):
            return

        for git_pdb_file in self._staged[GitFile.Status.NEW][0]:
            self._repo.index.add(git_pdb_file.get_files())
        for git_pdb_file in self._staged[GitFile.Status.MODIFIED][0]:
            self._repo.index.add(git_pdb_file.get_files())
        for git_pdb_file in self._staged[GitFile.Status.REMOVED][0]:
            self._repo.index.remove(git_pdb_file.get_files())

        self._repo.index.commit(git_msg)

        try:
            origin = self._repo.remote()
            for info in origin.push():
                logger.info(
                    f"{info.local_ref}, {info.remote_ref}, {info.summary}"
                )
        except GitCommandError as e:
            if e.status == 128:
                logger.warning(f"No internet, can't push to {origin}")
            else:
                logger.error("Something went wrong, see the logs")
                logger.error(e)
        except ValueError:
            logger.warning("No remote found")

    def get_diff(self, uuid: str) -> str:
        return self[uuid].get_diff()

    def get_remote_url(self) -> str:
        return self._repo.remote().url


@silent_keyboard_interrupt
def run_git_in_terminal():
    try:
        if terminal_yes_no("Git?"):
            git = PhysGit()
            git.interactive_staging()
            git.commit(for_terminal=True)
    except InvalidGitRepositoryError:
        print("The database is not managed by git.")
        setup_git_repository(
            input("Enter url of remote git repository: ")
        )
    input("Press any key to quit.")
    return


def setup_git_repository(remote_url: str) -> None:
    is_valid_remote = False
    repo = Repo.init(config.PDB_DB_DIR)
    if re.match("git@(.*):(.*).git", remote_url):
        repo.create_remote('origin', remote_url)
        try:
            if repo.git.ls_remote():
                msg = "The remote is not empty."
            else:
                is_valid_remote = True
        except GitCommandError as e:
            if e.status == 128:
                msg = "The remote can't be found."
            else:
                msg = str(e)
        except Exception as e:
            msg = str(e)
    else:
        msg = "The url is not formatted correctly."

    if not is_valid_remote:
        rmtree(repo.git_dir)
        raise InvalidGitRepositoryError(msg)

    gitignore = config.PDB_DB_DIR / ".gitignore"
    with gitignore.open("wt") as gf:
        gf.write(
            "\n".join(["0_metadata.pkl", "/*.pdf"])
        )
    repo.index.add([str(gitignore)])

    repo.index.commit("initial commit: setup gitconfig")
    repo.git.add(update=True)
    repo.git.push('--set-upstream', 'origin', 'master')
    repo.remote("origin").push()
    logger.info("The git repository was correctly initialized")
