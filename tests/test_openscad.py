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
import logging

import pytest

from jupyterscad import _openscad, exceptions

LOGGER = logging.getLogger(__name__)


@pytest.fixture()
def scad_file(tmp_path):
    input_scad_file = tmp_path / "test.scad"
    with open(input_scad_file, "w") as fp:
        fp.write("cube([60,20,10],center=true);")
    return input_scad_file


@pytest.fixture()
def output_file(tmp_path):
    return tmp_path / "out.stl"


def test_invalid_openscad_exec(scad_file, output_file):
    """What happens when the provided openscad_exec doesn't exist"""
    with pytest.raises(exceptions.OpenSCADException):
        _openscad.process(scad_file, output_file, "invalid")


def test_detect_executable_failure(monkeypatch):
    """No executable found"""
    monkeypatch.setattr(_openscad, "OS_OPENSCAD_EXECUTABLES", [])
    monkeypatch.setattr(_openscad, "which", lambda x: None)

    with pytest.raises(exceptions.OpenSCADException):
        _openscad.detect_executable()


def test_detect_executable_success(monkeypatch, tmp_path):
    """The default executable exists"""
    monkeypatch.setattr(_openscad, "which", lambda x: "found")
    _openscad.detect_executable()


@pytest.fixture()
def check_openscad():
    try:
        _openscad.detect_executable()
    except exceptions.OpenSCADException:
        pytest.skip("OpenSCAD not detected.")


def test_process_success(check_openscad, scad_file, output_file):
    _openscad.process(scad_file, output_file)
    assert output_file.is_file()

    # make sure its a legitimate stl
    assert "vertex" in open(output_file, "r").read()


def test_process_invalid_scad(check_openscad, tmp_path, output_file):
    input_scad_file = tmp_path / "test.scad"
    with open(input_scad_file, "w") as fp:
        fp.write("invalid_scad;")

    with pytest.raises(exceptions.OpenSCADException):
        _openscad.process(input_scad_file, output_file)
