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
from pathlib import Path
from shutil import which

from .exceptions import OpenSCADException

LOGGER = logging.getLogger(__name__)


def process(scad_file, output_file, executable: Path = None):
    """Generate stl from scad using OpenSCAD executable"""
    if executable and not Path(executable).is_file():
        raise OpenSCADException(f"Specified executable {executable} does not exist.")

    if not executable:
        executable = detect_executable()

    cmd = [executable, "-o", output_file, scad_file]
    LOGGER.info(cmd)
    try:
        subprocess.run(cmd, check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        raise OpenSCADException(str(e.stderr))


def detect_executable() -> Path:
    """Detect the OpenSCAD executable"""

    detected_executable = (
        which("openscad")
        or which("openscad", path="/Applications/OpenSCAD.app/Contents/MacOS")  # macOS
    )

    if not detected_executable:
        raise OpenSCADException(
            "OpenSCAD executable autodetection failed. "
            "Please specify the path to the OpenSCAD executable."
        )

    LOGGER.debug(f"Executable path ({detected_executable}) found.")

    return Path(detected_executable)
