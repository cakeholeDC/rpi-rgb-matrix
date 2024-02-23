from pathlib import Path

from invoke import task

GIT_ROOT = Path(__file__).resolve().parent
APP_ROOT = GIT_ROOT / "impl"


@task
def setup(context):
    """
    Poetry install
    """
    with context.cd(GIT_ROOT):
        context.run(f"poetry install --no-root", pty=True)

@task
def clean(context):
    """
    rm -rf poetry.lock .venv
    """
    with context.cd(GIT_ROOT):
        context.run(f"rm -rf .venv poetry.lock", pty=True)

@task
def run64(context, emulate=True, fullscreen=False):
    """
    runs the 64x64 RGB matrix. emulation=True by default
    """
    with context.cd(APP_ROOT):
        emulate = "-e" if emulate else ''
        fullscreen = "-f" if fullscreen else ''
        context.run(f"poetry run python controller_v3.py {emulate} {fullscreen}", pty=True)

@task
def run32(context, emulate=True, fullscreen=False):
    """
    runs the 64x32 RGB matrix. emulation=True by default
    """
    with context.cd(APP_ROOT):
        emulate = "-e" if emulate else ''
        fullscreen = "-f" if fullscreen else ''
        context.run(f"poetry run python controller_62x32.py {emulate} {fullscreen}", pty=True)
