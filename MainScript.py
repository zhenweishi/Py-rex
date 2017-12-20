"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""
import DCM_ImgRT_Reader
import PyrexWithParams
import Pyrex_output
import os
import yaml
import csv

'''
reading pathes of DICOM file and output via 'Pyrex_Params.ymal' and handling multiple ROI names
    via ROI_match function:
    python MainScript.py 

Read parameter file of Pyrex:

DICOM image
DICOM-RT 
RDF output 
ROI_name
output_format
######################################
'''

# if os.path.isfile('./ParamsSettings/Pyradiomics_Params.yaml'):
    # paramsFile = 'Params.yaml'
# else:
    # print 'Error: pyradiomics params setting file is needed!'

#read Params file of Pyradiomics
try:
	paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
except:
	print 'Error: Could not find params file of Pyradiomics!'

#reading Params file of Pyrex
try:
    inputFile = os.path.join(os.getcwd(),'ParamsSettings','Pyrex_Params.yaml')
    with open(inputFile,'r') as params:
        p = yaml.load(params)
    Img_path = p['PATH']['Img_path']
    RT_path = p['PATH']['RT_path']
    exportDir = p['PATH']['exportDir']
    ROI = p['ROI'][0]
    export_format = p['export_format'][0]
    export_name = p['export_name'][0]
except:
	print 'Error: Could not find params file of Pyrex!'

#match the input ROI to the ROI in RTstruct
target = DCM_ImgRT_Reader.ROI_match(ROI,RT_path)
print target

#PatientID = os.listdir(myWorkingDirectory)
PatientID = [1]
for i in range(len(target)):
    Image,Mask,Modality,StudyInstanceUID = DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[i]) #create image array and binary mask
    featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
    featureVector.update({'patient':PatientID,'contour':target[i]}) #add patient ID and contour
    Pyrex_output.RFeature_store(featureVector,exportDir,PatientID,target[i],export_format,Modality,StudyInstanceUID,export_name) #store radiomics locally with a specific format   