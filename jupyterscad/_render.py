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
import platform
import subprocess
import tempfile
import typing

from .exceptions import OpenSCADException

DEFAULT_OPENSCAD_EXECUTABLE = {
    'Linux': ['/usr/bin/openscad', '/usr/local/bin/openscad'],
    'Darwin': ['/Applications/OpenSCAD.app/Contents/MacOS/OpenSCAD']
}

LOGGER = logging.getLogger(__name__)


def render(obj, output_file, openscad_exec: Path = None):
    
    with tempfile.NamedTemporaryFile(suffix='.scad', delete=False) as scad_tmp_file:
        with open(scad_tmp_file.name, 'w') as fp:
            fp.write(str(obj))

        OpenSCAD(openscad_exec).render(scad_tmp_file.name, output_file)


class OpenSCAD():
    def __init__(self, openscad_exec: Path = None):
        if openscad_exec:
            if not self._is_executable(openscad_exec):
                raise OpenSCADException(
                    f'Provided path to openscad executable ({openscad_exec}) does not '
                    'exist.')
            self.executable = openscad_exec
        else:
            self.executable = self._detect_executable()

    @classmethod
    def _detect_executable(cls) -> Path:
        detected_executable = None
        system = platform.system()
        try:
            default_paths = DEFAULT_OPENSCAD_EXECUTABLE[system]
        except KeyError:  # system not supported
            raise OpenSCADException(
                    f'This system ({system}) is not supported for '
                    'OpenSCAD executable autodetect. Please specify the path '
                    'to the OpenSCAD executable.')
        else:
            for test_path in default_paths:
                if cls._is_executable(test_path):
                    LOGGER.debug(
                            f'executable path ({test_path}) found for '
                            f'system ({system}).')
                    detected_executable = Path(test_path)
                    break
        
            if not detected_executable:
                raise OpenSCADException(
                        'OpenSCAD executable not found at the default '
                        f'locations for this system ({system}), '
                        f'{DEFAULT_OPENSCAD_EXECUTABLE[system]}. '
                        'Please specify the path to the OpenSCAD '
                        'executable.')
    
        return detected_executable

    @staticmethod
    def _is_executable(path: str):
        return Path(path).is_file()

    def render(self, scad_file, output_file):
        '''Generate stl from scad'''
        cmd = [self.executable, '-o', output_file, scad_file]
        LOGGER.info(cmd)
        try:
            subprocess.run(cmd, check=True, capture_output=True, text=True)
        except subprocess.CalledProcessError as e:
            raise OpenSCADException(str(e.stderr))
