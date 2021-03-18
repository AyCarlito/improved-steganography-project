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

Documentation of JPEG Tool

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

Documentation of Detection Tool

stegdetect.py
*************

