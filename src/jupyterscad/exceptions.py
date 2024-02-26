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

import sys


class JupyterSCADError(Exception):
    pass


class OpenSCADError(JupyterSCADError):
    pass


class RenderError(JupyterSCADError):
    def __init__(self, message: str, src: str) -> None:
        super().__init__(message)
        self.message = message
        self.src = src

    def show(self) -> None:
        print(f"{self.message}\nSCAD SOURCE:\n\n{self.src}", file=sys.stderr)
