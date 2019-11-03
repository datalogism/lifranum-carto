# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 09:20:49 2019

@author: Celian
"""
import json

def normalize_names(rw_name):
    name=rw_name.strip()
    idx=name.find("(")
    if idx>0:
        name=name[0:idx-1]
    idx=name.find("[")
    if idx>0:
        name=name[0:idx-1]
    splitted_names=name.split(",")
    if(len(splitted_names)==2):
        resp=[n.title().strip() for n in splitted_names]
        return resp
    elif(len(splitted_names)==1):
        splitted_names=name.split(" ")
        if(len(splitted_names)<3):
            resp=[n.title().strip() for n in splitted_names]
            return resp
        else:
            first_name_cand=[]
            last_name_cand=[]
            for part in splitted_names:
                if(len(part)==sum(1 for c in part if c.isupper())):
                    last_name_cand.append(part)
                else:
                    first_name_cand.append(part)
            if(len(first_name_cand)>0 and len(last_name_cand)>0):
                resp=[" ".join(first_name_cand).title().strip()," ".join(last_name_cand).title().strip()]
                return resp
    
        
    resp=[n.title().strip() for n in splitted_names]
    return resp
 
#### SPLA FILE

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/spla_haiti3.json'

with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
    
corpus_haiti_spla=[d for d in data if ("country" in d.keys() and d["country"]=="Haiti")]
list_author_spla=list(set([d['nom auteur'] for d in corpus_haiti_spla if d['nom auteur']!=""]))
list_author_spla_norm=["_".join(normalize_names(n)) for n in list_author_spla]
# COTE CORPUS
corpus_haiti_cote=[]
import csv
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Corpus_Haitiv3.csv'
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        current={header[i]:row[i] for i  in range(len(header))}
        corpus_haiti_cote.append(current)
list_author_cote=list(set([d['Auteur'] for d in corpus_haiti_cote if d['Auteur']!=""]))
list_author_cote_norm=["_".join(normalize_names(n)) for n in list_author_cote]
both=set(list_author_cote_norm).intersection(set(list_author_spla_norm))

#### CORPUS RDF 
from rdflib.graph import Graph
file_path='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/LIFRANUM.rdf'
g = Graph()
from urllib import parse

meta_by_domain={}
for subj, pred, obj in g:
    url=parse.urlsplit(subj)
    p=pred.replace("http://purl.org/dc/elements/1.1/","")
    if url.netloc not in meta_by_domain.keys():
        meta_by_domain[url.netloc]={}
    if p not in meta_by_domain[url.netloc].keys():
        meta_by_domain[url.netloc][p]=[]
    if obj not in meta_by_domain[url.netloc][p]:
        meta_by_domain[url.netloc][p].append(str(obj))  
        
list_url_from_rdf=[]
for k in meta_by_domain.keys():
    if('haiti' in k):
        print("haiti link")
        list_url_from_rdf.append(k)
    if("creator" in meta_by_domain[k].keys()):
        if("haiti" in ' '.join(meta_by_domain[k]["creator"])):
            
            print("haiti authors")
            list_url_from_rdf.append(k)
            
        for creator in meta_by_domain[k]["creator"]:
            normalized="_".join(normalize_names(creator))
            if(normalized in list_author_cote_norm or normalized in list_author_spla_norm):
                
                print("cited authors")
                list_url_from_rdf.append(k)            
    if("title" in meta_by_domain[k].keys()):
        if("haiti" in ' '.join(meta_by_domain[k]["title"]).lower()):
            print("haiti title")
            list_url_from_rdf.append(k)
    if("rights" in meta_by_domain[k].keys()):
        if("haiti" in ' '.join(meta_by_domain[k]["rights"]).lower()):
            
            print("haiti rights")
            list_url_from_rdf.append(k)
    if("publisher" in meta_by_domain[k].keys()):
        if("haiti" in ' '.join(meta_by_domain[k]["publisher"]).lower()):
            print("haiti publisher")
            list_url_from_rdf.append(k)
    if("contributor" in meta_by_domain[k].keys()):
        if("haiti" in ' '.join(meta_by_domain[k]["contributor"]).lower()):
            print("haiti contributor")
            list_url_from_rdf.append(k)
            
# /!\ UN SITE SANS CREATEUR
#list_rdf_author=[meta_by_domain[k]["creator"] for k in list_url_from_rdf]

list_rdf_author=list(set([meta_by_domain[k]["creator"] for k in list_url_from_rdf if "creator" in meta_by_domain[k].keys()]))
list_rdf_author_norm=["_".join(normalize_names(aut[0])) for aut in list_rdf_author]                

###### SEARCH DATA BNF VIA AUTHOR LIST

import requests
url = 'https://data.bnf.fr/sparql?'
every_author_norm=list(set(list_rdf_author_norm+list_author_cote_norm+list_author_spla_norm))
bfn_found={}
for auth in every_author_norm:
    splitted=auth.split("_")
    combinaisons=[]
    if(len(splitted)>1):
        for i in range(len(splitted)):
            if i >0:
                first_part=splitted[0:i]
                first_part=' '.join(first_part)
                second_part=splitted[i:len(splitted)]
                second_part=' '.join(second_part)
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
                  FILTER ((?family='"""+first_part+"""' && ?name='"""+second_part+"""') || (?family='"""+second_part+"""' && ?name='"""+first_part+"""'))
                }
                """
                r = requests.get(url, params = {'format': 'json', 'query': query})
                try:
                    data = r.json()
                    vars_found=data["head"]["vars"]
                    res=data["results"]["bindings"]
                    if(len(res)>0):
                        print("FOUND SOMETHING for >"+first_part+"_"+second_part)
                        bfn_found[first_part+"_"+second_part]=data
                        break
                except:
                    print("PB")


file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/bnf_data_for_authors.json'
with open(file, 'w', encoding='utf-8') as f:
    json.dump(bfn_found, f, ensure_ascii=False, indent=4)
    
viaf_found={}
for auth in bfn_found.keys():
    
        res=bfn_found[auth]["results"]["bindings"]
        for r in res:
            if "link" in r.keys():
                if "viaf" in r["link"]["value"]:
                    r=requests.get(r["link"]["value"]+"/")
                    data=r.text
                    viaf_found[auth]=data

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/viaf_data_for_authors.json'
with open(file, 'w', encoding='utf-8') as f:
    json.dump(viaf_found, f, ensure_ascii=False, indent=4)
                    
            
        