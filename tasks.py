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
def emualte(context, emulate=True, fullscreen=False):
    """
    emulates the RGB matrix
    """
    with context.cd(APP_ROOT):
        emulate = "-e" if emulate else ''
        fullscreen = "-f" if fullscreen else ''
        context.run(f"poetry run python controller_v3.py {emulate} {fullscreen}", pty=True)

@task
def half(context, emulate=True):
    """
    emulates the RGB matrix; half size
    """
    with context.cd(APP_ROOT):
        emulate = "-e" if emulate else ''
        context.run(f"poetry run python controller_half.py {emulate}", pty=True)
        # context.run(f"poetry run python controller_kc.py {emulate}")
