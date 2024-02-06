# code to download the date-to-date satellite (SENTINEL-1A) data zip folders according to the specified start and end date of the required data
# import required libraries : Python 3.11.0
import asf_search as asf
import geopandas as gpd
import fiona, os, shutil
from fiona.crs import to_string
from pathlib import Path

print(os.path.abspath(os.curdir))

file1 = open(str(os.getcwd()) + '\\items.txt', 'r')
Lines = file1.readlines()
dates = []
count = 0

for line in Lines:
	count += 1
	print("Line{}: {}".format(count, line.strip()))
	dates.append(line.strip())
print(dates)

path_to_shapefile = str(os.getcwd()) + r'\data\shapeFiles\AOI\district_projected.shp'
# path_to_shapefile = r'\\172.17.102.248\RRSCN_share_folder\testing\sample_inputs\aoi\\Aligrah_Export_Output.shp'
print(path_to_shapefile)

vector_layer= gpd.read_file(path_to_shapefile)

c= fiona.open(path_to_shapefile, crs= 'epsg:4326')

print("Total GT polygon  found in shape file:",len(list(c)) )
print("CRS:",to_string(c.crs))
print("Bounds:",c.bounds)
print("Schema:",c.schema)

xyz= vector_layer.to_crs(epsg= 4326)
print(xyz)

wkt_aoi= str(xyz['geometry'][0])
startDate = dates[0]
print(startDate)
endDate = dates[1]
print(endDate)
findOrbit = asf.geo_search(platform=[asf.PLATFORM.SENTINEL1A], intersectsWith=wkt_aoi,processingLevel='GRD_HD',start=startDate, end= endDate,flightDirection='Descending') ##startDate in gui
# print(findOrbit[-1])
# firstDateFile=findOrbit[-1].geojson()
# print(firstDateFile['properties']['fileName'][49:55])

print('Total files found in the duration: ', len(findOrbit))
orbit = int(findOrbit[-1].geojson()['properties']['fileName'][49:55])
print('Orbit number: ', orbit)

x=(orbit-73)%175  # defining orbit number formula to find orbit of a zip file of a particular date
relativeOrbit=x+1
print('Relative Orbit number: ', relativeOrbit)

results = asf.geo_search(
    platform= asf.PLATFORM.SENTINEL1,
    processingLevel=[asf.PRODUCT_TYPE.GRD_HD],
    start= startDate,
    end = endDate,
    intersectsWith = wkt_aoi,
    flightDirection='Descending',
    relativeOrbit= relativeOrbit
    )
print(f'Total Images Found: {len(results)}')

### Save Metadata to a Dictionary
metadata = results.geojson()
# print(results)

print('List of files to be downloaded: ')
for i in range(len(results)):
    print(results[i].geojson()['properties']['fileName'])
session = asf.ASFSession().auth_with_creds('mayankbhardwaj', 'TOPsecret27')
download_path = str(os.getcwd()) + r'\data\SeNtinel-1A\downloadData'
if os.path.exists(download_path):
    shutil.rmtree(download_path)
Path(download_path).mkdir(parents=True, exist_ok=True)

results.download(
     path = download_path,
     session = session
  )