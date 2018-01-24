## Py-rex (Pyradiomics extension) Version 1.3

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
2. Clone/Download Py-rex to the sub-directory of pyardiomics-master
3. Fill in configuration file "./pyradiomics-master/Py-rex/ParamsSettings/Pyrex_Params.yaml"
4. Execute HelloPyrex.py
5. Results are saved in "./RFstore"

		
### Example
We provide a test dataset in `./data`. This dataset has a series of CT/MRI scans of a lung cancer patient and the corresponding RTSTRUCT.

```
python ./HelloPyrex.py
```
### License

Py-rex may not be used for commercial purposes. This package is freely available to browse, download, and use for scientific 
and educational purposes as outlined in the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

### Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1,2</sup>
 - [Leonard Wee]<sup>1,2</sup>
 - [Andre Dekker]<sup>1,2</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), Maastricht, The Netherlands,
<sup>2</sup>GROW-School for Oncology and Developmental Biology, Maastricht University Medical Center, Maastricht, The Netherlands,

