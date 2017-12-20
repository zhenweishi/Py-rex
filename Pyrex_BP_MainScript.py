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
from PyrexBatchProcessing import ParseStructure #, xnat_collection
#import logging
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

#read Params file of Pyradiomics
try:
	paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
except:
	print 'Error: Could not find params file of Pyradiomics!'


#reading Params file of Pyrex
try:
    inputFile = os.path.join(os.getcwd(),'ParamsSettings','PyrexBatchProcessingParams.yaml')
    with open(inputFile,'r') as params:
        p = yaml.load(params)
        
    #read parameters from configuration file.
    #Img_path = p['PATH']['Img_path']  
    #RT_path = p['PATH']['RT_path']
    myWorkingDirectory = p['PATH']['myWorkingDirectory']
    collectionURL = p['collectionURL'][0]
    myProjectID = p['myProjectID'][0]
    exportDir = p['PATH']['exportDir']
#    ROI = p['ROI'][0]
    export_format = p['export_format'][0]
    export_name = p['export_name'][0]
except:
	print 'Error: Could not find params file of Pyrex!'


PatientID = os.listdir(myWorkingDirectory)
#xnat_collection(myWorkingDirectory,collectionURL,myProjectID)
Img_path,RT_path = ParseStructure(myWorkingDirectory) #detect the path of Image and RTstruct

#create a log file
#LOG_FILENAME = 'RIDER.log'
#logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)

#match the input ROI to the ROI in RTstruct
for i in range(0,len(RT_path)):
    mask_vol=DCM_ImgRT_Reader.Read_RTSTRUCT(RT_path[i])
    M=mask_vol[0]
    target = []
    for j in range(0,len(M.StructureSetROISequence)):
        target.append(M.StructureSetROISequence[j].ROIName)
    print target
    
    for k in range(0,len(target)):
       try:
           print i,k
           Image,Mask,Modality,StudyInstanceUID = DCM_ImgRT_Reader.Img_Bimask(Img_path[i],RT_path[i],target[k]) #create image array and binary mask
           featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
           featureVector.update({'patient':PatientID[i],'contour':target[k]}) #add patient ID and contour
           if export_format == 'csv' and i == 0 and k ==0:
               with open(os.path.join(exportDir,export_name),'wb') as mydata:
                   w = csv.DictWriter(mydata,featureVector.keys())
                   w.writeheader()
                   w.writerow(featureVector)
           else:      
               Pyrex_output.RFeature_store(featureVector,exportDir,PatientID[i],target[k],export_format,Modality,StudyInstanceUID,export_name) #store radiomics locally with a specific format   
       except:
   #       logging.debug('Error: Could not find %s' % target[k])
           print 'Error: Could not find', target[k]    