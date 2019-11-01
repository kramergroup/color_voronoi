
"""
--------------------------------
 GENERAL PORPOUSE FUNCTIONS
--------------------------------

A pletora of general functions:
 - small ones just to save time, aka code shortcuts;
 - smart file readers (skip bash comments, divide in fields, ...);
 - string formatter (fix width, ...);
 - container manipulators (flatten nested strings)
Python 3 only.

Created:    Silva 29-01-2018
Last edit:  Silva 04-04-2019
"""

import collections
import logging

#--------------------------------
# Set up LOGGER
#--------------------------------

def logger_setup(module_name):
    """Set up standar logger for a module and return it"""

    # Set up LOGGER
    c_log = logging.getLogger(module_name) # Use name of the calling moduel, not this function
    # Adopted format: level - current function name - mess. Width is fixed as visual aid
    std_format = '[%(levelname)5s - %(funcName)10s] %(message)s'
    logging.basicConfig(format=std_format)
    # Logging level is defined by calling module via root logger
    return c_log

#--------------------------------
# Short functions with heavly used combos
#--------------------------------

def strlist(listarg, sep=' '):
    """Create a string out of a list with gien separator (def=space)"""
    sep = str(sep)
    return sep.join(lmap(str, listarg))

def lmap(func, listarg):
    """Map given function to given list and return a list instead of iterator"""
    return list(map(func, listarg))

#--------------------------------
# Read files smartly
#--------------------------------

def load_file_lines(filename):
    """Try to open the given file and read the content.
    Return the file as list of lines (each as string)
    """
    c_log = logger_setup(__name__)

    filename = str(filename)
    # Try to open file and report failures
    try:
        in_f = open(filename, 'r')
    except:
        c_log.error("Invalid file %s", filename)

    lines = [l.strip() for l in in_f.readlines()]
    in_f.close()
    return lines

# Load data (comments+data)
def load_stream(stream, comment_char="#", f=lambda x: x):
    """Load given stream object. Divide lines between comments and data.
    Comment char can be given as input.
    A function f can be given given as input and applied to each non-comment field."""
    tmp_in = stream.readlines()

    # Read the input file and filter the bash-like commentss
    comments = [l.split() for l in tmp_in if l[0] == comment_char]
    tmp_in = [[f(x) for x in l.split()]
              for l in tmp_in if l[0] != comment_char]
    return comments, tmp_in

def load_file(filename, comment_char="#"):
    """Load given filename. Divide lines between comments and data.
    Comment char can be given as input. Wrapped of load_stream function."""
    # TODO Regex support for multiple comment types.
    with open(filename, 'r') as in_file:
        return load_stream(in_file, comment_char)
    
def load_float_file(filename, comment_char="#"):
    """Load given numeric filename: each non-comment field will be cast to float. 
    Divide lines between comments and data.
    Comment char can be given as input. Wrapped of load_stream function."""
    # TODO Regex support for multiple comment types.
    with open(filename, 'r') as in_file:
        # Appreciate the power of **kwarg expansion!
        return load_stream(in_file, **{"comment_char" : comment_char, "f": float})

#--------------------------------
# String formatting
#--------------------------------

def bash_lines2fields_list(line_lst, delim="\s"):
    """Load filename, read lines and divide into fields.
    Returns a list of list of fields, i.e. [ [f11,f12,..], [f21,f22,...] ] .
    Lines starting with # are skipped (assumed as comments)
    """

    # Skip comments, i.e. lines starting with "#"
    return [l.split(delim) for l in line_lst
            if l.strip()[0] != '#']

#def list_fixwidth(in_l, width=None):
#    """Return a equally width-formatted string from a list.
# 
#    Width is give as param or auto-computed from strings length
#    """
# 
#    in_l = lmap(str, in_l) # You're never safe enough
#    # If not given, width is the max length of the given strings plus 2 (arbitrary)
#    if width is None:
#        width = 2+max([len(s) for s in in_l])
#    # Apply the format to each string
#    in_l = [field.ljust(width) for field in in_l]
#    # Join them together and return
#    return strlist(in_l).strip()
def list_fixwidth(args, w=None):
    """Return a constant-width string from a list."""
    args = list(map(str, args)) # Converte all fields to string. You're never safe enough
    # If width is not provided, compute a reasonable estimation from arguments.
    if w is None: w = 2 + max([len(s.strip()) for s in args])
    # Join the pieces together
    # Quick-explain: join n formatting command together and sub the provided args (expanded list).
    # Strip to avoid traling and leading spaces. w-1 bc we join using spaces.
    return " ".join(["{:<{width}}"]*len(args)).format(*args, width=(w-1)).strip()

def cols_width_fix(rows, width=None):
    """Apply fixwidth to a nested container.

    Width is max width of strings in obj.
    Structure assumed is list of rows: [ [<row1>], [<row2>], ...]
    Returns a list of fixed-colum-width strings.
    """

    # Flat eventually nested rows and convert to string
    rows = [lmap(str, lflatten(r)) for r in rows]
    if width == None:
        # Find max width amonst all fields. Add arbitrary spacing
        width = 1+max([len(s.strip()) for s in flatten(rows)])
    return [list_fix_width(r, width) for r in rows]

def list_fix_width(args, w=None):
    """Return a equally width-formatted string from a list.

    Width is give as param or auto-computed from strings length.
    Everything is converted to str using std settings.
    """

    args = lmap(str, args) # You're never safe enough
    # Convert to str, just in case.
    if w is None:
        w = 2+max([len(s.strip()) for s in args])
    return " ".join(["{:<{width}}"]*len(args)).format(*args, width=w).strip()

#--------------------------------
# Flatten nested lists
#--------------------------------

# Nice recursive, yield-wise flatten function
def flatten(l):
    for el in l:
        if isinstance(el, collections.Iterable) and not isinstance(el, (str, bytes)):
            yield from flatten(el)
        else:
            yield el

# Lazy way of do it...
def lflatten(l):
    """Returns a flat list from a nested one"""

    return  list(flatten(l))
