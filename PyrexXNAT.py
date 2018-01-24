# -*- coding: utf-8 -*-
"""
Created on Sat Oct 14 16:55:42 2017

@author: zhenwei.shi
"""

#batch computing radiomics of datasets (RIDER and Multi-delineation)



#this needs the xnat package installed i.e.
#pip install xnat
import xnat
import os
import dicom
import zipfile

#myProjectID = 'stwstrategyrdr' #for RIDER

#myProjectID = 'stwstrategymmd' #for multi-delineation

# Download data from XNAT in .zip format
def xnat_collection(myWorkingDirectory,collectionURL,myProjectID):
    os.chdir(myWorkingDirectory)
    #connections to public collections do not require passwords
    with xnat.connect(collectionURL) as mySession:
        myProject= mySession.projects[myProjectID]
        mySubjectsList = myProject.subjects.values()
        for s in mySubjectsList:
            mySubjectID = s.label
            print('\nEntering subject ...' + mySubjectID)
            mySubject = myProject.subjects[mySubjectID]
            myExperimentsList = mySubject.experiments.values()
            for e in myExperimentsList:
                myExperimentID = e.label
                #print('\nEntering experiment ...' + myExperimentID)
                myExperiment = mySubject.experiments[myExperimentID]
                #the next line downloads each subject, experiment pair one-by-one into separate zip files
                myExperiment.download(myWorkingDirectory + '\\' + myProjectID + '_' + mySubjectID + '_' + myExperimentID + '.zip')
	# Unzip zip files download from XNAT
	files = os.listdir(os.curdir)
	for zip_name in files:
		zip_ref = zipfile.ZipFile(zip_name,'r')
		zip_ref.extractall()
		zip_ref.close()
	
	#remove all zip file
	dir = os.curdir
	test=os.listdir(dir)

	for item in test:
		if item.endswith(".zip"):
			os.remove(os.path.join(dir, item))

# Parsing dataset directory	
def ParseStructure(myWorkingDirectory):
    img_dirs = []
    rtss_dirs = []
    for root, dirs, files in os.walk(myWorkingDirectory):
        if 'DICOM' in dirs:
            img_dirs.append(os.path.join(root, 'DICOM', 'files'))
        if 'secondary' in dirs:
            rtss_dirs.append(os.path.join(root, 'secondary', 'files'))
    return img_dirs,rtss_dirs

        