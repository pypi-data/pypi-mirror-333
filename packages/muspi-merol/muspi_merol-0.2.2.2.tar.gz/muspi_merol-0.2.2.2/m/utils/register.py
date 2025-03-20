from contextlib import suppress
from pathlib import Path
from shutil import which
from sys import executable, path

from typer import Typer

if (cwd := str(Path.cwd())) not in path:
    path.append(cwd)

if venv_python := which("python"):
    p = Path(venv_python)
    if not p.samefile(executable) and p.is_relative_to(cwd):
        from subprocess import CalledProcessError, run

        with suppress(CalledProcessError):
            site_packages: list[str] = eval(run([venv_python, "-c", "import site; print(repr(site.getsitepackages()))"], capture_output=True, text=True, check=True).stdout)
            path.extend(site_packages)

            from site import addsitepackages

            addsitepackages(set(site_packages))


def get_commands():
    from importlib import import_module
    from pkgutil import iter_modules

    commands = import_module("m.commands")

    for info in iter_modules(commands.__path__):
        module = import_module(f"m.commands.{info.name}")
        app = getattr(module, "app")
        if isinstance(app, Typer):
            yield app
        elif app is None:
            print(f"{info.name} is not a command")
        else:
            raise TypeError(f"{app} is not a Typer app")
