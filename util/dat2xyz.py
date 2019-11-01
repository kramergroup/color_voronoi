#!/usr/bin/env python3
import sys, io, logging
from useful_functions import load_float_file

def dat2xyz(argv):
    """Convert dat file (columns of numbers) to xyz file.
    Input from file or stdin.
    Output stringIO (print in standalone).

    Silva 01-11-2019"""
    
    # Choose between file and stdin
    if argv[0]:
        c, d = load_float_file(argv[0])
    else:
        c, d = load_stream(sys.stdin, **{"comment_char" : comment_char, "f": float})

    # Decide arbitrary atom type for xyz
    atm_type = "H"

    # String stream object for outpu
    output = io.StringIO()
    
    # Print number of atoms
    print(len(d), file=output)
    # Print comment line
    print("#xyz from %s" % argv[0], file=output)
        
    # For each line, print atom and all fields
    for l in d:
        if len(l) < 3:
            raise ValueError("Not valid xyz vector: %s", "%f "*len(l) % tuple(l))
        print("H "+"%25.15f"*len(l) % tuple(l), file=output) 

    # Return stringIO object
    return output

###################################################################
# MAIN
###################################################################
if __name__ == "__main__":
    # Print StringIO
    print(dat2xyz(sys.argv[1:]).getvalue())
