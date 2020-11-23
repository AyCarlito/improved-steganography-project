from PIL import Image
from scipy.fftpack import dct, idct
import numpy as np
import argparse
import zigzag_encoding


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

def clean_values(matrix):
    matrix[matrix>255] = 255
    matrix[matrix<0] = 0
    return matrix

def create_image(matrix):
    compressed_image = Image.fromarray(matrix, mode="L")
    compressed_image.save("compressed.bmp")

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


def dct2(block):
    return dct(dct(block.T, norm='ortho').T, norm='ortho')

def idct2(block):
    return idct(idct(block.T, norm='ortho').T, norm='ortho')

def split_into_blocks(matrix, qtmatrix):
    compressed = np.copy(matrix)
    for i in range(matrix.shape[0]//8):
        for j in range(matrix.shape[1]//8):
            block = matrix[i*8:i*8+8,j*8:j*8+8]
            discrete_cosine_transform = dct2(block)     
            quantised_matrix = np.divide(discrete_cosine_transform, qtmatrix).astype(int)
            normalised = zigzag_encoding.zigzag_single(quantised_matrix)  
            compressed[i*8:i*8+8,j*8:j*8+8] = quantised_matrix.reshape(8,8)
    
    return compressed


def create_run_length_encoding(image):
    i = 0
    skip = 0
    stream = []    
    bitstream = ""
    image = image.astype(int)
    while i < image.shape[0]:
        if image[i] != 0:            
            stream.append((image[i],skip))
            bitstream = bitstream + str(image[i])+ " " +str(skip)+ " "
            skip = 0
        else:
            skip = skip + 1
        i = i + 1

    return bitstream

    
def rle_to_file(matrix):
    flattened = matrix.flatten()
    bitstream = create_run_length_encoding(flattened)
    bitstream = str(matrix.shape[0]) + " " + str(matrix.shape[1]) + " " + bitstream + ";"
    rle_file = open("image.txt","w")
    rle_file.write(bitstream)
    rle_file.close()
    return 


def rle_from_file():
    with open("image.txt", "r") as f:
        rle = f.read()
    return rle

def run_length_to_image2(qtmatrix):
    with open("image.txt", "r") as f:
        rle = f.read()
    details = rle.split()
    h = int(''.join(filter(str.isdigit, details[0])))
    w = int(''.join(filter(str.isdigit, details[1])))

    array = np.zeros(h*w).astype(int)
    k = 0
    i = 2
    x = 0
    j = 0
    while k < array.shape[0]:
        if(details[i] == ';'):
                break
        if "-" not in details[i]:
            array[k] = int(''.join(filter(str.isdigit, details[i])))        
        else:
            array[k] = -1*int(''.join(filter(str.isdigit, details[i])))        
        if(i+3 < len(details)):
            j = int(''.join(filter(str.isdigit, details[i+3])))

        if j == 0:
            k = k + 1
        else:                
            k = k + j + 1        

        i = i + 2
    print(array)
    array = np.reshape(array,(h,w))
    padded_img = np.zeros((h,w))


    while i < h:
        j = 0
        while j < w:        
            temp_stream = array[i:i+8,j:j+8]                
            block = inverse_zigzag(temp_stream.flatten(), int(block_size),int(block_size))            
            de_quantized = np.multiply(block,qtmatrix)                
            padded_img[i:i+8,j:j+8] = idct2(de_quantized)        
            j = j + 8        
        i = i + 8
    padded_img[padded_img > 255] = 255
    padded_img[padded_img < 0] = 0


    create_image(padded_img)

def run_length_to_image(matrix, qtmatrix):
    compressed_image = np.copy(matrix)
    for i in range(matrix.shape[0]//8):
        for j in range(matrix.shape[1]//8):
            block = matrix[i*8:i*8+8,j*8:j*8+8]
            normalised = zigzag_encoding.inverse_zigzag_single(block.flatten())
            de_quantized = np.multiply(normalised, qtmatrix).astype(int)
            compressed_image[i*8:i*8+8,j*8:j*8+8] = idct2(de_quantized)
    return compressed_image

def main():

    args = get_arguments()
    
    vessel_arr = get_file(args.v)
    
    quantization_matrix = create_quantization_matrix()
    compressed_arr = split_into_blocks(vessel_arr, quantization_matrix)

    
    compressed = run_length_to_image(compressed_arr, quantization_matrix)
    create_image(compressed)
    #create_image(run_length_to_image(compressed_arr, quantization_matrix))
    
   
    #rle_to_file(compressed_arr)
    #run_length_to_image(quantization_matrix)
    #create_image(compressed_arr)



    


if __name__ == "__main__":
    main()