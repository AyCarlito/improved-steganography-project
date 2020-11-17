from PIL import Image
from scipy.fftpack import dct, idct
import numpy as np
import os
import argparse



def create_quantization_matrix():
    return(np.array([
        16,11,10,16,24,40,51,61,
        12,12,14,19,26,58,60,55,
        14,13,16,24,40,57,69,56,
        14,17,22,29,51,87,80,62,
        18,22,37,56,68,109,103,77,
        24,35,55,64,81,104,113,92,
        49,64,78,87,103,121,120,101,
        72,92,95,98,112,100,103,99
    ]).reshape(8,8))

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("v", type=str, help="Vessel Image")
    parser.add_argument("s", type=str, help="Secret Image")
    args = parser.parse_args()
    return args

def get_file(name):
    """
    Takes a string parameter indicating file name.
    Reads in file and converts to np array, closes image. Returns np array.
    This function gets the vessel and secret object arrays. 
    """
    print("Opening %s" % name)
    temp = Image.open("%s" % name).convert("L")
    temp_arr = np.array(temp)
    temp.close()
    return temp_arr

def create_zigzag_pattern():
    zigzag_indices = [
        (0,0), (0,1), (1,0), (2,0), (1,1), (0,2), (0,3), (1,2), 
        (2,1), (3,0), (4,0), (3,1), (2,2), (1,3), (0,4), (0,5), 
        (1,4), (2,3), (3,2), (4,1), (5,0), (6,0), (5,1), (4,2),
        (3,3), (2,4), (1,5), (0,6), (0,7), (1,6), (2,5), (3,4),
        (4,3), (5,2), (6,1), (7,0), (7,1), (6,2), (5,3), (4,4),
        (3,5), (2,6), (1,7), (2,7), (3,6), (4,5), (5,4), (6,3),
        (7,2), (7,3), (6,4), (5,5), (4,6), (3,7), (4,7), (5,6),
        (6,5), (7,4), (7,5), (6,6), (5,7), (6,7), (7,6), (7,7)
    ]
    return zigzag_indices

def zigzag(matrix, zigzag_indices):
    return(np.array([matrix[i] for i  in zigzag_indices]).reshape(8,8))


def split_into_blocks(matrix, qtmatrix):
    compressed = np.copy(matrix)
    zigzag_indices = create_zigzag_pattern()
    for i in range(matrix.shape[0]//8):
        for j in range(matrix.shape[1]//8):
            block = matrix[i*8:i*8+8,j*8:j*8+8]
            discrete_cosine_transform = dct(dct(block).T).T
            quantised_matrix = np.divide(discrete_cosine_transform, qtmatrix).astype(int)
            normalised = zigzag(quantised_matrix, zigzag_indices)
            compressed[i*8:i*8+8,j*8:j*8+8] = normalised
    return compressed

def run_length_to_image(matrix, qtmatrix):
    zigzag_indices = create_zigzag_pattern()
    zigzag_indices.reverse()
    compressed_image = np.zeros((matrix.shape[0], matrix.shape[1]))
    for i in range(matrix.shape[0]//8):
        for j in range(matrix.shape[1]//8):
            block = matrix[i*8:i*8+8,j*8:j*8+8]
            block = zigzag(block, zigzag_indices)
            de_quantized = np.multiply(block, qtmatrix)
            compressed_image[i*8:i*8+8,j*8:j*8+8] = idct(idct(de_quantized).T).T
    return compressed_image

def clean_values(matrix):
    matrix[matrix>255] = 255
    matrix[matrix<0] = 0
    matrix = np.positive(matrix)
    return matrix
def create_image(matrix):
    compressed_image = Image.fromarray(matrix, mode="L")
    compressed_image.save("compressed.jpeg")

def main():

    args = get_arguments()
    
    vessel_arr = get_file(args.v)
   # secret_arr = get_file(args.s)

    quantization_matrix = create_quantization_matrix()
    compressed_arr = split_into_blocks(vessel_arr, quantization_matrix)

   # compressed_arr = clean_values(run_length_to_image(compressed_arr, quantization_matrix))
    create_image(compressed_arr)

    


if __name__ == "__main__":
    main()