import numpy as np
from PIL import Image
import os
import encode
import plotly.graph_objects as go

def complexity(data):
    complexities = []
    for block in data:
        complexities.append(encode.get_complexity(block))
    return complexities

def get_probability(value, total):
    return (value/total)


def plot(x, y, gtitle, xtitle, ytitle):
    print("Plotting graph")
    fig = go.Figure()   
    fig.add_trace(go.Scattergl(x=x, y=y, mode='markers', name='markers'))
    fig.update_layout(
        title=gtitle,
        xaxis_title=xtitle,
        yaxis_title=ytitle,
        font=dict(
            family="Courier New, monospace",
            size=18,
            color="#7f7f7f"
        )
    )
    fig.show()

def create_histogram(x):
    fig = go.Figure(data=[go.Histogram(x=x, histnorm="probability")])
    fig.show()

def main():

    vessel_arr = encode.get_file("vessel")
    stego_arr= encode.get_file("stego")


    print("Getting binary encoding of vessel")
    vessel_bitplane_arr = np.zeros((vessel_arr.shape[0], vessel_arr.shape[1], 8))
    vessel_bitplane_arr[:,:,0] = np.copy(vessel_arr)
    vessel_bitplane_arr = encode.get_bitplane_arr(vessel_bitplane_arr)

    print("Getting binary encoding of secret")
    stego_bitplane_arr = np.zeros((stego_arr.shape[0], stego_arr.shape[1], 8))
    stego_bitplane_arr[:,:,0] = np.copy(stego_arr)
    stego_bitplane_arr = encode.get_bitplane_arr(stego_bitplane_arr)

    vessel_data = encode.split_into_blocks(vessel_bitplane_arr)
    stego_data = encode.split_into_blocks(stego_bitplane_arr)

    vessel_complexities = complexity(vessel_data)
    stego_complexities = complexity(stego_data)

    fig = go.Figure(data=[go.Histogram(x=vessel_complexities, histnorm="probability")])
    fig.show()

    fig = go.Figure(data=[go.Histogram(x=stego_complexities, histnorm="probability")])
    fig.show()



    plot(np.arange(len(vessel_data)), vessel_complexities, "Complexity Histogram of Vessel Image", "8x8 Blocks", "Complexity of Block")
    plot(np.arange(len(stego_data)), stego_complexities, "Complexity Histogram of Stego Image", "8x8 Blocks", "Complexity of Block")

if __name__ == "__main__":
    main()