from PIL import Image
from math import log10, sqrt
import argparse
import numpy as np
import subprocess
import os
import math
import plotly.graph_objects as go


def get_arguments():
    parser = argparse.ArgumentParser(description="JPEG Encoding tool")
    parser.add_argument("-u", "--uncompressed", type=str, help="Uncompressed Image")
    parser.add_argument("-c", "--compressed", type=str, help="Compressed Image")
    parser.add_argument("-m", "--mode", choices=["single", "all"], type=str, help="Mode")
    args = parser.parse_args()
    return args

def convert_to_grayscale(name):
    img=Image.open(name).convert("LA")
    temp = np.array(img)
    img.close()
    return temp

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    img = Image.open("%s" % name)
    img = img.resize((8*(math.ceil(img.width/8)), 8*(math.ceil(img.height/8))))
    temp = np.array(img)
    img.close()
    return temp
    
#https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/ - Adapted MSE and PSNR implementation

def MSE(uncompressed, compressed):
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
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel/sqrt(mean_square_error))
    return psnr

def handle_single(*args):
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
    fig = go.Figure(data=[
        go.Bar(name="MSE", x=images, y=mse_list),
        go.Bar(name="PSNR", x=images, y=psnr_list)
    ])

    fig.update_layout(barmode="group", title="Mean Square Error and Peak Signal to Noise Ratio of images compressed using JPEG algorithm")
    fig.show()
    
def main():
    args = get_arguments()

    image_list = []
    mse_list = []
    psnr_list = []

    if args.mode == "single":
        handle_single(args)
    else:
        image_files = []
        dir = "../test_images"
        for image in os.listdir(dir):
            if image.endswith(".bmp") or image.endswith(".jpg"):
                full_path = os.path.join(dir, image)
                subprocess.call(["python", "jpeg_encode.py", "-v", full_path, "-s", full_path, "-m", "Compress"])
                mse, psnr = handle_single(full_path, "compressed.jpeg")
                image_list.append(image)
                mse_list.append(mse)
                psnr_list.append(psnr)
    create_figure(image_list, mse_list, psnr_list)

    

if __name__ == "__main__":
    main()