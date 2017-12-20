"""
###############################
@author: zhenwei.shi, Maastro##
###############################
"""

from rdflib import Graph, Literal
from rdflib.namespace import RDF,Namespace
from datetime import datetime
import json
import os
import csv

#function to store readiomics in different types of formats, such txt and RDF.
def RFeature_store(featureVector,exportDir,PatientID,ROI_name,export_format,Modality,StudyInstanceUID,export_name):
    if export_format == 'txt':
        json.dump(featureVector,open(exportDir + os.sep +"RF_"+ Modality+'_'+ ROI_name + PatientID+'_'+ datetime.now().strftime('%Y%m%d_%H_%M_%S') +".txt",'w'))
    
    elif export_format == 'csv':
        with open(os.path.join(exportDir,export_name),'ab') as mydata:
            w = csv.DictWriter(mydata,featureVector.keys())
            w.writeheader()
            w.writerow(featureVector)
    elif export_format == 'rdf':
		#print "			RDF Output:"
		print "Converting into RDF format......"
		g = Graph()
		#RO represents radiomics ontology, which can be found on Bioportal
		#add RO to rdflib namespace
		RO = Namespace('http://purl.bioontology.org/ontology/RO/')
		g.bind('RO',RO)
		list_key = featureVector.keys()
		list_value = featureVector.values()
		#a dictionary contains the radiomics feature that has a unit
		dict_unit = {'original_shape_Volume':'mm^3','original_shape_SurfaceArea': 'mm^2','original_shape_Maximum3DDiameter': 'mm'}
		for i in range(len(list_key)):
			tmp_value = Literal(list_value[i])
			tmp_name = Literal(list_key[i])
			
			#calcrun1 = Literal('calcrun1')
			g.add((RO.calcrun1, RO.has_feature,tmp_name))
			g.add((tmp_name,RDF.type,RO.feature))
			g.add((tmp_name, RO.has_value,tmp_value))
		
			if list_key[i] in dict_unit.keys():
				tmp_unit = Literal(dict_unit[list_key[i]])
				g.add((tmp_name,RO.has_unit,tmp_unit))		
		#output = g.serialize(format='n3')
	   #Namespace in Graph
		# for ns in g.namespaces():
			# print ns
		##Create a rdf file for storing output
		g.serialize(exportDir + os.sep +"RF_"+ Modality+'_'+ ROI_name + '_'+ StudyInstanceUID +".ttl", format="nt")
		#g.serialize(exportDir + os.sep +"RF_"+ Modality+'_'+ ROI_name + '_'+ datetime.now().strftime('%Y%m%d_%H_%M_%S') +".ttl", format="n3")
        
      		print "Converting into RDF format......"