from itertools import groupby
import numpy as np
import argparse
import zigzag_encoding
import cv2
import csv
import math
import os
import ast

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("v", type=str, help="Vessel Image")
    parser.add_argument("s", type=str, help="Secret Image")
    args = parser.parse_args()
    return args

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    img = cv2.imread(name, cv2.IMREAD_GRAYSCALE)
    return img

def remove_rle_file():
    try:
        os.remove("image.csv")
    except OSError:
        pass
    return

def clean_values(matrix):
    matrix[matrix>255] = 255
    matrix[matrix<0] = 0
    return matrix

def create_image(matrix):
    cv2.imwrite("compressed.bmp",np.uint8(matrix))
    return

def create_quantization_matrix():
    return(np.array([
        16,11,10,16,24,40,51,61,
        12,12,14,19,26,58,60,55,
        14,13,16,24,40,57,69,56,
        14,17,22,29,51,87,80,62,
        18,22,37,56,68,109,103,77,
        24,35,55,64,81,104,113,92,
        49,64,78,87,103,121,120,101,
        72,92,95,98,112,100,103,99
    ]).reshape(8,8))

def image_size_to_csv(height, width):
    with open("image.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow([height, width])
    return

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

def create_run_length_encoding(block):
    rle = [[i, len([*group])] for i, group in groupby(block)]
    with open("image.csv", "a") as f:
        wr = csv.writer(f)
        wr.writerow(rle)
    return

def construct_block(row, qtmatrix):
    block = []
    for each_rle in row:
        each_rle_as_list = ast.literal_eval(each_rle)
        block.extend([each_rle_as_list[0]]*each_rle_as_list[1])
    normalised = zigzag_encoding.inverse_zigzag_single(np.asarray(block))
    de_quantized = np.multiply(normalised, qtmatrix)
    compressed_image_block = cv2.idct(np.float32(de_quantized))
    return compressed_image_block


def run_length_to_image():
    block_arr = []
    height_and_width_found = False
    quantization_matrix = create_quantization_matrix()
    with open("image.csv", "r") as f:
        reader = csv.reader(f)
        for row in reader:
            if not height_and_width_found:
                height = int(row[0])
                width = int(row[1])
                height_and_width_found = True
                continue
            block = construct_block(row, quantization_matrix)
            block_arr.append(block)
    compressed_arr = np.zeros((height,width))
    block_n = 0
    for i in range(height//8):
        for j in range(width//8):
            compressed_arr[i*8:i*8+8, j*8:j*8+8] = block_arr[block_n]
            block_n+=1
    return compressed_arr
    
def main():

    remove_rle_file()

    args = get_arguments()
    
    img = get_file(args.v)
    
   
    quantization_matrix = create_quantization_matrix()
    compressed_arr = split_into_blocks(img, quantization_matrix)
    compressed_arr = run_length_to_image()
    
    create_image(compressed_arr)
    remove_rle_file()
    
if __name__ == "__main__":
    main()