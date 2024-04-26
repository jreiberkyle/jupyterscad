# Jupyter SCAD: SCAD in Jupyter


Jupyter SCAD provides rendering and interactive visualization for 3D objects described in [SolidPython2](https://github.com/jeff-dh/SolidPython) within a Jupyter notebook. Additionally, it provides interactive visualization for STLs.

This program is focused on the use case of generating stl files with Python (aka SolidPython2) interactively within a Jupyter notebook.

## Status: MATURE

This project has reached it's goal, a basic Jupyter notebook viewer for SolidPython2. Any further improvements are best served by just using the OpenSCAD
GUI (see Alternatives below).

At this time, the only work that is planned for this project is bugfixes. If you are interested in continuing to add functionality,
make an issue expressing your interest and we can discuss passing the baton.


## Documentation

Documentation is hosted at https://jreiberkyle.github.io/jupyterscad/.

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

## Alternatives

As an alternative to Jupyter SCAD, one could use a Jupyter notebook as an external editor, using SolidPython2 to update the SCAD file and OpenSCAD to visualize and render the SCAD file.
The benefit to this approach is that one can visualize the preview. The drawback is that the two-program workflow can feel distracting.
See more on using external editors for OpenSCAD [here](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual/Using_an_external_Editor_with_OpenSCAD).

Or, one can use [ViewSCAD](https://github.com/nickc92/ViewSCAD), which was the motivation for this project. However the last time ViewSCAD was updated was 2019 (checked on 9/21/2023). It only supports SolidPython, not SolidPython2.

## Transitioning from ViewSCAD

This package was inspired by [ViewSCAD](https://github.com/nickc92/ViewSCAD) and therefore
maintains a very similar interface.

To transition from ViewSCAD, replace
```python
import viewscad

r = viewscad.Renderer()
r.render(obj)
```

with
```python
from jupyterscad import view

view(obj)
```

## Visualization Backend

This package uses [pythreejs](https://pythreejs.readthedocs.io/) for visualization.

Alternatives considered, ordered from closest fit to farthest:
- [pyvolume](https://pyvolume.readthedocs.io/): provides mesh visualization and interaction but (as of 2023.09.24) the latest release is alpha and documentation is sparse.
- [matplotlib mplot3d](https://matplotlib.org/2.2.2/mpl_toolkits/mplot3d/faq.html#toolkit-mplot3d-faq): provides mesh visualization and interaction but is slow.
- [pyvista](https://pyvista.org/): provides stl loading and visualization but visualization does not work in docker image.

## Acknowledgements

Thanks to [nickc92](https://github.com/nickc92) for creating [ViewSCAD](https://github.com/nickc92/ViewSCAD), which is the inspiration for this project.
