from .cli import build


def run_dev_build():
    # This will run by itself as a command, so it can exit()
    build(["--watch"], standalone_mode=True)


def run_build():
    # Standalone mode prevents it from exit()ing
    build(["--minify"], standalone_mode=False)
