import numpy as np
from PIL import Image
import os
import argparse

COMPLEXITIES = {"improved":{0:0, 1:0, 2:0.4, 3:0.425, 4:0.45, 5:0.475, 6:0.5, 7:0.525}, "standard":{0:0.3, 1:0.3, 2:0.3, 3:0.3, 4:0.3, 5:0.3, 6:0.3, 7:0.3}}

#Gray Coding Functions Sourced from https://www.geeksforgeeks.org/decimal-equivalent-gray-code-inverse/# 

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

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Decoding tool")
    parser.add_argument("s", type=str, help="Stego Image")
    parser.add_argument("a", choices=["standard", "improved"], type=str, help="Algorithm. Standard or Improved")

    args = parser.parse_args()
    return args


def get_grayscale_channel(image):
    img_arr = np.array(image)
    image.close()
    return [img_arr]

def get_colour_channels(image):
    img_arr = np.array(image)
    r = img_arr[:,:,0]
    g = img_arr[:,:,1]
    b = img_arr[:,:,2]
    image.close()
    return [r,g,b]
   

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
    else:
        channels = get_colour_channels(temp.convert("RGB"))
    return channels

def create_image(array, no_channels):
    modes = {1: "L", 3: "RGB"}
    extracted = Image.fromarray(array, mode=modes[no_channels])
    extracted.save("extracted.bmp")


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

def extract_single_channel_from_single_channel(channel, complexities):
    stego_bitplane_arr = get_bitplane_arr(channel)
    data = split_into_blocks(stego_bitplane_arr, complexities)
    try:
        meta_data = extract_meta_data(data, channel)
    except MemoryError as e:
        return (np.zeros((channel.shape[0], channel.shape[1])))
    payload_arr = extract_payload(meta_data, data)
    secret_payload_arr = np.packbits(payload_arr[:,:]).reshape((meta_data[1], meta_data[2]))
    return secret_payload_arr

def main():

    args = get_arguments()
    
    stego_arr = get_file(args.s)
    stego_arr = [convert_to_gray_coding(channel) for channel in stego_arr]
    complexities = COMPLEXITIES[args.a]

    if len(stego_arr)==1:
        secret_payload_arr = convert_from_gray_coding(extract_single_channel_from_single_channel(stego_arr[0], complexities))
        create_image(secret_payload_arr, 1)
    else:
        secret_channels = []
        for i in range(3):
            secret_payload_arr = convert_from_gray_coding(extract_single_channel_from_single_channel(stego_arr[i], complexities))
            if(np.any(secret_payload_arr)):
                secret_channels.append(secret_payload_arr)
        extracted_array = np.zeros((secret_channels[0].shape[0], secret_channels[0].shape[1], len(secret_channels)))
        for i, channel in enumerate(secret_channels):
            extracted_array[:,:,i] = channel
        if len(secret_channels) == 1:
            create_image(extracted_array[:,:,0].astype(np.uint8), 1)
        else:
            create_image(extracted_array.astype(np.uint8), 3)

if __name__ == "__main__":
    main()