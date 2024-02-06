# code to transform pixel values of all the tiles in the subset folder
# import required libraries : Python 3.11.0
import rasterio, os
import numpy as np
def transform():
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    for p in polar:
        prevPath= str(os.getcwd()) + r'\data\commonData\subset\\' + str(p) + '\\'
        for i in os.listdir(prevPath):
            filename = prevPath + i
            dataset = rasterio.open(filename)
            profile = dataset.profile
            band = dataset.read(1)
            result = 10 * np.log10(band, where=band>0)                  # main formula, converts values to decibel unit
            
            profile.update(dtype=rasterio.float32, count=1, nodata= 0)
            with rasterio.open(prevPath + str(i[:6]) + '_' + str(i[6:]), 'w', **dataset.profile) as dst:
                dst.write(np.array(result, dtype=rasterio.float32), 1)
            dataset.close()
            os.remove(filename)     
    return

# transform()