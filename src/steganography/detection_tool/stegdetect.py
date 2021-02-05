from subprocess import Popen, PIPE
from collections import Counter
import numpy as np
import os
import argparse
import plotly.graph_objects as go
import plotly.figure_factory as ff
from BPCS_Steganography import encode
import steganalysis

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS StegDectect Tool")
    parser.add_argument("-m", "--mode", choices=[0,1,2,3], type=int, help="Mode. 0-Known Cover and Stego. 1-Known Algorithm and Stego")
    parser.add_argument("-c", "--cover", nargs="?", type=str, help="Cover Image")
    parser.add_argument("-s", "--stego", nargs="?", type=str, help="Stego Image")
    parser.add_argument("-p", "--payload", nargs="?", type=str, help="Payload")
    parser.add_argument("-a", "--algorithm", choices=["standard", "improved"], nargs="?", type=str, help="Algorithm used in embedding")

    args = parser.parse_args()
    return args

def process_call(command):
    p = Popen(command, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    return p.returncode

def known_cover_and_stego(args):
    cover_arr = encode.get_file(args.cover)
    stego_arr = encode.get_file(args.stego)
    if (cover_arr==stego_arr).all():
        print("No hidden payload")
    else:
        print("Hidden payload")
       # if(process_call(["python3", "decode.py", "stego", "standard"])) == 0: return
        #if(process_call(["python3", "decode.py", "stego", "improved"])) == 0: return
        #print("Failed recovery")
    return

def known_algorithm_and_stego(args):
    stego_arr = decode.get_file(args.stego)
    if args.algorithm == "improved":
        stego_arr = decode.convert_to_gray_coding(stego_arr)
    complexities = decode.create_complexity_dictionary(args.algorithm)
    stego_bitplane_arr = decode.get_bitplane_arr(stego_arr)
    data = decode.split_into_blocks(stego_bitplane_arr, complexities)
    try:
        meta_data = decode.extract_meta_data(data, stego_arr)
        print("Hidden Payload")
    except MemoryError:
        print("No Hidden payload")
    return

def known_message_and_stego(args):
    message_arr = encode.get_file(args.payload)
    stego_arr = encode.get_file(args.stego)
    return

def stego_only(args):
    stego_arr = encode.get_file(args.stego)
    stego_bitplane_arr = encode.get_bitplane_arr(stego_arr[0])
    stego_data = encode.split_into_blocks(stego_bitplane_arr, 0)
    stego_complexities = steganalysis.complexity(stego_data)
    max_complexity = max(stego_complexities)
    if (max_complexity>0.9):
        print("Hidden Payload")
    else:
        print("No Hidden Payload")
    quit()
    chunk = len(stego_complexities)//8
    bitplane_complexities = []
    group_labels = ["Bitplane 7", "Bitplane 6", "Bitplane 5", "Bitplane 4", "Bitplane 3", "Bitplane 2", "Bitplane 1", "Bitplane 0"]
    fig = ff.create_distplot(stego_complexities, ["Bitplanes"], show_hist=False, show_rug=False)
    fig.show()
    quit()
    for i in range(8):
        bitplane_complexities.append(stego_complexities[i*chunk:i*chunk+chunk])

    fig = ff.create_distplot(bitplane_complexities, group_labels, show_hist=False, show_rug=False)
    fig.show()
    quit()

    stego_complexities = [complexity for complexity in stego_complexities if(complexity >= 0.1)]
    frequencies = Counter(stego_complexities).most_common(2)    
    if not (0.5<=frequencies[0][0] and frequencies[0][0]<=0.6):
        print("Hidden Payload")
    else:
        print("No Hidden Payload")
    return

def create_histogram(x):
    fig = go.Figure(data=[go.Histogram(x=x, histnorm="probability")])
    fig.show()



def main():
    args = get_arguments()
    mode = args.mode
    

    function_calls = {
        0: known_cover_and_stego,
        1: known_algorithm_and_stego,
        2: known_message_and_stego,
        3: stego_only
    }

    function_calls[mode](args)


if __name__ == "__main__":
    main()