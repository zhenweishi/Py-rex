## pyradiomics-extension Version 1.0, which is developed based on the latest pyradiomics v1.2.

### Advantages: 
1. pyradiomics-extension is allowed users input original DICOM files and RTstruture;
2. computation of radiomics features on specific ROI in RTstruture;
3. semi-automatic ROI name matching
4. allow users to output radiomics features in different formats (e.g., RDF, csv, xml)

### Usage:

1. install [pyradiomics](https://github.com/Radiomics/pyradiomics)
2. Download pyradiomics-extension in the sub-directory of pyardiomics
3. provide input parameters in "UserInputFile.txt" (see below input) and parameters of pyradiomics in "Params.yaml"
4. execute MainScript.py
5. Results are saved in "Output_path"



Input: four parameters of pyradiomics-extension are in "UserInputFile.txt". Note that, Users must provide the parameters in separate lines (i.e., 1,2,3 and 4).

1. Img_path. Local path of DICOM images
2. RT_path. Local path of RTstruct files
3. Output_path. Local path of output
4. ROI name (e.g., [Gg][Tt][Vv][-][1])
	
Output: the default output of pyradiomics-extension V1.0 is in [Resource Description Framework](https://en.wikipedia.org/wiki/Resource_Description_Framework) (RDF) format.
		

### Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1,2</sup>
 - [Alberto Traverso]<sup>1,2</sup>
 - [Zhen Zhou]<sup>1,2</sup>
 - [Leonard Wee]<sup>1,2</sup>
 - [Andre Dekker]<sup>1,2</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), Maastricht, The Netherlands,
<sup>2</sup>GROW-School for Oncology and Developmental Biology, Maastricht University Medical Center, Maastricht, The Netherlands,

