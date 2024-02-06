# in-season-crop-acreage-forecasting
This repository contains a summary of the research study about the project I completed during my internship at RRSC, ISRO.
###### Mentored by: Scientist/Engineer 'SE' Akash Goyal
###### [A research paper of the study is also under submission.](https://docs.google.com/document/d/1oOewcrIgAmFQGtBUtfjht36DOOgw9990/edit?usp=sharing&ouid=106225230077402086577&rtpof=true&sd=true)
## Introduction
![image](https://github.com/aggarwalradhika29/in-season-crop-acreage-forecasting/assets/91591831/d7a2be5c-7b30-4e62-ae01-b575c296acb4)

The study proposes a GUI-based automation system for in-season multi-class crop classification and crop acreage estimation on SAR data using ML algorithms. The system provides options for two satellites - Sentinel-1A and RISAT-1, enabling users to download, preprocess, and classify the data quickly and efficiently. The preprocessing steps include radiometric calibration, speckle filtering, subset, geometric/terrain correction, mosaic, district masking, crop masking, and layer stacking. A backscatter curve is plotted using the ground truth points to validate the accuracy of the preprocessed image. The classification is performed using six ML algorithms, and hyperparameter tuning is done to optimize the model training parameters. After the classification, the output is sieved, and the area of each crop class is calculated using Python CSVs. The proposed automation system generates a single PDF file as a summarizing document, which includes the classification report, confusion matrix, backscatter curve, and classified image. The calculated multi-crop areas can also be visualized using pie charts, bar charts, etc. The system is highly efficient and accurate, available to be used by any layman, and it can provide valuable insights for stakeholders in the agricultural sector.

###### An abbreviated name for the system has been drafted, i.e. Automated Numerical Analysis for Agricultural Juxtaposition (ANAAJ).


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
        
2.	Software Requirements
      - Python 3.6.0 (for SNAP Python Interface), Python 3.11.0 (for ML models)
      - GDAL - Geospatial Data Abstraction Library
      - SNAP Python Interface
      - ASF-Alaska or Earthdata Python Interface
      - Scikit-Learn Library
      - PyQt5 technology for GUI

## Methodology
The automation flow is:
1.	Data download using ASF-Search
2.	Preprocessing using SNAP-Py
3.	Calibration
4.	Speckle Filter
5.	Subset
6.	Geometric Terrain Correction
7.	Mosaic
8.	Layer Stack
9.	LULC Mask
10.	Classification using scikit-learn
      - Random Forests
      - K-Nearest Neighbors
      - Support Vector Machines
      - Naive Bayes
      - Decision Trees
      - Multi-Layer Perceptron
12.	Area Estimation

## GUI
#### Welcome Screen
<img src="https://github.com/aggarwalradhika29/in-season-crop-acreage-forecasting/assets/91591831/bf08e8a0-9780-4819-ad43-3e35f7e411d6.png" width=50% height=50%>

#### User Inputs
<img src="https://github.com/aggarwalradhika29/in-season-crop-acreage-forecasting/assets/91591831/99162804-d4f5-43b0-b472-1de58f339933.png" width=50% height=50%>

#### Data Download
<img src="https://github.com/aggarwalradhika29/in-season-crop-acreage-forecasting/assets/91591831/202f194e-a3d3-4d6c-9a4f-f15d7d622959.png" width=50% height=50%>

#### End Results
<img src="https://github.com/aggarwalradhika29/in-season-crop-acreage-forecasting/assets/91591831/12a4fb73-8e2b-4a67-a33c-8db20397949c.png" width=50% height=50%>
