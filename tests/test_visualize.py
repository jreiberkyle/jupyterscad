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

import numpy as np
import pytest

from jupyterscad import _visualize, visualize_stl


def test_Visualizer_create_renderer(test_data):
    v = _visualize.Visualizer(test_data("test.stl"))
    v.create_renderer(v.create_mesh(), v.create_camera())


def test_visualize_stl_success(test_data):
    visualize_stl(test_data("test.stl"))


@pytest.mark.parametrize(
    "min_, max_, unit, grid_min, grid_center, grid_extent",
    [
        ((0, 0, 0), (5, 5, 5), 1, (-1, -1, -1), (2.5, 2.5, 2.5), 7),
        ((0, 0, 0), (5, 5, 5), 10, (-10, -10, -10), (0, 0, 0), 20),
    ],
)
def test_get_grid_dimensions(min_, max_, unit, grid_min, grid_center, grid_extent):
    calc_grid_min, calc_grid_center, calc_grid_extent = _visualize.get_grid_dimensions(
        np.array(min_), np.array(max_), unit
    )
    np.testing.assert_equal(calc_grid_min, grid_min)
    np.testing.assert_equal(calc_grid_center, grid_center)
    assert calc_grid_extent == grid_extent
