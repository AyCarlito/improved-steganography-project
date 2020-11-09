import numpy as np
from PIL import Image
import os
import argparse
import encode, decode
from subprocess import Popen, PIPE

def get_arguments():
    parser = argparse.ArgumentParser(description="BPCS StegDectect Tool")
    parser.add_argument("-m", "--mode", choices=[0,1], type=int, help="Mode. 0-Known Cover and Stego. 1-Known Message and Stego")
    parser.add_argument("-c", "--cover", nargs="?", type=str, help="Cover Image")
    parser.add_argument("-s", "--stego", nargs="?", type=str, help="Stego Image")
    parser.add_argument("-p", "--payload", nargs="?", type=str, help="Payload")
    parser.add_argument("-a", "--algorithm", choices=["Standard", "Improved"], nargs="?", type=str, help="Algorithm used in embedding")

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
        print("Hidden payload. Attempting recovery")
        if(process_call(["python3", "decode.py", "stego", "standard"])) == 0: return
        if(process_call(["python3", "decode.py", "stego", "improved"])) == 0: return
        print("Failed recovery")

def known_message_and_stego(args):
    message_arr = encode.get_file(args.payload)
    stego_arr = encode.get_file(args.stego)

def known_algorithm_and_stego(args):
    stego_arr = encode.get_file(arg)

def main():
    args = get_arguments()
    mode = args.mode

    function_calls = {
        0: known_cover_and_stego,
        1: known_message_and_stego,
        2: known_algorithm_and_stego
    }

    stego_bitplane_arr = np.zeros((stego_arr.shape[0], stego_arr.shape[1], 8))
    stego_bitplane_arr[:,:,0] = np.copy(stego_arr)
    stego_bitplane_arr = get_bitplane_arr(stego_bitplane_arr)

    function_calls[mode](args)



main()