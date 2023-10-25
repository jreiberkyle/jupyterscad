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
from os import PathLike
from typing import Union

import numpy as np
import pythreejs as pjs
import stl


def visualize_stl(
    stl_file: Union[str, PathLike],
    width: int = 400,
    height: int = 400,
    grid_unit: float = 1,
) -> pjs.Renderer:
    """Render a visualization of a stl.

    Typical usage example:

        >>> display(visualize_stl(cube(3)))

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
        grid_min, grid_center, grid_extent = get_grid_dimensions(
            self.stl_mesh.min_, self.stl_mesh.max_, unit
        )

        # X/Z plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="green",
            colorGrid="green",
        )
        gh.position = (grid_center[0], grid_min[1], grid_center[2])
        scene.add(gh)

        # X/Y plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="blue",
            colorGrid="blue",
        )
        gh.rotateX(math.pi / 2)
        gh.position = (grid_center[0], grid_center[1], grid_min[2])
        scene.add(gh)

        # Y/Z plane
        gh = pjs.GridHelper(
            grid_extent,
            grid_extent / unit,
            colorCenterLine="red",
            colorGrid="red",
        )
        gh.rotateZ(math.pi / 2)
        gh.position = (grid_min[0], grid_center[1], grid_center[2])
        scene.add(gh)


def get_grid_dimensions(mesh_min, mesh_max, unit):
    view_min = mesh_min
    view_extent = (mesh_max - mesh_min).max()

    if unit == -1:
        unit = 10 ** math.floor(math.log10(view_extent))

    grid_min = np.floor(view_min / unit) * unit
    print(grid_min)

    # if grid falls right on extent, add one unit buffer
    grid_min_buff = np.logical_not(np.mod(view_min, unit)) * unit
    print(grid_min_buff)

    view_max = view_min + view_extent
    grid_max = np.ceil(view_max / unit) * unit
    print(grid_max)

    # if grid falls right on extent, add one unit buffer
    grid_max_buff = np.logical_not(np.mod(view_max, unit)) * unit
    print(grid_max_buff)

    grid_extent = (grid_max + grid_max_buff - grid_min + grid_min_buff).max()
    grid_center = grid_min - grid_min_buff + grid_extent / 2

    return grid_min - grid_min_buff, grid_center, grid_extent
