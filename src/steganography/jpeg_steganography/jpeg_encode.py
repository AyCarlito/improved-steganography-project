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
    parser.add_argument("q", type=str, help="Quality Factor")
    parser.add_argument("m", type=str, choices=["LSB"], help="Embedding Algorithm")
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
    cv2.imwrite("%s.jpeg" % name, matrix, [cv2.IMWRITE_JPEG_QUALITY, 100])


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


# def lsb_embed_secret(secret, compressed):
#     block_count = 0
#     for i in range(compressed.shape[0]//8):
#         for j in range(compressed.shape[1]//8):
#             if block_count<=len(secret):
#                 block = compressed[i*8:i*8+8, j*8:j*8+8]
#                 block_count+=1
#                 for row in range(8):
#                     secret_to_embed = np.unpackbits(secret[0])
#                     secret.pop(0)
#                     for column in range(8):
#                         binary_repr = np.unpackbits(block[row,column])
#                         binary_repr[-1] = secret_to_embed[column]
#                         block[row, column] = np.packbits(binary_repr)
#                 compressed[i*8:i*8+8, j*8:j*8+8] = block       
#             else:
                
#                 return compressed
#     return compressed

# def lsb_decode_secret():
#     img = get_file("compressed.jpeg")
#     data = create_blocks(img)
#     secret = []
#     retrieved = 0
#     for block in data:
#         secret_pixel = []
#         if retrieved<14568:
#             for row in range(8):
#                 for column in range(8):
#                     pixel = np.unpackbits(block[row,column])
#                     secret_pixel.append(pixel[-1])
#                 secret.extend(np.packbits(secret_pixel))
#                 retrieved+=1
#     return secret

def lsb_embed_secret(secret, vessel):
    index = 0

    height = vessel.shape[0]
    width = vessel.shape[1]

    secret_height = secret.shape[0]
    secret_width = secret.shape[1]
    secret = secret.flatten()
    vessel = vessel.flatten()

    for secret_pixel in secret:
        secret_bin_repr = np.unpackbits(secret_pixel)
        vessel_selection = vessel[index*8:index*8+8]
        for i, vessel_pixel in enumerate(vessel_selection):
            vessel_pixel_bin_repr = np.unpackbits(vessel_pixel)
            vessel_pixel_bin_repr[-1] = 1
            vessel_pixel_bin_repr[-2] = 0
            vessel_pixel_bin_repr[-3] = secret_bin_repr[i]
            vessel_pixel = np.packbits(vessel_pixel_bin_repr)
            vessel_selection[i] = vessel_pixel
        vessel[index*8:index*8+8] = vessel_selection
        index+=1
    vessel[0] = (secret_height/8)
    vessel[8] = (secret_width/8)
    return vessel.reshape((height,width))

def lsb_decode_secret():
    stego = get_file("compressed.jpeg").flatten()
    secret = []
    index = 0

    height = stego[0]*8
    width = stego[8]*8
    for index in range(len(stego)//8):
        stego_selection = stego[index*8:index*8+8]
        secret_pixel = []
        for i, stego_pixel in enumerate(stego_selection):
            stego_pixel_bin_repr = np.unpackbits(stego_pixel)
            secret_pixel.append(stego_pixel_bin_repr[-3])
        secret.append(np.packbits(secret_pixel)[0])
        index+=1
    return np.asarray(secret)[0:(height*width)].reshape((height, width))
    
def handle_grayscale(vessel, secret, qtmatrix, mode):
    compressed_arr = clean_values(handle_channel(vessel, qtmatrix))
    if mode=="LSB":
            compressed_arr = lsb_embed_secret(secret, np.uint8(compressed_arr))
            create_image(compressed_arr, "compressed")
            recovered = lsb_decode_secret()
            create_image(recovered, "secret")
    else:
        create_image(compressed_arr, "compressed")
    
def handle_colour(vessel, secret, channel_matrix, mode):
    for i in range(3):
        vessel[:,:,i] = handle_channel(vessel[:,:,i], channel_matrix[i])
    if mode=="LSB":
        vessel[:,:,0] = lsb_embed_secret(secret, np.uint8(vessel[:,:,0]))
        vessel[0,0,1] = vessel[0,0,0]
        vessel[0,0,2] = vessel[0,0,0]
        vessel[0,8,1] = vessel[0,8,0]
        vessel[0,8,2] = vessel[0,8,0]
        compressed_arr = cv2.cvtColor(vessel, cv2.COLOR_YCrCb2BGR)
        create_image(clean_values(compressed_arr), "compressed")
        recovered = np.asarray(lsb_decode_secret())
        create_image(recovered, "secret")
    else:
        compressed_arr = cv2.cvtColor(img, cv2.COLOR_YCrCb2BGR)
        create_image(clean_values(compressed_arr), "compressed")
    remove_rle_file()

def main():

    remove_rle_file()

    args = get_arguments()

    img = get_file(args.v)
    secret = get_file(args.s)
    quality_factor = int(args.q)
    mode = args.m

    SCALED_LUMINANCE_MATRIX = np.floor_divide(LUMINANCE_MATRIX, quality_factor)
    SCALED_CHROMINANCE_MATRIC = np.floor_divide(CHROMINANCE_MATRIX, quality_factor)

    if((secret.shape[0]*secret.shape[1])>(img.shape[0]*img.shape[1]/8)):
        print("Cannot embed secret in image")
        quit()

    if len(img.shape) == 2:
        handle_grayscale(img, secret, SCALED_LUMINANCE_MATRIX, mode)
    else:
        channel_matrix = {0: SCALED_LUMINANCE_MATRIX, 1:SCALED_CHROMINANCE_MATRIC, 2:SCALED_CHROMINANCE_MATRIC}
        handle_colour(vessel, secret, channel_matrix, mode)
        
        

if __name__ == "__main__":
    main()