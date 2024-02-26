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
import subprocess
import tempfile
from os import PathLike
from pathlib import Path
from shutil import which
from typing import Optional, Union

from .exceptions import OpenSCADError, RenderError

LOGGER = logging.getLogger(__name__)


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
    with tempfile.NamedTemporaryFile(suffix=".scad", dir=".") as scad_tmp_file:
        with open(scad_tmp_file.name, "w") as fp:
            fp.write(str(obj))

        process(scad_tmp_file.name, outfile, executable=openscad_exec)


def process(scad_file, output_file, executable: Optional[Union[str, PathLike]] = None):
    """Generate stl from scad using OpenSCAD executable"""
    if executable:
        executable = Path(executable)
        if not executable.is_file():
            raise OpenSCADError(f"Specified executable {executable} does not exist.")
    else:
        executable = detect_executable()

    cmd = [executable, "-o", output_file, scad_file]
    LOGGER.info(cmd)
    try:
        out = subprocess.run(cmd, check=True, capture_output=True, text=True)
        if "ERROR" in out.stderr:
            with open(scad_file) as fp:
                scad_str = fp.read()
            raise RenderError(message=out.stderr, src=scad_str)
    except subprocess.CalledProcessError as e:
        raise OpenSCADError(str(e.stderr))


def detect_executable() -> Path:
    """Detect the OpenSCAD executable"""

    detected_executable = which("openscad") or which(
        "openscad", path="/Applications/OpenSCAD.app/Contents/MacOS"
    )  # macOS

    if not detected_executable:
        raise OpenSCADError(
            "OpenSCAD executable autodetection failed. "
            "Please specify the path to the OpenSCAD executable."
        )

    LOGGER.debug(f"Executable path ({detected_executable}) found.")

    return Path(detected_executable)
