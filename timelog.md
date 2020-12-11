# Timelog

* Improved Steganography Algorithm
* Daniel Hislop
* 2317990H
* Dr Ron Poet

## Guidance

* This file contains the time log for your project. It will be submitted along with your final dissertation.
* **YOU MUST KEEP THIS UP TO DATE AND UNDER VERSION CONTROL.**
* This timelog should be filled out honestly, regularly (daily) and accurately. It is for *your* benefit.
* Follow the structure provided, grouping time by weeks.  Quantise time to the half hour.

## Week 1

## Week 2 

### 1 Oct 2020

* *0.5 Hour* Finding relevant research papers
* *0.5 Hour* Writing short summary of each paper to gauge understanding
* *0.5 Hour* Creation of mindmap to outline initial thoughts and direction of project

### 2 Oct 2020

* *0.5 Hour* First meeting with supervisor
* *0.5 Hour* Recorded agreed thoughts on direction of project, outlined logistical details such as frequency of meetings. 

## Week 3

### 10 Oct 2020

* *0.5 Hour* Created GitHub repository with template file structure
* *0.5 Hour* Update markdown files for meetings/timelog and plan

* *1 Hour*  Used Pillow library to read in images and convert to array
* *1 Hour*  Get each individual bit plane of vessel image and secret image. Will need to change this in future to make use of numpy speed

### 11 Oct 2020
* *0.5 Hour* Separated existing code into functions
* *2 hours*  Added function to split vessel and secret images into 8x8 blocks

### 12 Oct 2020

* *1.5 Hours* Added function which calculates complexity measure
* *0.5 Hour* Modified bitplane array function to to take advantage of numpy indexing speed
* *1 Hour* Started work on tests.py file. Only a few test cases so far. Directory structure was modified to accomodate this. These will be updated as time goes on

### 13 Oct 2020

* *0.5 Hour* Added requirements.txt file
* *0.5 Hour* Preparation for supervisor meeting

## Week 4

### 14 Oct 2020

* *0.5 Hour* Supervisor meeting
* *0.5 Hour* Writeup of meeting in markdown file

### 17 Oct 2020

* *1 Hour* Complexity function changed to iterate using np.ndenumerate, rather than iterating over its shape with i,j
* *2 Hours* Added conjugation function. This is the function to handle the XORing operation. Had problems creating the checkerboard shape. np.tile seems to work 
* *5 Hours* Added replacement function. 

### 18 Oct 2020

* *3 Hours* Implemented decoding algorithm. The recovered image is not correct.
* *2 Hours* Spent time comparing the array of the secret before encoding, and the recovered array. Array is different.
* *1 Hour* Changed conjugation function in encoding. Update how checkerboard is created. Hasn't worked
* *1 Hour* Changed conjugation function again. 

## Week 5

### 19 Oct 2020

* *2 Hours* Fixed Issue with image not been recovered correctly. Problem was with both conjugation and complexity functions. Indexing the numpy matrix instead of using value from enumeration caused problem. Checkerboard pattern is now correct and scales to shape of passed in matrix. 
* *0.5 Hour* Update timelog
* *0.5 Hour* Update plan
* *1 Hour* Performed some steganalysis. Generated graph of complexities of each block in the vessel and secret

### 21 Oct 2020

* *0.5 Hour* Supervisor meeting
* *0.5 Hour* Type up notes from meeting


## Week 6

### 31 Oct 2020

* *1 Hour* Added argparsing to encoding and decoding algorithms
* *1 Hour* Added variable complexities. This is 1 part of the improved algorithm. 


### 1 Nov 2020

* *0.5 Hour* Update timelog.md and meetings.md
* *3 Hours* Added gray coding improvement
* *1 Hour* Moved gray coding improvement to 2 functions
* *1 Hour* Moved creation of complexity dictionary to function
* *1 Hour* Created script which calculates the embedding capacity of a file

## Week 7

### 2 Nov 2020

* *4 Hours* Found issue with improved algorithm. Tried alterations to gray coding functions since decoding seemed to work fine for standard algorithm
* *0.5 Hour* Fixed issue by converting image to grayscale using Pillow when reading in

## Week 8

### 9 Nov 2020

* *2 Hours* Improved argparsing. Choice of algorithm now confined to predfined options
* *1 Hours* Moved code from main function to bitplane_arr function. Reduces duplicate code and improves readability
* *0.5 Hour* Added code to modify "__name__" variable in each script. Means modules can be ran as main program and improted by other module
* *0.5 Hour* Started automated tool to detect stego objects
* *0.5 Hour* Argparsing for stegdetect tool
* *0.5 Hour* Implemented case for known cover image and stego object
* *0.5 Hour* Created dictionary for calling functions based on provided argument

### 10 Nov 2020

