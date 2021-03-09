from PIL import Image
from math import log10, sqrt
import argparse
import numpy as np

def get_arguments():
    parser = argparse.ArgumentParser(description="JPEG Encoding tool")
    parser.add_argument("-u", "--uncompressed", type=str, help="Uncompressed Image")
    parser.add_argument("-c", "--compressed", type=str, help="Compressed Image")
    args = parser.parse_args()
    return args

def get_grayscale_channel(image):
    img_arr = np.array(image)
    image.close()
    return [img_arr]

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    print("Opening %s" % name)
    temp = Image.open("%s" % name)
    if temp.mode == "L":
        channels = get_grayscale_channel(temp.convert("L"))
    elif temp.mode == "P":
        channels = get_grayscale_channel(temp.convert("L"))
    return channels

def MSE(uncompressed, compressed):
    err = np.sum((uncompressed.astype("float") - compressed.astype("float")) ** 2)
    err /= float(uncompressed.shape[0] * uncompressed.shape[1])
    return err

def PSNR(mean_square_error):
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel/sqrt(mean_square_error))
    return psnr


def main():
    args = get_arguments()
    uncompressed_image = get_file(args.uncompressed)[0]
    compressed_image = get_file(args.compressed)[0]

    mean_square_error = MSE(uncompressed_image, compressed_image)
    psnr = PSNR(mean_square_error)
    print(f"Mean Square Error: {mean_square_error}")
    print(f"Peak Signal to Noise Ratio: {psnr} dB")
    
if __name__ == "__main__":
    main()