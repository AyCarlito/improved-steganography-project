import pytest
import sys
import os
import numpy as np
sys.path.append("..")

from bpcs_tool import encode

vessel_path = "../test_images/vessel.bmp"
secret_path = "../test_images/secret.bmp"
p_image_path = "../test_images/goldhill.bmp"
colour_path = "../test_images/apple.bmp"

def test_vessel_exists():
    assert(os.path.isfile(vessel_path)) == True
    
def test_secret_exists():
    assert(os.path.isfile(secret_path)) == True

def test_vessel_image_to_array():
    vessel_array = encode.get_file(vessel_path)
    assert(type(vessel_array)) == list
    assert(type(vessel_array[0]) == type(np.array([1])))

def test_secret_image_to_array():
    secret_array = encode.get_file(secret_path)
    assert(type(secret_array)) == list
    assert(type(secret_array[0]) == type(np.array([1])))

def test_grayscale_image_has_single_channel():
    test_array = encode.get_file(vessel_path)
    assert(len(test_array)) == 1

def test_Pmode_image_has_single_channel():
    test_array = encode.get_file(p_image_path)
    assert(len(test_array)) == 1

def test_colour_image_has_three_channels():
    test_array = encode.get_file(colour_path)
    assert(len(test_array)) == 3

def test_gray_coding():
    test_matrix = np.array([[1,2,3], [4,5,6]])
    to_gray_coding = encode.convert_to_gray_coding(test_matrix)
    from_gray_coding = encode.convert_from_gray_coding(to_gray_coding)
    assert np.array_equal(test_matrix, from_gray_coding) == True

def test_conjugation():
    test_matrix = np.array([[0, 1, 1], [1,1,0]])
    conjugated_matrix = encode.conjugate(test_matrix)
    unconjugated_matrix = encode.conjugate(conjugated_matrix)
    expected_matrix = np.array([[1,1,0], [1,0,0]])
    assert np.array_equal(conjugated_matrix, expected_matrix) == True
    assert np.array_equal(unconjugated_matrix, test_matrix) == True

def test_conjugation_gives_correct_complexity():
    test_matrix = np.array([
        [1, 1, 1, 1, 0, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 0, 1, 1, 1], 
        [1, 1, 1, 1, 1, 1, 1, 1],
        ])
    intiial_complexity = encode.get_complexity(test_matrix)
    expected_complexity = 1 - intiial_complexity
    conjugated_complexity = encode.get_complexity(encode.conjugate(test_matrix))
    assert (abs(conjugated_complexity-expected_complexity) <= 0.05)

def test_get_bitplane_array():
    test_matrix = np.array([[128], [16]])
    bitplane_arr = encode.get_bitplane_arr(test_matrix)
    assert np.array_equal(bitplane_arr[0][0], np.array([1,0,0,0,0,0,0,0]))
    assert np.array_equal(bitplane_arr[1][0], np.array([0,0,0,1,0,0,0,0]))

def test_split_into_blocks():
    test_array = encode.get_file(vessel_path)
    test_bitplane_array = encode.get_bitplane_arr(test_array[0])
    data = encode.split_into_blocks(test_bitplane_array, 1)
    assert len(data) == ((test_array[0].shape[0]/8) * (test_array[0].shape[1]/8) * 8)







