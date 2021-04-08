#!/bin/sh
python3 -m  BPCS_Steganography.encode $1 $2 $3 && python3 -m detection_tool.stegdetect -m 3 -s stego.bmp
