# code to sieve the classified image with a 3x3 window size
# import required libraries : Python 3.11.0
import os, sys, subprocess
def sieveImage():
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)
    for p in polar:
        gm = os.path.join('F:\Python311\Scripts','gdal_sieve.py')
        input = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + '\\classifiedImage.tif'
        output = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + '\\classifiedSievedImage.tif'
        sieve_command = ["python", gm, '-st', '10', '-4', '-nomask', '-of', 'GTiff', input, output]
        subprocess.call(sieve_command,shell=True)


# sieveImage()

