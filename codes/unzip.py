# code to unzip the date-to-date satellite data zip folders
# import required libraries : Python 3.11.0
import os, shutil
import zipfile
from pathlib import Path

# function to unzip data, parameter: type of data (SENTINEL-1A or EOS-4)
def unzipData(dataType):

        i = 1
        dpath = ''
        if dataType == 'SENTINEL-1A':
            dpath = str(os.getcwd()) + r'\data\SeNtinel-1A\downloadData'

        elif dataType == 'EOS-4':
            dpath = str(os.getcwd()) + r'\data\EOS-4\downloadData'
        upath = str(os.getcwd()) + r'\data\commonData\unzipData'
        if os.path.exists(upath):
            shutil.rmtree(upath)
        Path(upath).mkdir(parents=True, exist_ok=True)
        for file in os.listdir(dpath):
            try:
                with zipfile.ZipFile(dpath + '\\'+file, 'r') as zip_ref:
                    zip_ref.extractall(upath)       # extracts all contents from the specified path
                print('File '+str(i)+' unzipped.')
                i=i+1

            except zipfile.BadZipFile:              # exception for empty zip folders or any other error in the folder/file
                print(f"{dpath} + '\\' + {file} is not a valid ZIP archive.")
                continue                            # skip and continue
