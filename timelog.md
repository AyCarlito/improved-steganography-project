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

## Project Week

### 8 Dec 2020

* *0.5 Hour* Review of Improved BPCS Algorithm
* *1 Hour* 1st Improvement - Different complexity threshold for each bit plane. - Can't have threshold higher than 0.5 or will be unable to recover image
* *1 Hour* 2nd Improvement - Random selection of ordering of bit planes when embedding. Standard algorithm embedds from LSB to MSB, now does so randomly. Provided seed is height of vessel image to ensure random ordering is the same. 
* *0.5 Hour* Modified 2nd improvement to reduce code required. 
* *0.5 Hour* Update timelog

### 11 Dec 2020

* *0.5 Hour* Review of JPEG Algorithm
* *0.5 Hour* Check shape of image read in. (IMG_UNCHANGED) parameter stops cv2 from converting image to 3 channels. Grayscale image will be 2 dimensional, RGB 3 dimensional.
* *0.5 Hour* Creating separate quantizaiton matrices for luminance and chrominance. 
* *0.5 Hour* Function to handle an individual channel. Takes a quantization matrix and channel and calls functions to split into blocks and create RLE
* *0.5 Hour* JPEG Compression now working for colour and grayscale, but compressed image will have green border around outside if image dimensions not divisable by 8.
* *0.5 Hour* Tried using cv2.copyMakeBorder function to correct problem. Did not work
* *0.5 Hour* Fixed issue by resizing image as it is read in.


### 13 Dec 2020

* *0.5 Hour* Removed functions to create quantization matrices. These are now global variables. 
* *0.5 Hour* Removed function to pad image which is no longer necessary. 
* *2 Hours* LSB Steganography. Does not work.

### 14 Dec 2020

* *3 Hours* Created seperate functions to handle grayscale and colour images. Makes use of function to handle single channel.
* *1 Hour* Fixed LSB steganography by adding paramter to openCV write image.

### 15 Dec 2020

* *2 Hours* Added random LSB steganography.
* *0.5 Hour* Moved LSB functions to seperate file.

## Christmas Break

## Semester 2

### 4 Jan 2021

* *1 Hour* Motivation section of dissertation introduction. Gave historical example of steganography usage and description of what steganography is.
* *0.5 Hour* Outline of the differences between simple steganography like LSB and BPCS
* *0.5 Hour* Reason for JPEG being steganographhy being different.

### 5 Jan 2021

* *1 Hour* List of project aims
* *1 Hour* Finished off motivation.

### 6 Jan 2021 

* *1 Hour* Skeleton outline of backgrouns chapter. Will be Lit Review followed by explanation of relevant information.

## Week 1

### 12 Jan 2021

* *0.5 Hour* Supervisor meeting

### 15 Jan 2021

* *1 Hour* Started background chapter. Explained terminology and fundamental concepts like bitplanes and pixels.
* *0.5 Hour* Brief overview of BPCS algorithm.
* *0.5 Hour* Brief overview of JPEG compression.

### 17 Jan 2021

* *0.5 Hour* Reworked pixels subsection.
* *1 Hour* Did LSB emebdding section. Added figures to this.

## Week 2

### 18 Jan 2021

* *1 Hour* Explanation of Discrete Cosine Transformation
* *0.5 Hour* Creation of cosine functions graphed using desmos.
* *0.5 Hour* DC vs AC Coefficients.

### 19 Jan 2021

* *0.5 Hour* Supervisor meeting
* *0.5 Hour* Update meetings.md
* *1 Hour* Update timelog

### 23 Jan 2021

* *1 Hour* Analysis Section of dissertation. Proivded list of requirements (these were written with MoSCoW prioritisation).
* *1 Hour* Literature Review section in background of disseration.

### 24 Jan 2021

* *0.5 Hour* Created Gantt Chart
* *1 Hour* Discussed libraries used
* *0.5 Hour* Rest of implementation

## Week 3

### 31 Jan 2021

* *1 Hour* BPCS Background. Expanded on steps.
* *0.5 Hour* JPEG Background. Quantization, Zig Zag. RLE

## Week 4

### 1 Feb 2021

* *1 Hour* Steganalysis background. 
* *0.5 Hour* Design. System architecture and bpcs tool

### 2 Feb 2021

* *1 Hour* Evaluation section. Overview of chapter, experiment methodology, meeting the requirements section.

### 5 Feb 2021

