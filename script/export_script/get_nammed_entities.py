# -*- coding: utf-8 -*-
"""
Created on Tue Jan  7 21:02:40 2020

@author: Celian
"""

import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from lxml import etree
from xml.dom import minidom
from xml.etree import ElementTree
import json
import unicodedata
import spacy

nlp=spacy.load('fr_core_news_sm')

from spacy_lefff import LefffLemmatizer, POSTagger

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')


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


def getNammedEntities(txt):
    current_doc = nlp(txt)
    tempo_text=txt
    data={"org":[],"per":[],"loc":[]}
    for entity in current_doc.ents:
        if(entity.label_=="ORG"):
            data["org"].append(entity.text)
        if(entity.label_=="PER"):
            data["per"].append(entity.text)
        if(entity.label_=="LOC"):
            data["loc"].append(entity.text)
    return data

def GetGeoloc(place_name):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(place_name)
    return [location.latitude, location.longitude]

    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/list_authors.json'
with open(file, encoding='utf-8') as json_file:
    list_authors = json.load(json_file)
    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/spla_haiti_final.json'
with open(file, encoding='utf-8') as json_file:
    data_spla0 = json.load(json_file)
data_spla_ok={}
for d in data_spla0:
    if ("_".join(normalize_names(d['nom auteur'])) in list_authors):
        data_spla_ok["_".join(normalize_names(d['nom auteur']))]=d

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/ile_en_ile.json'
with open(file, encoding='utf-8') as json_file:
    data_ile_en_ile0 = json.load(json_file)

other_auth_list=[]
for aa in list_authors:
    other_auth_list.append( strip_accents(normalize_names(aa)[0]))

data_ile_en_ile_ok={}
for aut_k in data_ile_en_ile0.keys():
    if ("_".join(normalize_names(aut_k)) in list_authors):
        current= data_ile_en_ile0[aut_k]
        current["name_auth"]=aut_k
        data_ile_en_ile_ok["_".join(normalize_names(aut_k))]=current
bios_content={}

with open('C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/list_nammed_entities.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    spamwriter.writerow(["id_auth","content","type","ana"])
            
    for auth in list_authors:
        print(auth)
        auth_name=None
        bio_content=[]
        
        if(auth in data_ile_en_ile_ok.keys()):
            
            auth_name=data_ile_en_ile_ok[auth]["name_auth"]
            
            writer_bio=''
            for component in data_ile_en_ile_ok[auth]["bio"]:
                bio_content.append(component)
        if(auth in data_spla_ok.keys()):
            if(auth_name and "nom auteur" in data_spla_ok[auth].keys()):
                auth_name=data_spla_ok[auth]["nom auteur"]
            if("desc" in data_spla_ok[auth].keys()):
                if("content" in data_spla_ok[auth]["desc"].keys()):
                    bio_content.append(data_spla_ok[auth]["desc"]["content"].encode('latin-1').decode("utf-8"))
        if(auth_name):
            
            id_auth= strip_accents(normalize_names(auth)[0])
            for txt in bio_content:
                current_doc = nlp(txt)
                tempo_text=txt
                for entity in current_doc.ents:
                    if(entity.label_=="ORG"):
                        spamwriter.writerow([id_auth,entity.text,"ORG",""])
                    if(entity.label_=="PER"):
                        test=strip_accents(normalize_names(entity.text)[0])
                        if(test!=id_auth):
                            if(test in other_auth_list):
                                spamwriter.writerow([id_auth,entity.text,"PER",test])
                            else:
                                spamwriter.writerow([id_auth,entity.text,"PER",""])
                    if(entity.label_=="LOC"):
                        spamwriter.writerow([id_auth,entity.text,"LOC"],"")
                        