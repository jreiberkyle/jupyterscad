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
from pathlib import Path

import pytest

from jupyterscad import exceptions, _render, render_stl, render

LOGGER = logging.getLogger(__name__)


def test_OpenSCAD_invalid_openscad_exec():
    """What happens when the provided openscad_exec doesn't exist"""
    with pytest.raises(exceptions.OpenSCADException):
        _render.OpenSCAD('invalid')
  

def test_OpenSCAD__detect_executable_notsupported(monkeypatch):
    """What happens when the detected system is not one that provides a 
    default"""
    monkeypatch.setattr(_render.platform, 'system', lambda: 'NotSupported')
    with pytest.raises(exceptions.OpenSCADException):
        _render.OpenSCAD._detect_executable()



def test_OpenSCAD__detect_executable_success(monkeypatch, tmp_path):
    """The default executable exists"""
    monkeypatch.setattr(_render.platform, 'system', lambda: 'Linux')

    fake_path = tmp_path / 'executable'
    fake_path.touch()

    monkeypatch.setattr(_render,
                        'DEFAULT_OPENSCAD_EXECUTABLE',
                        {'Linux': [str(fake_path)]})
    _render.OpenSCAD._detect_executable()

def test_OpenSCAD__detect_executable_failure(monkeypatch, tmp_path):
    """The default executable does not exist"""
    monkeypatch.setattr(_render.platform, 'system', lambda: 'Linux')

    fake_path = tmp_path / 'executable'

    monkeypatch.setattr(_render,
                        'DEFAULT_OPENSCAD_EXECUTABLE',
                        {'Linux': [str(fake_path)]})

    with pytest.raises(exceptions.OpenSCADException):
        _render.OpenSCAD._detect_executable()


@pytest.fixture()
def openscad():
    openscad = None
    try:
        openscad = _render.OpenSCAD()
    except exceptions.OpenSCADException:
        pytest.skip("OpenSCAD not detected.")
    return openscad

def test_OpenSCAD_render_success(tmp_path, openscad):
    input_scad_file = tmp_path / 'test.scad'
    with open(input_scad_file, 'w') as fp:
        fp.write('cube([60,20,10],center=true);')

    output_file = tmp_path / 'out.stl'
    openscad.render(input_scad_file, output_file)
    assert output_file.is_file()

    # make sure its a legitimate stl
    assert 'vertex' in open(output_file, 'r').read()


def test_OpenSCAD_render_invalid_scad(tmp_path, openscad):
    input_scad_file = tmp_path / 'test.scad'
    with open(input_scad_file, 'w') as fp:
        fp.write('invalid_scad;')

    output_file = tmp_path / 'out.stl'

    with pytest.raises(exceptions.OpenSCADException):
        openscad.render(input_scad_file, output_file)


def test_render_stl(tmp_path, openscad):
    output_file = tmp_path / 'test.stl'
    
    openscad_str = 'cube([60,20,10],center=true);'
    render_stl(openscad_str, output_file)

    # make sure its a legitimate stl
    assert 'vertex' in open(output_file, 'r').read()


def test_render_success(openscad):
    openscad_str = 'cube([60,20,10],center=true);'
    render(openscad_str)

