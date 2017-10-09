## Py-rex (Pyradiomics extension), which is developed based on the latest [pyradiomics](https://github.com/Radiomics/pyradiomics).

This is an open-source python package for extension of [pyradiomics](https://github.com/Radiomics/pyradiomics) on both input and output sides.
With this pacakge we aim to allow users to use origial DICOM file (CT/PET/MRI) and RTSTRUCT for radiomics calculation. 

### Features
1. Py-rex is allowed original DICOM files and RTstruture;
2. Internal module for the creation of numeric images and ROI binary mask;
3. Computation of radiomics features on a specific ROI;
4. Semi-automatic approach to handle multiple ROI names;
5. Output radiomics features in different formats such as [Resource Description Framework](https://en.wikipedia.org/wiki/Resource_Description_Framework) (RDF) or txt. The radiomics in RDF format are with related ontologies (e.g., [Radiomics Ontology](www.radiomics.org/RO) and [Radiation Oncology Ontology](www.cancerdata.org/roo)).

### Usage

1. Install [pyradiomics](https://github.com/Radiomics/pyradiomics)
2. Clone/Download Py-rex to the main directory of pyardiomics
3. Configure files of Pyradiomics and Py-rex are in `./ParamsSettings`. 
4. Execute `MainScript.py`
5. Results are stored in `./RFstore`.


	
### Example
We provide two test datasets (CT/MRI) in `./data`. The default configure files are in ParamsSettings.

```
python ./MainScript.py
```
### License

Py-rex may not be used for commercial purposes. This package is freely available to browse, download, and use for scientific 
and educational purposes as outlined in the [Creative Commons Attribution 3.0 Unported License](https://creativecommons.org/licenses/by/3.0/).

### Developers
 - [Zhenwei Shi](https://github.com/zhenweishi)<sup>1,2</sup>
 - [Alberto Traverso]<sup>1,2</sup>
 - [Zhen Zhou]<sup>1,2</sup>
 - [Leonard Wee]<sup>1,2</sup>
 - [Andre Dekker]<sup>1,2</sup>
 
<sup>1</sup>Department of Radiation Oncology (MAASTRO Clinic), Maastricht, The Netherlands,
<sup>2</sup>GROW-School for Oncology and Developmental Biology, Maastricht University Medical Center, Maastricht, The Netherlands,

