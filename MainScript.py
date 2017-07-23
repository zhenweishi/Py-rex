# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 12:37:50 2017

@author: zhenwei.shi
"""
import DCM_ImgRT_Reader
import RadiomicsFeatureWithParams
import Pyradiomics_output
'''

Usage: two modes 
(1) reading DICOM path and handling multiple ROI names via MIA
(2) reading pathes of DICOM file and output via 'UserInputFile.txt' and handling multiple ROI names
    via ROI_match function

'''

'''
Read input file
############ the format of input file:
#DICOM image path\n
#DICOM-RT path\n
#RDF output path\n
#ROI_name
'''
inputFile = 'UserInputFile.txt'
lines=[]
f = open(inputFile,'r')
for line in f:
	lines.append(line)

Img_path = lines[0].replace("\n","")
RT_path = lines[1].replace("\n","")
Output_path = lines[2].replace("\n","")
ROI = lines[3].replace("\n","")
paramsFile ='.\Params.yaml'
#ROIs match
target = DCM_ImgRT_Reader.ROI_match(ROI,RT_path)
#print target


if len(target)==1:
	Image,Mask = DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[0])
	featureVector = RadiomicsFeatureWithParams.CalculationRun(Image,Mask,paramsFile)
	Pyradiomics_output.RDF_OUTPUT(featureVector,Output_path,target[0])
##-----------------------------------------
    
else:
	for i in range(0,len(target)):
		Image,Mask,ROI_name= DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[i])
		featureVector = RadiomicsFeatureWithParams.CalculationRun(Image,Mask,paramsFile)
		Pyradiomics_output.RDF_OUTPUT(featureVector,Output_path,target[0])
