"""
.. module:: jpeg_evaluate
   :synopsis: Functionality of JPEG evaluation is defined here
.. moduleauthor::  Daniel Hislop
"""

from PIL import Image
from math import log10, sqrt
import argparse
import numpy as np
import subprocess
import os
import math
import platform
import plotly.graph_objects as go


def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Arguments are specified as optional arguments meaning any combination of arguments 
        can be provided. Additionally, choice of algorithm is restricted to predefined selection.
    
    Returns:
        Namespace: Parsed user arguments.
    """

    parser = argparse.ArgumentParser(description="JPEG Evaluation tool")
    parser.add_argument("-u", "--uncompressed", type=str, help="Uncompressed Image")
    parser.add_argument("-c", "--compressed", type=str, help="Compressed Image")
    parser.add_argument("-m", "--mode", choices=["single", "all"], type=str, help="Mode")
    args = parser.parse_args()
    return args

def convert_to_grayscale(name):
    """**Convert image to grayscale**

    Args:
        name (String): File Name

    Returns:
        ndarray: Numpy array of converted image
    """

    img=Image.open(name).convert("LA")
    temp = np.array(img)
    img.close()
    return temp

def get_file(name):
    """**Read in image**

       Read image using pillow library, resize diemensions to be divisible by 8, convert to
       numpy array.

    Args:
        name (String): File Name

    Returns:
        ndarray: Image as numpy array
    """
    img = Image.open("%s" % name)
    img = img.resize((8*(math.ceil(img.width/8)), 8*(math.ceil(img.height/8))))
    temp = np.array(img)
    img.close()
    return temp
    
#https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/ - Adapted MSE and PSNR implementation

def MSE(uncompressed, compressed):
    """**Calculate Mean Square Error between two images**

        Use try and except to check if we have single channel images or three channels. Loop
        through each channel and keep running total of error for each channel. Mean of these
        error is taken by dividing by number of channels, then dividing by float of 
        (height x width).

    Args:
        uncompressed (ndarray): Numpy array of Uncompressed image
        compressed (ndarray): Numpy array of compressed image

    Returns:
        float: mean square error
    """
    try:
        val = uncompressed.shape[2]
    except:
        val = 1
    err = 0
    for channel in range(val):
        try:
            err += np.sum((uncompressed[:,:,channel].astype("float") - compressed[:,:,channel].astype("float")) ** 2)
        except IndexError as e:
            err += np.sum((uncompressed.astype("float") - compressed.astype("float")) ** 2)
    err /= val
    err /= float(uncompressed.shape[0] * uncompressed.shape[1])
    return err

def PSNR(mean_square_error):
    """**Calculate Peak Signal to Noise Ratio**

    Args:
        mean_square_error ([type]): Mean Square Error of two images

    Returns:
        float: Peak signal to noise ratio of compressed image
    """
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel/sqrt(mean_square_error))
    return psnr

def handle_single(*args):
    """**Handle a single image**

        Read in files. Bug in jpeg compression where single channel image becomes three
        channel after compression. Check for this and convert both to grayscale if necessary.
        Calculate MSE and psnr.

    Returns:
        2-tuple: 2 element tuple of mean square error and peak signal to noise ratio
        for a single image.
    """
    uncompressed_image = get_file(args[0])
    compressed_image = get_file(args[1])
    if len(compressed_image.shape)== 3 and len(uncompressed_image.shape) == 2:
        uncompressed_image = convert_to_grayscale(args[0])
        compressed_image = convert_to_grayscale(args[1])
    # print(f"Image: {args[0]}")
    mse = MSE(uncompressed_image, compressed_image)
    psnr = PSNR(mse)
    # print(f"Mean Square Error: {mse}")
    # print(f"Peak Signal to Noise Ratio: {psnr} dB")
    return mse, psnr

def create_figure(images, mse_list, psnr_list):
    """**Create graph of MSE and PSNR for each image using plotly**

        Two traces on bar graph, where one is MSE and other is PSNR. x-axis is 
        image file names.

    Args:
        images (list): List of image file names
        mse_list (list): List of MSE values
        psnr_list (list): List of PSNR values
    """
    fig = go.Figure(data=[
        go.Bar(name="MSE", x=images, y=mse_list),
        go.Bar(name="PSNR", x=images, y=psnr_list)
    ])

    fig.update_layout(barmode="group", title="Mean Square Error and Peak Signal to Noise Ratio of images compressed using JPEG algorithm")
    fig.show()
    
def main():
    """**Driver Code**

        Parse user arguments. If only single image to be used then handle single.
        Otherwise, collect each image in test_images directory, compress using jpeg tool,
        calculate MSE and PSNR, and plot graph after all have been done.
    """
    args = get_arguments()

    image_list = []
    mse_list = []
    psnr_list = []

    if args.mode == "single":
        handle_single(args)
    else:
        image_files = []
        dir = "test_images"
        for image in os.listdir(dir):
            if image.endswith(".bmp") or image.endswith(".jpg"):
                full_path = os.path.join(dir, image)
                if platform.system() == "Windows":
                    subprocess.call(["py", "-m", "jpeg_tool.jpeg_encode", "-v", full_path, "-s", full_path, "-m", "Compress"])
                else:
                    subprocess.call(["python3", "-m", "jpeg_tool.jpeg_encode", "-v", full_path, "-s", full_path, "-m", "Compress"])
                mse, psnr = handle_single(full_path, "compressed.jpeg")
                image_list.append(image)
                mse_list.append(mse)
                psnr_list.append(psnr)
    
    image_list.append("Average")
    mse_list.append(sum(mse_list) / len(mse_list))
    psnr_list.append(sum(psnr_list) / len(psnr_list))
    create_figure(image_list, mse_list, psnr_list)

    

if __name__ == "__main__":
    main()