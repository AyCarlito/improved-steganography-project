Documentation of Code
#####################

BPCS Tool
#########

The BPCS tool is used for embedding a payload within a cover image using the Bit Plane Complexity
Segmentation algorithm. This tool provides functionality for 8-bit colour and 24-bit colour
images. Either the standard or modified algorithm can be selected for embedding and extraction.

Usage
*****

While in the steganography directory, usage of the tool is as follows:

**Encoding**

*Windows*

``py -m bpcs_tool.encode <path_to_cover_image> <path_to_payload_image> <algorithm>``

*Linux*

``python3 -m bpcs_tool.encode <path_to_cover_image> <path_to_payload_image> <algorithm>``

**Decoding**

*Windows*

``py -m bpcs_tool.decode <path_to_cover_image> <path_to_payload_image> <algorithm>``

*Linux*

``python3 -m bpcs_tool.decode <path_to_cover_image> <path_to_payload_image> <algorithm>``

Using the "-h" flag will display a help message in the terminal.

encode.py
*********
.. automodule:: bpcs_tool.encode
   :members:

decode.py
*********
.. automodule:: bpcs_tool.decode
   :members:

JPEG Tool
#########

The JPEG Tool is used for performing image compression using the JPEG algorithm. Additionally,
it is responsible for the embedding and extraction of a payload within compressed images. As
part of the evaluation, MSE and PSNR metrics can be calculated and displayed in a plotly graph.

Usage
*****

While in the steganography directory, usage of the tool is as follows:

**Encoding**

*Windows*

``py -m jpeg_tool.jpeg_encode -v <path_to_cover_image> -s <path_to_payload_image> -m <choice of algorithm>``

*Linux*

``python3 -m jpeg_tool.jpeg_encode -v <path_to_cover_image> -s <path_to_payload_image> -m <choice of algorithm>``

**Decoding**

*Windows*

``py -m jpeg_tool.jpeg_decode -s <path_to_stego_image> -m <choice of algorithm>``

*Linux*

``python3 -m jpeg_tool.jpeg_decode -s <path_to_stego_image> -m <choice of algorithm>``

**Evaluation**

*Windows*

``py -m jpeg_tool.jpeg_evaluate -u <path_to_uncompressed_image> -c path_to_compressed_image -m <choice of algorithm>``

*Linux*

``python3 -m jpeg_tool.jpeg_evaluate -u <path_to_uncompressed_image> -c path_to_compressed_image -m <choice of algorithm>``


jpeg_encode.py
**************
.. automodule:: jpeg_tool.jpeg_encode
   :members:

jpeg_decode.py
**************
.. automodule:: jpeg_tool.jpeg_decode
   :members:

zigzag_encoding.py
******************
.. automodule:: jpeg_tool.zigzag_encoding
   :members:

lsb_jpeg.py
***********
.. automodule:: jpeg_tool.lsb_jpeg
   :members:
 
jpeg_evaluate.py
****************
.. automodule:: jpeg_tool.jpeg_evaluate
   :members:   

Detection Tool
##############

The detection tool is used to determine the presence of a hidden payload within a stego object. 
Detection tool implements four detection cases where any one can be selected by the user.
These are: known cover and stego, known payload and stego, known algorithm and stego, stego
object only.

Usage
*****

While in the steganography directory, usage of the tool is as follows:

*Windows*

``py -m detection_tool.stegdetect -m <detection_case> -c <path_to_cover_image> -s <path_to_stego_image> -p <path_to_payload_image> -a <embedding_algorithm>``

*Linux*

``python3 detection_tool.stegdetect -m <detection_case> -c <path_to_cover_image> -s <path_to_stego_image> -p <path_to_payload_image> -a <embedding_algorithm>``


stegdetect.py
*************
.. automodule:: detection_tool.stegdetect
   :members:

