# Color Voronoi
Color Voronoi diagram according to scalar property of points.

The notebook Tutorial_color_Voronoi.ipynb provides an introduction to Vornoi construction and how the coloring function works.

The real module is in xyz_color_voronoi, which contains the python function color_voronoi and the wrapper for bash xyz_color_voronoi.

In order to use the functions the module useful_functions must be available to the Python kernel, i.e. either in the same folder or in the python path.
As a temporary solution, you can do:
- from bash PYTHONPATH="$PYTHONPATH:/path/to/util"
- from python import sys; sys.path.append("/path/to/util")
