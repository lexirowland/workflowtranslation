#-------------------------------------------------------------------------------
# Name:        pipeWorkFlowInput.py
# Purpose:      generates input data for workflow generator (APE) from a given OWL
#               data ontology and a given tool annotation file, by projecting classes to ontology dimensions.
#
# Author:      Schei008
#
# Created:     08-04-2020
# Copyright:   (c) Schei008 2020
# Licence:     MIT
#-------------------------------------------------------------------------------


import cleanWfTaxonomy, toolannotator, projectSemDimensions
import rdflib
import os

CCD= rdflib.Namespace("http://geographicknowledge.de/vocab/CoreConceptData.rdf#")
                      

    
                      

def pipe(tooldescfile = 'rowland_arcgis_tooldescriptions.ttl', ontologyfile = 'CoreConceptData.ttl', targetfolder='../preprocessing_arcgis'): 
#def pipe(tooldescfile = 'ToolDescription.ttl', ontologyfile = 'CoreConceptData.ttl', targetfolder='../test'):  
#def pipe(tooldescfile = '../../ToolRepository/ToolDescription_TransformationAlgebra.ttl', ontologyfile = 'CoreConceptData.ttl', targetfolder='../testwfalgebra'): 
    
    dimnodes=[CCD.CoreConceptQ,CCD.LayerA,CCD.NominalA]   
    
    #1) Generates a taxonomy (_tax) version of the ontology as well as of the given tool hierarchy (using rdfs:subClassOf), by applying reasoning and removing all other statements
    name, ext = os.path.splitext(os.path.basename(tooldescfile)) 
    to = os.path.join(targetfolder,name+"_tax"+ext) # to='rowland_arcgis_tooldescriptions_tax.ttl'
    name, ext = os.path.splitext(os.path.basename(ontologyfile))
    dto = os.path.join(targetfolder,name+"_tax"+ext) # dto = 'coreconceptdata_tax.ttl'
    cleanWfTaxonomy.main(ontologyfile=ontologyfile, tooldesc=tooldescfile, to=to, dto=dto)
    
    #2) Computes a projection of classes to any of a given set of dimensions given by superconcepts in the type taxonomy file
    tax, ext = os.path.splitext(os.path.basename(dto))
    coretax = os.path.join(targetfolder,tax+'_core'+ext) #'CoreConceptData_tax_core.ttl'
    project = projectSemDimensions.main(taxonomy=dto,dimnodes=dimnodes, targetfolder=targetfolder, coretax=coretax)
    #print(project) 
    #Also generates a file 'CoreConceptData_tax_core.ttl' which contains the ontology cleaned from non-core nodes (=not belonging to the core of a dimension)
    
    #3) Generates a single ontology (of tool_tax + type_tax), and generates a new new tool annotation file (json) with the projected classes as input for APE
    final = rdflib.Graph()
    final.parse(os.path.join(targetfolder,coretax), format='turtle')
    final.parse(os.path.join(targetfolder,to), format='turtle')
    final.serialize(destination=os.path.join(targetfolder, 'GISTaxonomy.rdf'), format = "application/rdf+xml")
    #Then generates a JSON version of the tooldescription for the full taxonomy (to be used with GISTaxonomy.rdf)
    # Generates a new json file "ToolDescription.json" in the targetfolder to be used as APE input 
    toolannotator.main(tooldescfile, project, dimnodes, mainprefix=CCD, targetfolder=targetfolder)
   
   
def main():
    pipe()




if __name__ == '__main__':
    main()
