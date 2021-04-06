# Meetings 

## First Meeting - 2 Oct 2020

* Meeting Duration: 11:00 - 11:06

### Discussion

Meetings - Once every 2 weeks. Wednesday 12:30

Implement algorithm in any language. Will be using Python

Interesting part of project is lossy compression and improving detectability component rather than capacity

## Second Meeting - 14 Oct 2020

* Meeting Duration: 12:31 - 12:40

### Discussion

Asked how replacement portion of algorithm works. Find which blocks are complex and replace. Have some way to track which blocks have been conjugated and store this conjugation map. 

## Third Meeting - 21 Oct 2020

* Meeting Duration: 12:32-12:47

### Discussion

Showed progress on encoding and decoding algorithms as well as visualisations produced.

Asked which visualisations should be produced.
- Complexity Histogram - Frequency of colour values

Should also implement an automated steganalysis tool to determine if image is stego object or not.

## Fourth Meeting - 4 Nov 2020

* Meeting Duration: 17:31-17:37

### Discussion 

Showed improved histogram -> A result of gray coding and variable complexities. 

Asked about steganalysis cases and whether I was missing any. Cases are as follows:
- Stego Object Only
- Known cover and stego
- Known message and stego
- Known algorithm and stego
- Known cover, algorithm and stego
- Known message, algorithm and stego

## Fifth Meeting - 11 Nov 2020

* Meeting Duration: 12:31-12:35

### Discussion 

Will finish automated tool by next week. Then will make a start on JPEG steganography


## Sixth Meething - 18 Nov 2020

* Meeting Duration: 12:30-12:38

### Discussion

Started looking at JPEG steganography but struggling to implement JPEG compression.

Reviewed the steps involved in compression:
- Split into blocks
- Discrete Cosine Transform on each block
- Normalise with Quantisation Matrix
- Do ZigZag Encoding

Discussed run length encoding -> clarified that every two number in RLE file are a pair. 

## Seventh Meeting - 25 Nov 2020

* Meeting Duration: 12:30-12:38

### Discussion

JPEG compression is now working. Issue was with Discrete Cosine Transform and Inverse Cosine Transform. Switched libraries and fixed problem -> Pillow and SciPy to open-cv

Agreed to have next meeting in 3 weeks time -> Don't expect to get much work done, as coursework due in next week and exam the week after.


## Eighth Meeting - 15th Dec 2020

* Meeting Duration: 12:31-12:38

### Discussion

Went over everything I've missed. 
- Standard BPCS Algorithm. Works for both graysale and colour. Moved gray coding into standard. Added 2 modifications.
- JPEG. Now works for colour images. Third LSB Steganography, Random LSB steganography. Fixed issue with recovering secret due to openCV.

Discussed plan going forwards. Start writeup and finish automated tool.

## Ninth Meeting - 12th Jan 2021

* Meeting Duration: 13:31-13:35

### Discussion

Asked for guidance on writing dissertation. Will be sticking to plan laid out in status report. These meetings will be used to get feedback on sections of dissertation.

## Tenth Meeting - 19th Jan 2021

* Meeting Duration: 13:30-13:35

### Discussion

Went over Introduction in dissertation. This only needs to be a working version for now to motivate rest of writing, will likely rewrite at the end.

## Eleventh Meeting - 26th Jan 2021

* Meeting Duration: 13:30 - 13:35

### Discussion

Went over Background in dissertation. Explicitly reference. Need to alter terminology section.

## Twelfth Meeting - 2 Feb 2021

* Meeting Duration: 13:30 - 13:33

### Discussion

Went over sections of dissertation. Will be working on detection tool this week and performing evaluation the week after. Design section left till the end. In implemenation include screenshots of all parts of code. 

## Meeting 12 - 9 Feb 2021

* Meeting Duration: 13:31 - 13:39

### Discussion

Started write up of evaluation, done enough of automated tool to start this. One modificatio will likely have no improvement, this is finde as long as it is explained why. 
Extensive documentaton isn't needed, only a README to allow for usage. Next meeting will be in 2 weeks, will email section of evaluation and hopefully start conclusion.

## Meeting 13 - 23rd February 2021

* Meeting Duration: 13:30-13:40

### Discussion

Revaluation as it currently stands has a lots of repeated informaiton with only small variance, e.g. evaluation of standard and improved algorithms. Should reword and shorten. 
Increase figure size.
Images are broken and not displaying.
Making jpeg tool work for 24-bit colour and 24-bit colour is worth putting in future work section. 
Detection method in background section did not work. Keep it and explain why it didn't work, and what was performed instead.
Improvemens don't have to actually improve the algorithm, so long as it is explained why they didn't work, and what steps can be taken to address it.

## Meeting 14 - 2nd March 2021

* Meeting Duration: 13:30-13:38

### Discussion

Literature review does not have to be much longer than it already is. Lit review for this prooject should not be a wide survey. 
Small figure size in design section.
Missing arrow in system archicture diagram. 
Plan to have implementation done for next meeting, and then evaluation for meeting after that. 
Also worth putting in section to show maximum embedding capacity of each algorithm. Can also explain how modifications impacted the capacity. 
Meetings closer to deadline will be used for full read through. 

## Meeting 15 - 9th March 2021

* Meeting Duration: 13:31-13:35

### Discussion

No issues with sections of dissertation that were emailed. Implemented MSE and PSNR calculations and dicsussed why this
would be of benefit in evaluation. Plan to finish evaluation for following week. Expect first draft in 2 weeks, after this
will go through diss from start. 

##  Meeting 16 - 16th March 2021

* Meeting Duration: 13:31-13:38

### Discussion

Visual inspection of recovered and original payloads in evaluation section is prone to bias as it is performed by me. Istead
use something like "diff" command on linux to check difference between two images. For "improved, same, worse" section, 
get external participation to evaluate visual degradation. (give them images and ask them to say if it has payload or not)

## Meeting 17 - 23rd March 2021

* Meeting Duration: 13:30-13:49

### Discussion

Have performed evaluation with external participants and the procedure used. Recieved feedback on dissertation.

Fundamental concepts - Computers don't all represent images in the same way. Describe image as array of values. Be clearer about what 
bitplanes are. Change example black images in LSB section to  colour. Images don't have complexity measure, blocks do.

JPEG - Use subsub headings. 

RLE - RLE is lossless compression. Can discuss other examples like GIF. 

Analysis - Change to functional and non functional requirements.

Design - Move modifications to subheading under BPCS tool. Consider figure size. More detail needed about detection cases design.

Implementation - Increase gantt chart size. Test driven development diagram is irrelevant. Too many code blocks. Reduce number to only have interesting sections. Maintanability section is redundant.

Next week will recieve feedback on evaluation and conclusion. 

## Meeting 18 - 30th March 2021

* Meeting Duration: 13:33-13:42

### Discussion

Will have one final meeting before dissertation submission. Showed sphinx documentation.

Evaluation - Good test bank image set. More discussion needed on strategy used by participants in visual detection evaluation. Mention vessel.bmp (old image) and
prtiicpants confusing wear and tear for signs of embedding. JPEG results are good. Conclusion fine.

Will send revised dissertation with all required changes in advance of next meeting.








