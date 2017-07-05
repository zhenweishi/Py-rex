# pyradiomics-extension Version 1.0
# Author: Zhenwei Shi, Maastro

# pyradiomics-extension is developed based on the latest pyradiomics v1.2.

# advantages: 
	1. pyradiomics-extension is allowed users input original DICOM files and RTstruture;
	2. computation of radiomics features on specific ROI in RTstruture;
	3. semi-automatic ROI name matching
	4. allow users to output radiomics features in different formats (e.g., RDF, csv, xml)


Input: four parameters stored in "UserInputFile.txt". Note that, Users must provide the parameters in separate lines (i.e., 1,2,3 and 4).
	1. Img_path. Local path of DICOM images
	2. RT_path. Local path of RTstruct files
	3. Output_path. Local path of output
	4. ROI name (e.g., [Gg][Tt][Vv][-][1])
	
Output: the default output of current version of pyradiomics-extension is in RDF format, which is based on Radiomics Ontology (RO).
		