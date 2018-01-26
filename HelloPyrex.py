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
import csv

'''
Usage for individual case: python HelloPyrex.py 

Read parameter file of Pyrex:

# - path:
#    - Img_path 
#    - RT_path
#    - exportDir 
# - ROI: specify the Region of Interest (ROI), e.g., GTV
# - myProject: specify the name of dataset on cloud reposity, like 'stwstrategyrdr'
# - export_format: specify the format of output, such as rdf or csv.
# - export_name: specify the name of result file.
######################################
'''

# Reading Params file of Pyradiomics
try:
	paramsFile = os.path.join(os.getcwd(),'ParamsSettings','Pyradiomics_Params.yaml')
except:
	print ('Error: Could not find params file of Pyradiomics!')

# Reading the parameter file of Pyrex
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
	print('Error: Could not find params file of Pyrex!')

# fuzzy match the input ROI to the ROI in RTstruct
try:
    target = PyrexReader.ROI_match(ROI,RT_path)
except:
    print('Error: ROI extraction failed')

PatientID = 'Pyradiomics_patient'

# Calculation starting
try:
    for k in range(0,len(target)):
        Image,Mask = PyrexReader.Img_Bimask(Img_path,RT_path,target[k]) #create image array and binary mask
        featureVector = PyrexWithParams.CalculationRun(Image,Mask,paramsFile) #compute radiomics
        featureVector.update({'Patient':PatientID,'ROI':target[k]}) #add patient ID and contour
        print ('Radiomcis calculation on %s') % target[k]
        if export_format == 'csv' and k==0:
            with open(os.path.join(exportDir,export_name),'wb') as mydata:
                w = csv.DictWriter(mydata,featureVector.keys())
                w.writeheader()
                w.writerow(featureVector)
        else:
            PyrexOutput.RadiomicsStore(featureVector,exportDir,PatientID,target[k],export_format,export_name) #store radiomics locally with a specific format
    print('Calculation done')
except:
    print('Error: Failed')