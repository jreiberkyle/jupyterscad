"""
Jupyter SCAD
Copyright (C) 2023 Jennifer Reiber Kyle

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <https://www.gnu.org/licenses/>.
"""
from pathlib import Path
import shutil

import nox

BUILD_DIRS = ["build", "dist"]

nox.options.stop_on_first_error = True
nox.options.reuse_existing_virtualenvs = False

nox.options.sessions = ["format", "lint", "analyze", "test"]


@nox.session(python=["3.8", "3.9", "3.10", "3.11", "3.12"])
def test(session):
    session.install(".[test]")

    options = session.posargs
    session.run("python", "-m", "pytest", "-v", *options)


@nox.session
def format(session):
    errors = []

    session.install("isort")
    try:
        session.run("python", "-m", "isort", "--check-only", "src", "tests")
    except nox.command.CommandFailed:
        errors.append(
            "isort check failed. Pip install isort then run "
            "'python -m isort src tests' to format files"
        )

    session.install("black")
    try:
        session.run("python", "-m", "black", "--check", "src", "tests")
    except nox.command.CommandFailed:
        errors.append(
            "Black check failed. Pip install black then run "
            "'python -m black src tests' to format files"
        )

    if errors:
        session.error(f"The following format error(s) occurred: {errors}")


@nox.session
def lint(session):
    session.install("flake8")

    session.run("flake8", "src")


@nox.session
def analyze(session):
    session.install("mypy")

    session.run("mypy", "--ignore-missing", "src")


@nox.session
def build(session):
    """Build package"""
    # check preexisting
    exist_but_should_not = [p for p in BUILD_DIRS if Path(p).is_dir()]
    if exist_but_should_not:
        session.error(
            f"Pre-existing {', '.join(exist_but_should_not)}. "
            "Run clean session and try again"
        )

    session.install("build", "twine", "check-wheel-contents")

    session.run(*"python -m build --sdist --wheel".split())
    session.run("check-wheel-contents", "dist")


@nox.session
def clean(session):
    """Remove build directories"""
    to_remove = [Path(d) for d in BUILD_DIRS if Path(d).is_dir()]
    for p in to_remove:
        shutil.rmtree(p)


@nox.session
def publish_testpypi(session):
    """Publish to TestPyPi using API token"""
    _publish(session, "testpypi")


@nox.session
def publish_pypi(session):
    """Publish to PyPi using API token"""
    _publish(session, "pypi")


def _publish(session, repository):
    missing = [p for p in BUILD_DIRS if not Path(p).is_dir()]
    if missing:
        session.error(
            f"Missing one or more build directories: {', '.join(missing)}. "
            "Run build session and try again"
        )

    session.install("twine")

    files = [str(f) for f in Path("dist").iterdir()]
    session.run("twine", "check", *files)
    session.run("twine", "upload", f"--repository={repository}", "-u=__token__", *files)
