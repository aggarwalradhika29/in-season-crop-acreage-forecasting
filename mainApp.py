# code to automate the processes and maintain the GUI
# import required libraries : Python 3.11.0
# PyQt5 for GUI
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from PyQt5 import uic, QtWidgets ,QtCore
import sys, subprocess, pickle
import pandas as pd
from json import load
import shutil, rasterio
from shutil import copy2
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import filedialog
from PyQt5.uic import loadUi
from fiona.crs import to_string
import geopandas as gpd
import os
from datetime import date
from timeit import default_timer as timer
from rasterio.plot import show, show_hist
from osgeo import gdal
import numpy as np
import unzip, preprocess2EOS4, mosaic, subset, formula, layerMask, backscatter, sieve, postClassMask, areaCalculation
script_dir = os.path.dirname( __file__ )
mymodule_dir = os.path.join( script_dir,'GUI' )
sys.path.append( mymodule_dir )
from pathlib import Path
import random_forest, knn, svm, naive_bayes, mlp, dt
from sklearn.metrics import confusion_matrix

# specifying all folder/file paths needed for the system
guiPath = str(os.getcwd()) + r'\GUI\\'
dataPath = str(os.getcwd()) + r'\data\\'
sDataPath = str(os.getcwd()) + r'\data\SeNtinel-1A\\'
rDataPath = str(os.getcwd()) + r'\data\EOS-4\\'
shpPath = str(os.getcwd()) + r'\data\shapeFiles\\'
dwnldSentinel = str(os.getcwd()) + r'\data\SeNtinel-1A\downloadData\\'
dwnldEOS4 = str(os.getcwd()) + r'\data\EOS-4\downloadData\\'
classifyPath = str(os.getcwd()) + r'\data\\\commonData\classifiedData'
models = str(os.getcwd()) + r'\data\\\commonData\mlModels'
Path(dataPath).mkdir(parents=True, exist_ok=True)
Path(sDataPath).mkdir(parents=True, exist_ok=True)
Path(rDataPath).mkdir(parents=True, exist_ok=True)
Path(shpPath).mkdir(parents=True, exist_ok=True)
Path(dwnldSentinel).mkdir(parents=True, exist_ok=True)
Path(dwnldEOS4).mkdir(parents=True, exist_ok=True)
Path(classifyPath).mkdir(parents=True, exist_ok=True)
Path(models).mkdir(parents=True, exist_ok=True)
polrz= ''

# class to display the error pop-up whenever any error is encountered
class error_window(QMainWindow): #error window class
    def __init__(self): #constructor
        super(error_window, self).__init__()        
        uic.loadUi(guiPath + "error.ui", self)
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Error")
        self.ExitError = self.findChild(QPushButton, "ExitButtonError") #exit button
        self.ExitError.clicked.connect(self.exit)
        self.back = self.findChild(QPushButton,"BackbuttonError")  
        self.errortype = self.findChild(QLabel, 'Error_type')     
        self.back.clicked.connect(self.Backbut) #back button
        self.show() #show the window

    def exit(self): #exit button
        sys.exit()  # exit the application
    def Backbut(self):  #back button
        # self.back.clicked.connect(UI().setPolarization)
        # self.close()    # close the window
        self.hide()
        return True

Ui_HomeWindow, QMainWindow = uic.loadUiType(guiPath + "FrontPage.ui")       # loads the welcome screen, the first screen that appears to the user

