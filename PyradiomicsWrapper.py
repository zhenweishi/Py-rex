import DCM_ImgRT_Reader
import RadiomicsFeatureWithParams
import Pyradiomics_output


def performRadiomicsComputation(ctPath, rtStructPath, roiName, outputPath, paramsFile):
    matchingRois = DCM_ImgRT_Reader.ROI_match(roiName, rtStructPath)
    for i in range(0, len(matchingRois)):
        Image, Mask = DCM_ImgRT_Reader.Img_Bimask(ctPath, rtStructPath, matchingRois[i])
        featureVector = RadiomicsFeatureWithParams.CalculationRun(Image, Mask, paramsFile)
        Pyradiomics_output.RDF_OUTPUT(featureVector, outputPath, matchingRois[0])


if __name__ == "__main__":
    ctPath = sys.argv[1]
    rtStructPath = sys.agsv[2]
    roiName = sys.argv[3]
    outputPath = sys.argv[4]
    paramsFile = sys.argv[5]
    performRadiomicsComputation(ctPath, rtStructPath, roiName, outputPath, paramsFile)
