## Data ##

The data directory contains the raw and processed data created during the evaluation of the developed sytem. Evaluated components include "BPCS Tool", "JPEG Tool" and "Detection Tool".

## Ethics ##

System evaluation was subject to ethical approval. The `data/ethics` directory contains the glasgow university standard ethics approval form for 3rd/4th/5th and taught MSci project. Ethics form has been signed by both myself and project supervisor.


## BPCS Tool ## 

Algorithm comparison was split into two phases. Visual detection and digital detection.

### Visual Detection ###

Visual detection evaluation involved the use of external participants. Five participaants provided informed consent after the purpose and method of experiment was explained to them. Participants provided a verdict on whether they believed an image contained a payload or not. The `bpcs_tool/bpcs_visual_detection_evaluation/images` directory contains the images presented to the users. The `bpcs_tool/bpcs_visual_detection_evaluation/google_form` directory contains a pdf of the google form which participants had to fill in. This google form was split into 3 sections: consenting to take part, visual detection phase, questionnaire. Response to the form for all participants were collected as shown in the pdf in the `bpcs_tool/bpcs_visual_detection_evaluation/results` directory. Additionlly, this gathered information is present as a spreadhseet in the same directory. This spreadhseet was used to process the raw data into a bar chart, which was placed in section **6.5.1** of the dissertation.

### Digital Detection ###

Digital detection evaluation involved supplying the detection tool with four types of images: natural, standard BPCS, variable complexity, random bitplane embedding order. The images used for this task can be seen in the `bpcs_tool/bpcs_digital_detection_evaluation/images` directory. This directory is further subdivded into the types of images.

The `natural_images` contains nine natural images, i.e. those with no hidden payload. This can be thought of as the test bank of images discussed in section **6.3** in the dissertation. The results of the detection tool for these images are seen in table **6.1** in the dissertation.

The `standard_algorithm` directory contains six stego images created by the BPCS encoder using the standard algorithm. Table **6.2** in the dissertation shows the detection tool results for these images.

The `variable_complexity` directory contains six stego images created by the BPCS encoder using the variable complexity modification. Table **6.3** in the dissertation shows the detection tool results for these images.

The `RBEO` directory contains six stego images created by the BPCS encoder using the random bitplane embedding order modification. Table **6.4** in the dissertation shows the detection tool results for these images.

A summarised table of results indicating the count of true positives, true negatives, false positives, false negatives and detection rate for each image category is shown in table **6.5** in the dissertation.

## JPEG Tool ##

### Compression ###

JPEG compression was evaluated by supplying the same natural images as in `bpcs_tool/bpcs_digital_detection_evaluation/images/natural images` to the JPEG tool. This raw data was processed into a table displaying, uncompressed size, compressed size and compression ratio for each image, seen in table **6.6** in the dissertation. 

Additional metrics, like mean square error (MSE) and peak signal to noise ratio (PSNR) are calculated for each image. The procesed results are displayed in the bar graphs present in the `jpeg_tool/jpeg_compression_metrics` directory or alternatively figure **6.8** in the dissertation. 

### JPEG Steganography ###

JPEG steganography was evaluated by supplying the JPEG tool with a cover and payload image and selecting the desired algorithm. Three algorithms in total: LSB, TLSB, TLSBRandom.

The `jpeg_tool/jpeg_steganography/images/cover` directory contains the 8-bit colour cover "vessel.bmp" used in evaluation. 

The `jpeg_tool/jpeg_steganography/images/payload` directory contains the 8-bit colour payload "secret.bmp" used in evaluation. 

The `jpeg_tool/jpeg_steganography/images/stegos` directory shows the stego images created via the embedding of the payload in the cover for each algorithm. 

The `jpeg_tool/jpeg_steganography/images/recovered_payloads` directory shows the paylods recovered by the JPEG decoder from the previous stego images. 


