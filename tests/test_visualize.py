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

from jupyterscad import _visualize, visualize_stl


def test_Visualizer_create_renderer(test_data):
    v = _visualize.Visualizer(test_data("test.stl"))
    v.create_renderer(v.create_mesh(), v.create_camera())


def test_visualize_stl_success(test_data):
    visualize_stl(test_data("test.stl"))
