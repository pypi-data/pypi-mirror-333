from setuptools import setup, find_packages

setup(
    name="pypdftospeech",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pypdf==5.3.1",
        "pyttsx3==2.98"
    ]
)