# class to display the welcome screen and its gui
class home_screen(QMainWindow, Ui_HomeWindow):
    def __init__(self):

        super(home_screen, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Crop Classification and Mapping Tool")  
        # defining the buttons for the home screen and their methods
        self.Start= self.findChild(QPushButton, 'startButton')
        self.Start.clicked.connect(self.start_button)


    def start_button(self):             # connection to start button of welcome screen
        start= UI()
        widget.addWidget(start)
        widget.setCurrentIndex(widget.currentIndex() + 1)
        widget.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        widget.setWindowTitle("Crop Classification and Mapping Tool")
        self.close()

# class to display the main window of the system, i.e. the screen where user interacts with the systems to give inputs and set parameters
class UI(QMainWindow):
    def __init__(self):
        super(UI, self).__init__()
        __all__ = ["UI"]
        self.setFixedWidth(1920)
        self.setFixedHeight(1200)
        uic.loadUi(guiPath + "MainWindow.ui", self)                 # loading the main window gui file
        # reading all objects from gui file
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Crop Classification and Mapping Tool")

        self.aoiBrowse= self.findChild(QPushButton, 'aoiButton')
        self.aoiBrowse.setToolTip('Enter .shp file of the AOI.')
        self.aoiText= self.findChild(QLabel, 'text_aoi')
        
        self.gtBrowse= self.findChild(QPushButton, 'gtButton')
        self.gtText= self.findChild(QLabel, 'text_gt')

        self.cropBrowse= self.findChild(QPushButton, 'cropShpButton')
        self.cropText= self.findChild(QLabel, 'text_cropshp')
    
        self.combo_data_img= self.findChild(QComboBox, 'data_img')
        self.combo_dataType= self.findChild(QComboBox, 'dataType')
        self.combo_dataAvail= self.findChild(QComboBox, 'dataAvail')

        self.download= self.findChild(QPushButton, 'downloadButton')
        self.satDataBrowse= self.findChild(QPushButton, 'sat_data')
        self.dataText= self.findChild(QLabel, 'text_data')

        self.og_raster= self.findChild(QPushButton,'og_rasterButton')
        self.ogText = self.findChild(QLabel, 'text_og')

        self.clip_raster= self.findChild(QPushButton,'clip_rasterButton')
        self.gt_raster= self.findChild(QPushButton,'gt_rasterButton')


        self.combo_pol= self.findChild(QComboBox, 'pol_type')

        self.combo_pps= self.findChild(QComboBox, 'pps')
        self.combo_inter_out= self.findChild(QComboBox, 'inter_out')
        self.combo_train= self.findChild(QComboBox, 'trainModel')

        self.run= self.findChild(QPushButton, 'runButton')
        self.help= self.findChild(QPushButton, 'helpButton')

        self.progress= self.findChild(QLabel, 'progress_text')

        self.utmZone = self.findChild(QTextEdit, 'text_utm')

        self.refresh = self.findChild(QPushButton, 'refreshButton')
        ref = str(os.getcwd()) + '\photos\\refresh.jpg'
        self.refresh.setIcon(QIcon(ref))

        # connections with the functions
        self.refresh.clicked.connect(self.setPolarization)
        self.aoiBrowse.clicked.connect(self.findAOI)
        self.gtBrowse.clicked.connect(self.findGT)
        self.cropBrowse.clicked.connect(self.findCrop)
        self.download.clicked.connect(self.downloadData)
        self.satDataBrowse.clicked.connect(self.findData)
        self.og_raster.clicked.connect(self.findOgRaster)
        self.run.clicked.connect(self.runTool)
        self.help.clicked.connect(self.helpCentre)

        self.setPolarization()          # to set the polarization

        qr= self.frameGeometry()
        cp= QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()
    
    def helpCentre(self):
        # function connected to the help screen of the system
        self.winHelp = helpUI()
        self.winHelp.show()

    # function for user to browse the region of interest (.shp file)
    def findAOI(self):
        try:
            root= tk.Tk()
            root.withdraw()
            src= filedialog.askopenfilenames(initialdir='/', title='Select Area of Interest Files', filetypes=(("All Files", "*.*"), ("SHP Files", "*.shp*")))
            target= shpPath + r'AOI\\'
            if os.path.exists(target):
                shutil.rmtree(target)
            Path(target).mkdir(parents=True, exist_ok=True)
            for i in list(src):
                # copy2(i, target)
                if i.endswith('.shp'):
                    gdf= gpd.read_file(i)
                    gdf= gdf.to_crs(epsg= 4326)
                    gdf.to_file(target + 'district_projected.shp')

            gdf2 = gpd.read_file(str(os.getcwd()) + r'\data\shapeFiles\AOI\\district_projected.shp')
            fig, ax = plt.subplots(figsize=(8,8))
            gdf2.plot(ax=ax, edgecolor='black', facecolor='darkseagreen')
            # Save the plot as a PNG image using Matplotlib
            a= str(gdf['DISTRICT'][0]) + ', ' + str(gdf['STATE'][0])
            plt.title(a, weight = 'bold')
            figure_size = plt.gcf().get_size_inches()
            factor = 0.9
            plt.gcf().set_size_inches(factor * figure_size)
            plt.savefig(str(os.getcwd()) + r'\data\shapeFiles\AOI\\district.png', bbox_inches = 'tight', dpi= 200)
            if (len(src)!=0): 
                self.aoiText.setText(str("Data Loaded‼"))
                self.progress.setText(str("Area of Interest Loaded."))
                print("Area of Interest Loaded.")

        except:
            self.aoiText.setText(str(""))
            self.gtText.setText(str(""))
            self.cropText.setText(str(""))
            self.dataText.setText(str(""))
            self.ogText.setText(str(""))
            self.w =error_window()
            self.w.errortype.setText("You have not selected area of interest .shp polygon file.")
            self.w.show()
        
        
    # function for the user to browse the ground truth points (.shp file)
    def findGT(self):
        try:
            root= tk.Tk()
            root.withdraw()
            src= filedialog.askopenfilenames(initialdir='/', title='Select Ground Truth Files', filetypes=(("All Files", "*.*"), ("SHP Files", "*.shp*")))
            target= shpPath + r'GT\\'
            if os.path.exists(target):
                shutil.rmtree(target)
            Path(target).mkdir(parents=True, exist_ok=True)
            for i in list(src):
                if i.endswith('.shp'):
                    self.gdata= gpd.read_file(i)
            print(self.gdata.columns)
            for i in list(self.gdata.columns):
                print(self.gdata[i].dtype)
                if(self.gdata[i].dtype == 'object'):
                    self.gdata['name'] = self.gdata[i]
                    self.gdata.drop(i, inplace=True, axis=1)
            self.gdata['name'] = self.gdata['name'].str.lower()
            unicol = self.gdata['name'].unique()
            print(unicol)
            print(len(unicol))
            cnt= self.gdata['name'].value_counts()
            print(cnt)
            self.gdata['names'] = self.gdata['name'].astype('category')
            self.gdata['class_code'] = self.gdata['names'].cat.codes
            self.gdata['class_code'] = self.gdata['class_code'] + 1
            unicat = self.gdata['class_code'].unique()
            print(unicat)
            self.gdata.drop('names', inplace=True, axis=1)
            print(self.gdata.dtypes)
            self.gdata.to_file(target + 'groundTruth.shp')
            if (len(src)!=0):
                self.gtText.setText(str("Data Loaded‼"))
                print("Ground Truth Loaded.")
                self.progress.setText(str("Ground Truth Loaded."))

        except:
            self.aoiText.setText(str(""))
            self.gtText.setText(str(""))
            self.cropText.setText(str(""))
            self.dataText.setText(str(""))
            self.ogText.setText(str(""))
            self.w =error_window()
            self.w.errortype.setText("You have not selected ground truth .shp polygon file.")
            self.w.show()
        
    # function for the user to browse the crop mask of the area of interest (.shp file)
    def findCrop(self):
        
        root= tk.Tk()
        root.withdraw()
        self.cropSrc= filedialog.askopenfilenames(initialdir='/', title='Select Crop Mask Files', filetypes=(("All Files", "*.*"), ("SHP Files", "*.shp*")))
    
        self.ctarget= shpPath + r'cropMask\\'
        if os.path.exists(self.ctarget):
            shutil.rmtree(self.ctarget)
        Path(self.ctarget).mkdir(parents=True, exist_ok=True)
        if(len(self.cropSrc)!=0):
            for i in list(self.cropSrc):
            #     # shutil.copy(i, target + 'cropMasked.tif')
                if i.endswith('.shp'):
                    self.cropText.setText(str("Data Loaded‼"))
                    self.progress.setText(str("Crop Mask Loaded."))
                    print("Crop Mask Loaded.")
        #         gdf= gpd.read_file(i)
        #         gdf= gdf.to_crs(epsg= 4326)
        #         gdf.to_file(self.ctarget + 'cropMask_projected.shp')
        
        else:
            self.aoiText.setText(str(""))
            self.gtText.setText(str(""))
            self.cropText.setText(str(""))
            self.dataText.setText(str(""))
            self.ogText.setText(str(""))
            self.w =error_window()
            self.w.errortype.setText("You have not selected crop mask .shp polygon file.")
            self.w.show()

    # function for the user to browse the satellite data files, if available (.zip files)
    def findData(self):

        if(self.combo_dataAvail.currentText() == 'Yes' and self.combo_data_img.currentText() == 'Raw Data'):
            root=tk.Tk()
            root.withdraw()
            self.satDataSource = filedialog.askopenfilenames(initialdir="/", title="Select Satellite Data files", filetypes=(("Zip Files","*.zip"), ("All Files", "*.*")))
            if(len(self.satDataSource) == 0):
                self.aoiText.setText(str(""))
                self.gtText.setText(str(""))
                self.cropText.setText(str(""))
                self.dataText.setText(str(""))
                self.ogText.setText(str(""))
                self.w =error_window()
                self.w.errortype.setText("You have not selected satellite data .zip files.")
                self.w.show()
            else:
                self.dataText.setText(str("Data Loaded‼"))
                self.progress.setText(str("Satellite Data Loaded."))
                print("Satellite Data Loaded‼")
        
    # function for the user to browse the preprocessed image (.tif file)
    def findOgRaster(self):

        if(self.combo_data_img.currentText() == 'Pre-processed Image' and self.combo_dataAvail.currentText() == 'Yes'):
            root= tk.Tk()
            root.withdraw()
            self.imgSrc= filedialog.askopenfilenames(initialdir='/', title='Select Pre-processed Multi-Band Crop Raster Image Files', filetypes=(("All Files", "*.*"), ("TIF Files", "*.tif*")))
            self.imagePath = str(os.getcwd()) + r'\data\commonData\layerStack\\'
            Path(self.imagePath).mkdir(parents=True, exist_ok=True)

            if(len(self.imgSrc)!=0):
                for i in list(self.imgSrc):
                #     # shutil.copy(i, target + 'cropMasked.tif')
                    if i.endswith('.shp'):
                        self.cropText.setText(str("Data Loaded‼"))
                        self.progress.setText(str("Crop Raster Image Loaded."))
                        print("Crop Raster Image Loaded.")
            #         gdf= gpd.read_file(i)
            #         gdf= gdf.to_crs(epsg= 4326)
            #         gdf.to_file(self.ctarget + 'cropMask_projected.shp')
            
            else:
                self.aoiText.setText(str(""))
                self.gtText.setText(str(""))
                self.cropText.setText(str(""))
                self.dataText.setText(str(""))
                self.ogText.setText(str(""))
                self.w =error_window()
                self.w.errortype.setText("You have not selected crop mask .shp polygon file.")
                self.w.show()

    # function to set polarization according to the satellite chosen
    def setPolarization(self):
        # return str(self.combo_pol.currentText())
        polrz = self.combo_pol.currentText()
        if(self.combo_dataType.currentText() == 'SENTINEL-1A'):
            self.combo_pol.clear()
            list = ['VH', 'VV', 'VV + VH']
            self.combo_pol.addItems(list)

            

        elif(self.combo_dataType.currentText() == 'EOS-4'):
            self.combo_pol.clear()
            list = ['HH', 'HV', 'HH + HV']
            self.combo_pol.addItems(list)


    # function for the user to download data
    def downloadData(self):
        if(self.combo_data_img.currentText() == 'Raw Data' and self.combo_dataType.currentText() == 'SENTINEL-1A' and self.combo_dataAvail.currentText() == 'No, Download'):
            self.win= downloadUI()
            self.win.show()

    # function for the user to run the automation process, the main program starts here
    def runTool(self):
        import warnings
        warnings.filterwarnings('ignore')
        self.progress.setText(str("Process has been started!"))
        start = timer()
        print('Process start time: ', start)
        try:
            utm = self.return_utm()
            print('UTM Zone : ', utm)
            if(self.combo_pol.currentText() == 'HH + HV'):
                with open(str(os.getcwd()) + r'\data\commonData\\'+'polarization.txt', 'w') as f:
                    f.write('HH\nHV')

            elif(self.combo_pol.currentText() == 'VV + VH'):
                with open(str(os.getcwd()) + r'\data\commonData\\'+'polarization.txt', 'w') as f:
                    f.write('VV\nVH')

            else:
                with open(str(os.getcwd()) + r'\data\commonData\\'+'polarization.txt', 'w') as f:
                    f.write(str(self.combo_pol.currentText()))

            print('Polarizations have been set.')
            self.progress.setText(str("Polarizations have been set."))

            for i in list(self.cropSrc):
                # shutil.copy(i, target + 'cropMasked.tif')
                if i.endswith('.shp'):
                    gdf= gpd.read_file(i)
                    gdf= gdf.to_crs(epsg= 4326)
                    gdf.to_file(self.ctarget + 'cropMask_projected.shp')
            print('Crop Mask has been loaded to the system.')

            # for raw data
            if(self.combo_data_img.currentText() == 'Raw Data'):
                # for sentinel-1a
                if(self.combo_dataType.currentText() == 'SENTINEL-1A'):
                    # data available
                    if(self.combo_dataAvail.currentText() == 'Yes'):
                        target= sDataPath + r'downloadData\\'
                        if os.path.exists(target):
                            shutil.rmtree(target)
                        Path(target).mkdir(parents=True, exist_ok=True)
                        for i in list(self.satDataSource):
                            copy2(i, target)
                    # data not available
                    elif(self.combo_dataAvail.currentText() == 'No, Download'):
                        self.progress.setText(str('Satellite Data Loading...'))
                        downloadUI().oribtDataDownload()
                        self.progress.setText(str("Dates have been assigned!"))
                        print("Dates assigned!")

                    self.dataText.setText(str("Data Copied!"))
                    self.progress.setText(str('Satellite Data Loaded!'))
                    print("Satellite Data Loaded!")
                    self.progress.setText(str('Unzipping satellite data files...'))
                    unzip.unzipData(self.combo_dataType.currentText())
                    self.progress.setText(str('Data Unzipped!'))
                    self.progress.setText(str('Opening preprocess.bat'))
                    preprocess_path = str(os.getcwd()) + r'\codes\\preprocess.bat'
                    self.progress.setText(str('Preprocessing has been started!'))
                    self.progress.setText(str('Preprocessing...'))
                    subprocess.call(preprocess_path)
                    # to_preprocess.transfer()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('unzipData')
                    self.progress.setText(str('Preprocessing completed!'))
                    self.progress.setText(str('Mosaicing the preprocessed files...'))
                    mosaic.mosaicTiles()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('toPreprocess')
                    self.progress.setText(str('Mosaic has been implemented!'))
                    self.progress.setText(str('District masking the mosaiced files...'))
                    subset.district_mask()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('mosaic')
                    self.progress.setText(str('District mask applied!'))
                    formula.transform()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('subset')
                    self.progress.setText(str('Layer stacking...'))
                    layerMask.layerStack()
                    self.progress.setText(str('Layers has been stacked!'))
                    self.progress.setText(str('Calculating zonal statistics and backscatter curve...'))
                    backscatter.backscatterCurve(str(self.combo_dataType.currentText()))
                    self.progress.setText(str('Backscatter curve has been created. You can find it in the \\CropClassification_MappingTool\data\shapeFiles\zonal_stats folder.'))
                    self.progress.setText(str('Loading UTM zone..'))
                    
                    self.progress.setText(str('UTM Zone : ' + utm))
                    self.progress.setText(str('Clipping layer stacked data with the crop mask...'))
                    layerMask.cropMask()

                # for risat-1 or eos-4, data should be available
                else:
                    target= rDataPath + r'downloadData\\'
                    if os.path.exists(target):
                        shutil.rmtree(target)
                    Path(target).mkdir(parents=True, exist_ok=True)
                    for i in list(self.satDataSource):
                        copy2(i, target)


                    self.dataText.setText(str("Data Copied!"))
                    self.progress.setText(str('Satellite Data Loaded!'))
                    print("Satellite Data Loaded!")
                    self.progress.setText(str('Unzipping satellite data files...'))
                    unzip.unzipData(self.combo_dataType.currentText())

                    self.progress.setText(str('Data Unzipped!'))
                    self.progress.setText(str('Opening preprocess.bat'))
                    preprocess_path = str(os.getcwd()) + r'\codes\\preprocessEOS4.bat'
                    self.progress.setText(str('Preprocessing has been started!'))
                    self.progress.setText(str('Preprocessing...'))
                    subprocess.call(preprocess_path)
                    preprocess2EOS4.calib()
                    print('Preprocessing done.')
                    # to_preprocess.transfer()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('unzipData')
                    self.progress.setText(str('Preprocessing completed!'))
                    self.progress.setText(str('Mosaicing the preprocessed files...'))
                    mosaic.mosaicTiles()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('toPreprocess')
                    self.progress.setText(str('Mosaic has been implemented!'))
                    self.progress.setText(str('District masking the mosaiced files...'))
                    subset.district_mask()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('mosaic')
                    self.progress.setText(str('Layer stacking...'))
                    layerMask.layerStack()
                    if (self.combo_inter_out.currentText() == 'No'):
                        self.deleteprev('subset')
                    self.progress.setText(str('Layers has been stacked!'))
                    self.progress.setText(str('Calculating zonal statistics and backscatter curve...'))
                    backscatter.backscatterCurve(str(self.combo_dataType.currentText()))
                    self.progress.setText(str('Backscatter curve has been created. You can find it in the \\CropClassification_MappingTool\data\shapeFiles\zonal_stats folder.'))
                    self.progress.setText(str('Loading UTM zone..'))
                    
                    self.progress.setText(str('UTM Zone : ' + utm))
                    self.progress.setText(str('Clipping layer stacked data with the crop mask...'))
                    layerMask.cropMaskEOS4()


                self.progress.setText(str('Data clipped!'))
                self.progress.setText(str('Classification has been started!'))
                self.progress.setText(str('Model selected : ' + self.combo_train.currentText()))
                self.training_model()
                self.progress.setText(str('Classification Done!'))
                self.progress.setText(str('Sieving...'))
                sieve.sieveImage()
                print('Image sieved!')
                self.progress.setText(str('Sieving completed!'))
                if(self.combo_dataType.currentText() == 'SENTINEL-1A'):
                    postClassMask.mask(utm)
                else:
                    postClassMask.maskEOS4()
                self.progress.setText(str('Post Classification District Masking has been done!'))
                self.progress.setText(str(''))
                
            # for preprocessed image classification
            else:
                for i in list(self.imgSrc):
                    # copy2(i, self.imagePath)
                    shutil.copy(i, self.imagePath + 'layerStacked' + str(self.combo_pol.currentText()) + '.tif')
                self.progress.setText(str('Layers has been stacked!'))
                self.progress.setText(str('Calculating zonal statistics and backscatter curve...'))
                if(self.combo_dataType.currentText() == 'SENTINEL-1A'):
                    backscatter.backscatterCurve(str(self.combo_dataType.currentText()))
                self.progress.setText(str('Backscatter curve has been created. You can find it in the \\CropClassification_MappingTool\data\shapeFiles\zonal_stats folder.'))
                self.progress.setText(str('Loading UTM zone..'))
                
                self.progress.setText(str('UTM Zone : ' + utm))
                self.progress.setText(str('Clipping layer stacked data with the crop mask...'))
                if(self.combo_dataType.currentText() == 'SENTINEL-1A'):
                    layerMask.cropMask()
                else:
                    layerMask.cropMaskEOS4()
                self.progress.setText(str('Data clipped!'))
                self.progress.setText(str('Classification has been started!'))

                # image

                self.training_model()

                sieve.sieveImage()
                postClassMask.mask(utm)


            self.progress.setText(str("Image has been classified."))
            print('Starting area calculation...')
            areaCalculation.areaCalc()
            print('Area calculation done!')
            print('Generating classification report...')
            self.generatePDF()
            print('Report generated!')
            print('Moving on to visualize the outputs and results: ')
            self.win = classifiedUI(self.combo_train.currentText())

            end = timer()
            print('Process end time: ', end)
            print('Total time elapsed: ', (end-start))


        
        except Exception as e:
            print(e)
            self.w =error_window()
            self.w.errortype.setText("Error in running file.")
            self.w.show()

    # function to generate automated pdf report of the process
    def generatePDF(self):
        filename = 'codes\\pdf.ipynb'
        with open(filename) as fp:
            nb = load(fp)

        for cell in nb['cells']:
            if cell['cell_type'] == 'code':
                source = ''.join(line for line in cell['source'] if not line.startswith('%'))
                exec(source, globals(), locals())

    # function to return progress
    def return_progress(self, text):
        self.progress.setText(str(text))

    # function to set the utm zone for the projection of the file
    def return_utm(self):
        return str(self.utmZone.toPlainText())

    # function to set the training model to the automation
    def return_model(self):
        return self.combo_train.currentText()

    # function to redirect to the file of the specified ml training model
    def training_model(self):
        myModels= {
            "Random Forest": random_forest,
            "Support Vector Machines": svm,
            "Naive Bayes": naive_bayes,
            "K-Nearest Neighbour": knn,
            "Multi-Layer Perceptron": mlp,
            "Decision Tree": dt
            }
        if(self.combo_train!=""):
            myModels[self.combo_train.currentText()].train()

    def deleteprev(folder):
        path = str(os.getcwd()) + 'data\\commonData\\' + str(folder)
        shutil.rmtree(path)


# to return polarization
def returnPol():
    return str(polrz)

# class to display help screen
class helpUI(QDialog):
    def __init__(self):
        super(helpUI, self).__init__()
        
        uic.loadUi(guiPath + "HelpWindow.ui", self)
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Help Centre")

        self.continueTool= self.findChild(QPushButton, 'continueButton')
        self.continueTool.clicked.connect(self.continueToMain)

        # self.show()
    def continueToMain(self):
        self.hide()
        return True

# class to display the download window for the user to choose start and end date of the data to be processed
class downloadUI(QWidget):
    def __init__(self):
        super(downloadUI, self).__init__()
        
        uic.loadUi(guiPath + "DownloadWindow.ui", self)
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Set-Up Download Dates")

        self.startDate= self.findChild(QCalendarWidget, 'startDateCalendar')
        self.endDate= self.findChild(QCalendarWidget, 'endDateCalendar')
        self.continueTool= self.findChild(QPushButton, 'continueButton')
        self.continueTool.clicked.connect(self.continueToMain)

        self.startDate.clicked[QtCore.QDate].connect(self.selectStartDate)
        self.sdate=self.startDate.selectedDate()
        self.endDate.clicked[QtCore.QDate].connect(self.selectEndDate)
        self.edate=self.endDate.selectedDate()
        # self.show()

    def selectStartDate(self, date):
        global startMonth
        global startDay 
        global startYear
        startMonth= date.month()
        startDay= date.day()
        startYear=date.year()
        print(f'start date is {date}')
        sdate = f'{startYear}-{startMonth}-{startDay}'
        print(f'start date is {date}')

    def selectEndDate(self, date):
        global endMonth
        global endDay
        global endYear
        endMonth= date.month()
        endDay= date.day()
        endYear= date.year()
        print(f'end date is {date}')
        edate= f'{endYear}-{endMonth}-{endDay}'
        print(f'end date is {date}')

    def continueToMain(self):
        self.hide()
        return True

    # main function to download the data files
    def oribtDataDownload(self):
            district_shapefile= ''
            path= str(os.getcwd()) + r'\data\shapeFiles\AOI'
            # startDate, endDate= self.return_dates()
            startDate = f'{startYear}-{startMonth}-{startDay}'
            endDate = f'{endYear}-{endMonth}-{endDay}'
            print(int(startYear))
            print(int(endMonth))
            startDate = str(date(int(startYear), int(startMonth), int(startDay))) + 'T00:00:00.000Z'
            endDate = str(date(int(endYear), int(endMonth), int(endDay))) + 'T23:59:59.000Z'
            print(startDate)
            print(endDate)
            dates= []
            dates.append(startDate)
            dates.append(endDate)
            print(dates)
            file = open('items.txt','w')
            for item in dates:
                file.write(item+"\n")
            file.close() 
            print('Text File saved!')

            filename = 'codes\\download.ipynb'
            with open(filename) as fp:
                nb = load(fp)

            for cell in nb['cells']:
                if cell['cell_type'] == 'code':
                    source = ''.join(line for line in cell['source'] if not line.startswith('%'))
                    exec(source, globals(), locals())

# class to display the gui after classification is done to visualize the results
class classifiedUI(QMainWindow):

    def __init__(self, trainModel):
        self.polar = []
        for line in open((os.getcwd()) + r'\data\commonData\\polarization.txt','r').readlines():
            self.polar.append(line.strip())
        print("Polarization specified: ", self.polar)
        super(classifiedUI, self).__init__()
        uic.loadUi(guiPath + "result_final.ui", self)
        self.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
        # set the title
        self.setWindowTitle("Classified Results")

        self.ppiImgpreviewB= self.findChild(QPushButton,'ppi_prev')
        self.ppiImgdwnldB= self.findChild(QPushButton,'ppi_dwnld')
        self.clImgpreviewB= self.findChild(QPushButton,'ci_prev')
        self.clImgdwnldB= self.findChild(QPushButton,'ci_dwnld')
        self.clReppreviewB= self.findChild(QPushButton,'cr_prev')
        self.clRepdwnldB= self.findChild(QPushButton,'cr_dwnld')
        self.pcprevB= self.findChild(QPushButton,'pc_prev')
        # self.pcdwnldB= self.findChild(QPushButton,'pc_dwnld')
        self.bcprevB= self.findChild(QPushButton,'bar_prev')
        # self.bcdwnldB= self.findChild(QPushButton,'bar_dwnld')
        # self.scprevB= self.findChild(QPushButton,'sc_prev')
        # self.scdwnldB= self.findChild(QPushButton,'sc_dwnld')
        self.vigprevB= self.findChild(QPushButton,'vig_prev')

        self.accButtonB= self.findChild(QPushButton,'accuracyButton')
        self.accuracy= self.findChild(QPlainTextEdit,'text_acc')
        self.cmB= self.findChild(QPushButton, 'cmButton')


        self.ppiImgpreviewB.clicked.connect(self.findppi_prev)
        self.ppiImgdwnldB.clicked.connect(self.findppi_dwnld)
        self.clImgpreviewB.clicked.connect(self.findci_prev)
        self.clImgdwnldB.clicked.connect(self.findci_dwnld)
        self.clReppreviewB.clicked.connect(self.findcr_prev)
        self.clRepdwnldB.clicked.connect(self.findcr_dwnld)
        self.pcprevB.clicked.connect(self.findpc_prev)
        # self.pcdwnldB.clicked.connect(self.findpc_dwnld)
        self.bcprevB.clicked.connect(self.findbc_prev)
        # self.bcdwnldB.clicked.connect(self.findbc_dwnld)
        # self.scprevB.clicked.connect(self.findsc_prev)
        self.vigprevB.clicked.connect(self.findvig_prev)
        # self.scdwnldB.clicked.connect(self.findsc_dwnld)
        self.accButtonB.clicked.connect(self.findAccuracy)
        self.cmB.clicked.connect(self.findcm)
        self.progress= self.findChild(QLabel, 'progress_text')

        self.myModels= {
            "Random Forest": 'rf',
            "Support Vector Machines": 'svm',
            "Naive Bayes": 'nb',
            "K-Nearest Neighbour": 'knn',
            "Multi-Layer Perceptron": 'mlp',
            "Decision Tree": 'dt'
            }
        self.trainModel = trainModel

        qr= self.frameGeometry()
        cp= QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())
        self.show()



    def return_progress(self, text):
        self.progress.setText(str(text))

    # to plot preprocessed image
    def findppi_prev(self):
        for p in self.polar:
            prevPath = str(os.getcwd()) + r'\data\commonData\toClassify\\cropMasked' + str(p) + '.tif'
            dataset = gdal.Open(prevPath)
            band1 = dataset.GetRasterBand(1)
            band2 = dataset.GetRasterBand(2)
            band3 = dataset.GetRasterBand(3)
            b1 = band1.ReadAsArray()
            b2 = band2.ReadAsArray()
            b3 = band3.ReadAsArray()
            img = np.dstack((b1, b2, b3))
            f = plt.figure()
            plt.imshow(img)
            # plt.savefig('Tiff.png')
            print(plt.show())

    # to download preprocessed image
    def findppi_dwnld(self):
        try:
            for p in self.polar:
                prevPath = str(os.getcwd()) + r'\data\commonData\toClassify\\cropMasked' + str(p) + '.tif'
                name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File','/Desktop',"TIF File(*.tif)")
                print(name[0])
                shutil.copy(prevPath, name[0])
                self.return_progress('Pre-processed Image Saved!')

        except:
            print()


    # to plot classified image
    def findci_prev(self):
        for p in self.polar:
            src = rasterio.open(str(os.getcwd()) +r'\data\commonData\classifiedData\\classifiedImage' + str(p) +  '.tif')
            show(src.read(1), transform=src.transform, cmap='inferno')

    # to download classified image
    def findci_dwnld(self):
        try:
            for p in self.polar:
                prevPath = str(os.getcwd()) + r'\data\commonData\classifiedData\\classifiedImage' + str(p) + '.tif'
                name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File','/Desktop',"TIF File(*.tif)")
                print(name[0])
                shutil.copy(prevPath, name[0])
                self.return_progress('Classified Image Image Saved!')
        except:
            print()

    # to open the report document
    def findcr_prev(self):
        for p in self.polar:
            path = str(os.getcwd()) + r'\\report\\' + str(p) + r'\\classificationReport.pdf'
            subprocess.Popen([path], shell=True)


    # to download the report document
    def findcr_dwnld(self):
        try:
            for p in self.polar:
                prevPath = str(os.getcwd()) + r'\\report\\' + str(p) + r'\\classificationReport.pdf'
                name = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File','/Desktop',"PDF File(*.pdf)")
                print(name[0])
                shutil.copy(prevPath, name[0])
                self.return_progress('Classification Report Saved!')
        except:
            print()

    # to plot the pie chart, crop and their areas
    def findpc_prev(self):
        for p in self.polar:
            path = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\cropArea.csv'
            df = pd.read_csv(path)
            t = (0.3,)*len(df['Crops'])
            plt.pie(df['Area (in hectares)'],labels=df['Crops'],autopct='%.2f%%',explode=t,shadow = True,startangle = 180, radius= 1)
            plt.legend(loc="upper right",fontsize=12,bbox_to_anchor=(1.95,1.1))
            print(plt.show())
            

    # to plot the bar chart, crop vs area
    def findbc_prev(self):
        for p in self.polar:
            path = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + r'\\cropArea.csv'
            df = pd.read_csv(path)
            fig = plt.figure(figsize =(10, 7))
            plt.bar(df['Crops'], df['Area (in hectares)'])
            plt.xlabel('Crops',weight = 'bold')
            plt.ylabel('Area (in hectares)',weight = 'bold')
            plt.title('Bar Chart for the Area Calculated for the respective crops', weight = 'bold', fontsize = 12)
            print(plt.show())

    # to plot the variable importance graph, band vs importance in algorithm
    def findvig_prev(self):
        for p in self.polar:
            self.trainFile = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + '\\' + str(self.myModels[str(self.trainModel)]) + '.pkl'
            self.model, self.y_test, self.y_pred = pickle.load(open(self.trainFile, 'rb'))
            importance = self.model.best_estimator_.feature_importances_
            plt.ylabel('Band Number', fontsize= 10)
            plt.xlabel('Backscatter Coefficient (dB)', fontsize= 10)
            titleText = 'Variable Importance Graph'
            plt.title(titleText, weight = 'bold', fontsize = 12)
            plt.barh([x for x in range(len(importance))], importance, color='darksalmon')
            plt.legend()
            plt.show()
            # print(plt.imshow(im))

    # to display the accuracy on screen
    def findAccuracy(self):
        for p in self.polar:
            acc = 0
            for line in open(str(os.getcwd()) + r'\data\commonData\\accuracy' + str(p) + '.txt','r').readlines():
                acc = (line.strip())
            acc = acc[:6]
            acc = float(acc) * 100
            ac = str(acc) + '%'
            self.accuracy.insertPlainText(str(ac))


    # to display the confusion matrix over the crops according to the ml model used
    def findcm(self):
        inputVector = str(os.getcwd()) + r'\data\shapeFiles\GT\\groundTruth.shp'
        gdf= gpd.read_file(inputVector)
        class_names = list(gdf['name'].unique())
        labels= sorted(class_names)
        print(labels)
        for p in self.polar:
            self.trainFile = str(os.getcwd()) + r'\data\commonData\classifiedData\\' + str(p) + '\\' + str(self.myModels[str(self.trainModel)]) + '.pkl'
            self.model, self.y_test, self.y_pred = pickle.load(open(self.trainFile, 'rb'))
            import seaborn as sns
            sns.heatmap(confusion_matrix(self.y_test, self.y_pred), annot=True, fmt = 'd', cmap='Blues', xticklabels=labels, yticklabels=labels)
            plt.show()


# executing the automation
app = QApplication(sys.argv)    #creating an application
welcome = home_screen() #creating an object of the home screen
widget = QtWidgets.QStackedWidget() #creating a stacked widget
widget.addWidget(welcome)   #adding the home screen to the stacked widget
widget.setFixedHeight(1080)  #setting the height of the stacked widget
widget.setFixedWidth(1920)  #setting the width of the stacked widget
widget.setWindowIcon(QIcon(str(os.getcwd()) + '\photos\\gui.png'))
# set the title
widget.setWindowTitle("ANAAJ")

widget.show()   #showing the stacked widget
sys.exit(app.exec_())


