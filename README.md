## Py-rex (Pyradiomics extension) Version 1.3

This is an open-source python package for [pyradiomics](https://github.com/Radiomics/pyradiomics) extension on both input and output sides.
With this pacakge we aim to allow users to use origial DICOM file and RTSTRUCT for radiomics calculation. 

### Features
1. Py-rex is allowed users employ original DICOM files and RTstruture;
2. Internal module for creation of ROI binary mask;
3. Computation of radiomic features on a specific ROI;
4. Semi-automatic approach to handle multiple ROI names;
5. Radiomic features output in different formats (e.g., rdf, text and csv) with related ontologies (e.g., [Radiomics Ontology](https://bioportal.bioontology.org/ontologies/ROO) and [Radiation Oncology Ontology](https://bioportal.bioontology.org/ontologies/RO));
6. Applicable for CT and MRI;
7. Allow batch processing.

### Using Py-rex

1. Install [pyradiomics](https://github.com/Radiomics/pyradiomics)
2. Clone/Download Py-rex to the sub-directory of pyardiomics-master
3. Execute: `python -m pip install -r pyrex_requirements.txt`
4. Fill in configuration file "./pyradiomics-master/Py-rex-master/ParamsSettings/Pyrex_Params.yaml"
5. Execute `HelloPyrex.py`
6. Results in "./RFstore"

		
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
 - [Alberto Traverso]<sup>1,2</sup>
 - [Leonard Wee]<sup>1,2</sup>
 - [Andre Dekker]<sup>1,2</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), Maastricht, The Netherlands,
<sup>2</sup>GROW-School for Oncology and Developmental Biology, Maastricht University Medical Center, Maastricht, The Netherlands,

