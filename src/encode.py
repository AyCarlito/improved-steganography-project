import numpy as np
from PIL import Image

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
    
    # for i in range(matrix.shape[0]):
    #     for j in range(matrix.shape[1]):
    #         bit_array = np.unpackbits(np.uint8(matrix[i,j,0]))
    #         for k in range(8):
    #             matrix[i,j,k] = bit_array[k]
    # return matrix


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
    top_left = matrix[0,0]
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            if top_left!=matrix[i,j]:
                current_complexity+=1
                top_left=matrix[i,j]
    top_left = matrix[0,0]
    for i in range(matrix.shape[1]):
        for j in range(matrix.shape[0]):
            if top_left!=matrix[j,i]:
                current_complexity+=1
                top_left=matrix[j,i]
    return current_complexity/maximum_complexity

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
    print(complexity)


main()
#find complex segements and replace

#Confirm all of secret was placed

#Create new image with embedded secret

