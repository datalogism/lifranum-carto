# -*- coding: utf-8 -*-
"""
Created on Sun Jan 19 09:51:41 2020

@author: Celian
"""

# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:46:44 2020

@author: Celian
"""

import sys
import json
import re
import codecs
import os.path
from os import path
from os.path import dirname
textFilePath = "C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/script/export_script/"
textFileFolder = dirname( textFilePath ) # = "/home/me/somewhere/textfiles"

sys.path.append(textFileFolder)

from lifranum_lib2 import *

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/list_authors.json'
with open(file, encoding='utf-8') as json_file:
    list_authors = json.load(json_file)
list_auth_temp=[]
list_auth2=[]
for auth in list_authors:
    list_auth2.append("_".join(normalize_names(strip_accents(auth).replace("-","_"))))
    if(auth.replace("-","_") not in list_auth_temp):
        list_auth_temp.append(auth.replace("-","_"))
        
list_authors=list_auth_temp 
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/spla_haiti_final.json'
with open(file, encoding='utf-8') as json_file:
    data_spla0 = json.load(json_file)
data_spla_ok={}
for d in data_spla0:
    if ("_".join(normalize_names(d['nom auteur'].replace("-","_"))) in list_authors):
        data_spla_ok["_".join(normalize_names(d['nom auteur']))]=d

    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/ile_en_ile.json'
with open(file, encoding='utf-8') as json_file:
    data_ile_en_ile0 = json.load(json_file)
    
data_ile_en_ile_ok={}
for aut_k in data_ile_en_ile0.keys():
    if ("_".join(normalize_names(aut_k)) in list_authors):
        current= data_ile_en_ile0[aut_k]
        current["name_auth"]=aut_k
        data_ile_en_ile_ok["_".join(normalize_names(aut_k.replace("-","_")))]=current


    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/viaf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:
    data_viaf = json.load(json_file)
    
data_viaf2={}
from xml.etree import ElementTree as ET
for auth_id in data_viaf.keys():
    if auth_id in data_viaf.keys():
        current={"viaf_id":None,"nationalities":[],"occupations":[],"countries":[],"gender":None,"birthDate":None,"deathDate":None,"co_authors":[]}
        xml_str=data_viaf[auth_id].replace('\"','"').replace("\n","")
        
        auth_id=auth_id.replace("-","_")
        tree = ET.fromstring(xml_str)
        for elem in tree:
           if "viafID" in elem.tag and elem.text:
               current["viaf_id"]=elem.text
           if "birthDate" in elem.tag and elem.text and elem.text!="0":
               
               current["birthDate"]=elem.text
           if "deathDate" in elem.tag and elem.text and elem.text!="0":
               
               current["deathDate"]=elem.text
           if "coauthors" in elem.tag:
               for subelem in elem:
                   
                   current_co_auth={"name":None,"refs":[]}
                   for subsubelem in subelem:
                       if "text" in subsubelem.tag and subsubelem.text:
                           name_=re.sub("(\d{4}-\d{4})|(\d{4}-.{0,4})","",subsubelem.text)
                           name_=re.sub("(\(|\)|\.|\,)","",name_)
                           
                           current_co_auth["name"]=name_.strip()
                       if "sources" in subsubelem.tag:
                           for source in subsubelem:
                               if("sid" in source.tag and source.text):
                                   
                                   current_co_auth["refs"].append(source.text)
                   if current_co_auth["name"]:
                       current["co_authors"].append(current_co_auth)
                       
           if "fixed" in elem.tag:
               for subelem in elem:
                   if("gender" in subelem.tag and elem.text):
                       current["gender"]=elem.text
           if "nationalityOfEntity"  in elem.tag:
               for subelem in elem:
                   for subsubelem in subelem:
                       if("text" in subsubelem.tag and subsubelem.text):
                           current["nationalities"].append(subsubelem.text)
           if "occupation" in elem.tag:
               for subelem in elem:
                   for subsubelem in subelem:
                       if("text" in subsubelem.tag and subsubelem.text):
                           current["occupations"].append(subsubelem.text)
                     
                      
           if "countries"    in elem.tag:
               for subelem in elem:
                   for subsubelem in subelem:
                       if("text" in subsubelem.tag and subsubelem.text):
                           current["countries"].append(subsubelem.text)
               
        data_viaf2[auth_id]=current
          
        
#    

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/bnf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:

    data_bnf = json.load(json_file)


file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/bnf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:

    data_bnf = json.load(json_file)

file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/bnf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:

    data_bnf = json.load(json_file)


file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/bnf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:

    data_bnf = json.load(json_file)

data_lifranum={}
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Corpus_Haitiv3.csv'
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        current={header[i]:row[i] for i  in range(len(header))}
        current["URL"]=current["URL"][0:len(current["URL"])-1]
        
        if(current["Auteur"]!=""):
            auth="_".join(normalize_names(current["Auteur"].replace("-","_")))
            id_auth= strip_accents(auth)
            if(id_auth not in data_lifranum.keys()):
                data_lifranum[id_auth]={"name_auth":current["Auteur"],"data":[]}
            data_lifranum[id_auth]["data"].append({"title":current['Titre de la page'],"url":current["URL"]})

from flashtext import KeywordProcessor
place_list=[]
loc_processor = KeywordProcessor()
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Loc_entities1.csv'
with open(file, encoding='utf-8') as csvfile:
    header=next(csvfile)
    for row in csvfile:
        lieu=row.replace("\n","").replace("-","_")
        current=auth="_".join(normalize_names(lieu))      
        id_auth=strip_accents(current)
        place_list.append(id_auth)
        loc_processor.add_keyword(lieu,"<placeName ana='"+id_auth+"'>"+lieu+"</placeName>")


pers_processor = KeywordProcessor()
pers_processor2 = KeywordProcessor()
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Pers_entities1.csv'
with open(file, encoding='utf-8') as csvfile:
    header=next(csvfile)
    for row in csvfile:
        auth_name=row.replace("\n","").replace("-","_")
        current=auth="_".join(normalize_names(auth_name))      
        id_auth=strip_accents(current)
        if id_auth not in place_list:
            pers_processor2.add_keyword(auth_name)
            pers_processor.add_keyword(auth_name,"<persName ana='"+id_auth+"'>"+auth_name+"</persName>")



list_noeuds={}
link_list={}
for auth in list_authors:
    author_name=None
    id_auth= strip_accents(auth).replace("-","_")
    if auth in data_viaf2.keys():
            if("name" in data_viaf2[auth].keys() and "family_name" in data_viaf2[auth].keys()):
                author_name=data_viaf2[auth]["name"]+" "+data_viaf2[auth]["family_name"]
            else:
                author_name=" ".join(auth.split("_"))
            if(id_auth not in list_noeuds.keys()):    
                list_noeuds[id_auth]= author_name
                
                 
            if(len(data_viaf2[auth]["co_authors"])>0):
                for c in data_viaf2[auth]["co_authors"]:
                    id_auth_temp=strip_accents("_".join(normalize_names(c["name"])))
                    if(id_auth_temp not in list_noeuds.keys()):
                        list_noeuds[id_auth_temp]=c["name"]
                        link_id=id_auth+"_TO_"+id_auth_temp
                        if(link_id not in link_list.keys()):
                            link_list[link_id]="viaf"
                 
         
    if(auth in data_ile_en_ile_ok.keys()):
        
        if(author_name is None):
            author_name=data_ile_en_ile_ok[auth]["name_auth"]
            
            if(id_auth not in list_noeuds.keys()):    
                list_noeuds[id_auth]= author_name
               
            bio_content=[]
            writer_bio=''
            for component in data_ile_en_ile_ok[auth]["bio"]:
                if(component[0:2]=="– "):
                    writer_bio=component[2:]
                else:
                    bio_content.append(component)
            
            annoteted_bio=[]
            for content in bio_content:
                found_pers=[]
                found_pers = pers_processor2.extract_keywords(content)
                if(len(found_pers)>0):
                    for pers in found_pers:
                        id_auth_temp=strip_accents("_".join(normalize_names(pers)))
                        if(id_auth!=id_auth_temp):
                            
                            if(id_auth_temp not in list_noeuds.keys()):    
                                list_noeuds[id_auth_temp]= pers
                                link_id=id_auth+"_TO_"+id_auth_temp
                                if(link_id not in link_list.keys()):
                                    link_list[link_id]="ile_en_ile_auto"
                            

            
        if(auth in data_spla_ok.keys()):
            
            
            if(author_name is None and "nom auteur" in data_spla_ok[auth].keys()):
                author_name=data_spla_ok[auth]["nom auteur"]
            if("desc" in data_spla_ok[auth].keys()):
                if("content" in data_spla_ok[auth]["desc"].keys()):
    
                    bio_content=data_spla_ok[auth]["desc"]["content"].encode('latin-1').decode("utf-8")
                    if(len(bio_content)>0):
                        found_pers=[]
                        found_pers = pers_processor2.extract_keywords(bio_content)
                        if(len(found_pers)>0):
                             for pers in found_pers:
                                id_auth_temp=strip_accents("_".join(normalize_names(pers)))
                                if(id_auth!=id_auth_temp):
                                    
                                    if(id_auth_temp not in list_noeuds.keys()):    
                                        list_noeuds[id_auth_temp]= pers
                                        link_id=id_auth+"_TO_"+id_auth_temp
                                        if(link_id not in link_list.keys()):
                                            link_list[link_id]="spla_auto"

import csv
with open('C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/data_network_pers_noeuds.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    spamwriter.writerow(["id","label"])
    for k in list_noeuds.keys():    
        spamwriter.writerow([k,list_noeuds[k]])
        
with open('C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/data_network_pers_links.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    spamwriter.writerow(["Source","Target","Type","Id"])
    for k in link_list.keys(): 
        noeuds=k.split("_TO_")
        spamwriter.writerow([noeuds[0],noeuds[1],link_list[k],k])
        
     
                       
