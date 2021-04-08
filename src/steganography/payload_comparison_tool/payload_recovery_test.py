"""
.. module:: payload_recovery_test
   :synopsis: Functionality of payload comparison is defined here
.. moduleauthor::  Daniel Hislop
"""

import argparse
import numpy as np
from PIL import Image

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Mode is a positional argument meaning it has to be provided. Others are optional
        so any can be specified. Both mode and algorithm are restricted choice.
    
    Returns:
        Namespace: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="Payload Comparison Tool")
    parser.add_argument("-o", "--original", type=str, help="Original Payload")
    parser.add_argument("-r", "--recovered", nargs="?", type=str, help="Recovered Payload")
    args = parser.parse_args()
    return args

def get_file(name):
    """**Get File**

        Read in image using pillow library and return as numpy array

    Args:
        name (String): Name of image file
    Returns:
        ndarray: Numpy array of image file
    """
    print("Opening %s" % name)
    temp = Image.open("%s" % name)
    return (np.array(temp))

def compare(args):
    """**Image Comparison**

        Compare two images using numpy. Image 1 and 2 are numpy arrays. Use np_array_equal to
        compare. If equal then match, otherwise no match.

    Args:
        args (Namespace): Parsed user arguments containing path to original and path to 
        recovered payloads.
    """
    original = get_file(args.original)
    recovered = get_file(args.recovered)
    if (np.array_equal(original, recovered)):
        print("Recovered matches original")
    else:
        print("Recovered does not match original")

def main():
    """**Driver Code**

        Parse user arguments and call comparison function
    """
    args = get_arguments()
    compare(args)

if __name__ == "__main__":
    main()

