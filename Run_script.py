# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 20:12:20 2017

@author: zhenwei.shi
"""


import DCM_ImgRT_Reader
import RadiomicsFeatureWithParams
import Pyradiomics_output
import os

def Run(Img_path,RT_path,Output_path,ROI):
    if os.path.isfile('Params.yaml'):
        paramsFile = 'Params.yaml'
    else:
        print 'Error: pyradiomics params setting file is needed!'
    
    
    target = DCM_ImgRT_Reader.ROI_match(ROI,RT_path)
    print target
    
        
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
