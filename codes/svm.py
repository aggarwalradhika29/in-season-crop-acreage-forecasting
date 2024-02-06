# code to classify the masked image using support vector machines ml algorithm
# import required libraries : Python 3.11.0
import rasterio
import rasterio.mask
import pandas as pd
import numpy as np
# from fiona.crs import to_string
from osgeo import gdal, ogr
import csv, os, shutil
import subprocess, pickle
import geopandas as gpd
import warnings
import dataframe_image as dfi
from PIL import Image
warnings.filterwarnings('ignore')

import pandas as pd
from sklearn.metrics import accuracy_score, classification_report, ConfusionMatrixDisplay
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from pathlib import Path
import warnings
import matplotlib.pyplot as plt
from sklearn.svm import SVC


accuracy = 0
def train():
    import warnings
    warnings.filterwarnings('ignore')
    from timeit import default_timer as timer
    start= timer()
    print('Classification started at : ', start)

    polar = []
    for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
        polar.append(line.strip())
    print("Polarization specified: ", polar)
    for p in polar:
    # required folders
        out= str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + '\\'
        if os.path.exists(out):
                shutil.rmtree(out)
        Path(out).mkdir(parents=True, exist_ok=True)

        inter_out= str(os.getcwd()) + r'\data\commonData\intermediateData\\' + str(p) + '\\'
        if os.path.exists(inter_out):
                shutil.rmtree(inter_out)
        Path(inter_out).mkdir(parents=True, exist_ok=True)


        input_raster_file = str(os.getcwd()) + r'\data\commonData\toClassify\\cropMasked' + str(p) + '.tif'
        input_gtshp= str(os.getcwd()) + r'\data\shapeFiles\GT\\groundTruth.shp'
        gt_field_name = 'ATTRIBUTE=class_code'
        stacked_file = inter_out + 'stacked.tif'
        training_testing_csv_file = inter_out + 'training_testing_data.csv'
        all_data_csv_file = inter_out + 'all_data.csv'
        classifiedImage = out + 'classifiedImage.tif'
        # reading crop masked image
        input_raster = rasterio.open(input_raster_file)
        no_data_values      =input_raster.nodatavals
        input_bands         =input_raster.count
        no_data             =input_raster.nodata
        height              =input_raster.shape[0]
        width               =input_raster.shape[1]
        data_type           =input_raster.dtypes
        bands_name          =[]

        for x in range(input_bands):
            bands_name.append("B"+str(x+1))
        print(bands_name)
        print(data_type)
        print(height)
        print(width)

        if no_data == 0:
            print('data is good')
        else:
            with rasterio.open(input_raster_file, 'r+') as src:
                src.nodata = 0
                profile = src.profile
            
                with rasterio.open(out + 'input_filledZero.tif', 'w', **profile) as dst:
                    for i in range(1, src.count + 1):
                        band = src.read(i)
                        band = np.where(band == 1, 0, band)
                        dst.write(band, i)
            
            input_raster_file = out + 'input_filledZero.tif'
            input_raster = rasterio.open(input_raster_file)
            

        # vector to raster conversion
        inputVector= input_gtshp
        gtRaster= out + 'gtRaster.tif'

        refImage = input_raster_file
        gdalformat = 'GTiff'
        datatype = gdal.GDT_Byte
        burnVal = 8
        image = gdal.Open(refImage, gdal.GA_ReadOnly)

        # open shapefile
        shp= ogr.Open(inputVector)
        shp_layer= shp.GetLayer()

        # rasterization
        print('Rasterizing GT Shapefile....')
        data= gdal.GetDriverByName(gdalformat).Create(gtRaster, image.RasterXSize, image.RasterYSize, 1, datatype, options= ['COMPRESS=DEFLATE'])
        data.SetProjection(image.GetProjectionRef())
        data.SetGeoTransform(image.GetGeoTransform())

        band= data.GetRasterBand(1)
        band.SetNoDataValue(0)
        gdal.RasterizeLayer(data, [1], shp_layer, options= [gt_field_name])

        # close the datasets
        band = None
        data = None
        image = None
        shp = None
        gdf = gpd.read_file(input_gtshp)
        length = int(input_bands)
        print(length)
        num_cat = list(range(1, length + 1))
        final = ' '.join([str(elem) for elem in num_cat])
        print(final)
        subprocess.call("gdaladdo --config COMPRESS_OVERVIEW DEFLATE "+gtRaster+" " + final + " ", shell=True) ####### count number of gt cats
        print("Done.")

        gt_raster= rasterio.open(gtRaster)
        dtype= gt_raster.dtypes
        print(dtype)

        file_list = [input_raster_file, gtRaster]
        bands= input_raster.count
        meta = input_raster.meta
        bands= bands+1

        # Update meta to reflect the number of layers
        meta.update(count = bands)

        i=1
        with rasterio.open(stacked_file, 'w', **meta) as dst:
            print('loop entered')
            while i<bands:
                dst.write_band(i, input_raster.read(i))
                i+=1
            print('loop exited')
            dst.write_band(i, gt_raster.read(1))
            print('stacked file created')

        stacked_raster=rasterio.open(stacked_file)
        bands= stacked_raster.count
        height=stacked_raster.shape[0]
        width=stacked_raster.shape[1]
        dn_data=stacked_raster.read()
        stacked_raster.close()


        f = open(training_testing_csv_file, 'w')
        g = open(all_data_csv_file, 'w')
        # create the csv writer
        writer = csv.writer(f)
        writer2 = csv.writer(g)

        i=1
        bands_name=[]
        while i<bands: 
            bands_name.append("B"+str(i))
            i+=1
        bands_name
        writer2.writerow(bands_name)
        bands_name.append("Output")
        writer.writerow(bands_name)
        print('Creating CSVs...')
        i=0
        j=0
        b=0
        while i<height:
            while j<width:
                data=[]
                b=0
                while b<bands-1: 
                    if np.isnan(dn_data[b][i][j]) == 1 :
                        data.append(0)
                    else:
                        data.append(dn_data[b][i][j])
                    b+=1
                writer2.writerow(data )
                if dn_data[b][i][j] !=0:
                    data.append(dn_data[b][i][j])
                    writer.writerow( data)
                j+=1
            i+=1
            j=0
        f.close()
        g.close()
        print('CSVs created!')


        df=pd.read_csv(training_testing_csv_file)
        rows=df.shape[0]
        colums=df.shape[1]
        print ( rows,colums )
        print(df.head())

        y=df['Output']
        x=df.drop('Output',axis=1)
        print(x.head())

        #test and train split 
        X_train,X_test,y_train, y_test = train_test_split( x,y,test_size=.25,random_state=42323232)

       

        #List Hyperparameters that we want to tune.
        param_grid = {'C': [0.1, 1, 5, 10], 'gamma': [1,0.1,0.01,0.001],'kernel': ['rbf', 'poly', 'sigmoid']}

        svm = GridSearchCV(SVC(), param_grid, refit=True, cv=10)#Fit the model
        svm_ml = svm.fit(X_train, y_train)#Print The value of best Hyperparameters
        
        print (f'Train Accuracy - : {svm_ml.score(X_train,y_train):.3f}')
        print (f'Test Accuracy - : {svm_ml.score(X_test,y_test):.3f}')
        print(svm_ml.best_params_)
        print('Model fitted...')
        y_pred = svm_ml.predict(X_test)
        print("Accuracy:", accuracy_score(y_test, y_pred))
        acc= accuracy_score(y_test, y_pred)

        with open(str(os.getcwd()) + r'\data\commonData\\'+'accuracy' + str(p) + '.txt', 'w') as f:
            f.write(str(acc))
        df = pd.DataFrame()
        df['truth'] = y_test
        df['predict'] = svm_ml.predict(X_test)
        print('Predicting...')
        # Cross-tabulate predictions
        print(pd.crosstab(df['truth'], df['predict'], margins=True))
        print()
        print()

        gdf= gpd.read_file(inputVector)
        class_names = list(gdf['name'].unique())
        class_names= sorted(class_names)
        print(class_names)
        print('Classification Report: ')
        print(classification_report(y_test, y_pred, target_names=class_names))

        report = classification_report(y_test, y_pred,target_names=class_names, output_dict=True)
        df = pd.DataFrame(report).transpose()
        
        dfi.export(df, out + r"\\table.png")
        # Importing Image class from PIL module


        # Opens a image in RGB mode
        im = Image.open(out + r"\\table.png")
        newsize = (950, 600)
        im1 = im.resize(newsize)
        im1.save(out + r'\\crDF.png')
        im1.close()

        df=pd.read_csv(all_data_csv_file)
        print(df.head())
        classified_data=svm_ml.predict(df)
        # print(classified_data)

        bands=input_raster.count
        i=0
        j=0
        m=0
        output_raster_image=input_raster.read(1)

        while i<height:
            while j<width:
                output_raster_image[i][j]=classified_data[m]
                j+=1
                m+=1
            i+=1
            j=0
        # saving the classified image
        print('Writing Image...')
        output_image = rasterio.open(classifiedImage, 'w', 
                                            driver = 'Gtiff',
                                            height = height,
                                            width = width,
                                            count= 1,
                                            crs = input_raster.crs,
                                            transform = input_raster.transform,
                                            dtype = rasterio.int16,
                                            nodata= 0
                                        )

        output_image.write(output_raster_image,1)
        output_image.close()
        print('Image written')



        with open(out + r'\\svm.pkl', 'wb') as file:  # opening the file
            model= (svm_ml, y_test, y_pred)
            pickle.dump(model, file)


        IC = type('IdentityClassifier', (), {"predict": lambda i : i, "_estimator_type": "classifier"})
        cm=ConfusionMatrixDisplay.from_estimator(IC, y_pred, y_test, cmap= 'Greens_r')
        # cm=ConfusionMatrixDisplay.from_estimator(IC, y_pred, y_test , normalize='true', cmap= 'Greens_r', values_format='.2%')
        figure_size = plt.gcf().get_size_inches()
        factor = 0.95
        plt.gcf().set_size_inches(factor * figure_size)
        cm.figure_.savefig(out + r'confusionMatrix.png', bbox_inches = 'tight', dpi= 200 )
        end= timer()
        print(end)
        print('Elapsed time for classification (s) : ', (end-start))
