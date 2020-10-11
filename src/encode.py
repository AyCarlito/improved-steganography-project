import numpy
import time
from PIL import Image


# #Open Images
# print("Opening images")
# vessel = Image.open("goldhill.bmp")
# secret = Image.open("cameraman.bmp")

# #Convert Images to arrays
# print("Converting to arrays")
# vessel_arr = numpy.array(vessel)
# secret_arr = numpy.array(secret)

# #Close Images
# vessel.close()
# secret.close()

def get_file(name):
    print("Opening %s" % name)
    temp = Image.open("%s.bmp" % name)
    temp_arr = numpy.array(temp)
    temp.close()
    return temp_arr


vessel_arr = get_file("vessel")
secret_arr = get_file("secret")

#Slice bitplanes
print("Getting binary encoding of vessel")
vessel_bitplane_arr = numpy.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
vessel_bitplane_arr[:,:,0] = numpy.copy(vessel_arr)

print("Getting binary encoding of secret")
secret_bitplane_arr = numpy.zeros((secret_arr.shape[0], secret_arr.shape[1], 8))
secret_bitplane_arr[:,:,0] = numpy.copy(secret_arr)

def getBitplaneArr(matrix):
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            bit_array = numpy.unpackbits(numpy.uint8(matrix[i,j,0]))
            for k in range(8):
                matrix[i,j,k] = bit_array[k]
    return matrix

vessel_bitplane_arr = getBitplaneArr(vessel_bitplane_arr)
secret_bitplane_arr = getBitplaneArr(secret_bitplane_arr)


def split_into_blocks(matrix):
    print("Creating 8x8 Blocks for each bitplane")
    for k in range(7, -1, -1):
        for i in range(matrix.shape[0]//8):
            for j in range(matrix.shape[1]//8):
                data.append(matrix[i*8:i*8+8,j*8:j*8+8,k])
        return data

data = []
data = split_into_blocks(secret_bitplane_arr)

#Chop sceret into 8x8 bitplanes and place in queue

# for i in range(secret_bitplane_arr.shape[0]/8):
#     for j in range(secret_bitplane_arr.shape[1]/8)


# for i in range(bitplane_arr.shape[0]):
#     for j in range(bitplane_arr.shape[0]):
#         bit_array= numpy.unpackbits(numpy.uint8(bitplane_arr[i,j,0]))
#         for k in range(8):
#             bitplane_arr[i,j,k] = bit_array[k]



# for i in range(secret_bitplane_arr.shape[0]):
#     for j in range(secret_bitplane_arr.shape[0]):
#         secret_bit_array= numpy.unpackbits(numpy.uint8(secret_bitplane_arr[i,j,0]))
#         for k in range(8):
#             secret_bitplane_arr[i,j,k] = secret_bit_array[k]


#find complex segements and replace

#Confirm all of secret was placed

#Create new image with embedded secret

