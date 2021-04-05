"""
.. module:: encode
   :synopsis: Functionality of BPCS Embedding is defined here
.. moduleauthor::  Daniel Hislop
"""

import numpy as np
from PIL import Image
import os
import argparse
import random

COMPLEXITIES = {"standard":{0:0.3, 1:0.3, 2:0.3, 3:0.3, 4:0.3, 5:0.3, 6:0.3, 7:0.3}, "improved":{0:0.1, 1:0.2, 2:0.25, 3:0.30, 4:0.35, 5:0.40, 6:0.45, 7:0.45}}

bitplanes = [7,6,5,4,3,2,1,0]
#Gray Coding Functions Sourced from https://www.geeksforgeeks.org/decimal-equivalent-gray-code-inverse/# 

def convert_to_gray_coding(matrix):
    """**Convert binary code to gray coding**

        This function takes a channel in an image and converts its binary representation 
        decimal value to gray coding decimal value. Conversion of each pixel achieved 
        through logical XOR of pixel and pixel rightshifted by 1.

    Args:
        matrix (ndarray): 2-Dimensional numpy array representing an image channel. 
        8-bit colour images will have a single channel. 
        24-bit colour images will have 3 channels (RGB).

    Returns:
        ndarray: 2-Dimensional numpy array of channel converted to gray coding.
    """
    return matrix[:,:]^(matrix[:,:] >> 1)

def convert_from_gray_coding(matrix):
    """**Convert gray coding to binary code**

        This function takes a channel in an image and converts its gray coding representation 
        decimal value to binary represntation decimal value.Conversion of a pixel - 
        Logical XOR of inverse and pixel to give new inverse value. Rightshit pixel by 1. 
        Loop until pixel cannot be rightshifted, converted pixel value is the final inverse.

    Args:
        matrix (ndarray): 2-Dimensional numpy array representing an image channel. 
        8-bit colour images will have a single channel. 
        24-bit colour images will have 3 channels (RGB)

    Returns:
        ndarray: 2-Dimensional numpy array of channel converted to binary code.
    """
    for (row, col), value in np.ndenumerate(matrix):
        inv = 0
        while(value):
            inv = inv ^ value
            value = value >> 1
        value = inv
        matrix[row,col] = value
    return matrix

def conjugate(matrix):
    """**Conjugation of an image block**

        Conjugation is the process of transforming a non-complex block to a complex one. 
        New complexity measure will be 1-x, where x is the original complexity measure.
        Conjugation achieved by the logical XOR of image block and checkerboard pattern.

    Args:
        matrix (ndarray): 8x8 numpy array of an image block. 

    Returns:
        ndarray: 8x8 numpy array of conjugated block. 
    """
    checkerboard = np.indices((matrix.shape[0],matrix.shape[1])).sum(axis=0) % 2
    ones = np.ones((matrix.shape[0], matrix.shape[1]))
    conjugated = np.logical_xor(checkerboard, matrix).astype(int)
    conjugated = np.logical_xor(conjugated,ones).astype(int)
    return conjugated

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Arguments are specified as positional arguments meaning something must be provied. 
        Additionally, choice of algorithm is restricted to predefined selection.
    
    Returns:
        Namespace: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("v", type=str, help="Cover Image")
    parser.add_argument("s", type=str, help="Payload Image")
    parser.add_argument("a", choices=["standard", "improved"], type=str, help="Algorithm. Standard or Improved")

    args = parser.parse_args()
    return args

def get_grayscale_channel(image):
    """**Helper Function**

    Args:
        image (PIL Image Object): 8-bit colour image read in from file by Pillow.
    Returns:
        List: Returns a single element list containing numpy array of single channel in image.
    """
    img_arr = np.array(image)
    image.close()
    return [img_arr]

def get_colour_channels(image):
    """**Helper Function**

    Args:
        image (PIL Image Object): 24-bit colour image read in from file by Pillow

    Returns:
        List: Three element list containing a numpy array for each channel in an RGB image.
    """
    img_arr = np.array(image)
    r = img_arr[:,:,0]
    g = img_arr[:,:,1]
    b = img_arr[:,:,2]
    image.close()
    return [r,g,b]
   

