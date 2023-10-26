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
import tempfile
from os import PathLike
from typing import Optional, Union

import pythreejs as pjs

from ._openscad import process
from ._visualize import visualize_stl
from .exceptions import RenderError


def render(
    obj,
    width: int = 400,
    height: int = 400,
    grid_unit: float = 1,
    outfile: Optional[Union[str, PathLike]] = None,
    openscad_exec: Optional[Union[str, PathLike]] = None,
) -> pjs.Renderer:
    """Render a visusualization of an OpenSCAD object.

    Typical usage example:

        >>> display(render(cube(3)))

    Args:
        obj: OpenSCAD object to visualize.
        width: Visualization pixel width on page.
        height: Visualization pixel height on page.
        grid_unit: Grid cell size, 0 to disable, -1 for automatic
        outfile: Name of stl file to generate. No stl file is generated if None.
        openscad_exec: Path to openscad executable.

    Returns:
        Rendering to be displayed.

    Raises:
        exceptions.OpenSCADException: An error occurred running OpenSCAD.
    """
    try:
        if outfile:
            render_stl(obj, outfile, openscad_exec=openscad_exec)
            r = visualize_stl(outfile, width=width, height=height, grid_unit=grid_unit)
        else:
            with tempfile.NamedTemporaryFile(suffix=".stl", delete=False) as stl_tmp_file:
                render_stl(obj, stl_tmp_file.name, openscad_exec=openscad_exec)
                r = visualize_stl(
                    stl_tmp_file.name, width=width, height=height, grid_unit=grid_unit
                )
        return r
    except RenderError as e:
        e.show()


def render_stl(
    obj,
    outfile: Union[str, PathLike],
    openscad_exec: Optional[Union[str, PathLike]] = None,
):
    """Render a stl from an OpenSCAD object.

    Typical usage example:

        >>> render_stl(cube(3), 'cube.stl')

    Args:
        obj: OpenSCAD object to visualize.
        outfile: Name of stl file to generate. No stl file is generated if None.
        openscad_exec: Path to openscad executable.

    Raises:
        exceptions.OpenSCADException: An error occurred running OpenSCAD.
    """
    with tempfile.NamedTemporaryFile(suffix=".scad", delete=False) as scad_tmp_file:
        with open(scad_tmp_file.name, "w") as fp:
            fp.write(str(obj))

        process(scad_tmp_file.name, outfile, executable=openscad_exec)
