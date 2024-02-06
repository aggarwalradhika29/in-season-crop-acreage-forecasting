# code to preprocess the satellite(SENTINEL-1A) data using SNAP Python Interface
# import required libraries : Python 3.6.0
import snappy
from snappy import ProductIO, HashMap, WKTReader, GPF
import geopandas as gpd
import os, gc, requests, shutil
from pathlib import Path
# from mainApp import returnPol
from timeit import default_timer as timer
start= timer()
print(start)
# http://sisdp_rrscn:SISdp_RRscn@192.168.0.9:8080
# proxy details
proxies = {
    "http": "http://sisdp_rrscn:SISdp_RRscn@192.168.0.9:8080",
    "https": "https://sisdp_rrscn:SISdp_RRscn@192.168.0.9:8080",
}

# Find and download earth gravitational model model 

egm96url = "http://step.esa.int/auxdata/dem/egm96/ww15mgh_b.zip"
response = requests.get(egm96url, proxies=proxies)
home_dir = os.path.expanduser("~")
snap_folder = os.path.join(home_dir, ".snap")

if os.path.exists(snap_folder):
    print(f"The .snap folder is located at: {snap_folder}")
else:
    print("The .snap folder does not exist.")
print(snap_folder)
fileegm = str(snap_folder) + '\\auxdata\dem\egm96\\/ww15mgh_b.zip'
with open(fileegm, "wb") as f:
    f.write(response.content)

print('Earth Gravitational Model Loaded!')
# load SNAP GPF
GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis()
HashMap = snappy.jpy.get_type('java.util.HashMap')
# Now loop through all Sentinel-1 data sub folders that are located within a super folder (of course, make sure, that the data is already unzipped):


path = str(os.getcwd()) + r'\data\commonData\unzipData\\'
polar = []
for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
    polar.append(line.strip())
print("Polarization specified: ", polar)


