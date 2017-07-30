## Py-rex (Pyradiomics extension) Version 1.2, which is developed based on the latest pyradiomics v1.2.

This is an open-source python package for extension of [pyradiomics](https://github.com/Radiomics/pyradiomics) on both input and output sides.
With this pacakge we aim to allow users to use origial DICOM file and RTSTRUCT for radiomics calculation. 

### Features
1. Py-rex is allowed users employ original DICOM files and RTstruture;
2. Internal module for creation of ROI binary mask;
3. computation of radiomics features on a specific ROI;
4. semi-automatic approach to handle multiple ROI names;
5. output radiomics features in different formats (e.g., RDF, csv, xml and so on) with related ontologies (e.g., Radiomics Ontology and Radiation Oncology Ontology).

### Usage

1. install [pyradiomics](https://github.com/Radiomics/pyradiomics)
2. Clone/Download Py-rex to the sub-directory of pyardiomics
3. provide input parameters in "UserInputFile.txt" (see below) and configuration file "Params.yaml" of pyradiomics 
4. execute MainScript.py
5. Results are saved in "Output_path"


Input: four parameters of Py-rex are in "UserInputFile.txt". Note that, Users must provide the parameters in separate lines (i.e., 1,2,3 and 4).

1. Img_path. Local path of DICOM images
2. RT_path. Local path of RTstruct files
3. Output_path. Local path of output
4. ROI name (e.g., [Gg][Tt][Vv][-][1])
	
Output: the default output of Py-rex V1.2 is in [Resource Description Framework](https://en.wikipedia.org/wiki/Resource_Description_Framework) (RDF) format.
		
### Example

'''
python MainScript.py
'''


### Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1,2</sup>
 - [Alberto Traverso]<sup>1,2</sup>
 - [Zhen Zhou]<sup>1,2</sup>
 - [Leonard Wee]<sup>1,2</sup>
 - [Andre Dekker]<sup>1,2</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), Maastricht, The Netherlands,
<sup>2</sup>GROW-School for Oncology and Developmental Biology, Maastricht University Medical Center, Maastricht, The Netherlands,

