# -*- coding: utf-8 -*-
"""
Created on Tue Oct 29 23:39:02 2019

@author: Celian
"""

import requests

url = 'https://data.bnf.fr/sparql?'
nom="Théard"
prenom="Marie-Alice"
  
#nom="Selmy"
#prenom="Accilien"
query = """
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX owl: <http://www.w3.org/2002/07/owl#>
PREFIX rdagroup2elements: <http://rdvocab.info/ElementsGr2/>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX isni: <http://isni.org/ontology#>
PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
PREFIX dcterms: <http://purl.org/dc/terms/>
PREFIX dc: <http://purl.org/dc/elements/1.1/>
PREFIX bio: <http://vocab.org/bio/0.1/>
SELECT  ?identity   ?type ?genre ?country ?lang ?family ?name ?link
WHERE {
 
  ?concept  foaf:focus ?identity.
  ?identity foaf:familyName ?family.
  ?identity foaf:givenName ?name.
  ?identity  rdf:type ?type.
    ?identity foaf:gender ?genre.
  
  
  
  OPTIONAL{
  
    ?identity owl:sameAs ?link.
  	?identity rdagroup2elements:countryAssociatedWithThePerson  ?country.
  	?identity rdagroup2elements:languageOfThePerson ?lang.
  
  }
  FILTER ((?family='"""+nom+"""' && ?name='"""+prenom+"""') || (?family='"""+prenom+"""' && ?name='"""+nom+"""'))
}
"""
#?isni ?label ?first_bnf ?ref_bfn ?bio_info 
 # ?concept skos:prefLabel ?label.
 
   # ?identity rdagroup2elements:biographicalInformation ?bio_info.
  	#?concept isni:identifierValid ?isni.
  #  ?concept bnf-onto:FRBNF ?ref_bfn.
    #?concept dcterms:created ?first_bnf.
r = requests.get(url, params = {'format': 'json', 'query': query})
data = r.json()
vars_found=data["head"]["vars"]
res=data["results"]["bindings"]

len(res)