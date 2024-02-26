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
from unittest.mock import Mock

import pytest
import solid2

from jupyterscad import _view, view, view_stl


def test_view_success(monkeypatch):
    mock_view_stl = Mock()
    monkeypatch.setattr(_view, "view_stl", mock_view_stl)
    monkeypatch.setattr(_view, "render_stl", Mock())

    view(solid2.cube(3))
    mock_view_stl.assert_called_once()


def test_Visualizer_create_renderer(test_data):
    v = _view.Visualizer(test_data("test.stl"))
    v.create_renderer(v.create_mesh(), v.create_camera())


def test_view_stl_success(test_data):
    view_stl(test_data("test.stl"))
