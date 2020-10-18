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
    
def split_into_blocks(matrix):
    """
    Creates 8x8 blocks of pixels for each bitplane in the secret object
    """
    data = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in range(7, -1, -1):
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

def conjugate(matrix):
    checkerboard = np.fliplr(np.indices((matrix.shape[0],matrix.shape[1])).sum(axis=0) % 2)
    for index, value in np.ndenumerate(checkerboard):
        matrix[index] = checkerboard[index]^matrix[index]
    return matrix


def find_and_replace(vessel, secret, payload):
    got_metadata = False
    for k in range(7, -1, -1):
        for i in range(vessel.shape[0]//9):
            for j in range(vessel.shape[1]//9):
                if(len(payload)>0):
                    is_conjugated = 0
                    if(get_complexity(vessel[i*9:i*9+8,j*9:j*9+8,k]) > 0.45):
                        payload_block = np.copy(payload[0])
                        if not got_metadata:
                            meta_data = get_metadata(secret, payload)
                            payload_block = meta_data
                        if (get_complexity(payload_block) < 0.45):
                            payload_block = conjugate(payload_block)
                            is_conjugated = 1
    
                        if not got_metadata:
                            vessel[i*9:i*9+9,j*9:j*9+9,k] = payload_block
                            vessel[i*9+8, j*9+8, k] = is_conjugated
                            got_metadata = True
                            payload.pop(0)
                        else:
                            vessel[i*9:i*9+8,j*9:j*9+8,k] = payload_block
                            vessel[i*9+8, j*9+8, k] = is_conjugated
                            payload.pop(0)
                        # if not got_metadata:
                        #     meta_data = get_metadata(secret, payload)
                        #     vessel[i*9:i*9+9,j*9:j*9+9,k] = meta_data
                        #     got_metadata = True
                        # else:
                        #     payload_block = np.copy(payload[0])
                        #     vessel[i*9:i*9+8,j*9:j*9+8,k] = payload_block
                        #     vessel[i*9+8,j*9+8,k] = 0
                        #     payload.pop(0)
                        # if(get_complexity(vessel[i*9:i*9+8,j*9:j*9+8,k]) <= 0.45):
                        #     vessel[i*9:i*9+8,j*9:j*9+8,k] = conjugate(vessel[i*9:i*9+8,j*9:j*9+8,k])
                        #     vessel[i*9+8,j*9+8,k] = 1  
    if len(payload)>0:
        print("Not enough complex regions")
        return vessel
    else:
        return vessel

                    
def main():
    vessel_arr = get_file("vessel")
    secret_arr = get_file("secret")

    print("Getting binary encoding of vessel")
    vessel_bitplane_arr = np.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
    vessel_bitplane_arr[:,:,0] = np.copy(vessel_arr)
    vessel_bitplane_arr = get_bitplane_arr(vessel_bitplane_arr)

    print("Getting binary encoding of secret")
    secret_bitplane_arr = np.zeros((secret_arr.shape[0], secret_arr.shape[1], 8))
    secret_bitplane_arr[:,:,0] = np.copy(secret_arr)
    secret_bitplane_arr = get_bitplane_arr(secret_bitplane_arr)


    data = split_into_blocks(secret_bitplane_arr)
    complexity = get_complexity(vessel_arr)
    print("Complexity of vessel image: %f" % complexity)

    stego_array = find_and_replace(vessel_bitplane_arr,secret_bitplane_arr,data)
    stego_array=np.packbits(stego_array[:,:]).reshape((vessel_bitplane_arr.shape[0], vessel_bitplane_arr.shape[1]))
    
    stego = Image.fromarray(stego_array, mode="L")
    stego.save("stego.bmp")

main()

#find complex segements and replace

#Confirm all of secret was placed

#Create new image with embedded secret