def get_file(name):
    """**Read in image from file**

        Reads in the specified image using Pillow and returns a list of numpy arrays 
        representing each channel in the image. Makes use of two helper functions. 
        Image.mode is used to check the colour depth of an image. "L" and "P" are 8-bit 
        grayscale images. Anything else will be RGB. 
        Helper functions called based on result of Image.mode

    Args:
        name (String): Name of image to be read.

    Returns:
        List: Variable length list contaning either one or three elements where each element 
        is a numpy array representing the respective channel in an image.
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
    """**Creates an image from the stego array**

    Args:
        array (ndarray): Numpy array of cover image containing an embedded payload.

        channel_type (String): Akin to Pillow Image.mode. This specifies channels in the image. 
        Either "L" or "RGB".
    """
    stego = Image.fromarray(array, mode=channel_type)
    stego.save("stego.bmp")

def get_bitplane_arr(matrix):
    """**Create bitplane array**


        Create array of zeros using np.zeros in shape (N,M,8) where N and M are dimensions of
        matrix argument respectively. Use np.unpackbits to create binary represenation. We 
        first convert to uint8 as unpackbits requires it. Reshape bitplane array. 

    Args:
        matrix ([ndarray]): 2-Dimensional numpy array of channel in an image.

    Returns:
        ndarray: 3-Dimensional numpy array of shape (NxMx8) where N and M are width and height 
        of image respectively. Binary representation of every pixel.
    """

    temp_bitplane_arr = np.zeros((matrix.shape[0], matrix.shape[1], 8))
    temp_bitplane_arr[:,:,0] = np.copy(matrix)

    binary_encoding = np.unpackbits(np.uint8(temp_bitplane_arr[:,:,0]))
    binary_encoding = np.reshape(binary_encoding,(temp_bitplane_arr.shape[0], temp_bitplane_arr.shape[1],8))
    return binary_encoding

    
def split_into_blocks(matrix, vessel_height):
    """**Split image into 8x8 blocks**

        Loop through each bitplane in the bitplane array. For each 8 element slice in rows
        we loop through every 8 element slice of columns. Append this 8x8 block to list.

    Args:
        matrix (ndarray): Bitplane array.
        vessel_height (Int): Height of vessel object.

    Returns:
        List: Variable length list where each element is an 8x8 block. 
    """

    data = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in bitplanes:
        for i in range(matrix.shape[0]//8):
            for j in range(matrix.shape[1]//8):
                data.append(matrix[i*8:i*8+8,j*8:j*8+8,k])
    return data

def get_complexity(matrix):
    """Calculate complexity of an image block**
    
        First calculate maximum complexity of block with given dimenssions. This is a
        checkerboard pattern. To caculate complexity of argument block, we take the summation
        of colour changes row wise, and the number of colour changes column wise. We can loop
        through columns by taking the transpose of the matrix. Complexity measure is the
        summation of changes divided by maximum complexity.
        
    Args:
        matrix (ndarray): Image block.

    Returns:
        int: Complexity measure of an image block
    """     

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
    """Create metadata of payload to be hidden**

        Metadata is a 9x9 block. 
        np.binary_repr creates binary representation of number as string.
        Loop through this string and convert each element to integer. Reshape this int array
        to desired dimensions. The total blocks are the first four rows in 9x9.
        height is next 2 rows, and width next 2 rows after that. Set reamining row to zeros.

    Args:
        matrix (ndarray): Bitplane array of payload.
        payload (list): List containing 8x8 payload blocks.

    Returns:
        ndarray: 9x9 block of metadata.
    """
    total_blocks = np.reshape(np.array([int(i) for i in (np.binary_repr(len(payload), width=36))]), (4,9))
    height = np.reshape(np.array([int(i) for i in (np.binary_repr(matrix.shape[0], width=18))]), (2,9))
    width = np.reshape(np.array([int(i) for i in (np.binary_repr(matrix.shape[1], width=18))]), (2,9))
    remainder = np.zeros((1,9), dtype=int)

    meta_data = np.concatenate((np.concatenate((total_blocks, height), axis=0), np.concatenate((width, remainder), axis=0)))
    return meta_data


def find_and_replace(vessel, secret, payload, complexity_dictionary):
    """**Embedding of payload blocks in complex cover blocks**

        For eeach bitplane, loop through every 9x9 block. If payload blocks still to embed.
        If block in cover is complex. get metadata and embed in first complex 9x9. 
        Embed 8x8 block of payload in the 8x8 region of the 9x9block in cover. 
        Conjugate if embedded block is not complex. Set 9th row, 9th column bit to 1 if block 
        has been conjugated otherwise set to 0. If blocks are still left after this process
        then there are not enough complex regions and embedding can't take place so program 
        exits. Otherwise we return the newly created stego array.

    Args:
        vessel (ndarray): Bitplane array of cover.
        secret (ndarray): Bitplane array of payload.
        payload (list): List containing 8x8 payload blocks.
        complexity_dictionary (dict): Dictionary with bitplanes as keys, and complexity
        thresholds as values. 

    Returns:
        ndarray: Stego array
    """
    got_metadata = False
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
    """**Driver Code for embedding single channel in another**

        Get cover and payload bitplane arrays. Split payload into 8x8 blocks.
        Embed payload within cover to create stego array.

    Args:
        vessel_arr (ndarray): Single channel of cover image
        secret_arr (ndarray): Single channel of payload image
        complexities (dict): Dictionary mapping bitplanes to complexity thresholds.

    Returns:
        [ndarray]: Stego array for single channel
    """
    vessel_bitplane_arr = get_bitplane_arr(vessel_arr)
    secret_bitplane_arr = get_bitplane_arr(secret_arr)
    data = split_into_blocks(secret_bitplane_arr, vessel_arr.shape[0])
    stego_array = find_and_replace(vessel_bitplane_arr,secret_bitplane_arr,data, complexities)
    stego_array=np.packbits(stego_array[:,:]).reshape((vessel_bitplane_arr.shape[0], vessel_bitplane_arr.shape[1]))
    return stego_array


def main():
    """**Driver Code for BPCS tool**

        Parse user arguments. Get numpy arrays of cover and payload. Convet each channel to
        gray coding. Index complexity dictionary. If 2 grayscales, call embed single channel
        once and convert from gray coding and create stego image with "L" (grayscale) flag.
        If 24-bit cover and 8-bit cover payload then embed payload in red channel of cover. 
        Convert back from gray coding and create stego image "RGB" flag. Otherwise, embed 
        each channel of payload in each channel of cover, convert back from gray coding and
        create image with "RGB" flag.

    """

    args = get_arguments()
    
    vessel_arr = get_file(args.v)
    secret_arr = get_file(args.s)
 
    
    
    vessel_arr = [convert_to_gray_coding(channel) for channel in vessel_arr]
    secret_arr = [convert_to_gray_coding(channel) for channel in secret_arr]

    complexities = COMPLEXITIES["standard"]
    if args.a == "improved":
        random.Random(vessel_arr[0].shape[0]).shuffle(bitplanes)

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


