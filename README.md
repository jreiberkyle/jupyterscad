# Jupyter SCAD: SCAD in Jupyter

Jupyter SCAD renders and interactively visualizes 3D objects described in [SolidPython2](https://github.com/jeff-dh/SolidPython) within a Jupyter notebook.

SolidPython2 generates [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) code from Python code. Jupyter SCAD then uses [OpenSCAD](https://openscad.org) to render the OpenSCAD code to a 3D model and provides interactive visualization. As an alternative to SolidPython2, the OpenSCAD code can also be provided directly.


## Use Case and Alternatives

This program is focused on the use case of generating stl files with Python interactively within a Jupyter notebook.

Alternatively, one could use a Jupyter notebook as an external editor, using SolidPython2 to update the SCAD file and OpenSCAD to visualize and render the SCAD file.
The benefit to this approach is that one can visualize the preview. The drawback is that the two-program workflow can feel distracting.
See more on using external editors for OpenSCAD [here](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_an_external_Editor_with_OpenSCAD).

Or, one can use [ViewSCAD](https://github.com/nickc92/ViewSCAD), which was the motivation for this project. However the last time ViewSCAD was updated was 2015 (checked on 9/21/2023). It only supports SolidPython, not SolidPython2.

## Installation

To simply install the package, use pip:

```
pip install githubaddress
```

Alternately, the entire Jupyter notebook, SolidPython2, and Jupyter SCAD setup could be run as a [podman]() container.
The podman image is given at [jupyter-scad-image]().


## Usage

### Define an OpenSCAD object

Using SolidPython2:
```python
from solid2 import *
obj = cube(1)
```

OpenSCAD:
```python
obj = 'cube([60,20,10],center=true);'
```

Note: If a 3D object description integrates an external stl file, then the stl must be in the same directory as the notebook.

See the [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) and [SolidPython2](https://github.com/jeff-dh/SolidPython) pages for more information on how to use these tools.

### Render an OpenSCAD object to a stl

```python
from jupyter_scad import render

render(obj, 'cube.stl')
```
where `obj` is described in OpenSCAD as described above.

### Visualize a stl

```python
from jupyter_scad import visualize

visualize('cube.stl')
```

## Visualization Design

This package uses [pythreejs](https://pythreejs.readthedocs.io/) for visualization.

Alternatives considered, ordered from closest fit to farthest:
- [pyvolume](https://pyvolume.readthedocs.io/): provides mesh visualization and interaction but (as of 2023.09.24) the latest release is alpha and documentation is sparse.
- [matplotlib mplot3d](https://matplotlib.org/2.2.2/mpl_toolkits/mplot3d/faq.html#toolkit-mplot3d-faq): provides mesh visualization and interaction but is slow.
- [pyvista](https://pyvista.org/): provides stl loading and visualization but visualization does not work in docker image.

## Acknowledgements

Thanks to [nickc92](https://github.com/nickc92) for creating [ViewSCAD](https://github.com/nickc92/ViewSCAD), which is the inspiration for this project.
