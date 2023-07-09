# in-season-crop-acreage-forecasting
This repository contains a summary of the research study about the project I completed during my internship at RRSC, ISRO.

## Introduction
The study proposes a GUI-based automation system for in-season multi-class crop classification and crop acreage estimation on SAR data using ML algorithms. The system provides options for two satellites - Sentinel-1A and RISAT-1, enabling users to download, preprocess, and classify the data quickly and efficiently. The preprocessing steps include radiometric calibration, speckle filtering, subset, geometric/terrain correction, mosaic, district masking, crop masking, and layer stacking. A backscatter curve is plotted using the ground truth points to validate the accuracy of the preprocessed image. The classification is performed using six ML algorithms, and hyperparameter tuning is done to optimize the model training parameters. After the classification, the output is sieved, and the area of each crop class is calculated using Python CSVs. The proposed automation system generates a single PDF file as a summarizing document, which includes the classification report, confusion matrix, backscatter curve, and classified image. The calculated multi-crop areas can also be visualized using pie charts, bar charts, etc. The system is highly efficient and accurate, available to be used by any layman, and it can provide valuable insights for stakeholders in the agricultural sector.

## Objectives
The major objectives of the study are:
1.	Automation of a set of processes to classify the SAR Sentinel-1A and EOS-4 data:
      - Data Download from earthdata.nasa.gov,
      - Preprocessing using SNAP Python Interface,
      - Feature Engineering (Mosaic, Subset, Layer Mask),
      - Classification using ML algorithms.
2.	A user-friendly GUI for the software.
3.	Optimization of time and space complexity of the processes.
4.	Estimation and forecasting of in-season crop acreage using the classified data.

## Technology Stack
1.	Hardware Requirements
      - A high-end workstation containing GPU.
      - Good Internet Connectivity.
      - High Storage Drives.
        
3.	Software Requirements
      - Python 3.6.0 (for SNAP Python Interface), Python 3.11.0 (for ML models)
      - GDAL - Geospatial Data Abstraction Library
      - SNAP Python Interface
      - ASF-Alaska or Earthdata Python Interface
      - Scikit-Learn Library
      - PyQt5 technology for GUI

## Methodology
The automation flow is:
      > Data download using ASF-Search
      > Preprocessing using SNAP-Py
      > Calibration
      > Speckle Filter
      > Subset
      > Geometric Terrain Correction
      > Mosaic
      > Layer Stack
      > LULC Mask
      > Classification using scikit-learn
      > Area Estimation

