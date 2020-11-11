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

