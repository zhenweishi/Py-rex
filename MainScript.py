"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""
import DCM_ImgRT_Reader
import RadiomicsFeatureWithParams
import Pyradiomics_output
import os

'''
Usage: two modes 
(1) reading pathes of DICOM file and output via 'UserInputFile.txt' and handling multiple ROI names
    via ROI_match function:
    python MainScript.py 

Read input file
########### the format of input file:
DICOM image path\n
DICOM-RT path\n
RDF output path\n
ROI_name
######################################
'''

if os.path.isfile('Params.yaml'):
    paramsFile = 'Params.yaml'
else:
    print 'Error: pyradiomics params setting file is needed!'

if os.path.isfile('Userinputfile1.txt'):
    inputFile = 'Userinputfile1.txt'
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
    
for i in range(len(target)):
    print ('Calculating Radiomics Features on %s '% target[i])
    Image,Mask= DCM_ImgRT_Reader.Img_Bimask(Img_path,RT_path,target[i])
    featureVector = RadiomicsFeatureWithParams.CalculationRun(Image,Mask,paramsFile)
    Pyradiomics_output.RDF_OUTPUT(featureVector,Output_path,target[i])