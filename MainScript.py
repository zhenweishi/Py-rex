# -*- coding: utf-8 -*-
"""
Created on Tue Mar 07 12:37:50 2017

@author: zhenwei.shi
"""
import DCM_ImgRT_Reader
import RadiomicsFeatureWithParams
import Pyradiomics_output
import os
import argparse

'''
Usage: two modes 
(1) reading DICOM path and handling multiple ROI names via MIA:
    python MainScript.py -pyradiomicsyaml Params.yaml -computationdata computationData.json -MIA 1
(2) reading pathes of DICOM file and output via 'UserInputFile.txt' and handling multiple ROI names
    via ROI_match function:
    python MainScript.py -pyradiomicsyaml Params.yaml -userinputfile UserInputFile.txt

Read input file
########### the format of input file:
DICOM image path\n
DICOM-RT path\n
RDF output path\n
ROI_name
######################################
'''

'''
arguments of pyradiomics
pyradiomicsyaml - parameters of pyradiomics
computationdata - json file
'''
#argument_parser = argparse.ArgumentParser(description='Radiomics feature in RDF Format')
#argument_parser.add_argument('-pyradiomicsyaml',help='Params Setting')
##argument_parser.add_argument('path_yaml',help='path of pyradiomics yaml file')
##argument_parser.add_argument('-computationdata', help='Json Config File')
#argument_parser.add_argument('-userinputfile', help='User Input File')
##argument_parser.add_argument('path_Jason', help='path of Jason Config File')
##argument_parser.add_argument('-MIA', help='select using MIA or Not')
#args = argument_parser.parse_args()
if os.path.isfile('Params.yaml'):
    paramsFile = 'Params.yaml'
else:
    print 'Error: pyradiomics params setting file is needed!'

if os.path.isfile('Userinputfile.txt'):
    inputFile = 'Userinputfile.txt'
    lines=[]
    f = open(inputFile,'r')
    for line in f:
        lines.append(line)           	
    Img_path = lines[0].replace("\n","")
    RT_path = lines[1].replace("\n","")
    Output_path = lines[2].replace("\n","")
#    Output_path = './'
    ROI = lines[3].replace("\n","")    
    target = DCM_ImgRT_Reader.ROI_match(ROI,RT_path)
    print target
else:
    print 'Error: User input file is needed!'
    
if len(target)==1:
    print ('Starting Radiomics Features on %s ' % target[0])
    Image,Mask = DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[0])
    featureVector = RadiomicsFeatureWithParams.CalculationRun(Image,Mask,paramsFile)
    Pyradiomics_output.RDF_OUTPUT(featureVector,Output_path,target[0])
    ##-----------------------------------------
            
else:
    for i in range(0,len(target)):
        print ('Calculating Radiomics Features on %s '% target[0])
        Image,Mask,ROI_name= DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[i])
        featureVector = RadiomicsFeatureWithParams.CalculationRun(Image,Mask,paramsFile)
        Pyradiomics_output.RDF_OUTPUT(featureVector,Output_path,target[0])
