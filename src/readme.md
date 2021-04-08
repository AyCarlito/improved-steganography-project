# Readme


Source code is present in the `steganography/` directory. There are three main components in the system. Directory `bpcs_tool/` contains the code relating to steganography using the BPCS standard and modified algorithm. Directory `jpeg_tool/` contains the code relating to jpeg compression and jpeg steganography. Directory `detection_tool` contains the code relating to the automated detection tool. 

Test images are located in the `test_images/` directory. Directory `tests/` contains the unit tests for the source code. Directory `payload_comparison_tool/` contains the code for the novel comparison tool - this is intended to compare original and extracted payloads.  


## Build instructions

### Getting Started  

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

### Test steps

First navigate to the required directory using the following command:

`cd steganography/tests`

Tests can be run in one of two ways. First with pytest:

`pytest tests.py`

Secondly, using the coverage library:

`coverage run -m pytest tests.py`

**NB: If using a virtual environment while running the project, the virtual environment files will need to be omitted otherwise they will be included in the coverage report. This can be performed with the follow command:**

`coverage run --omit="*<name_of_virtual_environment*" -m pytest tests.py`

An example of this, while using the virtual environment ".venv":

`coverage run --omit="*.venv*" -m pytest tests.py`


