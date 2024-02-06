# code to mask the sieved image according to the crop mask of the area of interest provided
# import required libraries : Python 3.11.0
from timeit import default_timer as timer
import os, shutil, fiona, rasterio
from pathlib import Path
from rasterio.crs import CRS
import rasterio.mask
from osgeo import gdal

# function to mask the classified image, parameter: Universal Transverse Mercator (UTM) zone, integer type, for SENTINEL-1A
def mask(utm):
    start= timer()
    print(start)
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    outPath= str(os.getcwd()) + r'\data\commonData\classifiedData\\'
   

    shpin= str(os.getcwd()) + r'\data\shapeFiles\cropMask\\cropMask_projected.shp'
    print(shpin)

    with fiona.open(shpin, 'r') as shapefile:
        shapes= [feature['geometry'] for feature in shapefile]

    for p in polar:
        tifin = outPath  + str(p) + r'\\classifiedImage.tif'

        with rasterio.open(tifin) as src:
            out_image, out_transform= rasterio.mask.mask(src, shapes, crop= True)
            out_meta= src.meta
        utm_crs = CRS.from_epsg(4326)

        out_meta.update(
            {
                "driver" : "GTiff",
                'crs': utm_crs,
                "nodata" : 0,
                "height" : out_image.shape[1],
                "width" : out_image.shape[2],
                "transform" : out_transform,
                
            }
        )

        target= outPath + 'classifiedImage' + str(p) + '.tif'
        with rasterio.open(target, 'w', **out_meta) as dest:
            dest.write(out_image)

        output = outPath + 'classifiedImage' + str(p) + '.tif'
        zone= utm                                     # TIME ZONE TO BE NOTED AND TAKEN BY THE USER
        proj= '+proj=utm +zone=' + zone + ' +datum= WGS84 +units=m +no_defs'
        warp= gdal.Warp(output, target, dstSRS= proj )
        os.remove(target)
        warp= None
    end= timer()
    print(end)
    print('Total time elapsed for crop masking: ',end-start)

# function to mask the classified image, for EOS-4
def maskEOS4():
    start= timer()
    print(start)
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)

    outPath= str(os.getcwd()) + r'\data\commonData\classifiedData\\'
   

    shpin= str(os.getcwd()) + r'\data\shapeFiles\cropMask\\cropMask_projected.shp'
    print(shpin)

    with fiona.open(shpin, 'r') as shapefile:
        shapes= [feature['geometry'] for feature in shapefile]

    for p in polar:
        tifin = outPath  + str(p) + r'\\classifiedSievedImage.tif'


        target= outPath + 'classifiedImage' + str(p) + '.tif'
        gdal.Warp(target, tifin, cutlineDSName = shpin, format="GTiff", cropToCutline = True)
    
    end= timer()
    print(end)
    print('Total time elapsed for crop masking: ',end-start)

# maskEOS4()
# mask('44')