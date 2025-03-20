from phystool.physgit import PhysGit


def run_A() -> None:
    pg = PhysGit()
    print(pg.get_remote_url())


if __name__ == "__main__":
    run_A()
