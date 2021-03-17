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
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("-s", "--stego", type=str, help="Stego Image")
    parser.add_argument("-m", "--mode", type=str, choices=["LSB", "LSBRandom"], help="Extraction Algorithm")
    args = parser.parse_args()
    return args

def recover(stego_name, algorithm):
    call  = {"LSB": lsb_jpeg.lsb_decode_secret, "LSBRandom": lsb_jpeg.random_lsb_decode_secret}
    recovered = np.asarray(call[algorithm](stego_name))
    if recovered.shape[0] == 1:
        recovered = recovered[0]
    jpeg_encode.create_image(recovered, "secret")

def main():

    args = get_arguments()
    recover(args.stego, args.mode)

if __name__ == "__main__":
    main()


    