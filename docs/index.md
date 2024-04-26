# Jupyter SCAD

Jupyter SCAD provides rendering and interactive visualization for 3D objects described in [SolidPython2](https://github.com/jeff-dh/SolidPython) within a Jupyter notebook. Additionally, it provides interactive visualization for STLs.

This program is focused on the use case of generating stl files with Python (aka SolidPython2) interactively within a Jupyter notebook.

SolidPython2 generates [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) code from Python code. Jupyter SCAD then uses [OpenSCAD](https://openscad.org) to render the OpenSCAD code to a 3D model and provides interactive visualization. As an alternative to SolidPython2, the OpenSCAD code can also be provided directly.

## Quick Start

Jupyter SCAD can be installed with `pip`:

```console
pip install jupyterscad
```

An OpenSCAD object can be defined using SolidPython2, viewed in a Jupyter
notebook, and saved to an `stl` file with:

```python
from jupyterscad import view
from solid2 import cube

view(cube([1.5,2,1],center=True), outfile='cube.stl')
```

![render example](https://github.com/jreiberkyle/jupyterscad/blob/main/images/render_cube.png?raw=True)

See the [Usage](usage.md) page for more examples.

## Status: MATURE

This project has reached it's goal, a basic Jupyter notebook viewer for SolidPython2, and no further improvements are planned.

## License

Jupyter SCAD is licensed under the [GNU GENERAL PUBLIC LICENSE](https://www.gnu.org/licenses/gpl-3.0.en.html).
