<<<<<<< HEAD
It's a pdf to speech package that I'm planning to upload it to the pip package. 

Package used
1. pypdf
2. os
3. time
4. pyttsx3
5. platform
6. psutil



So this python package is object-oriented type so if you want to use the module you have to create a variable that will store the instance of the class.
The instance will take about 3 attributes
1. File name
2. Page Number - The exact page you want to get
3. incwd - True or False. If the pdf that you want to work with is in the current working directory or not. Which for me I recommend that you should move your pdf file into your directory
   because if don't, it will take a longer time that normal because the program will run through all of your files in your computer just to find your file.


When you created your instance. Call the pdf_to_speech() function and then let the magic begins.
=======
# PdfToSpeech package
My package allows you to read pdf and convert those text into speech.
It's a simple project that I decide to create to practice more in Python plus gain experience by creating real world projects.
I'm just a passionate builder who likes building projects. In the future I planned to update more features and to make it more user-friendly.

# Package used
1. [PyPdf][https://pypi.org/project/pypdf/]
2. [Pyttsx3][https://pypi.org/project/pyttsx3/]


# Table of Contents
- [Installation](#installation)
- [Usage](#usage)
- [Features](#features)


## Installation
```bash
pip install pypdftospeech
```


## Usage
```python
from pypdftospeech import PdfToSpeech
pdf = PdfToSpeech(filename="filename.pdf", pageNumber=10, incwd=True)

pdf.pdf_to_speech()
```
>>>>>>> 6013e12 (pypdftospeech 0.2)
