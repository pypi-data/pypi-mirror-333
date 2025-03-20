from setuptools import setup, find_packages


with open("README.md", "r") as readme:
    description = readme.read()

setup(
    name="pypdftospeech",
    version="1.0",
    packages=find_packages(),
    install_requires=[
        "pypdf==5.3.1",
        "pyttsx3==2.98"
    ],
    license="MIT",
    author="Pudis Stanmuang",
    author_email="pudis.2550@gmail.com",
    long_description=description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Ensure this matches the actual license
        "Operating System :: OS Independent",
    ],
    url="https://github.com/pudisss/pdf-to-speech",
)