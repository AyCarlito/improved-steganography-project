import numpy as np
from PIL import Image
import os
import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Decoding tool")
    parser.add_argument("s", type=str, help="Stego Image")
    parser.add_argument("a", choices=["standard", "improved"], type=str, help="Algorithm. Standard or Improved")

    args = parser.parse_args()
    return args


def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    print("Opening %s" % name)
    temp = Image.open("%s.bmp" % name).convert("L")
    temp_arr = np.array(temp)
    temp.close()
    return temp_arr

def get_bitplane_arr(matrix):
    """
    Gets binary encoding of each pixel.
    512x512x8 matrix. -> 512x512 pixels. 8 -> binary value of pixel.
    """
    temp_bitplane_arr = np.zeros((matrix.shape[0], matrix.shape[1], 8))
    temp_bitplane_arr[:,:,0] = np.copy(matrix)

    binary_encoding = np.unpackbits(np.uint8(temp_bitplane_arr[:,:,0]))
    binary_encoding = np.reshape(binary_encoding,(temp_bitplane_arr.shape[0], temp_bitplane_arr.shape[1],8))
    return binary_encoding

def get_complexity(matrix):
    current_complexity = 0
    maximum_complexity = ((matrix.shape[0]-1) * matrix.shape[1]) + ((matrix.shape[1]-1) * matrix.shape[0])

    current_pixel = matrix[0,0]
    for index, value in np.ndenumerate(matrix):
        if current_pixel!=value:
            current_complexity+=1
            current_pixel=value

    current_pixel = matrix[0,0]
    for index, value in np.ndenumerate(matrix.transpose()):
        if current_pixel!=value:
            current_complexity+=1
            current_pixel=value
    return current_complexity/maximum_complexity

def split_into_blocks(matrix, complexity_dictionary):
    data = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in range(7, -1, -1):
        for i in range(matrix.shape[0]//9):
            for j in range(matrix.shape[1]//9):
                if(get_complexity(matrix[i*9:i*9+8,j*9:j*9+8,k]) > complexity_dictionary[k]):
                    data.append(matrix[i*9:i*9+9,j*9:j*9+9,k])               
    return data

def create_complexity_dictionary(algorithm):
    complexities = {"improved":{0:0, 1:0, 2:0.4, 3:0.425, 4:0.45, 5:0.475, 6:0.5, 7:0.525}, 
                    "standard":{0:0.45, 1:0.45, 2:0.45, 3:0.45, 4:0.45, 5:0.45, 6:0.45, 7:0.45}}
    return complexities[algorithm]


def conjugate(matrix):
    checkerboard = np.indices((matrix.shape[0],matrix.shape[1])).sum(axis=0) % 2
    ones = np.ones((matrix.shape[0], matrix.shape[1]))
    conjugated = np.logical_xor(checkerboard, matrix).astype(int)
    conjugated = np.logical_xor(conjugated,ones).astype(int)
    return conjugated

def extract_meta_data(payload, stego_arr):
    meta_data = payload[0]  
    payload.pop(0)
    if meta_data[8,8] == 1:
        meta_data = conjugate(meta_data)
        meta_data[8,8]=0

    
    total_blocks = np.ravel(meta_data[:4,:])
    height = np.ravel(meta_data[4:6,:])
    width = np.ravel(meta_data[6:8,:])



    total_blocks = int("".join(str(elem) for elem in total_blocks), 2)
    height = int("".join(str(elem) for elem in height), 2)
    width = int("".join(str(elem) for elem in width), 2)

    if (height>stego_arr.shape[0]):
        raise MemoryError("Wrong algorithm used for decoding")
        quit()

    return (total_blocks, height, width)


def extract_payload(meta_data, payload):
    secret_payload_arr = np.zeros(( meta_data[1], meta_data[2], 8), dtype="uint8")
    blocks_retrieved = 0

    for k in range(7, -1, -1):
        for i in range(secret_payload_arr.shape[0]//8):
            for j in range(secret_payload_arr.shape[1]//8):
                if (blocks_retrieved < meta_data[0]):
                    block = payload[0]
                    payload.pop(0)
                    if (block[8,8] == 1):
                        block = conjugate(block)
                        block[8,8] = 0
                    secret_payload_arr[i*8:i*8+8, j*8:j*8+8, k] = block[:8,:8]
                    blocks_retrieved+=1
    return secret_payload_arr           


def convert_to_gray_coding(matrix):
    return matrix[:,:]^(matrix[:,:] >> 1)

def convert_from_gray_coding(matrix):
    for (row, col), value in np.ndenumerate(matrix):
        inv = 0
        while(value):
            inv = inv ^ value
            value = value >> 1
        value = inv
        matrix[row, col] = value
    return matrix

def main():

    args = get_arguments()
    stego_arr = get_file(args.s)


    if args.a == "improved":
        stego_arr = convert_to_gray_coding(stego_arr)
        complexities = create_complexity_dictionary("improved")
    else:
        complexities = create_complexity_dictionary("standard")

    stego_bitplane_arr = get_bitplane_arr(stego_arr)

    data = split_into_blocks(stego_bitplane_arr, complexities)
    meta_data = extract_meta_data(data, stego_arr)

    payload_arr = extract_payload(meta_data, data)
    secret_payload_arr = np.packbits(payload_arr[:,:]).reshape((meta_data[1], meta_data[2]))


    if args.a == "improved":
        secret_payload_arr = convert_from_gray_coding(secret_payload_arr)

    extracted = Image.fromarray(secret_payload_arr, mode="L")
    extracted.save("extracted.bmp")

if __name__ == "__main__":
    main()