* *0.5 Hour* Background reading of steganalysis paper. Uses histogram analysis to detect.
* *1 Hour* Tried to implement the steganlaysis technique found in paper, however results of the paper could not be reproduced. (Valley signature did not appear in my own results.)
* *1 Hour* Implemented a different mechanism for detection. Natural images seemed to have a maximum complexity value of no higher than 0.9. After emebdding it is over 0.9. A simple check for maximum block complexity value enables detection.

### 7 Feb 2021

* *1 Hour* Detection tool section of implementation. Provided overview of te 4 cases and how they were implemented. Also described the new setganalysis technique used insetad of the one specified in the background. 

## Week 5 

### 8 Feb 2021

* *1 Hour* Evaluation section - Test images section outlining what images are uased and where they are sources from. Evaluation of standard algorithm, shows usage of embedding and extractiono of grayscale and colour images. Evaluation of improved algorithm, same as standard just with modifications. 

### 12 Feb 2021

*0.5 Hour* - JPEG Compression section evaluation. Discussed metric to be used such as mean square error and peak signal to noise ratio.
*0.5 Hour* - Wrote start of conclusion section stating what chapter would be about.
*0.5 Hour *- Uploaded test images to overleaf and added tables into evaluation section.

### 14 Feb 2021

*0.5 Hour* - Revised system architecture section. 
*0.5 Hour *- Added User interface section. Describing consistency of design and command line application. 
*0.5 Hour* - Added maintainability section

## Reading Week

### 15 Feb 2021

*0.5 Hour* Wrote documentation section and added sphinx as library used in implementation.
*1 Hour *Added more code blocks in implementation section

### 16 Feb 2021

*1.5 Hours* - Performing evaluation of standard BPCS algorithm. Added figures to support claims.

### 17 Feb 2021

*1 Hour*- Adding figures to the modified algorithm evaluation section. 
*1 Hour*- JPEG Compression evaluation section. Includes table outlining , file name, type, size compressed size and compression ratio.

### 18 Feb 2021

*2 Hours* - Evaluation section, evaluating the modifications and reporting on detection rate. Tables produced for natural images, stegos created from standard algorithm, stegos created from variable complexity, stegos created from RBEO.

### 20 Feb 2021

*1 Hour* - Conclusion section of dissertation. Wrote summary and future work.

## Week 6

*0.5 Hour* - justification of modifications in design section
*1.5 Hour *- Making system architecture diagrams

### 26 Feb 2021

*0.5 Hour*- Writing textual description of bpcs, jpeg and detection tools and adding architectural diagrams.
*0.5 Hour*- Rewrote JPEG compression and steganography design.
*0.5 Hour*- Improved writing of system architecture section.

### 27 Feb 2021

*1 Hour* Rewrote sections in implementation. VErsion control, methodology, development language, issue tracking. 

### 28 Feb 2021

*1 Hour* - lLibraries Used

## Week 7

### 1 March 2021

*1.5 Hour *- implementation section. Writing about bpcs tool and jpeg

### 2 March 2021

*0.5 Hour* Meeting with supervisor.

### 4 March 2021

*1.5 Hours* Rewrite of BPCS tool. Includes additional paragraphs about decoder, metadata. Better explains how gray coding conversion works.

### 5 March 2021

*1.5 Hours* - Rewrite of Detection tool. Explanation of detection cases. Only one figure added. 

### 6 March 2021

*1.5 Hours* - going over code for four cases in detection tool. Removed redundant code. Moved plotly histogram creation to seprate function. Fixed known cover and stego case. updated argparse help command to show all cases that can be chosen.
*0.5 Hours* - Wrote up past meetings.
*0.5 Hours* - Writing up timelog. 
*0.5 Hours* - Added future work based on detection tool.
*1 Hour* - Rewrite of JPEG implementation.

### 7 March 2021

*0.5 Hour* - Wrote rough outline of JPEG steganography evaluation
*1 Hour* - Rewrite of JPEG steganography implementation. Discussed problems with OpenCV
*0.5 Hour* - Write up implementation of run length encoding

## Week 8

### 8 March 2021

*0.5 Hour* - Added figures for JPEG Steganography evaluation section. 
*0.5 Hour* - Implementation of MSE and PSNR calculaitons. Takes uncompressed and compressed images as parameters. Will be used in JPEG compression evaluation section.


### 10 March 2021

*1 Hour* - Added metric section to JPEG compression evaluation
*1 Hour* - Metrics code now calculated MSE and PSNR for all images in test_images directory.


### 11 March 2021

*1.5 Hours* - Started rewrite of evaluation section. Including, summary of chapter, methodolofy and test images section. Added a meeting the requirements section.

### 12 March 2021

