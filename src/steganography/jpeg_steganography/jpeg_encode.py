from itertools import groupby
import numpy as np
import argparse
import zigzag_encoding
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
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("v", type=str, help="Vessel Image")
    parser.add_argument("s", type=str, help="Secret Image")
    args = parser.parse_args()
    return args

def remove_rle_file():
    try:
        os.remove("image.csv")
    except OSError:
        pass

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
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
    cv2.imwrite("%s.jpeg" % name, matrix)


def clean_values(matrix):
    matrix[matrix>256] = 256
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
    with open("image.csv", "w") as f:
        wr = csv.writer(f)
        wr.writerow([height, width])

def create_run_length_encoding(block):
    rle = [[i, len([*group])] for i, group in groupby(block)]
    with open("image.csv", "a") as f:
        wr = csv.writer(f)
        wr.writerow(rle)

def run_length_to_image(qtmatrix):
    block_arr = []
    height_and_width_found = False
    count = 0
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

def create_blocks(matrix):
    data = []
    for i in range(matrix.shape[0]//8):
        for j in range(matrix.shape[1]//8):
            data.append(matrix[i*8:i*8+8,j*8:j*8+8])
    return data


def lsb_embed_secret(secret, compressed):
    block_count = 0
    for i in range(compressed.shape[0]//8):
        for j in range(compressed.shape[1]//8):
            if block_count<=len(secret):
                block = compressed[i*8:i*8+8, j*8:j*8+8]
                block_count+=1
                for row in range(8):
                    secret_to_embed = np.unpackbits(secret[0])
                    secret.pop(0)
                    for column in range(8):
                        binary_repr = np.unpackbits(block[row,column])
                        binary_repr[-1] = secret_to_embed[column]
                        block[row, column] = np.packbits(binary_repr)
                compressed[i*8:i*8+8, j*8:j*8+8] = block       
            else:
                
                return compressed
    return compressed

def lsb_decode_secret():
    img = get_file("compressed.jpeg")
    data = create_blocks(img)
    secret = []
    retrieved = 0
    for block in data:
        secret_pixel = []
        if retrieved<14568:
            for row in range(8):
                for column in range(8):
                    pixel = np.unpackbits(block[row,column])
                    secret_pixel.append(pixel[-1])
                secret.extend(np.packbits(secret_pixel))
                retrieved+=1
    return secret

def split_secret(matrix):
    secret_array = np.array(matrix)
    secret_array = list(secret_array[0:12,0:12].flatten())
    return secret_array


def handle_channel(img, quantization_matrix):
    split_into_blocks(img, quantization_matrix)
    compressed_arr = run_length_to_image(quantization_matrix)
    remove_rle_file()
    return compressed_arr

def main():

    remove_rle_file()

    args = get_arguments()

    img = get_file(args.v)
    secret = get_file(args.s)

    secret = split_secret(secret)

    if len(img.shape) == 2:
        compressed_arr = clean_values(handle_channel(img, LUMINANCE_MATRIX))
        compressed_arr = lsb_embed_secret(secret, np.uint8(compressed_arr))
        create_image(compressed_arr, "compressed")
        recovered  = np.uint8(lsb_decode_secret())
        create_image(recovered, "secret")
        #handle_channel(secret, luminance_quantization_matrix)
    else:
        channel_matrix = {0: LUMINANCE_MATRIX, 1:CHROMINANCE_MATRIX, 2:CHROMINANCE_MATRIX}
        for i in range(3):
            img[:,:,i] = handle_channel(img[:,:,i], channel_matrix[i])
        compressed_arr = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
        create_image(clean_values(compressed_arr))
        remove_rle_file()
        

if __name__ == "__main__":
    main()