"""
.. module:: jpeg_encode
   :synopsis: Functionality of JPEG Compression is defined here
.. moduleauthor::  Daniel Hislop
"""
from jpeg_tool import lsb_jpeg
from jpeg_tool import zigzag_encoding
from itertools import groupby
import numpy as np
import argparse
import cv2
import csv
import math
import os
import ast

LUMINANCE_MATRIX = np.array([
    [16,11,10,16,24,40,51,61],
    [12,12,14,19,26,58,60,55],
    [14,13,16,24,40,57,69,56],
    [14,17,22,29,51,87,80,62],
    [18,22,37,56,68,109,103,77],
    [24,35,55,64,81,104,113,92],
    [49,64,78,87,103,121,120,101],
    [72,92,95,98,112,100,103,99]
])

CHROMINANCE_MATRIX = np.array([
    [17,18,24,47,99,99,99,99],
    [18,21,26,66,99,99,99,99],
    [24,26,56,99,99,99,99,99],
    [47,66,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99],
    [99,99,99,99,99,99,99,99]
])

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Arguments are specified as optional arguments meaning any combination of arguments 
        can be provided. Additionally, choice of algorithm is restricted to predefined selection.
    
    Returns:
        Namespace: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="JPEG Encoding tool")
    parser.add_argument("-v", "--cover", type=str, help="Cover Image")
    parser.add_argument("-s", "--payload", type=str, help="Payload Image")
    parser.add_argument("-m", "--mode", type=str, choices=["LSB", "TLSBRandom", "TLSB", "Compress"], help="Algorithm")
    args = parser.parse_args()
    return args

def remove_rle_file():
    """**Remove RLE csv file if it exists**
    """
    try:
        os.remove("image.csv")
    except OSError:
        pass

def get_file(name):
    """**Read in image file using OpenCV**

        Read file using OpenCV imread. IMREAD_UNCHANGED flag reads file as is. Check length of
        shape, this will determine if we have an 8-bit grayscale of 24-bit colour RGB image. 
        If 8-bit colour, read in the image again using IMREAD_GRAYSCALE flag, otherwise read
        image and convert from BGR to YCrCb colour scheme. Images are resized such that 
        height and width are divisible by 8.

    Args:
        name (String): File name

    Returns:
        [type]: [description]
    """
    img = cv2.imread(name, cv2.IMREAD_UNCHANGED)
    if len(img.shape) == 2:
        matrix = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
        image = cv2.resize(matrix, (8*(math.ceil(matrix.shape[1]/8)), 8*(math.ceil(matrix.shape[0]/8))))
    else:
        BGR = cv2.imread(name)
        matrix = cv2.cvtColor(BGR, cv2.COLOR_BGR2YCrCb)
        image = cv2.resize(matrix, (8*(math.ceil(matrix.shape[1]/8)), 8*(math.ceil(matrix.shape[0]/8))))
    return image

def create_image(matrix, name):
    """**Write image to disk**

        

    Args:
        matrix ([type]): [description]
        name ([type]): [description]
    """
    cv2.imwrite("%s.jpeg" % name, matrix, [cv2.IMWRITE_JPEG_QUALITY, 100])


def clean_values(matrix):
    """**Clean pixel values outside minimum or maximum value**

        Compression process can result in negative values of values greater than 255. Since
        these are not valid values we change them. Less than 0 -> 0. Greater than 255 -> 255.

    Args:
        matrix ([type]): Non-cleaned pixel values of image

    Returns:
        [type]: Cleaned pixel values of image
    """
    matrix[matrix>255] = 255
    matrix[matrix<0] = 0
    return matrix


