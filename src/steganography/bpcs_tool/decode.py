"""
.. module:: decode
   :synopsis: Functionality of BPCS Extraction is defined here
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
        matrix[row, col] = value
    return matrix

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Arguments are specified as positional arguments meaning something must be provied. 
        Additionally, choice of algorithm is restricted to predefined selection.
    
    Returns:
        Namespcae: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="BPCS Decoding tool")
    parser.add_argument("s", type=str, help="Stego Image")
    parser.add_argument("a", choices=["standard", "improved"], type=str, help="Algorithm. Standard or Improved")
    parser.add_argument("-m1", "--variable_complexity", choices=["yes", "no"], nargs="?", type=str, help="Option to use variable complexity modification on its own")
    parser.add_argument("-m2", "--rbeo", choices=["yes", "no"], nargs="?", type=str, help="Option to use random bitplane embedding order modification on its own")
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

def create_image(array, no_channels):
    """**Creates an image from the recovered array**

    Args:
        array (ndarray): Numpy array of recovered payload.
        no_channels (int): Number of channels in image. 1 is 8-bit colour, 3 is 24-bit colour.
        Use this to index dictionary provide mode to Pillow Image.fromarray function. 
    """
    modes = {1: "L", 3: "RGB"}
    extracted = Image.fromarray(array, mode=modes[no_channels])
    extracted.save("extracted.bmp")


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

def split_into_blocks(matrix, complexity_dictionary):
    """**Split Stego image into 9x9 complex blocks**

    Args:
        matrix (ndarray): numpy array of stego image
        complexity_dictionary (dict): Dictionary mapping bitplanes to complexity thresholds

    Returns:
        list: Each element in list is 9x9 complex block of stego image 
    """
    data = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in bitplanes:
        for i in range(matrix.shape[0]//9):
            for j in range(matrix.shape[1]//9):
                if(get_complexity(matrix[i*9:i*9+8,j*9:j*9+8,k]) > complexity_dictionary[k]):
                    data.append(matrix[i*9:i*9+9,j*9:j*9+9,k])              
    return data

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

def extract_meta_data(payload, stego_arr):
    """**Extract Meta Data from stego image**

        Meta data will be in first complex 9x9 block. Check 9th row 9th column bit. If 1 then
        conjugate. np.ravel returns a flattened array. For total blocks, flatten first 4 rows 
        of 9x9, and so on. Convert flattened arrays to integers and return as 3-tuple.
        
    Args:
        payload (list): list of complex 9x9 blocks in payload
        stego_arr (ndarry): numpy array of stego image

    Raises:
        MemoryError: This is raised if the meta data height is larger than stego height. Since
        we cannot embed a payload of diensions greater than the stego, this would indicate the
        wrong algorithm has been selected for extraction. Memory error would occur when 
        trying to allocate space for height as we have a 36bit binary number of maximum value 
        2^36.

    Returns:
        [3-tuple int]: 3 element tuple containing the number of total embedded blocks, height 
        of embedded payload, width of embedded payload.
    """
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
    """**Extraction of Payload from stego**

        Extract meta data. Loop through each bitplane. Loop through each 8x8 block.
        Check if extracted blocks less than total blocks from meta data. Take block
        and check 9th row 9th column bit. if 1 then conjugate. Extract 8x8 region from the 9x9.
        Incrmement blocks_retrieved counter. 

    Args:
        meta_data (3-tuple): Meta data extracted from first complex 9x9 block.
        payload (List): Elements in lust are 9x9 complex blocks contanining payload.

    Returns:
        ndarray: Bitplane array of extracted payload
    """
    secret_payload_arr = np.zeros(( meta_data[1], meta_data[2], 8), dtype="uint8")
    blocks_retrieved = 0
    for k in bitplanes:
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
    """**Driver code for extracting single channel from single channel**

        Create bitplane array from stego image. Split into complex 9x9 blocks. Extract metadata.
        Extract payload. Reshape extracted payload into payload dimensions from metadata.

        Catch Memory Error exception. Can use this to check if we have an 8-bit grayscale
        embedded in 24-bit colour cover -> will be fine for red channel but give two memoery
        errors in blue and green channels.

    Args:
        channel (ndarray): Numpy array of single channel in image
        complexities (dict): Dictionary mapping bitplanes to complexity thresholds.

    Returns:
        [ndarray]: Extracted payload
    """
    stego_bitplane_arr = get_bitplane_arr(channel)
    data = split_into_blocks(stego_bitplane_arr, complexities)
    try:
        meta_data = extract_meta_data(data, channel)
    except MemoryError as e:
        return (np.zeros((channel.shape[0], channel.shape[1])))
    stego_height = channel.shape[0]
    payload_arr = extract_payload(meta_data, data)
    secret_payload_arr = np.packbits(payload_arr[:,:]).reshape((meta_data[1], meta_data[2]))
    return secret_payload_arr

def main():
    """**Driver code for BPCS tool**

        Parse user arguments. Read in stego image and convert each channel to gray coding. 
        Get complexities. If single channel image then extract single channel and create image.
        Otherwise, attempt extraction, if anything comes back ie. no memory error, then add to 
        secret channels list. If only one secret channel then we have an 8-bit grayscale
        payload. If 3 secret channels then we have 24-bit colour cover. Create image.
    """

    args = get_arguments()
    
    stego_arr = get_file(args.s)
    stego_arr = [convert_to_gray_coding(channel) for channel in stego_arr]
    
    complexities = COMPLEXITIES["standard"]

    if (args.a == "improved" and args.variable_complexity and not args.rbeo):
        complexities = COMPLEXITIES["improved"]
    elif (args.a == "improved" and not args.variable_complexity and args.rbeo):
        random.Random(stego_arr[0].shape[0]).shuffle(bitplanes)
    elif (args.a == "improved" and args.variable_complexity and args.rbeo):
        complexities = COMPLEXITIES["improved"]
        random.Random(stego_arr[0].shape[0]).shuffle(bitplanes)

    if len(stego_arr)==1:
        secret_payload_arr = convert_from_gray_coding(extract_single_channel_from_single_channel(stego_arr[0], complexities))
        create_image(secret_payload_arr.astype(np.uint8), 1)

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