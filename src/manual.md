# User manual #

This manual details instructions for use of each system component. General commands will be shown along with specific examples.

**NB: To use any of the components, you must be in the steganography directory. This can be performed like so:**

`cd steganography/`

**NB: If using windows, use the `py` alias for pyton. If on Linux, use `python3`. If neither of these work or apply then use the alias you have set on your system.**

## BPCS Tool ##

The BPCS tool is the system component responsible for embedding and extraction of a payload within a cover object using either the standard or modified algorithms. The tool functions in three cases: 8-bit colour payload and 8-bit colour cover, 8-bit colour payload and 24-bit colour cover and 24-bit colour payload and 24-bit colour cover. 

### Embedding ###



Help information can viewed at any time. This will indicate how to use the application:

`py -m bpcs_tool.encode -h`

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

Help information can viewed at any time. This will indicate how to use the application:

`py -m bpcs_tool.decode -h`

To extract a payload within a stego image, use the following command:

`py -m bpcs_tool.decode <path_to_stego_image> <algorithm_choice>`

Using the previously produced stego image and the standard algorithm:

`py -m bpcs_tool.decode stego.bmp standard`

Using the previously produced stego image and the improved algorithm:

`py -m bpcs_tool.decode stego.bmp improved`

Using the previously produced stego image and the variable complexity modification:

`py -m bpcs_tool.decode stego.bmp improved -m1 yes`

Using the previously produced stego image and random bitplane embedding order modification:

`py -m bpcs_tool.decode stego.bmp improved -m2 yes`

The extracted payload will be named `extracted.bmp` and and will appear in the current `steganography/` directory.

## Detection Tool ## 

The detection tool is the system component responsible for detecting the presense of a hidden payload within a suspected stego image. There are four detection cases that can be used. In all cased, text will appear in the terminal stating either "No Hidden Payload" or "Hidden payload"


Help information can viewed at any time. This will indicate how to use the application:

`py -m detection_tool.stegdetect -h`

##### Stego Object Only 

This is the main case in the detection tool. This case faciliated the comparison of the standard algorithm and modifications.

`py -m detection_tool.stegdetect -m 3 -s <path_to_stego_image>`

Using the stego of secret.bmp in vessel.bmp:

`py -m detection_tool.stegdetect -m 3 -s stego.bmp`

##### Known Cover and Stego Detection Case

`py -m detection_tool.stegdetect -m 0 -c <path_to_cover_image> -s <path_to_stego_image>`

Using the stego image, secret.bmp embedded in vessel.bmp, and the known cover, vessel.bmp:

`py -m detection_tool.stegdetect -m 0 -c test_images/vessel.bmp -s stego.bmp`

##### Known Algorithm and Stego Detection Case

`py -m detection_tool.stegdetect -m 1 -s <path_to_stego_image> -a <algorithm_choice>`

Using the standard algorithm and stego:

`py -m detection_tool.stegdetect -m 1 -s stego.bmp -a standard`

Using the modified algorithm (modified covers both modifications) and stego:

`py -m detection_tool.stegdetect -m 1 -s stego.bmp -a improved`

Using the variable complexity modification and stego:

`py -m detection_tool.stegdetect -m 1 -s stego.bmp -a variable_complexity`

Using the random bitplane embedding order modification and stego:

`py -m detection_tool.stegdetect -m 1 -s stego.bmp -a RBEO`

**NB: The embedding signature for each of these algorithms is the same - checking for a memory error when attempting to extract metadata"**.

##### Known Payload and Stego Detection Case

`py -m detection_tool.stegdetect -m 2 -s <path_to_stego_image> -p <path_to_payload_image>`

Using the stego of secret.bmp in vessel.bmp and the payload secret.bmp:

`py -m detection_tool.stegdetect -m 2 -s stego.bmp -p secret.bmp`






Describe how to use your software, if this makes sense for your code. Almost all projects should have at least some instructions on how to run the code. More extensive instructions can be provided here.
