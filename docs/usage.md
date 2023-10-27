# Usage Examples

## Defining an OpenSCAD object

An OpenSCAD object can be defined using SolidPython2 or OpenSCAD.

### SolidPython2
```python
from solid2 import cube
obj = cube([1.5,2,1],center=True)
```

### OpenSCAD
```python
obj = 'cube([1.5,2,1],center=true);'
```

Note: If a 3D object description integrates an external stl file, then the stl must be in the same directory as the notebook running the code.

See the [OpenSCAD language](https://en.wikibooks.org/wiki/OpenSCAD_User_Manual#The_OpenSCAD_Language_Reference) and [SolidPython2](https://github.com/jeff-dh/SolidPython) pages for more information on how to use these tools.

## Rendering and Viewing an OpenSCAD object

### Visualizing and Rendering to an stl

To visualize an OpenSCAD object, use `view`:

```python
from jupyterscad import view
from solid2 import cube

obj = cube([1.5,2,1],center=True)
view(obj)
```
![render example](https://github.com/jreiberkyle/jupyterscad/blob/main/images/render_cube.png?raw=True)

The rendered 3D OpenSCAD object can also save the stl file by defining 'outfile':

```python
from jupyterscad import view
from solid2 import cube

obj = cube([1.5,2,1],center=True)
view(obj, outfile='obj.stl')
```

### Rendering directly to an stl

An stl can be generated directly without visualization with:

```python
from jupyterscad import render_stl

render_stl(obj, 'obj.stl')
```
### Visualizing an stl

A stl can be visualized with:

```python
from jupyterscad import view_stl

view_stl('obj.stl')
```

### Adjusting grid size

In `view` and `view_stl`, the default grid unit is 1. The grid unit can
be set to e.g. `10` with `grid_unit=10`, disabled with `grid_unit=0` or set to
automatic scaling with `grid_unit=-1`.
