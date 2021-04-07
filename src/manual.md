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

Additionally, the complexity histogram graph can be viewed if needed. This is the graph which presented the vulnerability that the stego object only case operates around.

To produce the graph as well when evaluating this case we do:

`py -m detection_tool.stegdetect -m 3 -s stego.bmp -g yes`

To compare the impact of the embedding we can view the graphs for the clean cover and subsequent stego image. For example, for the clean cover `vessel.bmp` and stego image `stego.bmp` we can do:

``py -m detection_tool.stegdetect -m 3 -s test_images/vessel.bmp -g yes`

followed by:

`py -m detection_tool.stegdetect -m 3 -s stego.bmp -g yes`

Two complexity histograms would be created and displayed in the browser. Can compare to see the impact of embedding. Individual bitplanes can be isolated by selecting one in the graph legend.

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

## JPEG Tool

The JPEG tool is responsible for performing two functions: the compression of images using the JPEG compression algorithm, and steganography following compression. 

### Compression

8-bit and 24-bit colour images can be compressed. Implemented compression steps follow the baseline JPEG standard.

Help information can viewed at any time. This will indicate how to use the application:

`py -m jpeg_tool.jpeg_encode -h`

To compress an image, we use the following command:

`py -m jpeg_tool.jpeg_encode -v <path_to_uncompressed_image> -s<path_to_uncompressed_image> -m Compress`

Note that the uncompressed image path must be provided twice. Using the uncompressed "vessel.bmp" as an example:

`py -m jpeg_tool.jpeg_encode -v test_images/vessel.bmp -s test_images/vessel.bmp -m Compress`

Succssful compression will produce the image named `compressed.jpeg` in the current `steganography/` directory.

### Steganography

**NB: Due to the limited capacity of LSB techniques, only 12.5% of vessel bits can be replaced. Meaning most images currently in the test bank are unsuitable for embedding.**

JPEG steganography functions for three implemented techniques: Least Significant Bit (LSB), Third Least Significant Bit (TLSB) and Third Least Significant Bit (TLSBRandom). The embedding process will work for an 8-bit colour cover and 8-bit colour payload, as well as a 24-bit colour cover and 8-bit colour payload. It does not work two 24-bit colour images. Additionally, extraction will only work for two 8-bit colour images. 

Steganography takes place after compression. Both are performed if using any of the command in the following section.

#### Embedding

To embed we use the following command:

`py -m jpeg_tool.jpeg_encode -v <path_to_cover_image> -s<path_to_payload_image> -m <algorithm_choice>`

Using "vessel.bmp" as the cover, "secret.bmp" as the payload and LSB as the algorithm we have:

`py -m jpeg_tool.jpeg_encode -v test_images/vessel.bmp -s test_images/secret.bmp -m LSB`

Using "vessel.bmp" as the cover, "secret.bmp" as the payload and TLSB as the algorithm we have:

`py -m jpeg_tool.jpeg_encode -v test_images/vessel.bmp -s test_images/secret.bmp -m TLSB`

Using "vessel.bmp" as the cover, "secret.bmp" as the payload and TLSBRandom as the algorithm we have:

`py -m jpeg_tool.jpeg_encode -v test_images/vessel.bmp -s test_images/secret.bmp -m TLSBRandom`

A successful emebdding will produce the stego image named `compressed.jpeg` in the current `steganography/` directory.

#### Extraction

Help information can viewed at any time. This will indicate how to use the application:

`py -m jpeg_tool.jpeg_decode -h`

To recover a payload we use the following command: 

`py -m jpeg_tool.jpeg_decode -s <path_to_stego_image> -m <algorithm_choice>`

Using the previously created stego image, "compressed.jpeg" and LSB we have:

`py -m jpeg_tool.jpeg_decode -s compressed.jpeg -m LSB`

Using the previously created stego image, "compressed.jpeg" and TLSB we have:

`py -m jpeg_tool.jpeg_decode -s compressed.jpeg -m TLSB`

Using the previously created stego image, "compressed.jpeg" and TLSBRandom we have:

`py -m jpeg_tool.jpeg_decode -s compressed.jpeg -m TLSBRandom`

Successful extraction will produce the recovered payload `extracted.jpeg` in the current `steganography` directory.

#### Evaluation

Compressed images can be evaluated to produce metrics like Mean Square Error and peak-signal to noise ratio. We can visualise this through a bar chart.

Help information can viewed at any time. This will indicate how to use the application:

`py -m jpeg_tool.jpeg_evaluate -h`

JPEG evaluation is performed through the following command:

`py -m jpeg_tool.jpeg_evaluate -u <path_to_uncompressed_image> -c <path_to_compressed_image> -m <evaluation_mode>`

To evaluate the single image `vessel.bmp` which has been compressed to produce `compressed.jpeg` we do:

`py -m jpeg_tool.jpeg_evaluate -u test_images/vessel.bmp -c compressed.jpeg -m single`

Or if want to evaluate all images in the `test_images` directory we do:

`py -m jpeg_tool.jpeg_evaluate -m all`

The graph produced will display in browser once the program has finished. Individual metrics can be isolated by selecting the desired one by clicking it in the graph legend.

## Payload Comparison Tool

The payload comparison tool faciliates evaluation of the emebdding and extraction operations in each releveant component. It is used to compare the original and extracted payloads to check for a match.

Help information can viewed at any time. This will indicate how to use the application:

`py -m payload_comparison_tool.payload_recovery_test -h`

Payloads can be compared using the following command:

`py -m payload_comparison_tool.payload_recovery_test -o <path_to_original_payload> -r <path_to_extracted_payload>`

Using an example of `secret.bmp` and `extracted.bmp` we have:

`py -m payload_comparison_tool.payload_recovery_test -o test_images\secret.bmp -r extracted.bmp`

This comparison will produce text in the terminal saying either "Recovered matched original" or "Recovered does not match original.

