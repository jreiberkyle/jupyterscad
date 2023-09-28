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
import tempfile

from pythreejs import *
import stl

from ._render import render

def visualize(obj, width=400, height=400, grid_unit=1):
    with tempfile.NamedTemporaryFile(suffix='.stl', delete=False) as stl_tmp_file:
        render(str(obj), stl_tmp_file.name)

        v = Visualizer(stl_tmp_file.name)
        v.create_renderer(v.create_mesh(), v.create_camera(), width=width, height=height, grid_unit=grid_unit)
    return v


def visualize_stl(filename, width=400, height=400, grid_unit=1):
    v = Visualizer(filename)
    return v.create_renderer(v.create_mesh(), v.create_camera(), width=width, height=height, grid_unit=grid_unit)


class Visualizer():
    def __init__(self, stl_file):
        self.stl_mesh = stl.mesh.Mesh.from_file(stl_file)

    def create_mesh(self, color:str = '#ebcc34'):
        mesh = self.stl_mesh

        vertices = BufferAttribute(array=mesh.vectors, normalized=False)

        # broadcast face normals to each face vertex
        normals = BufferAttribute(array=np.repeat(mesh.normals, 3, axis=0))

        geometry = BufferGeometry( attributes={
            'position': vertices,
            'normal': normals
        })

        return Mesh(
            geometry=geometry,
            material=MeshLambertMaterial(color=color, opacity=1, transparent=True),
            position=[0, 0, 0],   
        )

    def create_camera(self):
        position=(np.array([5, 5, 5])*self.stl_mesh.max_).tolist()
        key_light = DirectionalLight(color='white', position=[3, 5, 1], intensity=0.7)
        camera = PerspectiveCamera(position=position, up=[0, 0, 1], children=[key_light], fov=20)
        return camera
        
    def create_renderer(self, mesh, camera, width=400, height=400, grid_unit=1):
        children=[mesh, camera, AmbientLight(color='#777777', intensity=0.5)]
        scene = Scene(children=children)
        
        if grid_unit:
            self.add_grid(scene, unit=grid_unit)

        self.add_axes(scene)
                
        renderer_obj = Renderer(camera=camera, scene=scene, controls=[OrbitControls(controlling=camera)], width=width, height=height)
        return renderer_obj

    def add_axes(self, scene):
        # The X axis is red. The Y axis is green. The Z axis is blue.
        scene.add(AxesHelper(max(self.stl_mesh.max_*2)))

    def add_grid(self, scene, unit=1):
        mesh = self.stl_mesh
        min_ = np.minimum(np.floor(mesh.min_), np.array([0,0,0]))
        max_ = np.maximum(np.ceil(mesh.max_), np.array([0,0,0]))
        extent = max_ - min_
        grid_extent = extent.max()

        grid_pos = (grid_extent/2 + min_[0], grid_extent/2 + min_[1], grid_extent/2 + min_[2])
        
        # X/Z plane
        gh = GridHelper(grid_extent + 2*unit, (grid_extent + 2*unit) / unit, colorCenterLine='blue', colorGrid='blue')
        gh.position = (grid_pos[0], 0, grid_pos[2])
        scene.add(gh)

        # X/Y plane
        gh = GridHelper(grid_extent + 2*unit, (grid_extent + 2*unit) / unit, colorCenterLine='red', colorGrid='red')
        gh.rotateX(math.pi/2)
        gh.position = (grid_pos[0], grid_pos[1], 0)
        scene.add(gh)
        
        # Y/Z plane
        gh = GridHelper(grid_extent + 2*unit, (grid_extent + 2*unit) / unit, colorCenterLine='green', colorGrid='green')
        gh.rotateZ(math.pi/2)
        gh.position = (0, grid_pos[1], grid_pos[2])
        scene.add(gh)
