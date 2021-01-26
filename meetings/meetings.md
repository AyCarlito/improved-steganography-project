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

