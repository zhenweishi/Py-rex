import argparse
import json
import os.path
import PyradiomicsWrapper
from shutil import copyfile


def miaWrapper(computationDataJson, paramsFile, outputPath):
    with open(computationDataJson) as computationDataJsonFile:
        computationDataJsonObject = json.load(computationDataJsonFile)

    images = computationDataJsonObject['images']
    images = sortImages(images, ['CT', 'RTSTRUCT'])

    ctImage = images['CT'][0]
    ctImagePath = ctImage['location']
    ctDirectory = os.path.dirname(ctImagePath)

    rtStructPath = images['RTSTRUCT'][0]['location']
    rtStructDirectory = os.path.dirname(rtStructPath)

    volumesOfInterest = computationDataJsonObject['volumesOfInterest']
    roiName = volumesOfInterest[0]['rois'][0]

    PyradiomicsWrapper.performRadiomicsComputation(ctDirectory, rtStructDirectory, roiName, outputPath, paramsFile)

# The best option would be to change the code in such a way that separate folders for each modality are not needed.
# For now, this method restructures the folder hierarchy to accommodate the use of different folders.
def sortImages(images, modalities):
    for modality in modalities:
        modalityImages = images[modality]
        if len(modalityImages) != 0:
            currentImageDirectory = os.path.dirname(modalityImages[0]['location'])
            newImageDirectory = os.path.join(currentImageDirectory, modality)
            if not os.path.isdir(newImageDirectory):
                os.mkdir(newImageDirectory)
            for modalityImage in modalityImages:
                currentImageLocation = modalityImage['location']
                filename = os.path.basename(currentImageLocation)
                newImageLocation = os.path.join(newImageDirectory, filename)
                if not os.path.isfile(newImageLocation):
                    copyfile(currentImageLocation, newImageLocation)
                modalityImage['location'] = newImageLocation
    return images


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='MIA wrapper for pyradiomics computations')
    parser.add_argument('computationDataJson', help='Path of computationData JSON file', type=str)
    parser.add_argument('paramsFile', help='Path of YAML file with config parameters for pyradiomics', type=str)
    parser.add_argument('outputPath', help='Directory for writing output RDF files', type=str)
    args = parser.parse_args()
    miaWrapper(args.computationDataJson, args.paramsFile, args.outputPath)