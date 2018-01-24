"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""
import PyrexReader
import PyrexWithParams
import PyrexOutput
import os
import yaml
from PyreXNAT import ParseStructure, xnat_collection
#import logging
import csv
'''
Usage for individual case: python HelloPyrexBatchProcessing.py 

Read parameter file of Pyrex:

# - path:
#    - myWorkingDirectory is the root directory where DICOM files are saved.
#    - exportDir is the directory where results are exported.
# - collectionURL: specify the URL of cloud repository, like 'XNAT'.
# - myProject: specify the name of dataset on cloud reposity, like 'stwstrategyrdr'
# - export_format: specify the format of output, such as rdf or csv.
# - export_name: specify the name of result file.
######################################
'''

#read Params file of Pyradiomics
try:
	paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
except:
	print 'Error: Could not find params file of Pyradiomics!'


#reading Params file of Pyrex
try:
    inputFile = os.path.join(os.getcwd(),'ParamsSettings','Pyrex_BatchProcessingParams.yaml')
    with open(inputFile,'r') as params:
        p = yaml.load(params)
        
    #read parameters from configuration file.
    myWorkingDirectory = p['PATH']['myWorkingDirectory']
    collectionURL = p['collectionURL'][0]
    myProjectID = p['myProjectID'][0]
    exportDir = p['PATH']['exportDir']
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
    mask_vol=PyrexReader.Read_RTSTRUCT(RT_path[i])
    M=mask_vol[0]
    target = []
    for j in range(0,len(M.StructureSetROISequence)):
        target.append(M.StructureSetROISequence[j].ROIName)
    print target
    
    for k in range(0,len(target)):
       try:
           print i,k
           Image,Mask = PyrexReader.Img_Bimask(Img_path[i],RT_path[i],target[k]) #create image array and binary mask
           featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
           featureVector.update({'patient':PatientID[i],'contour':target[k]}) #add patient ID and contour
           if export_format == 'csv' and i == 0 and k ==0:
               with open(os.path.join(exportDir,export_name),'wb') as mydata:
                   w = csv.DictWriter(mydata,featureVector.keys())
                   w.writeheader()
                   w.writerow(featureVector)
           else:      
               PyrexOutput.RadiomicsStore(featureVector,exportDir,PatientID[i],target[k],export_format,export_name) #store radiomics locally with a specific format   
       except:
   #       logging.debug('Error: Could not find %s' % target[k])
           print 'Error: Could not find', target[k]    