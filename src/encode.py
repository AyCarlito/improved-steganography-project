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
print("Slicing bitplanes of vessel")
vessel_bitplane_arr = numpy.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
vessel_bitplane_arr[:,:,0] = numpy.copy(vessel_arr)

print("Slicing bitplanes of secret")
#Slice bitplanes of secret
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

print(vessel_bitplane_arr[0:1,0:1])
print(secret_bitplane_arr[0:1,0:1])

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


#Chop sceret into 8x8 bitplanes and place in queue

# for i in range(secret_bitplane_arr.shape[0]/8):
#     for j in range(secret_bitplane_arr.shape[1]/8)

#find complex segements and replace

#Confirm all of secret was placed

#Create new image with embedded secret