*1.5 Hours* - Rewrite of standard algorithm evaluation section. Removed repeated figures. Instead now shoing stego and recovered payload for each part. Example command usage is shown once, rather than every time.


### 13 March 2021

*1 Hour* - Started rewrite of modified algorithm evaluation section.
*0.5 Hour* - Found issue with variable compleixty. High level of degradation, can be fixed by by changing which butplanes are mapped to which threshold. However this renders
payload unrecoverable in some instances.
*0.5 Hour* - Reformat of tables. Added centering, captions and horizontal lines. 

### 14 March 2021

*0.5 Hour* - Created table for meeting the requirements section.
*0.5 Hour* - Added unit testing section in evaluation
*1 Hour* - Rewrite of comparison of standard and improved BPCS section in evaluation.

## Week 9

### 17 March 2021

*1 Hour* - Documentation of BPCS Encode
*0.5 Hour* - Documentation of BPCS decode.
*0.5 Hour* - BPCS encode and encode usage documentation.

### 18 March 2021

*0.5 Hour* - Fixed issue with csv file during JPEG compression. Windows adds an extra carriage return; this was fixed using the "newline=''" flag when writing and appending csv file. Additionally,
fixed argparse terminiology -> swapped vessel for cover and secret for payload.
*1.5 Hour* - Documentation of JPEG Decode/Evaluate/LSB_Steganography/ZigZag.

### 19 March 2021

*0.5 Hour* - Documentation of Detection tool.
*0.5 Hour* - Documentation of JPEG encode.
*0.5 Hour* - Update meetings, plan and timelog. 

### 20 March 2021

*0.5 Hour* - Added payload comparison tool and documentation for it
*0.5 Hour* - Changed how known algorithm and stego detection case works. Now checks for memoryerror
*1 Hour* - Detection tool evaluation 
*0.5 Hour* - Added figures to test images section and fixed figures in jpeg steganography section.

### 21 March 2021
*0.5 Hour* - rewrote unit testing and summary part of evaluation
*0.5 hour* -  fixed figures in modified algorithm.
*0.5 hour* - outlines visual detection section.
*0.5 hour* - created google form and images to be used in external participant evaluation. 

## Week 10

### 22 March 2021

*2 hours*- Carried out external participant evaluation
*1 hour* - write up the visual detection section in evaluation.

### 24 March 2021

*0.5 hour* - added jpeg part to lit review
*0.5 hour* - fixing of background section up to and including lsb embedding. Also fixed headings of jpeg section in background.

### 25 March 2021

*0.5 Hour* - Rewrite BPCS embedding section of background
*1.5 Hour* - rewrite of jpeg section of background. Including added figures of zigzag encoding and quantisation tables.


### 26 March 2021

*1 Hour* - Rewrite of Analysis section. Change requirements to be split into functional and nonfunctional. Also added description of MoSCoW.
*1 Hour* - Rewrite of design. Added extra description of detection cases. Moved modifications to subheadings of bpcs tool.


### 27 March 2021

*1 Hour* - Rewrite version control. Development methodology, issue tracking. Took out figure of test driven development.
*1.5 hour* - rewrite libraries and language.
*0.5 hour* - rewrite user interface section. Maintainability section removed completely and instead summarised in couple sentences and put in rewritten command line application section.

### 28 March 2021

*0.5 Hour* - BPCS tool implementation intro. Rewrite of how argparse is used.
*0.5 Hour* - Removal of code block figures in BPCS tool implementation and addition of code listings.
*1.5 Hours* - Further rewrite bpcs tool implementation. - includes pillow reading in images, gray coding conversion. Dictionary of complexity thresholds. Embedding order. And embedding steps and metadata. Also rewrote last paragraph on decoder. 

## Week 11

### 29 March 2021

*2.5 Hours* - Rewrite JPEG tool implementation section.

### 30 March 2021

*2 Hour *- Rewrite detection tool implementation section.
*1 Hour* - Rewrite evaluation sections unit testing, experiment methodology and test images.

### 1 April 2021

3 Hours - Rewrite visual detection and digital detection section of algorithm comparison in evaluation.

### 2 April 2021

*3 Hours* - Rewrite JPEG compression section

### 4 April 2021

*3 Hours* - Rewrite JPEG steganography
*3 Hours* - Rewrite conclusion

## Final Week 

### 5 April 2021

*2 Hours* - Created data folder and added evaluation images
*0.5 Hour* - Rough abstract written
*0.5 Hour* - Can now select which modification to use in bpcs tool
*0.5 Hour* - Implementation of known payload case






















