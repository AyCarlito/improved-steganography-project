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
    matrix[matrix>255] = 255
    matrix[matrix<0] = 0
    return matrix


def split_into_blocks(img, qtmatrix):
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
    with open("image.csv", "w", newline='') as f:
        wr = csv.writer(f)
        wr.writerow([height, width])

def create_run_length_encoding(block):
    rle = [[i, len([*group])] for i, group in groupby(block)]
    with open("image.csv", "a", newline='') as f:
        wr = csv.writer(f)
        wr.writerow(rle)

def run_length_to_image(qtmatrix):
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
    block = []
    for each_rle in row:
        each_rle_as_list = ast.literal_eval(each_rle)
        block.extend([each_rle_as_list[0]]*each_rle_as_list[1])

    normalised = zigzag_encoding.inverse_zigzag_single(np.asarray(block))
    de_quantized = np.multiply(normalised, qtmatrix)
    compressed_image_block = cv2.idct(np.float32(de_quantized)).astype(int)
    return compressed_image_block

def handle_channel(img, quantization_matrix):
    split_into_blocks(img, quantization_matrix)
    compressed_arr = run_length_to_image(quantization_matrix)
    remove_rle_file()
    return compressed_arr

def handle_grayscale(vessel, secret, qtmatrix, mode):
    compressed_arr = clean_values(handle_channel(vessel, qtmatrix))
    if mode=="TLSB":
        compressed_arr = lsb_jpeg.lsb_embed_secret(secret, np.uint8(compressed_arr))
    elif mode=="TLSBRandom":
        compressed_arr = lsb_jpeg.random_lsb_embed_secret(secret, np.uint8(compressed_arr))
    create_image(compressed_arr, "compressed")
    
def handle_colour(vessel, secret, channel_matrix, mode):
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
    if((secret.shape[0]*secret.shape[1])>(vessel.shape[0]*vessel.shape[1]/8)):
        print("Insufficient number of vessel bits")
        return False
    elif(len(secret.shape)>len(vessel.shape)):
        print("Cannot embed colour image in grayscale")
        return False
    return True

def main():

    remove_rle_file()

    args = get_arguments()

    vessel = get_file(args.cover)
    secret = get_file(args.payload)
    mode = args.mode

    if not (embeddable(vessel, secret)):
        quit()

    if len(vessel.shape) == 2:
        handle_grayscale(vessel, secret, LUMINANCE_MATRIX, mode)
    else:
        channel_matrix = {0: LUMINANCE_MATRIX, 1:CHROMINANCE_MATRIX, 2:CHROMINANCE_MATRIX}
        handle_colour(vessel, secret, channel_matrix, mode)
        
        

if __name__ == "__main__":
    main()