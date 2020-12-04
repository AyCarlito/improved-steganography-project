import argparse
import encode
import numpy as np

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS Encoding tool")
    parser.add_argument("i", type=str, help="Image to be analysed")
    parser.add_argument("m", type=str, help="Algorithm to be used")

    args = parser.parse_args()
    return args.i, args.m

def split_into_blocks(matrix, complexity_dictionary):
    total = []
    embeddable = []
    print("Creating 8x8 Blocks for each bitplane")
    for k in range(7, -1, -1):
        for i in range(matrix.shape[0]//9):
            for j in range(matrix.shape[1]//9):
                total.append(matrix[i*8:i*8+8,j*8:j*8+8,k])
                if(encode.get_complexity(matrix[i*9:i*9+8,j*9:j*9+8,k]) > complexity_dictionary[k]):
                    embeddable.append(matrix[i*8:i*8+8,j*8:j*8+8,k])              
    return (total, embeddable)

def get_capacity(matrix, mode):
    return (split_into_blocks(matrix, encode.create_complexity_dictionary(mode)))


def main():
    image, mode = get_arguments()


    image_arr = encode.get_file(image)

    image_bitplane_arr = np.zeros((image_arr.shape[0], image_arr.shape[1], 8))
    image_bitplane_arr[:,:,0] = np.copy(image_arr)
    image_bitplane_arr = encode.get_bitplane_arr(image_bitplane_arr)


    complexity = encode.get_complexity(image_arr)
    capacity = get_capacity(image_bitplane_arr, mode)

    print("BPCS %s Algorithm" % mode)
    print("Complexity of image: %f" % complexity)
    print("Total blocks: %i" % len(capacity[0]*64))
    print("Capacity of image is %i bits -> %i blocks" % (len(capacity[1])*64, len(capacity[1])))

main()

