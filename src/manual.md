# User manual #

This manual details instructions for use of each system component. General commands will be shown along with specific examples.

**NB: To use any of the components, you must be in the steganography directory. This can be performed like so:**

`cd steganography/`

## BPCS Tool ##

The BPCS tool is the system component responsible for embedding and extraction of a payload within a cover object using either the standard or modified algorithms. The tool functions in three cases: 8-bit colour payload and 8-bit colour cover, 8-bit colour payload and 24-bit colour cover and 24-bit colour payload and 24-bit colour cover. 

### Embedding ###

**NB: If using windows, use the `py` alias for pyton. If on Linux, use `python3`. If neither of these work or apply then use the alias you have set on your system.**

To embed a payload within a cover image, use the following command:

`py -m bpcs_tool.encode <path_cover_image> <path_to_payload_image> <algorithm_choice>`

With the example    of the cover, vessel.bmp, and payload, secret.bmp, and standard algorithm choice:

`py -m bpcs_tool.encode test_images/vessel.bmp test_images/secret.bmp standard`

A choice of the modified algorithm will include both modifications:

`py -m bpcs_tool.encode test_images/vessel.bmp test_images/secret.bmp improved`

To use the variable complexity modification only, use the following command:

`py -m bpcs_tool.encode test_images/vessel.bmp test_images/secret.bmp improved -m1 yes`

To use the random bitplane embedding order modification, use the following command:

`py -m bpcs_tool.encode test_images/vessel.bmp test_images/secret.bmp improved -m2 yes`

The produced stego image will be named `stego.bmp` and will appear in the current `steganography/` directory.

### Extraction ###

To extract a payload within the previously produced stego image, use the following command:

`py -m bpcs_tool.decode <path_to_stego_image> <algorithm_choice>`

Describe how to use your software, if this makes sense for your code. Almost all projects should have at least some instructions on how to run the code. More extensive instructions can be provided here.
