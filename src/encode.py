import numpy
import time
from PIL import Image

#Open Images
print("Opening images")
vessel = Image.open("goldhill.bmp")
secret = Image.open("cameraman.bmp")

#Convert Images to arrays
print("Converting to arrays")
vessel_arr = numpy.array(vessel)
secret_arr = numpy.array(secret)

#Close Images
vessel.close()
secret.close()


#Slice bitplanes of vessel
print("Slicing bitplanes of vessel")
bitplane_arr = numpy.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
bitplane_arr[:,:,0] = numpy.copy(vessel_arr)

for i in range(bitplane_arr.shape[0]):
    for j in range(bitplane_arr.shape[0]):
        bit_array= numpy.unpackbits(numpy.uint8(bitplane_arr[i,j,0]))
        for k in range(8):
            bitplane_arr[i,j,k] = bit_array[k]

print("Slicing bitplanes of secret")
#Slice bitplanes of secret
secret_bitplane_arr = numpy.zeros((secret_arr.shape[0], secret_arr.shape[1], 8))
secret_bitplane_arr[:,:,0] = numpy.copy(secret_arr)

for i in range(secret_bitplane_arr.shape[0]):
    for j in range(secret_bitplane_arr.shape[0]):
        secret_bit_array= numpy.unpackbits(numpy.uint8(secret_bitplane_arr[i,j,0]))
        for k in range(8):
            secret_bitplane_arr[i,j,k] = secret_bit_array[k]


#Chop sceret into 8x8 bitplanes and place in queue

#find complex segements and replace

#Confirm all of secret was placed

#Create new image with embedded secret

