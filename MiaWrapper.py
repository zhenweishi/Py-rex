import argparse
import json
import os.path

import PyradiomicsWrapper


def miaWrapper(computationDataJson, paramsFile, outputPath):
    
    with open(computationDataJson) as computationDataJsonFile:
        computationDataJsonObject = json.load(computationDataJsonFile)
    
    images = computationDataJsonObject['images']
    
    ctImage = images['CT'][0]
    ctImagePath = ctImage['location']
    ctDirectory = os.path.dirname(ctImagePath)
    
    rtStructPath = images['RTSTRUCT'][0]['location']
    rtStructDirectory = os.path.dirname(rtStructPath)
    
    volumesOfInterest = computationDataJsonObject['volumesOfInterest']
    roiName = volumesOfInterest[0]['rois'][0]
   
    PyradiomicsWrapper.performRadiomicsComputation(ctDirectory, rtStructDirectory, roiName, outputPath, paramsFile)
    
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MIA wrapper for pyradiomics computations')
    parser.add_argument('computationDataJson', help='Path of computationData JSON file', type=str)
    parser.add_argument('paramsFile', help='Path of YAML file with config parameters for pyradiomics', type=str)
    parser.add_argument('outputPath', help='Directory for writing output RDF files', type=str)
    args = parser.parse_args()
    miaWrapper(args.computationDataJson, args.paramsFile, args.outputPath)
