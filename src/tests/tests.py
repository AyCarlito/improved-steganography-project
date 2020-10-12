import pytest
import sys
import os
import numpy as np
sys.path.append("..")

from steganography import encode
os.chdir("../steganography")


def test_vessel_exists():
    assert(os.path.isfile("vessel.bmp")) == True
    
def test_secret_exists():
    assert(os.path.isfile("secret.bmp")) == True

def test_vessel_image_to_array():
    vessel_array = encode.get_file("vessel")
    assert(type(vessel_array) == type(np.array([1])))

def test_secret_image_to_array():
    secret_array = encode.get_file("secret")
    assert(type(secret_array) == type(np.array([1])))

def test_get_vessel_bitplane_array():
    vessel_arr = encode.get_file("vessel")
    vessel_bitplane_arr = np.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
    vessel_bitplane_arr[:,:,0] = np.copy(vessel_arr)
    vessel_bitplane_arr = encode.get_bitplane_arr(vessel_bitplane_arr)
    assert (vessel_bitplane_arr.shape[0]==vessel_arr.shape[0])
    assert (vessel_bitplane_arr.shape[1]==vessel_arr.shape[1])
    assert (vessel_bitplane_arr.shape[2] == 8)




