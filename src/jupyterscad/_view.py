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

import math
import tempfile
from os import PathLike
from typing import Optional, Union

import numpy as np
import pythreejs as pjs
import stl

from ._render import render_stl
from .exceptions import RenderError


def view(
    obj,
    width: int = 400,
    height: int = 400,
    grid_unit: float = -1,
    outfile: Optional[Union[str, PathLike]] = None,
    openscad_exec: Optional[Union[str, PathLike]] = None,
) -> pjs.Renderer:
    """View an OpenSCAD object.

    Typical usage example:

        >>> view(cube(3))

    Args:
        obj: OpenSCAD object to visualize.
        width: Visualization pixel width on page.
        height: Visualization pixel height on page.
        grid_unit: Grid cell size, 0 to disable, -1 for automatic.
        outfile: Name of stl file to generate. No stl file is generated if None.
        openscad_exec: Path to openscad executable.

    Returns:
        Rendering to be displayed.

    Raises:
        exceptions.OpenSCADError: An error occurred running OpenSCAD.
    """
    try:
        if outfile:
            render_stl(obj, outfile, openscad_exec=openscad_exec)
            r = view_stl(outfile, width=width, height=height, grid_unit=grid_unit)
        else:
            with tempfile.NamedTemporaryFile(
                suffix=".stl", delete=False
            ) as stl_tmp_file:
                render_stl(obj, stl_tmp_file.name, openscad_exec=openscad_exec)
                r = view_stl(
                    stl_tmp_file.name, width=width, height=height, grid_unit=grid_unit
                )
        return r
    except RenderError as e:
        e.show()


def view_stl(
    stl_file: Union[str, PathLike],
    width: int = 400,
    height: int = 400,
    grid_unit: float = -1,
) -> pjs.Renderer:
    """View a stl.

    Typical usage example:

        >>> view_stl(cube(3))

    Args:
        stl_file: stl file to visualize.
        width: Visualization pixel width on page.
        height: Visualization pixel height on page.
        grid_unit: Grid cell size, 0 to disable, -1 for automatic

    Returns:
        Rendering to be displayed.
    """
    v = Visualizer(stl_file)
    r = v.create_renderer(
        v.create_mesh(),
        v.create_camera(),
        width=width,
        height=height,
        grid_unit=grid_unit,
    )
    return r


class Visualizer:
    def __init__(self, stl_file):
        self.stl_mesh = stl.mesh.Mesh.from_file(stl_file)

    def create_mesh(self, color: str = "#ebcc34"):
        mesh = self.stl_mesh

        vertices = pjs.BufferAttribute(array=mesh.vectors, normalized=False)

        # broadcast face normals to each face vertex
        normals = pjs.BufferAttribute(array=np.repeat(mesh.normals, 3, axis=0))

        geometry = pjs.BufferGeometry(
            attributes={"position": vertices, "normal": normals}
        )

        return pjs.Mesh(
            geometry=geometry,
            material=pjs.MeshLambertMaterial(color=color, opacity=1, transparent=True),
            position=[0, 0, 0],
        )

    def create_camera(self):
        position = (np.array([5, 5, 5]) * self.stl_mesh.max_).tolist()
        key_light = pjs.DirectionalLight(
            color="white", position=[3, 5, 1], intensity=0.7
        )
        camera = pjs.PerspectiveCamera(
            position=position, up=[0, 0, 1], children=[key_light], fov=20
        )
        return camera

    def create_renderer(self, mesh, camera, width=400, height=400, grid_unit=1):
        children = [mesh, camera, pjs.AmbientLight(color="#777777", intensity=0.5)]
        scene = pjs.Scene(children=children)

        if grid_unit:
            self.add_grid(scene, unit=grid_unit)

        self.add_axes(scene)

        renderer_obj = pjs.Renderer(
            camera=camera,
            scene=scene,
            controls=[pjs.OrbitControls(controlling=camera)],
            width=width,
            height=height,
        )
        return renderer_obj

    def add_axes(self, scene):
        # The X axis is red. The Y axis is green. The Z axis is blue.
        scene.add(pjs.AxesHelper(max(self.stl_mesh.max_ * 2)))

    def add_grid(self, scene, unit=1):
        def roundToUnits(x):
            return round(x / unit) * unit

        min_ = np.minimum(self.stl_mesh.min_, np.array([0, 0, 0]))
        max_ = np.maximum(self.stl_mesh.max_, np.array([0, 0, 0]))
        max_extend = (max_ - min_).max()

        if unit == -1:
            unit = 10 ** math.floor(math.log10(max_extend))

        grid_extent = roundToUnits(max_extend) + 2 * unit

        grid_pos = (
            grid_extent / 2 - unit + roundToUnits(min_[0]),
            grid_extent / 2 - unit + roundToUnits(min_[1]),
            grid_extent / 2 - unit + roundToUnits(min_[2]),
        )

        # X/Z plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="blue",
            colorGrid="blue",
        )
        gh.position = (grid_pos[0], 0, grid_pos[2])
        scene.add(gh)

        # X/Y plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="red",
            colorGrid="red",
        )
        gh.rotateX(math.pi / 2)
        gh.position = (grid_pos[0], grid_pos[1], 0)
        scene.add(gh)

        # Y/Z plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="green",
            colorGrid="green",
        )
        gh.rotateZ(math.pi / 2)
        gh.position = (0, grid_pos[1], grid_pos[2])
        scene.add(gh)
