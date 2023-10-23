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
from unittest.mock import Mock

import pytest
import solid2

from jupyterscad import _render, render, render_stl

LOGGER = logging.getLogger(__name__)


@pytest.mark.parametrize("obj", ["cube(size = 3);", solid2.cube(3)])
def test_render_stl(obj, tmp_path, monkeypatch):
    def side_effect(scad_file, output_file, executable):
        with open(scad_file, "r") as fp:
            assert fp.read().strip() == "cube(size = 3);"

        assert output_file == tmp_path / "test.stl"

    mock_process = Mock(side_effect=side_effect)
    monkeypatch.setattr(_render, "process", mock_process)

    output_file = tmp_path / "test.stl"

    render_stl(obj, output_file)
    mock_process.assert_called_once()


def test_render_success(monkeypatch):
    mock_visualize_stl = Mock()
    monkeypatch.setattr(_render, "visualize_stl", mock_visualize_stl)
    monkeypatch.setattr(_render, "render_stl", Mock())

    render(solid2.cube(3))
    mock_visualize_stl.assert_called_once()
