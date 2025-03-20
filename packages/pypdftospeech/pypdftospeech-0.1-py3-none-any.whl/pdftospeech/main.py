from pypdf import PdfReader
import pyttsx3
import os
import time
import platform
import psutil

class PdfToSpeech:
    def __init__(self, filename, pageNumber, incwd):
        self.filename = filename
        self.pageNumber = pageNumber
        self.filepath = ""
        self.incwd = incwd
        

  
        
    def __find_file(self, OSD, ):

        walk = None

        if self.incwd:
            walk = os.walk(os.getcwd())
        else:
            if OSD["OS"] == "Darwin":
                walk = os.walk("/Users")
            elif OSD["OS"] == "Linux":
                walk = os.walk("/home")
            else:
                drives = [drive.device for drive in psutil.disk_partitions()]
                walk = os.walk(drives[0])


        
        # Go through file path
        fileSep = OSD["fileType"]
        for (dirpath, dirnames, filenames) in walk:
          
            if (self.filename in filenames):
                self.filepath = dirpath + f"{fileSep}{[file for file in filenames if file == self.filename][0]}"
                
                return True
            
        return False
        
    
    def __read_files(self):
        find_file = self.__find_file(self.__check_os())

        if find_file:
            reader = PdfReader(self.filepath)
            page = reader.pages[self.pageNumber]

            text = page.extract_text()
            return text
        else:
            raise FileNotFoundError(f"There is no file name {self.filename} in your computer") if not self.incwd else FileNotFoundError(f"There is no file name {self.filename} in this directory")
        
        
    def __toSpeech(self, texts, tillend=True):
        engine = pyttsx3.init()
        engine.say(texts)
        engine.setProperty('rate', 300)
        engine.setProperty("volume", 0.3)
        engine.runAndWait()
        if not tillend:
            time.sleep(10)
            engine.stop()
        

    
    # Check what OS the user is using and return information for functions to operate
    def __check_os(self):
        OS = platform.system()
        if OS == "Darwin": # Macos
            return {
                "fileType": "/",
                "OS": "Darwin"
            }
        elif OS == "Linux": # Linux
            return {
                "fileType": "/",
                "OS": "Linux"
            }
        else: # Windows
            return {
                "fileType": "\\",
                "OS": "Windows"
            }

             
    # Main function which the user will interact the most
    def pdf_to_speech(self):
        self.__find_file(OSD=self.__check_os())
        textFromPdf = self.__read_files()

        self.__toSpeech(textFromPdf)

        

            


    
   