* *1 Hour* Implemented case in automated tool for known algorithm and stego
* *0.5 Hour* Added exception raise in decoding for when recovered meta data is larger than vessel image
* *2 Hour* Implemented case in automated tool for stego object only. Looks at probabiltiy histogram. Will be able to detect stego objects that used standard algorithm during embedding

### 11 Nov 2020

* *0.5 Hour* Removed redundant code in steganalysis.py
* *1 Hour* Added probability histogram to steganalysis


### 12 Nov 2020

* *0.5 Hour* Supervisor meeting
* *0.5 Hour* Writeup of meeting
* *3 Hour* Updating timelog

### 17 Nov 2020

* *2 Hours* Background reading on JPEG compression and steganography methods
* *0.5 Hour* Created argparsing and filereasing for JPEG encoder
* *0.5 Hour* Created function to generate quantisation matrix
* *1 Hour* Wrote function to perform discrete cosine transform on a block. SciPy method of doing this only worked for 1D array. 
* *1 Hour* Hardcoded the zigzag indices. This is for reordering the qauntized matrix
* *0.5 Hour* Created function to normalise each quantisation matrix using zigzag encoding. This normalised block is then added back to the original matrix.
* *2 Hours* Couldn't produce image properly. Initially though it could be the dct and idct causing problem, however using cv2 instead of scipy the problem persisted. Believe the problem is zigzag


## Week 9

### 23 Nov 2020

* *1 Hour* Sourced existing zigzag encoding functions from another compression algorithm. Source is noted in the file.
* *1 Hour*  Created seperate functions for discrete and inserse cosine transformations
* *3 Hours* Functions to create run length encoding and output to file. 
* *0.5 Hour* Moved JPEG algorithm files to seperate directory.

### 24 Nov 2020

* *3 Hours* Again tried to fix the problem of being unable to recover the image properly. Switched to open-cv python - this provided a DCT and IDCT that generalised to any shape of matrix. These functions would only work by providing it with an open-cv image.
* *0.5 Hour* Switched from Pillow to open-cv python for reading in image.
* *0.5 Hour* Unable to use DCT or IDCT on each block. Had to convert each block to type np.float32
* *0.5 Hour* Function write width and height of image to csv file
* *1 Hour* Redid run length encoding function
* *1 Hour* Redid function to write run length encoding to csv
* *1 Hour* Implemented function to create compressed image from run length encoding
* *3 Hours* Started steganography aspect of JPEG images. Implemented modified LSB steganography. 1 pixel of secret is embedded in the LSB's of the last column in an 8x8 vessel block. 
* *0.5 Hours* Evaluate LSB. Low capacity and large image degradation.

### 25 Nov 2020

* *0.5 Hours* Supervisor Meeting

## Week 10

### 3 Dec 2020

* *1.5 Hours* Update timelog.md
* *0.5 Hours Writeup of supervisor meeting

### 4 Dec 2020

* *0.5 Hour* Added sources for zigzag encoding and canonical gray coding.
* *0.5 Hour* Review of standard BPCS Algorithm
* *0.5 Hour* Moved Gray coding to standard algorithm
* *3 Hours* Updated standard algorithm to work for 24-bit colour images. Can now embed grayscale in grayscale, grayscale in colour and colour in colour. 
* *0.5 Hours* Fixed issue where some grayscale images caused program to crash. Fixed by adding case where image mode is "P" and converting to "L"
* *0.5 Hours* Restructured Directories. Seperate folders for JPEG, BPSC algorithms and Automated Tool. 


### 8 Dec 2020

* *0.5 Hour* Review of Improved BPCS Algorithm
* *1 Hour* 1st Improvement - Different complexity threshold for each bit plane. - Can't have threshold higher than 0.5 or will be unable to recover image
* *1 Hour* 2nd Improvement - Random selection of ordering of bit planes when embedding. Standard algorithm embedds from LSB to MSB, now does so randomly. Provided seed is height of vessel image to ensure random ordering is the same. 
* *0.5 Hour* Modified 2nd improvement to reduce code required. 
* *0.5 Hour* Update timelog

### 11 Dec 2020

* *0.5 Hour* Review of JPEG Algorithm
* *0.5 Hour* Check shape of image read in. (IMG_UNCHANGED) parameter stops cv2 from converting image to 3 channels. Grayscale image will be 2 dimensional, RGB 3 dimensional.
* *0.5 Hour* Creating separate quantixaiton matrices for luminance and chrominance. 
* *0.5 Hour* Function to handle an individual channel. Takes a quantization matrix and channel and calls functions to split into blocks and create RLE
* *0.5 Hour* JPEG Compression now working for colour and grayscale, but compressed image will have green border around outside if image dimensions not divisable by 8.
* *0.5 Hour* Tried using cv2.copyMakeBorder function to correct problem. Did not work
* *0.5 Hour* Fixed issue by resizing image as it is read in.



