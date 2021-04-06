# Improved Steganography Algorithm - L4 Project 

Repository for Level 4 Invididual Project, containing code, timelog, dissertation and related documentation. The Project supervisor was Dr Ron Poet.

## Project Proposal 
Stegonography is a way of hiding in plain sight. A secret payload is embedded in a cover object, typically an image, without making any visible changes. The standard algorithm is the Bit Plane Complexity Segment algorithm. Steganography can be detected by digital analysis of the image, and there are techniques to try and prevent digital artefacts from being present. This project will evaluate several techniques for improving the BPCS algorithm. It will also investigate ways of using lossy image compression algorithms such as jpeg with steganography.

## Getting Started  

These instructions will get a copy of the project running on your local machine for development, testing and evaluation purposes.

### Prerequisites

Python Version: 3.85 or greater

Pip Version: 20.0.2 or greater

Opeating System - Windows 10 or Linux Ubuntu

## Installation

Clone repository to a directory of your choice. The command for this is as follows:

`git clone https://github.com/AyCarlito/improved-steganography-project`

When in the root directory, the required libraries can be installed using the command:

`pip install -r requirements.txt`

This is all that is needed for development, testing and usage.

## Documentation
Source code documentation, generated using sphinx can be created through the following command:

```
cd docs
make html
```

The resulting documentation is available to view by opening the `docs/build/html/index.html` file. 

* Timelog - `timelog.md`
* Meetings - `meetings.md`
* Plan - `plan.md`
* Status Report - `status_report/status_report_template.tex`


## Dissertation

The project dissertation can be built with pdflatex. Alternatively, a prebuilt pdf file is available to view in the `dissertation/` directory. 

## Usage

For usage of the developed system refer to the `manual.md` file in the `src/` directory. If performing evaluation, the data used during evaluation is present in the `data/` directory. This directory includes a `readme.md` file to provide an overview of what data is present. 

