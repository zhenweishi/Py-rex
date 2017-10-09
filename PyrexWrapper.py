import DCM_ImgRT_Reader
import PyrexWithParams
import Pyrex_output
import sys


def performRadiomicsComputation(ctPath, rtStructPath, roiName, outputPath, paramsFile,output_format):
    matchingRois = DCM_ImgRT_Reader.ROI_match(roiName, rtStructPath)
    for i in range(0, len(matchingRois)):
        Image, Mask = DCM_ImgRT_Reader.Img_Bimask(ctPath, rtStructPath, matchingRois[i])
        featureVector = PyrexWithParams.CalculationRun(Image, Mask, paramsFile)
        Pyradiomics_output.RFeature_store(featureVector, outputPath, matchingRois[0],output_format)


if __name__ == "__main__":
    ctPath = sys.argv[1]
    rtStructPath = sys.agsv[2]
    roiName = sys.argv[3]
    outputPath = sys.argv[4]
    paramsFile = sys.argv[5]
    performRadiomicsComputation(ctPath, rtStructPath, roiName, outputPath, paramsFile)