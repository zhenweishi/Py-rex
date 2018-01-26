"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""

from rdflib import Graph, Literal
from rdflib.namespace import Namespace,URIRef
#from datetime import datetime
import json
import os
import csv

# Function to store readiomics in different types of formats, such as txt, csv and RDF.
def RadiomicsStore(featureVector,exportDir,PatientID,ROI,export_format,export_name):
    if export_format == 'txt':
        json.dump(featureVector,open(exportDir + os.sep +"RF_"+ '_'+ ROI + PatientID + ".txt",'w'))    
    elif export_format == 'csv':
        with open(os.path.join(exportDir,export_name),'ab') as mydata:
            w = csv.DictWriter(mydata,featureVector.keys())
            w.writeheader()
            w.writerow(featureVector)
            
    elif export_format == 'rdf':
	
        #print "RDF Output:"
        g = Graph() # Create a rdflib graph object
        feature_type = [] # Create a list for feature type
        feature_uri = [] # Create a list for feature uri (ontology)
        # Load the radiomics_ontology mapping table
        pyradiomics_ro = os.path.join(os.getcwd(),'RadiomicsOntology','RadiomicsOntology_Table.csv')
        with open(pyradiomics_ro,'rb') as mydata:
            reader = csv.reader(mydata)
            for row in reader:
                feature_type.append(row[0])
                feature_uri.append(row[1])
            # Adding Radiomics Ontology to namespace
        ro = Namespace('http://www.radiomics.org/RO/')
        
        g.bind('ro',ro)

        CalculationRun = URIRef('http://www.radiomics.org/RO/0101')
        has_radiomics_feature  = URIRef('http://www.radiomics.org/RO/0102')
        has_value = URIRef('http://www.radiomics.org/RO/0103')
        has_unit = URIRef('http://www.radiomics.org/RO/0104')
        #extract feature keys and values from featureVector that is the output of pyradiomcis
        radiomics_key = featureVector.keys()
        radiomics_value = featureVector.values()
        # A dictionary contains the radiomic feature that has a unit
        dict_unit = {'original_shape_Volume':'mm^3','original_shape_SurfaceArea': 'mm^2','original_shape_Maximum3DDiameter': 'mm'}
		
        #
        for i in range(len(radiomics_key)):
            ind = feature_type.index(radiomics_key[i])
            tmp_uri = feature_uri[ind]
            tmp_value = Literal(radiomics_value[i])
            feature_ontology = URIRef(tmp_uri)
            g.add((CalculationRun,has_radiomics_feature,feature_ontology))
            g.add((feature_ontology,has_value,tmp_value))
            # If radiomics have an unit, then add it to the graph.
            if radiomics_key[i] in dict_unit.keys():
                _unit = Literal(dict_unit[radiomics_key[i]])
                dd((feature_ontology,has_unit,tmp_unit))
    
        print(g.serialize(exportDir + os.sep +"RF_"+ '_'+ ROI + PatientID + ".ttl", format='turtle'))