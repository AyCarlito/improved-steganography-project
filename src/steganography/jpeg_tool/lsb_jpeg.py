"""
.. module:: lsb_jpeg
   :synopsis: Functionality of LSB Embedding and Extraction is defined here
.. moduleauthor::  Daniel Hislop
"""

from jpeg_tool import jpeg_encode
import numpy as np
import random


def lsb_embed_secret(secret, vessel, alg):
    """**Embed payload using LSB or TLSB**

    Payload height and payload width are the first things embedded.

    Flatten cover and payload arrays to 1D. For every pixel in payload use np.unpackbits
    to create binary representation. Select 8 pixel slice from cover. For each pixel in cover
    slice, convert to binary using np.unpackbits. Set LSB to 1, set second LSB to 0, and embed
    the payload bit in the third LSB of cover. Use np.packbits to create number from binary
    representation. Reshape flattened cover array (which has payload in it) to original 2D 
    shape.

    Args:
        secret (ndarray): Numpy array of payload
        vessel (ndarray): Numpy array of cover

    Returns:
        ndarray: Numpy array of stego
    """
    index = 0

    height = vessel.shape[0]
    width = vessel.shape[1]
    secret_height = secret.shape[0]
    secret_width = secret.shape[1]
   
    secret = secret.flatten()
    vessel = vessel.flatten()
    secret[0] = secret_height/8
    secret[1] = secret_width/8
    for secret_pixel in secret:
        secret_bin_repr = np.unpackbits(secret_pixel)
        vessel_selection = vessel[index*8:index*8+8]
        for i, vessel_pixel in enumerate(vessel_selection):
            vessel_pixel_bin_repr = np.unpackbits(vessel_pixel)
            if alg=="LSB":
                vessel_pixel_bin_repr[-1] = secret_bin_repr[i]
            elif alg=="TLSB":
                vessel_pixel_bin_repr[-1] = 1
                vessel_pixel_bin_repr[-2] = 0
                vessel_pixel_bin_repr[-3] = secret_bin_repr[i]
            vessel_pixel = np.packbits(vessel_pixel_bin_repr)
            vessel_selection[i] = vessel_pixel
        vessel[index*8:index*8+8] = vessel_selection
        index+=1
    return vessel.reshape((height,width))

def lsb_decode_secret(stego_name, algorithm):
    """**Extract payload using LSB or TLSB**
    
        Call decoder helper for each channel in stego. single channel will mean single call.
        Three channels -> loop through with try and except. We use try and except as there
        might not be a payload in each of the channels; a single channel payload can be
        embedded in the red channel of cover. 

    Args:
        stego_name (String): File Name of stego

    Returns:
        ndarray: Extracted payload
    """
    stego = jpeg_encode.get_file("%s" % stego_name)
    if len(stego.shape)==2:
        stego = stego.flatten()
        decoded = lsb_decode_helper(stego, algorithm)
    else:
        for i in range(3):
            stego_channel = stego[:,:,i].flatten()
            try:
                decoded = lsb_decode_helper(stego_channel, algorithm)
            except ValueError as e:
                pass
    return decoded
    

def lsb_decode_helper(stego, algorithm):
    """**Helper function for LSB extraction**

        For every 8 pixel selection in stego. Loop through each pixel, convert to binary and 
        append TLSB to list. First two recovered will be height and width of payload. Convert
        list to numpy array and reshapre using height and width.
            
    Args:
        stego (ndarray): Flattened stego array

    Returns:
        ndarray: Extracted payload.
    """
    secret = []
    index = 0
    for index in range(len(stego)//8):
        stego_selection = stego[index*8:index*8+8]
        secret_pixel = []
        for i, stego_pixel in enumerate(stego_selection):
            stego_pixel_bin_repr = np.unpackbits(stego_pixel)
            if algorithm=="LSB":
                secret_pixel.append(stego_pixel_bin_repr[-1]) 
            elif algorithm=="TLSB":
                secret_pixel.append(stego_pixel_bin_repr[-3]) 
        secret.append(np.packbits(secret_pixel)[0])
        index+=1
    height = secret[0]*8
    width = secret[1]*8
    return np.asarray(secret)[0:(height*width)].reshape((height, width))

def random_lsb_embed_secret(secret, vessel):
    """**Embed payload using TLSBRandom**

        Payload height and payload width are the first things embedded. Cover height used
        as seed for random function. Divide length of cover by 8 and use random sample to give
        random embedding order. Loop through each number in embedding order and use to create an 
        8x pixel slice. eg element in embedding order is "1" can use this as slice [1:9].
        Now that we have 8 pixel slice, the process is now the same as TLSB.

    Args:
        secret (ndarray): Numpy array of payload
        vessel (ndarray): Numpy array of cover

    Returns:
        ndarray: Numpy array of stego
    """
    index = 0

    height = vessel.shape[0]
    width = vessel.shape[1]
    secret_height = secret.shape[0]
    secret_width = secret.shape[1]

    secret = secret.flatten()
    vessel = vessel.flatten()

    random.seed(height)
    embedding_order = random.sample(range(len(vessel)//8), len(vessel)//8)
    embedded = 0
    for i, embedding_location in enumerate(embedding_order):
        if embedded < len(secret):
            secret_bin_repr = np.unpackbits(secret[i])
            vessel_selection = vessel[embedding_location*8:embedding_location*8+8]
            for j, vessel_pixel in enumerate(vessel_selection):
                vessel_pixel_bin_repr = np.unpackbits(vessel_pixel)
                vessel_pixel_bin_repr[-1] = 1
                vessel_pixel_bin_repr[-2] = 0
                vessel_pixel_bin_repr[-3] = secret_bin_repr[j]
                vessel_pixel = np.packbits(vessel_pixel_bin_repr)
                vessel_selection[j] = vessel_pixel
            vessel[embedding_location*8:embedding_location*8+8] = vessel_selection
           
            embedded+=1
    
    vessel[0] = (secret_height/8)
    vessel[8] = (secret_width/8)
    return vessel.reshape((height,width))

def random_lsb_decode_secret(stego_name, algorithm):
    """**Extract payload using TLSBRandom**

        Read in stego. Use height as seed. Flatten array. Recretae the embedding order.
        Use embedding order to make 8 pixel slices, for each pixel in slice, use np unpackbits
        to create binary representation. Extract TLSB from this and add to list. Reshape 
        list into dimensions of payload. (height and width of payload are first two numbers
        extracted)

    Args:
        stego_name (String): File name of stego

    Returns:
        ndarray: Extracted payload
    """
    stego = jpeg_encode.get_file("%s" % stego_name)
    random.seed(stego.shape[0])
    stego = stego.flatten()
    secret = []
    height = stego[0]*8
    width = stego[8]*8

    embedding_order = random.sample(range(len(stego)//8), len(stego)//8)
    for i, embedding_location in enumerate(embedding_order):
        secret_pixel = []
        stego_selection = stego[embedding_location*8:embedding_location*8+8]
        for j, stego_pixel in enumerate(stego_selection):
            stego_pixel_bin_repr = np.unpackbits(stego_pixel)
            secret_pixel.append(stego_pixel_bin_repr[-3])
        secret.append(np.packbits(secret_pixel)[0])

    return np.asarray(secret)[0:(height*width)].reshape((height, width))

    