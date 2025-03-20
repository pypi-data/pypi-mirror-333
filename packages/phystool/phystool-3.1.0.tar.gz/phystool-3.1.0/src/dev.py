from phystool.physgit import PhysGit
from phystool.helper import progress_bar
from time import sleep


def run_A() -> None:
    pg = PhysGit()
    for s, fs in pg._git_map.items():
        print(fs.message())


def run_B() -> None:
    n = 40
    for i in range(n):
        progress_bar(n, i+1, 20, "coucou")
        sleep(0.25)


if __name__ == "__main__":
    run_B()
