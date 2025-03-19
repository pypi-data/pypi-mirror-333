from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nox

DIR = Path(__file__).parent.resolve()

nox.options.sessions = ["lint", "pylint", "tests"]


@nox.session(reuse_venv=True)
def lint(session: nox.Session) -> None:
    """
    Run the linter.
    """
    session.install("pre-commit")
    session.run(
        "pre-commit", "run", "--all-files", "--show-diff-on-failure", *session.posargs
    )


@nox.session
def pylint(session: nox.Session) -> None:
    """
    Run PyLint.
    """
    # This needs to be installed into the package environment, and is slower
    # than a pre-commit check
    session.install(".", "pylint")
    session.run("pylint", "pysubconverter", *session.posargs)


@nox.session
def tests(session: nox.Session) -> None:
    """
    Run the unit and regular tests.
    """
    session.install(".[test]")
    session.run("pytest", *session.posargs)


@nox.session(reuse_venv=True)
def docs(session: nox.Session) -> None:
    """
    Build the docs. Pass "-- --help" to show helps.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--serve", action="store_true", help="Serve after building")
    parser.add_argument(
        "--check", action="store_true", help="Checks the docs with warnings as errors."
    )
    args, posargs = parser.parse_known_args(session.posargs)

    session.install("-e.[docs]")

    shared_args = [
        "build",
        "-d",
        "docs/_build/html",
        *posargs,
    ]

    if args.check:
        shared_args.append("--strict")

    if args.serve:
        session.run("mkdocs", "serve", *posargs)
    else:
        session.run("mkdocs", *shared_args)


@nox.session
def build(session: nox.Session) -> None:
    """
    Build an SDist and wheel.
    """

    build_path = DIR.joinpath("build")
    if build_path.exists():
        shutil.rmtree(build_path)

    session.install("build")
    session.run("python", "-m", "build")


@nox.session(reuse_venv=True)
def pyi(session: nox.Session) -> None:
    """
    Generate the Pyi type stubs.
    """
    session.install("pybind11-stubgen")
    session.install(".[test]")
    session.run("pybind11-stubgen", "pysubconverter._core", "-o", "src")
