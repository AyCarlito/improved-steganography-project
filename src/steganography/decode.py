import numpy as np
from PIL import Image
import os

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    print("Opening %s" % name)
    temp = Image.open("%s.bmp" % name)
    temp_arr = np.array(temp)
    temp.close()
    return temp_arr

def get_bitplane_arr(matrix):
    """
    Gets binary encoding of each pixel.
    512x512x8 matrix. -> 512x512 pixels. 8 -> binary value of pixel.
    """
    binary_encoding = np.unpackbits(np.uint8(matrix[:,:,0]))
    binary_encoding = np.reshape(binary_encoding,(matrix.shape[0],matrix.shape[1],8))
    return binary_encoding

def get_complexity(matrix):
    current_complexity = 0
    maximum_complexity = ((matrix.shape[0]-1) * matrix.shape[1]) + ((matrix.shape[1]-1) * matrix.shape[0])

    current_pixel = matrix[0,0]
    for index, value in np.ndenumerate(matrix):
        if current_pixel!=matrix[index]:
            current_complexity+=1
            current_pixel=matrix[index]

    current_pixel = matrix[0,0]
    for index, value in np.ndenumerate(matrix.transpose()):
        if current_pixel!=matrix[index]:
            current_complexity+=1
            current_pixel=matrix[index]
    return current_complexity/maximum_complexity

def split_into_blocks(matrix):
    data = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in range(7, -1, -1):
        for i in range(matrix.shape[0]//9):
            for j in range(matrix.shape[1]//9):
                if(get_complexity(matrix[i*9:i*9+8,j*9:j*9+8,k]) > 0.45):
                    data.append(matrix[i*9:i*9+9,j*9:j*9+9,k])
    return data

def conjugate(matrix):
    checkerboard = np.fliplr(np.indices((matrix.shape[0],matrix.shape[1])).sum(axis=0) % 2)
    for index, value in np.ndenumerate(checkerboard):
        matrix[index] = checkerboard[index]^matrix[index]
    return matrix

def extract_meta_data(payload):
    meta_data = payload[0]  
    if meta_data[8,8] == 1:
        meta_data = conjugate(meta_data)
        meta_data[8,8]=0
    
    payload.pop(0)
    total_blocks = np.ravel(meta_data[:4,:])
    height = np.ravel(meta_data[4:6,:])
    width = np.ravel(meta_data[6:8,:])

    total_blocks = int("".join(str(elem) for elem in total_blocks), 2)
    height = int("".join(str(elem) for elem in height), 2)
    width = int("".join(str(elem) for elem in width), 2)


    return (total_blocks, height, width)

def extract_payload(meta_data, payload):
    secret_payload_arr = np.zeros((meta_data[1], meta_data[2], 8), dtype="uint8")
    blocks_retrieved = 0

    for k in range(7, -1, -1):
        for i in range(meta_data[1]//8):
            for j in range(meta_data[2]//8):
                if (blocks_retrieved < meta_data[0]):
                    block = payload[0]
                    if block[8,8] == 1:
                        block = conjugate(block)
                        block[8,8] = 0
                    secret_payload_arr[i*8:i*8+8, j*8:j*8+8, k] = block[:8,:8]
                    blocks_retrieved+=1
                    payload.pop(0)
    return secret_payload_arr           

def main():
    stego_arr = get_file("stego")

    stego_bitplane_arr = np.zeros((stego_arr.shape[0], stego_arr.shape[1], 8))
    stego_bitplane_arr[:,:,0] = np.copy(stego_arr)
    stego_bitplane_arr = get_bitplane_arr(stego_bitplane_arr)

    data = split_into_blocks(stego_bitplane_arr)
    meta_data = extract_meta_data(data)


    secret_payload_arr = extract_payload(meta_data, data)
    secret_payload_arr = np.packbits(secret_payload_arr[:,:]).reshape((meta_data[1], meta_data[2]))

    extracted = Image.fromarray(secret_payload_arr)
    extracted.save("extracted.bmp")

main()