#!/usr/bin/env python3

"""Module description here

Silva 01-11-2019"""

import sys, argparse, logging, json
import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d
from useful_functions import load_float_file, logger_setup
from ase.io import read as ase_read

def get_x(l):
    """Get x coordinate from list of positions"""
    return [x[0] for x in l]

def get_y(l):
    """Get y coordinate from list of positions"""
    return [x[1] for x in l]

def get_xyz_col(xyz_stream, n): 
     """Return the nth column of an xyz stream""" 
     return [l.split()[n] for i, l in enumerate(xyz_stream) if i>1 ]

def color_voronoi(vor, z, ax, 
                  minima=None, maxima=None, c_code="RdYlBu_r",
                  p_size=1, show_points=True, show_vertices=False,
                  l_width=1, l_color="red", l_alpha=1):
    """Wrapper around scipy voronoi plot for the lines, then color the regions according to ginven z.
    Most options can be controlled from this wrapper."""
    
    # If not fiven, find min/max values for normalization
    if minima is None: minima = min(z)
    if maxima is None: maxima = max(z)
    
    # Normalize chosen colormap
    norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
    mapper = cm.ScalarMappable(norm=norm, cmap=c_code )
    
    # Plot Voronoi diagram: lines between regions and, possible, vertex
    voronoi_plot_2d(vor, ax=ax,
                    show_points=False, show_vertices=show_vertices, 
                    line_alpha=l_alpha, line_width=l_width, line_color=l_color,
                    s=0.2)    
    # For region index of ith point
    for i, p_r in enumerate(vor.point_region):
        # Get corresponding region
        region = vor.regions[p_r]
        # Open regions (contain -1 as vertex) do not define a polygon 
        if not -1 in region:
            # Define polygon from closed voronoi region
            polygon = [vor.vertices[v] for v in region]
            # Get ith color in z list corresponding to current point
            ax.fill(*zip(*polygon), color=mapper.to_rgba(z[i]))
            
    # If required, plot the points generating the Voronoi diagram
    if show_points:
        ax.plot(get_x(vor.points), get_y(vor.points), 'o', c='black', ms=p_size )
    return ax    

def xyz_color_vornoi(argv):
    """Compute Voronoi construction of xy posisions from xyz file and color polygons according to additional 4th column in xyz file.
    Plot the results (interactive or file). Plot options can be pass via json file.
    Field (with defaults) are:
    - minima=None (compute from data),
    - maxima=None (compute from data),
    - c_code='RdYlBu_r' (matplotlib palette name),
    - p_size=0.5,
    - show_points=True (write 0/1 in json, not string),
    - show_vertices=False (0/1),
    - l_width=1,
    - l_color='red',
    - l_alpha=1
    """

    # Output file details
    dpi = 800
    out_format = "png"
    #-------------------------------------------------------------------------------
    # Argument parser
    #-------------------------------------------------------------------------------
    parser = argparse.ArgumentParser(description=xyz_color_vornoi.__doc__,
                                     epilog="Silva 01-11-2019")
    # Positional arguments
    parser.add_argument('filename',
                        default=None,
                        type=str, nargs="?",
                        help='xyz file with 4th column for color. If blank use stdin;')
    # Optional args
    parser.add_argument('--p_opt',
                        dest='plt_opt', metavar="opt.json",
                        type=str, default={},
                        help='path to json file with plot options;')
    parser.add_argument('--noplot',
                        action='store_false', dest='plot_flg',
                        help='no iteractive plot;')
    parser.add_argument('-o', '--out',
                        dest='out_f',
                        type=str, default=None, metavar="basename",
                        help='save figure file in %s at %idpi'% (out_format, dpi))
    parser.add_argument('--debug',
                        action='store_true', dest='debug',
                        help='show debug information.')

    #-------------------------------------------------------------------------------
    # Initialize and check variables
    #-------------------------------------------------------------------------------
    args = parser.parse_args(argv) # Process arguments

    # Set up logger and debug options
    c_log = logger_setup(__name__)
    c_log.setLevel(logging.INFO)
    debug_opt = [] # Pass debug flag down to other functions
    if args.debug:
        c_log.setLevel(logging.DEBUG)
        debug_opt = ['-d']
    c_log.debug(args)

    #-------------------------------------------------------------------------------
    # Read data
    #-------------------------------------------------------------------------------
    c_log.info("Reading colors...")
    # Get points colors
    with open(args.filename, 'r') as xyz_stream:
        vor_col = list(map(float, get_xyz_col(xyz_stream, 4)))
    c_log.info("Load xy position via ASE...")
    # Get points positions
    xy = ase_read(args.filename).positions[:, 0:2]

    #for xyi, ci in zip(xy, vor_col):
    #    print(xyi, ci)

    #-------------------------------------------------------------------------------
    # Vornoi construction
    #-------------------------------------------------------------------------------
    c_log.info("Computing Voronoi via scipy-qhull...")
    # Get Voronoi construction 
    vor = Voronoi(xy)

    #-------------------------------------------------------------------------------
    # Define canvas
    #-------------------------------------------------------------------------------
    fig = plt.figure()   
    fig.set_dpi(dpi)
    ax = fig.add_subplot(111)              
    ax.set_aspect("equal")

    if args.plt_opt != {}:
        with open(args.plt_opt,'r') as json_in: args.plt_opt = json.load(json_in)

    # Call base function
    c_log.info("Plotting at %i dpi", dpi)
    color_voronoi(vor, vor_col, ax, **args.plt_opt)

    # Show interactive plot
    if args.plot_flg:
        plt.show()
    # Save figure
    if args.out_f != None:
        c_log.info("Saving file on %s.%s", args.out_f, out_format)
        plt.savefig("%s.%s" % (args.out_f, out_format), dpi=dpi)

    return 0

###################################################################
# MAIN
###################################################################
if __name__ == "__main__":
    xyz_color_vornoi(sys.argv[1:])
