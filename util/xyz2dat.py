#!/usr/bin/env python3
import sys, io, logging
from useful_functions import load_float_file

def xyz2dat(argv):
    """Convert xyz file to dat file (columns of numbers).
    Input from file or stdin.
    Output stringIO (print in standalone).
    
    Silva 01-11-2019"""
    
    if argv[0]:
        xyz_stream = open(argv[0]  , 'r')
    else:
        xyz_stream = sys.stdin 

    # String stream object for outpu
    output = io.StringIO()

    # Dump number of atoms
    xyz_stream.readline()
    
    # Comment line
    l = xyz_stream.readline().strip()
    # Add bash comment char if not there
    if l[0] != "#": l="#"+l
    # Print comment line
    print(l, file=output)

    # Print values
    for i, l in enumerate(xyz_stream):
        # Skip atom type field, convert to float
        lf = list(map(float, l.strip().split()[1:]))
        # Join and print
        print("%25.20f"*len(lf) % tuple(lf), file=output)

    # Return stringIO object
    return output

###################################################################
# MAIN
###################################################################
if __name__ == "__main__":
    # Print StringIO
    print(xyz2dat(sys.argv[1:]).getvalue())
