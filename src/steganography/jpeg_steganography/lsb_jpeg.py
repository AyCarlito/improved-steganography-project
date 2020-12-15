import numpy as np
import random
import jpeg_encode

def get_info(secret, vessel):
    height = vessel.shape[0]
    width = vessel.shape[1]

    secret_height = secret.shape[0]
    secret_width = secret.shape[1]
    return height, width, secret_height, secret_width

def lsb_embed_secret(secret, vessel):
    index = 0

    height, width, secret_height, secret_width = get_info(secret, vessel)
   
    secret = secret.flatten()
    vessel = vessel.flatten()

    secret[0] = secret_height/8
    secret[1] = secret_width/8
    for secret_pixel in secret:
        secret_bin_repr = np.unpackbits(secret_pixel)
        vessel_selection = vessel[index*8:index*8+8]
        for i, vessel_pixel in enumerate(vessel_selection):
            vessel_pixel_bin_repr = np.unpackbits(vessel_pixel)
            vessel_pixel_bin_repr[-1] = 1
            vessel_pixel_bin_repr[-2] = 0
            vessel_pixel_bin_repr[-3] = secret_bin_repr[i]
            vessel_pixel = np.packbits(vessel_pixel_bin_repr)
            vessel_selection[i] = vessel_pixel
        vessel[index*8:index*8+8] = vessel_selection
        index+=1
    return vessel.reshape((height,width))

def lsb_decode_secret(stego_name):
    stego = jpeg_encode.get_file("%s" % stego_name)
    if len(stego.shape)==2:
        stego = stego.flatten()
        decoded = lsb_decode_helper(stego)
    else:
        for i in range(3):
            stego_channel = stego[:,:,i].flatten()
            print(stego_channel[0:16])
            try:
                decoded = lsb_decode_helper(stego_channel)
            except ValueError as e:
                pass
    return decoded
    

def lsb_decode_helper(stego):
    secret = []
    index = 0
    for index in range(len(stego)//8):
        stego_selection = stego[index*8:index*8+8]
        secret_pixel = []
        for i, stego_pixel in enumerate(stego_selection):
            stego_pixel_bin_repr = np.unpackbits(stego_pixel)
            secret_pixel.append(stego_pixel_bin_repr[-3]) 
        secret.append(np.packbits(secret_pixel)[0])
        index+=1
    height = secret[0]*8
    width = secret[1]*8
    print(height)
    print(width)
    return np.asarray(secret)[0:(height*width)].reshape((height, width))

def random_lsb_embed_secret(secret, vessel):
    index = 0

    height, width, secret_height, secret_width = get_info(secret, vessel)

    secret = secret.flatten()
    vessel = vessel.flatten()

    random.seed(height)
    embedding_order = random.sample(range(len(vessel)//8), len(vessel)//8)
    embedded = 0
    for i, embedding_location in enumerate(embedding_order):
        if embedded < len(secret):
            secret_bin_repr = np.unpackbits(secret[i])
            vessel_selection = vessel[embedding_location*8:embedding_location*8+8]
            for j, vessel_pixel in enumerate(vessel_selection):
                vessel_pixel_bin_repr = np.unpackbits(vessel_pixel)
                vessel_pixel_bin_repr[-1] = 1
                vessel_pixel_bin_repr[-2] = 0
                vessel_pixel_bin_repr[-3] = secret_bin_repr[j]
                vessel_pixel = np.packbits(vessel_pixel_bin_repr)
                vessel_selection[j] = vessel_pixel
            vessel[embedding_location*8:embedding_location*8+8] = vessel_selection
           
            embedded+=1
    
    vessel[0] = (secret_height/8)
    vessel[8] = (secret_width/8)
    return vessel.reshape((height,width))

def random_lsb_decode_secret(stego_name):
    stego = jpeg_encode.get_file("%s" % stego_name)
    random.seed(stego.shape[0])
    stego = stego.flatten()
    secret = []
    
    height = stego[0]*8
    width = stego[8]*8

    embedding_order = random.sample(range(len(stego)//8), len(stego)//8)
    for i, embedding_location in enumerate(embedding_order):
        secret_pixel = []
        stego_selection = stego[embedding_location*8:embedding_location*8+8]
        for j, stego_pixel in enumerate(stego_selection):
            stego_pixel_bin_repr = np.unpackbits(stego_pixel)
            secret_pixel.append(stego_pixel_bin_repr[-3])
        secret.append(np.packbits(secret_pixel)[0])

    return np.asarray(secret)[0:(height*width)].reshape((height, width))

    