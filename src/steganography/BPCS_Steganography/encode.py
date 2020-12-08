import numpy as np
from PIL import Image
import os
import argparse
import random

COMPLEXITIES = {"improved":{0:0.1, 1:0.2, 2:0.25, 3:0.30, 4:0.35, 5:0.40, 6:0.45, 7:0.50}, "standard":{0:0.3, 1:0.3, 2:0.3, 3:0.3, 4:0.3, 5:0.3, 6:0.3, 7:0.3}}

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
        matrix[row,col] = value
    return matrix

def conjugate(matrix):
    checkerboard = np.indices((matrix.shape[0],matrix.shape[1])).sum(axis=0) % 2
    ones = np.ones((matrix.shape[0], matrix.shape[1]))
    conjugated = np.logical_xor(checkerboard, matrix).astype(int)
    conjugated = np.logical_xor(conjugated,ones).astype(int)
    return conjugated

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("v", type=str, help="Vessel Image")
    parser.add_argument("s", type=str, help="Secret Image")
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
    elif temp.mode == "P":
        channels = get_grayscale_channel(temp.convert("L"))
    else:
        channels = get_colour_channels(temp.convert("RGB"))
    return channels

def create_image(array, channel_type):
    stego = Image.fromarray(array, mode=channel_type)
    stego.save("stego.bmp")

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
    
def split_into_blocks(matrix, vessel_height):
    """
    Creates 8x8 blocks of pixels for each bitplane in the secret object
    """
    data = []
    print("Creating 8x8 Blocks for each bitplane")
    bitplanes = [0,1,2,3,4,5,6,7]
    random.Random(vessel_height).shuffle(bitplanes)
    for k in bitplanes:
        for i in range(matrix.shape[0]//8):
            for j in range(matrix.shape[1]//8):
                data.append(matrix[i*8:i*8+8,j*8:j*8+8,k])
    return data

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

def get_metadata(matrix, payload):
    total_blocks = np.reshape(np.array([int(i) for i in (np.binary_repr(len(payload), width=36))]), (4,9))
    height = np.reshape(np.array([int(i) for i in (np.binary_repr(matrix.shape[0], width=18))]), (2,9))
    width = np.reshape(np.array([int(i) for i in (np.binary_repr(matrix.shape[1], width=18))]), (2,9))
    remainder = np.zeros((1,9), dtype=int)

    meta_data = np.concatenate((np.concatenate((total_blocks, height), axis=0), np.concatenate((width, remainder), axis=0)))
    return meta_data


def find_and_replace(vessel, secret, payload, complexity_dictionary):
    got_metadata = False
    bitplanes = [0,1,2,3,4,5,6,7]
    random.Random(vessel.shape[0]).shuffle(bitplanes)
    for k in bitplanes:
        for i in range(vessel.shape[0]//9):
            for j in range(vessel.shape[1]//9):
                if(len(payload)>0):
                    if(get_complexity(vessel[i*9:i*9+8,j*9:j*9+8,k]) > complexity_dictionary[k]):
                        if not got_metadata:
                            meta_data = get_metadata(secret, payload)
                            payload_block = meta_data
                            vessel[i*9:i*9+9,j*9:j*9+9,k] = payload_block
                        else:
                            payload_block = np.copy(payload[0])
                            payload.pop(0)
                            vessel[i*9:i*9+8,j*9:j*9+8,k] = payload_block
                            vessel[i*9+8, j*9+8, k] = 0
                        if (get_complexity(vessel[i*9:i*9+8,j*9:j*9+8,k]) <= complexity_dictionary[k]):
                            if not got_metadata:
                                vessel[i*9:i*9+9,j*9:j*9+9,k] = conjugate(vessel[i*9:i*9+9,j*9:j*9+9,k])
                                vessel[i*9+8, j*9+8, k] = 1
                                got_metadata = True
                            else:
                                vessel[i*9:i*9+8,j*9:j*9+8,k] = conjugate(vessel[i*9:i*9+8,j*9:j*9+8,k])
                                vessel[i*9+8, j*9+8, k] = 1   
                else:
                    return vessel
    if len(payload)>0:
        print("Not enough complex regions")
        quit()

def embed_single_channel_in_single_channel(vessel_arr, secret_arr, complexities):
    vessel_bitplane_arr = get_bitplane_arr(vessel_arr)
    secret_bitplane_arr = get_bitplane_arr(secret_arr)
    data = split_into_blocks(secret_bitplane_arr, vessel_arr.shape[0])
    stego_array = find_and_replace(vessel_bitplane_arr,secret_bitplane_arr,data, complexities)
    stego_array=np.packbits(stego_array[:,:]).reshape((vessel_bitplane_arr.shape[0], vessel_bitplane_arr.shape[1]))
    return stego_array


def main():

    args = get_arguments()
    
    vessel_arr = get_file(args.v)
    secret_arr = get_file(args.s)
 
    
    
    vessel_arr = [convert_to_gray_coding(channel) for channel in vessel_arr]
    secret_arr = [convert_to_gray_coding(channel) for channel in secret_arr]

    complexities = COMPLEXITIES[args.a]
    if len(vessel_arr)==1 and len(secret_arr)==1:
        stego_array = embed_single_channel_in_single_channel(vessel_arr[0], secret_arr[0], complexities)
        stego_array = convert_from_gray_coding(stego_array)
        create_image(stego_array, "L")

    elif len(vessel_arr)>1 and len(secret_arr)==1:
        embedded_channel = embed_single_channel_in_single_channel(vessel_arr[0], secret_arr[0], complexities)
        vessel_arr[0] = embedded_channel
        stego_array = np.zeros((vessel_arr[0].shape[0], vessel_arr[0].shape[1], 3))
        for i in range(3):
            stego_array[:,:,i] = convert_from_gray_coding(vessel_arr[i])
        create_image(stego_array.astype(np.uint8), "RGB")
        
    else:
        stego_array = np.zeros((vessel_arr[0].shape[0], vessel_arr[0].shape[1], 3))
        for i in range(3):
            embedded_channel = embed_single_channel_in_single_channel(vessel_arr[i], secret_arr[i], complexities)
            vessel_arr[i] = embedded_channel
            stego_array[:,:,i] = convert_from_gray_coding(vessel_arr[i])
        create_image(stego_array.astype(np.uint8), "RGB")
    

if __name__ == "__main__":
    main()


