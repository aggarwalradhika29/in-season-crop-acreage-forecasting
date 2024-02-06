# code to calculate and estimate the area for each crop, using the classified image
# import required libraries : Python 3.11.0
import rasterio, os
import geopandas as gpd
from rasterio.features import shapes
from shapely.geometry import shape
import pandas as pd

# function to estimate the crop acreage
def areaCalc():
    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)
    for p in polar:
        # Open the TIF file
        with rasterio.open(str(os.getcwd()) + r'\data\commonData\classifiedData\\classifiedImage' + str(p) + '.tif') as src:
            # Read the TIF file as an array
            print('Image has been read')
            image = src.read(1)
            # Extract the polygon shapes and grid codes
            print('Preparing results..')
            results = (
                {'properties': {'grid_code': v}, 'geometry': s}
                for i, (s, v) in enumerate(shapes(image, mask=None, transform=src.transform))
            )
            # Convert the polygon shapes to a GeoDataFrame
            geoms = list(results)
            gdf = gpd.GeoDataFrame.from_features(geoms)
            # Calculate the shape area
            gdf['area'] = gdf['geometry'].apply(lambda x: shape(x).area)

        outPath = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\classAreaValues.shp'
        # Save the GeoDataFrame as a shapefile
        gdf.to_file(outPath)

        data = gpd.read_file(outPath)
        print(data.head())
        uniqueClass = list(data['grid_code'].unique())
        print(uniqueClass)
        print(data['grid_code'].value_counts())
        uniqueClass.sort()
        areaList = []
        for i in uniqueClass:
            areaList.append((data[data.grid_code == i]['area'].sum())/10000)
        areaList = areaList[1:]
        shp = gpd.read_file(str(os.getcwd()) + r'\data\shapeFiles\GT\\groundTruth.shp')
        class_names = list(shp['name'].unique())
        class_names.sort()

        df = pd.DataFrame(list(zip(class_names, areaList)), columns = ['Crops', 'Area (in hectares)'])
        print(df)
        df.to_csv(str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\cropArea.csv')
# areaCalc()