def split_into_blocks(img, qtmatrix):
    """**Lossy compression process**

        Write image dimensions to csv. Loop through each 8x8 block. Perform DCT on block.
        Normalise with quantisation matrix. Reorder coefficients using zigzag encoding.
        Create RLE encoding. Reshape back into 8x8 and add to compressed array.

    Args:
        img ([type]): [description]
        qtmatrix (ndarray): Quantization matrix

    Returns:
        ndarray: Compressed array.
    """
    compressed = np.zeros((img.shape[0], img.shape[1]))
    image_size_to_csv(img.shape[0],img.shape[1])
    compressed[0:compressed.shape[0], 0:compressed.shape[1]] = img[0:img.shape[0],0:img.shape[1]]
    for i in range(compressed.shape[0]//8):
        for j in range(compressed.shape[1]//8):
            block = compressed[i*8:i*8+8,j*8:j*8+8]        
            discrete_cosine_transform = cv2.dct(block)     
            quantised_matrix = np.divide(discrete_cosine_transform, qtmatrix).astype(int)
            normalised = zigzag_encoding.zigzag_single(quantised_matrix) 
            create_run_length_encoding(normalised)
            compressed[i*8:i*8+8,j*8:j*8+8] = quantised_matrix.reshape(8,8)
    return compressed

def image_size_to_csv(height, width):
    """**Height and width of image as first row in CSV**

    Args:
        height (int): Height of image
        width (int): Width of image
    """
    with open("image.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerow([height, width])

def create_run_length_encoding(block):
    """**Create RLE for a block**

        Create list of lists where each list is a value and count of consecutive occurences.

    Args:
        block ([ndarray]): 8x8 block of normalised coefficients
    """
    rle = [[i, len([*group])] for i, group in groupby(block)]
    with open("image.csv", "a", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(rle)

def run_length_to_image(qtmatrix):
    """**Create compressed array from RLE**

        Open CSV file. Read height and width first, (first row). Take each subsequent row 
        and create 8x8 block from it and add it to list. Resulting list is reshaped into 
        original dimensions by setting each block as an 8x8 array slice in compressed array. 

    Args:
        qtmatrix (ndarray): Quantization matrix

    Returns:
        ndarray: Array of compressed image
    """
    block_arr = []
    height_and_width_found = False
    with open("image.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not height_and_width_found:
                height = int(row[0])
                width = int(row[1])
                height_and_width_found = True
                continue
            block = construct_block(row, qtmatrix)
            block_arr.append(block)
            
    compressed_arr = np.zeros((height,width))
    block_n = 0
    for i in range(height//8):
        for j in range(width//8):
            compressed_arr[i*8:i*8+8, j*8:j*8+8] = block_arr[block_n]
            block_n+=1
    return compressed_arr

def construct_block(row, qtmatrix):
    """**Create block from RLE**

    take row, loop through each list in row, convert and add to 1D array. Use zigzag
    encoding to create 8x8. Normalise and perform IDCT to create block.

    Args:
        row (String): Row from csv. Lists of lists as string.
        qtmatrix (ndarray): Quantization matrix

    Returns:
        ndarray: Contructed 8x8 block
    """
    block = []
    for each_rle in row:
        each_rle_as_list = ast.literal_eval(each_rle)
        block.extend([each_rle_as_list[0]]*each_rle_as_list[1])

    normalised = zigzag_encoding.inverse_zigzag_single(np.asarray(block))
    de_quantized = np.multiply(normalised, qtmatrix)
    compressed_image_block = cv2.idct(np.float32(de_quantized)).astype(int)
    return compressed_image_block

def handle_channel(img, quantization_matrix):
    """*Helper function for handling single channel**

    Call lossy compression function with channel and quantization matrix. Create
    compressed area from RLE. Delete CSV file.

    Args:
        img ([type]): [description]
        quantization_matrix (ndarray): Quantization matrix

    Returns:
        ndarray: Compressed channel
    """
    split_into_blocks(img, quantization_matrix)
    compressed_arr = run_length_to_image(quantization_matrix)
    remove_rle_file()
    return compressed_arr

def handle_grayscale(vessel, secret, qtmatrix, mode):
    """**Compress 8-bit colour image**

    Compress and then embed if necessary. 

    Args:
        vessel ([type]): [description]
        secret ([type]): [description]
        qtmatrix (ndarray): Quantization matrix
        mode (String): Algorithm chosen by user
    """
    compressed_arr = clean_values(handle_channel(vessel, qtmatrix))
    if mode=="TLSB":
        compressed_arr = lsb_jpeg.lsb_embed_secret(secret, np.uint8(compressed_arr))
    elif mode=="TLSBRandom":
        compressed_arr = lsb_jpeg.random_lsb_embed_secret(secret, np.uint8(compressed_arr))
    create_image(compressed_arr, "compressed")
    
def handle_colour(vessel, secret, channel_matrix, mode):
    """**Compress 24-bit colour image**

    Loop through each channel in image and call handle_channel helper. If embedding, embed
    single channel in singel channel if two 8-bit colour images. Embed single channel in Y 
    channel if 8-bit colour payload and 24-bit colour cover. Embed each channel in each channel
    if two 24-bit colour images. Convert from YCrCb to BGR. Clean values, and create image. 
    Remove RLE file.

    Args:
        vessel ([type]): [description]
        secret ([type]): [description]
        channel_matrix (dict): Dictionary mapping channel to quantization matrices.
        mode (String): Algorithm chosen by user
    """
    for i in range(3):
        vessel[:,:,i] = handle_channel(vessel[:,:,i], channel_matrix[i])
    if mode=="TLSB":
        if len(secret.shape) == 2:
            vessel[:,:,0] = lsb_jpeg.lsb_embed_secret(secret, np.uint8(vessel[:,:,0]))
        else:
            for i in range(3):
                vessel[:,:,i] = lsb_jpeg.lsb_embed_secret(secret[:,:,i], np.uint8(vessel[:,:,i]))
    compressed_arr = cv2.cvtColor(vessel, cv2.COLOR_YCrCb2BGR)
    create_image(clean_values(compressed_arr), "compressed")
    remove_rle_file()

def embeddable(vessel, secret):
    """**Check if payload can be embedded in cover**

    Maximum capacity using LSB is 1/8 (12.5%). Equivalent to total pixels in cover divided by
    8. If payload pixels <= cover pixels / 8, then we can embed.

    Args:
        vessel (ndarray): Numpy array of cover image
        secret ([type]): Numpy array of payload image

    Returns:
        bool: True of False value indicating if payload can be embedded.
    """
    if((secret.shape[0]*secret.shape[1])>(vessel.shape[0]*vessel.shape[1]/8)):
        print("Insufficient number of vessel bits")
        return False
    elif(len(secret.shape)>len(vessel.shape)):
        print("Cannot embed colour image in grayscale")
        return False
    return True

def main():
    """**Driver code of JPEG encode**

        Remove existing RLE csv file if it exists. Read in files. Quit program if trying to
        embed and payload is not embeddable. If vessel is 8-bit colour call handle grayscale
        helper otherwise call handle_colour helper. 

    """

    remove_rle_file()

    args = get_arguments()

    vessel = get_file(args.cover)
    secret = get_file(args.payload)
    mode = args.mode

    if mode!="Compress":
        if not (embeddable(vessel, secret)):
            quit()

    if len(vessel.shape) == 2:
        handle_grayscale(vessel, secret, LUMINANCE_MATRIX, mode)
    else:
        channel_matrix = {0: LUMINANCE_MATRIX, 1:CHROMINANCE_MATRIX, 2:CHROMINANCE_MATRIX}
        handle_colour(vessel, secret, channel_matrix, mode)
        
        

if __name__ == "__main__":
    main()