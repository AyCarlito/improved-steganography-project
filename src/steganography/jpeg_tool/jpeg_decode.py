"""
.. module:: jpeg_decode
   :synopsis: Functionality of JPEG Decoding is defined here
.. moduleauthor::  Daniel Hislop
"""
from jpeg_tool import jpeg_encode
from jpeg_tool import lsb_jpeg
import argparse
import numpy as np

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Arguments are specified as optional arguments meaning any combination of arguments 
        can be provided. Additionally, choice of algorithm is restricted to predefined selection.
    
    Returns:
        Namespace: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="JPEG Decoding Tool")
    parser.add_argument("-s", "--stego", type=str, help="Stego Image")
    parser.add_argument("-m", "--mode", type=str, choices=["LSB", "TLSB", "TLSBRandom"], help="Extraction Algorithm")
    args = parser.parse_args()
    return args

def recover(stego_name, algorithm):
    """**Recovery of payload**

    Dictionary mapping algorithm choice to functions in helper file. Index dictionary with
    user algorithm choice to call function in helper file. Recover payload as numpy array and
    use jpeg encode create image function to write it to disk.

    
    Args:
        stego_name (String): File name of stego image
        algorithm (String): Algorithm to be used during extraction
    """
    call  = {"LSB": lsb_jpeg.lsb_decode_secret, "TLSB": lsb_jpeg.lsb_decode_secret, "TLSBRandom": lsb_jpeg.random_lsb_decode_secret}
    recovered = np.asarray(call[algorithm](stego_name, algorithm))
    if recovered.shape[0] == 1:
        recovered = recovered[0]
    jpeg_encode.create_image(recovered, "extracted")

def main():
    """**Driver Code**

       Parse user arguments. Call recover function with stego name and algorithm choice as
       parameters.
    """

    args = get_arguments()
    recover(args.stego, args.mode)

if __name__ == "__main__":
    main()


    