for pol in polar:
    opath = str(os.getcwd()) + r'\data\commonData\toPreprocess\\' + str(pol) + '\\'
    if os.path.exists(opath):
            shutil.rmtree(opath)
    Path(opath).mkdir(parents=True, exist_ok=True)
    
    for folder in os.listdir(path):
        print(str(folder))
        try:
            gc.enable()
            
            output = path + folder + "/"  
            date = folder.split("_")[4] 
            # date = timestamp[:8]
            # Then, read in the Sentinel-1 data product:

            sentinel_1 = ProductIO.readProduct(output + "\\manifest.safe")    
            print(sentinel_1)
            # If polarization bands are available, split up your code to process VH and VV intensity data separately. The first step is the calibration procedure by transforming the DN values to Sigma Naught respectively. You can specify the parameters to output the Image in Decibels as well.       

            polarization = pol
                
            ### CALIBRATION
            print('Calibration started.')
            parameters = HashMap() 
            parameters.put('outputSigmaBand', True) 
            parameters.put('sourceBands', 'Intensity_' + polarization) 
            parameters.put('selectedPolarisations', polarization) 
            parameters.put('outputImageScaleInDb', True)  

            calib = output + date + "_calibrate_" + polarization 
            target_0 = GPF.createProduct("Calibration", parameters, sentinel_1) 
            


            # SPECKLE FILTERING
            parameters= HashMap()
            parameters.put('filter', 'Lee')
            parameters.put('filterSizeX', 3)
            parameters.put('filterSizeY', 3)
            output1 = GPF.createProduct('Speckle-Filter', parameters, target_0)
            ProductIO.writeProduct(output1, calib, 'BEAM-DIMAP')
        # Next, specify a subset AOI to reduce the data amount and processing time. The AOI specified by its outer polygon corners and is formatted through a Well Known Text (WKT).

            ### SUBSET

            calibration = ProductIO.readProduct(calib + ".dim")    
            print('Calibration done.')
            district_shapefile= ''
            dpath= str(os.getcwd()) + r'\data\shapeFiles\AOI'
            # dpath = r'C:\CropClassification_MappingTool\data\shapeFiles\AOI'
            for file in os.listdir(dpath):
                if file.endswith('_projected.shp'):
                    shape_file= file
                    district_shapefile= dpath + '\\' + shape_file

            print('Subset started.')
            data= gpd.read_file(district_shapefile)
            final_data= data.to_crs(epsg= 4326)
            wkt= str(final_data['geometry'][0])
            geom = WKTReader().read(wkt)

            parameters = HashMap()
            parameters.put('geoRegion', geom)
            parameters.put('outputImageScaleInDb', False)
            parameters.put('subSamplingX', '1')
            parameters.put('subSamplingY', '1')
            parameters.put('fullSwath', 'false')
            parameters.put('tiePointGridNames', '')
            parameters.put('copyMetadata', 'true')
            subset = output + date + "_subset_" + polarization
            target_1 = GPF.createProduct("Subset", parameters, calibration)
            ProductIO.writeProduct(target_1, subset, 'BEAM-DIMAP')
            print('Subset done.')
        # Apply a Range Doppler Terrain Correction to correct for layover and foreshortening effects, by using the SRTM 1 arcsecond product (30m) that is downloaded automatically. You could also specify an own DEM product with a higher spatial resolution from a local path:


            # find and download srtm 1sec hgt for each tile
            subset1= ProductIO.readProduct(subset + '.dim')
            # Get the geocoding object
            geoCoding = subset1.getSceneGeoCoding()

            # Get the size of the product
            width = subset1.getSceneRasterWidth()
            height = subset1.getSceneRasterHeight()

            # Create arrays to store the latitude and longitude values
            lat_array = snappy.jpy.array('float', height*width)
            lon_array = snappy.jpy.array('float', height*width)

            # output1.close()
            
            # Iterate over all pixels in the product and retrieve the latitude and longitude values
            for y in range(height):
                for x in range(width):
                    pos = geoCoding.getGeoPos(snappy.PixelPos(x, y), None)
                    lat_array[y*width+x] = pos.getLat()
                    lon_array[y*width+x] = pos.getLon()

            if len(lat_array) != 0 or len(lon_array) != 0:
            # Print the latitude and longitude values of the first pixel in the product
                lat = int(lat_array[0])
                long= int(lon_array[0])
                print(lat)
                print(long)
                latitude_str = ''
                longitude_str = ''
                if lat>=0:
                    latitude_str = 'N'
                else:
                    latitude_str = 'S'

                if lat>=0:
                    longitude_str = 'E'
                else:
                    longitude_str = 'W'

                longList = [ long, long-1, long+1]
                latList = [lat, lat-1]
                for i in longList:
                    for j in latList:
                        hgtZip = 'http://step.esa.int/auxdata/dem/SRTMGL1/' + str(latitude_str) + str(j) + str(longitude_str) + '0' + str(i) + '.SRTMGL1.hgt.zip'
                        print(hgtZip)
                        filename = snap_folder + '\\auxdata\dem\SRTM 1Sec HGT\\' + hgtZip[-23:]
                        print(filename)
                        print(hgtZip[-23:])

                        srtm = requests.get(hgtZip, proxies=proxies)
                        with open(filename, "wb") as f:
                            f.write(srtm.content)
                print('DEM : SRTM 1Sec HGT Loaded!')    

            ### TERRAIN CORRECTION
            print('Terrain Correction started.')
            
            parameters = HashMap()     
            parameters.put('demResamplingMethod', 'BILINEAR_INTERPOLATION') 
            parameters.put('imgResamplingMethod', 'NEAREST_NEIGHBOUR') 
            parameters.put('demName', 'SRTM 1Sec HGT') 

            parameters.put('pixelSpacingInMeter', 10.0)
            parameters.put("Pixel Spacing (deg)",0.0000898315284119)
            parameters.put("Map Projection","WGS84(DD)") 
            parameters.put('Source Bands', 'Sigma0_' + polarization)
            parameters.put("Mask out areas without elevation",True)
            parameters.put("Selected source band",True)

            terrain = opath + date + "_corrected_" + polarization 
            target_2 = GPF.createProduct("Terrain-Correction", parameters, subset1) 
            ProductIO.writeProduct(target_2, terrain, 'GeoTIFF')
            print('Terrain Correction done')

        except (RuntimeError, IndexError):
            z= path + folder
            print(str(folder) + ' does not consist of any subset according to the AOI.')
            continue
        



end= timer()
print('time elapsed for preprocessing: ', (end-start))
