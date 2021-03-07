from collections import Counter
import numpy as np
import os
import argparse
import plotly.graph_objects as go
import plotly.figure_factory as ff
from BPCS_Steganography import encode, decode


COMPLEXITIES = {"standard":{0:0.3, 1:0.3, 2:0.3, 3:0.3, 4:0.3, 5:0.3, 6:0.3, 7:0.3}, "improved":{0:0.1, 1:0.2, 2:0.25, 3:0.30, 4:0.35, 5:0.40, 6:0.45, 7:0.50}}

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS StegDectect Tool")
    parser.add_argument("-m", "--mode", choices=[0,1,2,3], type=int, help="Mode. 0-Known Cover and Stego. 1-Known Algorithm and Stego. 2-Known Payload and Stego. 3-Stego Only")
    parser.add_argument("-c", "--cover", nargs="?", type=str, help="Cover Image")
    parser.add_argument("-s", "--stego", nargs="?", type=str, help="Stego Image")
    parser.add_argument("-p", "--payload", nargs="?", type=str, help="Payload")
    parser.add_argument("-a", "--algorithm", choices=["standard", "improved"], nargs="?", type=str, help="Algorithm used in embedding")
    args = parser.parse_args()
    return args

def complexity(data):
    complexities = []
    for block in data:
        complexities.append(encode.get_complexity(block))
    return complexities

def known_cover_and_stego(args):
    cover_arr = encode.get_file(args.cover)[0]
    stego_arr = encode.get_file(args.stego)[0]
    if (np.array_equal(cover_arr, stego_arr)):
        print("No Hidden payload")
    else:
        print("Hidden payload")
    return
   
def known_payload_and_stego(args):
    payload_arr = encode.get_file(args.payload)[0]
    stego_arr = encode.get_file(args.stego)[0]

    payload_bitplane_arr = encode.get_bitplane_arr(payload_arr)
    stego_bitplane_arr = encode.get_bitplane_arr(stego_arr)

    payload_blocks = encode.split_into_blocks(payload_bitplane_arr, 0)
    stego_blocks = encode.split_into_blocks(stego_bitplane_arr, 0)

    for payload_block in payload_blocks:
        flat_payload = payload_block.flatten()
        for block in stego_blocks:
            flat_stego = block.flatten()
            detected = flat_payload == flat_stego
            if detected.all():
                print("Yes")
                return
    return


def known_algorithm_and_stego(args):
    stego_arr = decode.get_file(args.stego)
    stego_arr = [decode.convert_to_gray_coding(channel) for channel in stego_arr][0]
    stego_bitplane_arr = decode.get_bitplane_arr(stego_arr)
    data = decode.split_into_blocks(stego_bitplane_arr, COMPLEXITIES[args.algorithm])
    meta_data = decode.extract_meta_data(data, stego_arr)
    if(meta_data[1]%8==0) and (meta_data[2]%8==0):
        print("Hidden payload")
    else:
        print("No Hidden payload")
    return

def stego_only(args):
    stego_arr = encode.get_file(args.stego)
    stego_bitplane_arr = encode.get_bitplane_arr(stego_arr[0])
    stego_data = encode.split_into_blocks(stego_bitplane_arr, 0)
    stego_complexities = complexity(stego_data)
    max_complexity = max(stego_complexities)
    if (max_complexity>0.90):
        print("Hidden Payload")
    else:
        print("No Hidden Payload")
    create_histogram(stego_complexities)

def create_histogram(stego_complexities):
    chunk = len(stego_complexities)//8
    bitplane_complexities = []
    group_labels = ["Bitplane 7", "Bitplane 6", "Bitplane 5", "Bitplane 4", "Bitplane 3", "Bitplane 2", "Bitplane 1", "Bitplane 0"]
    for i in range(8):
        bitplane_complexities.append(stego_complexities[i*chunk:i*chunk+chunk])

    fig = ff.create_distplot(bitplane_complexities, group_labels, show_hist=False, show_rug=False)
    fig.show()
    return

def main():
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