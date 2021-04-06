"""
.. module:: stegdetect
   :synopsis: Functionality of Detection Tool is defined here
.. moduleauthor::  Daniel Hislop
"""


from collections import Counter
import numpy as np
import os
import argparse
import plotly.graph_objects as go
import plotly.figure_factory as ff
from bpcs_tool import encode, decode


COMPLEXITIES = {"standard":{0:0.3, 1:0.3, 2:0.3, 3:0.3, 4:0.3, 5:0.3, 6:0.3, 7:0.3}, "improved":{0:0.1, 1:0.2, 2:0.25, 3:0.30, 4:0.35, 5:0.40, 6:0.45, 7:0.45}}

def get_arguments():
    """**Command line argument parsing**

        Use of the argparse library to parse user input in the command line application. 
        Mode is a positional argument meaning it has to be provided. Others are optional
        so any can be specified. Both mode and algorithm are restricted choice.
    
    Returns:
        Namespace: Parsed user arguments.
    """
    parser = argparse.ArgumentParser(description="BPCS StegDectect Tool")
    parser.add_argument("-m", "--mode", choices=[0,1,2,3], type=int, help="Mode. 0-Known Cover and Stego. 1-Known Algorithm and Stego. 2-Known Payload and Stego. 3-Stego Only")
    parser.add_argument("-c", "--cover", nargs="?", type=str, help="Cover Image")
    parser.add_argument("-s", "--stego", nargs="?", type=str, help="Stego Image")
    parser.add_argument("-p", "--payload", nargs="?", type=str, help="Payload")
    parser.add_argument("-a", "--algorithm", choices=["standard", "improved", "variable_complexity", "RBEO"], nargs="?", type=str, help="Algorithm used in embedding")
    parser.add_argument("-g", "--graph", choices=["yes", "no"], nargs="?", type=str, help="Option to display complexity histogram when using stego object only detection case")
    args = parser.parse_args()
    return args

def complexity(data):
    """**Get complexities of every block**

        Creates a list of complexities of each block using bpcs_encode get_complexity function. 

    Args:
        data (list): List of 8x8 blocks

    Returns:
        list: List of complexities for each block
    """
    complexities = []
    for block in data:
        complexities.append(encode.get_complexity(block))
    return complexities

def known_cover_and_stego(args):
    """**Detection case for known cover object and stego object**

        Reads in cover and stego images. Uses np.array_equal to check if single channel 
        from cover is the same as single channel in stego. If equal then we have hidden 
        payload, otherwise no hidden payload.

    Args:
        args (Namespace): Parsed user arguments - name of cover and name of stego.
    """
    cover_arr = encode.get_file(args.cover)[0]
    stego_arr = encode.get_file(args.stego)[0]
    if (np.array_equal(cover_arr, stego_arr)):
        print("No Hidden payload")
    else:
        print("Hidden payload")
    return
   
def known_payload_and_stego(args):
    """**Detection case for known payload object and stego object**

        Reads in payload and cover images. Gets bitplane arrays and splits into blocks.
        Check if single 8x8 block from payload exists in stego.

    Args:
        args (Namespace): Parsed user arguments - name of payload and name of stego.
    """
    payload_arr = encode.get_file(args.payload)[0]
    stego_arr = encode.get_file(args.stego)[0]

    payload_bitplane_arr = encode.get_bitplane_arr(payload_arr)[:,:,0]
    stego_bitplane_arr = encode.get_bitplane_arr(stego_arr)[:,:,0]

    payload_blocks = []
    for i in range(payload_bitplane_arr.shape[0]//8):
            for j in range(payload_bitplane_arr.shape[1]//8):
                payload_blocks.append(payload_bitplane_arr[i*8:i*8+8,j*8:j*8+8])

    
    stego_blocks = []
    for i in range(stego_bitplane_arr.shape[0]//9):
            for j in range(stego_bitplane_arr.shape[1]//9):
                stego_blocks.append(stego_bitplane_arr[i*8:i*8+8,j*8:j*8+8])
    
    count = 0
    payload_count =0 
    for payload_block in payload_blocks:
        for stego_block in stego_blocks:
            if(payload_block == stego_block).all():
                count+=1
                break

    if(count>(0.75*len(payload_blocks))):
        print("Hidden payload")
    else:
        print("No hidden payload")
    return


def known_algorithm_and_stego(args):
    """**Detection case for known algorithm and stego object**

        Read in stego image and convert each channel to gray coding. Get bitplane array
        and split into blocks using bpcs_decode function. Extract metadata. Recall,
        meta data is (total_blocks, height, width). Check if recovered height and
        width are divisible by 8. If divisible then hidden payload.


    Args:
        args (Namespace): Parsed user arguments - embedding algorithm  and name of stego.
    """

    stego_arr = decode.get_file(args.stego)
    stego_arr = [decode.convert_to_gray_coding(channel) for channel in stego_arr][0]
    stego_bitplane_arr = decode.get_bitplane_arr(stego_arr)

    complexities = COMPLEXITIES["standard"]
    if args.algorithm == "improved" or args.algorithm=="variable_complexity":
        complexities = COMPLEXITIES["improved"]
    data = decode.split_into_blocks(stego_bitplane_arr, complexities)
    try:
        meta_data = decode.extract_meta_data(data, stego_arr)
    except MemoryError:
        print("No Hidden payload")
        return
    print("Hidden payload")
    # if(meta_data[1]%8==0) and (meta_data[2]%8==0):
    #     print("Hidden payload")
    # else:
    #     print("No Hidden payload")
    return

def stego_only(args):
    """**Detection case for stego object only**

        Read in stego image, get bitplane array, split into blocks. Get list of complexities 
        for each block in stego. Find max complexity in this list. If max is greater than
        chosen threshold of 0.9 then hidden payload, otherwise no hidden payload.

    Args:
        args (Namespace): Parsed user arguments - name of stego.
    """
    stego_arr = encode.get_file(args.stego)
    stego_bitplane_arr = encode.get_bitplane_arr(stego_arr[0])
    stego_data = encode.split_into_blocks(stego_bitplane_arr, 0)
    stego_complexities = complexity(stego_data)
    max_complexity = max(stego_complexities)
    if (max_complexity>0.90):
        print("Hidden Payload")
    else:
        print("No Hidden Payload")
    if (args.graph=="yes"):
        create_histogram(stego_complexities)

def create_histogram(stego_complexities):
    """Graph of block complexity histogram**

        Uses plotly library to plot the histogram of block complexities. 
        
    Args:
        stego_complexities (list): List of block complexities
    """
    chunk = len(stego_complexities)//8
    bitplane_complexities = []
    group_labels = ["Bitplane 7", "Bitplane 6", "Bitplane 5", "Bitplane 4", "Bitplane 3", "Bitplane 2", "Bitplane 1", "Bitplane 0"]
    for i in range(8):
        bitplane_complexities.append(stego_complexities[i*chunk:i*chunk+chunk])

    fig = ff.create_distplot(bitplane_complexities, group_labels, show_hist=False, show_rug=False)
    fig.show()
    return

def main():
    """**Driver code of Detection tool**

        Parse user arguments. Call the relevant function (detection case) based on 
        chosen mode. 
    """
    args = get_arguments()
    mode = args.mode
    

    function_calls = {
        0: known_cover_and_stego,
        1: known_algorithm_and_stego,
        2: known_payload_and_stego,
        3: stego_only
    }

    function_calls[mode](args)


if __name__ == "__main__":
    main()