# quantumx_builtins.py
from builtins import input as builtin_input, range as builtin_range
import os
import numpy as np
import pandas as pd


DEBUG_ENABLED = False

def type_of(elem):
    if isinstance(elem, np.ndarray):  # Check if elem is an instance of numpy.ndarray
        return "<class 'array'>"
    else:
        return type(elem)


def array(elem):
    elem = np.array(elem)
    return elem

def about():
    Name = "QuantumX"
    Version = "V1.0"
    Description = "This is an basic programming laguage developed as a project to gain knowledge about how machines works by taking command from programmers, will be further developed in future :) "
    Author = "DHANUSH SELVARAJ"
    Email = "sdhanush451@gmail.com"
    qx ={"Name":"QuantumX","Version":"V1.0","Description":Description,"Author":Author,"Email":Email}
    return qx


def debug(*args):
    """Print debug messages if DEBUG_ENABLED is True."""
    if DEBUG_ENABLED == True:
        print("DEBUG:", " ".join(str(arg) for arg in args))

def output(*args):
    """Print arguments with spaces between them."""
    print(" ".join(str(arg) for arg in args))

def add(a, b):
    """Return the sum of two numbers."""
    return a + b

def input(prompt=""):
    """Read a line from standard input with an optional prompt."""
    return builtin_input(prompt)

def to_int(value):
    """Convert a value to an integer, with error handling."""
    try:
        return int(value)
    except (ValueError, TypeError):
        print(f"Error: Cannot convert '{value}' to integer")
        return 0

def to_float(value):
    """Convert a value to a float, with error handling."""
    try:
        return float(value)
    except (ValueError, TypeError):
        print(f"Error: Cannot convert '{value}' to float")
        return 0.0

def to_str(value):
    """Convert a value to a string."""
    return str(value)

# List operations
def append(lst, item):
    """Append an item to the end of a list and return the modified list."""
    if not isinstance(lst, list):
        raise TypeError("First argument must be a list")
    lst.append(item)
    return lst

def push(lst, item):
    """Synonym for append, adds an item to the end of a list."""
    if not isinstance(lst, list):
        raise TypeError("First argument must be a list")
    lst.append(item)
    return lst

def pop(lst):
    """Remove and return the last item from a list."""
    if not isinstance(lst, list):
        raise TypeError("First argument must be a list")
    if len(lst) == 0:
        raise ValueError("Cannot pop from an empty list")
    return lst.pop()

def length(lst):
    """Return the length of a list."""
    if not isinstance(lst, (list, tuple, str)):
        raise TypeError("Argument must be a list, tuple, or string")
    return len(lst)

def get(lst, index):
    """Return the item at the specified index in a list."""
    if not isinstance(lst, (list, tuple)):
        raise TypeError("First argument must be a list or tuple")
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if index < 0 or index >= len(lst):
        raise IndexError(f"Index {index} out of range for sequence of length {len(lst)}")
    return lst[index]

def set_at(lst, index, value):
    """Set the item at the specified index in a list to a new value."""
    if not isinstance(lst, list):
        raise TypeError("First argument must be a list")
    if not isinstance(index, int):
        raise TypeError("Index must be an integer")
    if index < 0 or index >= len(lst):
        raise IndexError(f"Index {index} out of range for list of length {len(lst)}")
    lst[index] = value
    return lst

# File operations
def fopen(fname, mode="r"):
    """Open a file with the specified mode and return the file object."""
    if not isinstance(fname, str):
        raise TypeError("Filename must be a string")
    try:
        return open(fname, mode)
    except IOError as e:
        print(f"Error opening file '{fname}': {str(e)}")
        return None

def read(f_obj):
    """Read and return the entire content of a file object."""
    if f_obj is None or not hasattr(f_obj, 'read'):
        raise TypeError("Argument must be a file object")
    try:
        content = f_obj.read()
        return content
    except IOError as e:
        print(f"Error reading file: {str(e)}")
        return ""

def store(f_obj, content):
    """Write content to a file object and return True on success."""
    if f_obj is None or not hasattr(f_obj, 'write'):
        raise TypeError("Argument must be a file object")
    try:
        f_obj.write(str(content))
        return True
    except IOError as e:
        print(f"Error writing to file: {str(e)}")
        return False

# Tuple operation
def tup(lst):
    """Convert arguments into a tuple."""
    return tuple(lst)

# Mathematical operation
def power(num, po):
    """Raise num to the power of po."""
    if not isinstance(num, (int, float)) or not isinstance(po, (int, float)):
        raise TypeError("Arguments must be numbers")
    return num ** po

# Utility function
def range(start, end):
    """Return a list of integers from start to end-1."""
    if not isinstance(start, int) or not isinstance(end, int):
        raise TypeError("range arguments must be integers")
    return list(builtin_range(start, end))

# New additions
def concat(str1, str2):
    """Concatenate two strings."""
    if not isinstance(str1, str) or not isinstance(str2, str):
        raise TypeError("Arguments must be strings")
    return str1 + str2

def max_val(*args):
    """Return the maximum value among the arguments."""
    if not args:
        raise ValueError("At least one argument is required")
    return max(args)

def min_val(*args):
    """Return the minimum value among the arguments."""
    if not args:
        raise ValueError("At least one argument is required")
    return min(args)

def close(f_obj):
    """Close a file object."""
    if f_obj is None or not hasattr(f_obj, 'close'):
        raise TypeError("Argument must be a file object")
    try:
        f_obj.close()
        return True
    except IOError as e:
        print(f"Error closing file: {str(e)}")
        return False

builtins = {
    "debug": debug,
    "output": output,
    "add": add,
    "input": input,
    "to_int": to_int,
    "to_float": to_float,
    "to_str": to_str,
    "append": append,
    "push": push,
    "pop": pop,
    "len": length,
    "get": get,
    "set_at": set_at,
    "range": range,
    "tup": tup,
    "power": power,
    "fopen": fopen,
    "read": read,
    "store": store,
    "concat": concat,
    "max": max_val,
    "min": min_val,
    "close": close,
    "about":about,
    "array":array,
    "type_of":type_of
}
