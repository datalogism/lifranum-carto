# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:46:44 2020

@author: Celian
"""

import sys
import json
import re
from os.path import dirname
textFilePath = "C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/script/export_script/"
textFileFolder = dirname( textFilePath ) # = "/home/me/somewhere/textfiles"

sys.path.append(textFileFolder)

from lifranum_lib import *
from lifranum_lib2 import *

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
    
data_ile_en_ile_ok={}
for aut_k in data_ile_en_ile0.keys():
    if ("_".join(normalize_names(aut_k)) in list_authors):
        current= data_ile_en_ile0[aut_k]
        current["name_auth"]=aut_k
        data_ile_en_ile_ok["_".join(normalize_names(aut_k))]=current


    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/viaf_data_for_authors.json'
with open(file, encoding='utf-8') as json_file:
    data_viaf = json.load(json_file)
    
data_viaf2={}
from xml.etree import ElementTree as ET
for auth_id in data_viaf.keys():
    if auth_id in data_viaf.keys():
        current={"viaf_id":None,"nationalities":[],"occupations":[],"countries":[],"gender":None,"birthDate":None,"deathDate":None,"co_authors":[]}
        xml_str=data_viaf[auth_id].replace('\"','"').replace("\n","")
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
                           current_co_auth["name"]=subsubelem.text
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
            auth="_".join(normalize_names(current["Auteur"]))
            id_auth= strip_accents(auth)
            if(id_auth not in data_lifranum.keys()):
                data_lifranum[id_auth]={"name_auth":current["Auteur"],"data":[]}
            data_lifranum[id_auth]["data"].append({"title":current['Titre de la page'],"url":current["URL"]})

from flashtext import KeywordProcessor
pers_processor = KeywordProcessor()
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Pers_entities1.csv'
with open(file, encoding='utf-8') as csvfile:
    header=next(csvfile)
    for row in csvfile:
        auth_name=row.replace("\n","")
        current=auth="_".join(normalize_names(auth_name))      
        id_auth=strip_accents(current)
        pers_processor.add_keyword(auth_name,"<persName ana='"+id_auth+"'>"+auth_name+"</persName>")

loc_processor = KeywordProcessor()
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/Loc_entities1.csv'
with open(file, encoding='utf-8') as csvfile:
    header=next(csvfile)
    for row in csvfile:
        lieu=row.replace("\n","")
        current=auth="_".join(normalize_names(lieu))      
        id_auth=strip_accents(current)
        loc_processor.add_keyword(lieu,"<location ana='"+id_auth+"'>"+lieu+"</location>")


    
for auth in list_authors:
    
    id_auth= strip_accents(auth)
    data_notices={"author_name":None, "file_authors":[{"auth_name":"Inès Burri","org_name":"Université Jean Moulin Lyon 3"},{"auth_name":"Anaïs Chambat","org_name":"ENS Lyon"},{"auth_name":"Célian Ringwald","org_name":"Université Lyon 2"}],
      "bio_data":{},"data_auth":{},"biblio_data":{}}
    dates_auth=None
    deathDate=None
    birthDate=None
    activity=None
    country=None
    id_bnf=None
    lang=None
    name= None
    family_name= None
    id_viaf=None
    id_dbpedia=None
    gender=None
    nationalities=[]
    occupations=[]
    viaf_countries=[]
    coauthors=[]
    if(auth in data_lifranum.keys()):
        if("name_auth" in data_lifranum[id_auth].keys()):
            data_notices["author_name"]=data_lifranum[id_auth]["name_auth"]
        data_notices["biblio_data"]["lifranum_db"]={}
        
        data_notices["biblio_data"]["lifranum_db"]={"content":{"livres":{},"sur_le_web":[]}}
        if("data" in data_lifranum[id_auth].keys()):
            for w in data_lifranum[id_auth]["data"]:
                data_notices["biblio_data"]["lifranum_db"]["content"]["sur_le_web"].append(w)
    if auth in data_viaf2.keys():

        data_notices["data_auth"]["viaf"]={}
        data_notices["data_auth"]["viaf"]["id_viaf"]=data_viaf2[auth]["viaf_id"]
        data_notices["data_auth"]["viaf"]["nationalities"]=data_viaf2[auth]["nationalities"] ######### TO ADD
        data_notices["data_auth"]["viaf"]["occupations"]=data_viaf2[auth]["occupations"] ######### TO PARSE
        data_notices["data_auth"]["viaf"]["viaf_countries"]=data_viaf2[auth]["countries"]
        if("co_authors" in data_notices["data_auth"]["viaf"].keys()):
            data_notices["data_auth"]["viaf"]["co_authors"]=data_notices["data_auth"]["viaf"]["co_authors"]
        if  data_viaf2[auth]["gender"]:
            if "a" in data_viaf2[auth]["gender"]:
                data_notices["data_auth"]["viaf"]["gender"]="f"
            if "b" in data_viaf2[auth]["gender"]:
                data_notices["data_auth"]["viaf"]["gender"]="m"
        
        data_notices["data_auth"]["viaf"]["birth_date"]=data_viaf2[auth]["birthDate"]
        data_notices["data_auth"]["viaf"]["death_date"]=data_viaf2[auth]["deathDate"]
        if(len(data_viaf2[auth]["co_authors"])>0):
            for c in data_viaf2[auth]["co_authors"]:
                temp=re.sub('\W+','', c["name"])
                id_auth_temp=strip_accents("_".join(normalize_names(temp)))
                c["id_lifranum"]=id_auth_temp
            data_notices["data_auth"]["viaf"]["coauthors"]=data_viaf2[auth]["co_authors"] ######### TO ADD
    if auth in data_bnf.keys():
        res_bnf=data_bnf[auth]["results"]["bindings"]
        data_notices["data_auth"]["bnf"]={}
        for current_bnf in res_bnf:
            for k in current_bnf.keys():
                if(k=="identity"):
                    data_notices["data_auth"]["bnf"]["id_bnf"]=current_bnf[k]["value"]
                if(k=="country"):
                    data_notices["data_auth"]["bnf"]["country"]=current_bnf[k]["value"]
                if(k=="lang"):
                    data_notices["data_auth"]["bnf"]["lang"]=current_bnf[k]["value"]
                if(k=="name"):
                    data_notices["data_auth"]["bnf"]["name"]=current_bnf[k]["value"]
                if(k=="gender" and gender is None):
                    data_notices["data_auth"]["bnf"]["gender"]=current_bnf[k]["value"]
                if(k=="family"):
                    data_notices["data_auth"]["bnf"]["family_name"]=current_bnf[k]["value"]
                if(k=="link" and "viaf" in current_bnf[k]["value"] and id_viaf is None):
                    data_notices["data_auth"]["bnf"]["id_viaf"]=current_bnf[k]["value"]
                if(k=="link" and "dbpedia" in current_bnf[k]["value"]):
                   data_notices["data_auth"]["bnf"]["id_dbpedia"]=current_bnf[k]["value"]
                    
                
    if(auth in data_ile_en_ile_ok.keys()):
        
        data_notices["data_auth"]["ile_en_ile_auto"]={}
        data_notices["bio_data"]["ile_en_ile"]={}
        data_notices["author_name"]=data_ile_en_ile_ok[auth]["name_auth"]
        
       
        
        data_notices["biblio_data"]["ile_en_ile"]={}
        data_notices["biblio_data"]["ile_en_ile"]["ref"]=data_ile_en_ile_ok[auth]["url"]
        data_notices["biblio_data"]["ile_en_ile"]["content"]={}
        data_notices["bio_data"]["ile_en_ile"]["ref"]=data_ile_en_ile_ok[auth]["url"]
        bio_content=[]
        writer_bio=''
        for component in data_ile_en_ile_ok[auth]["bio"]:
            if(component[0:2]=="– "):
                writer_bio=component[2:]
            else:
                bio_content.append(component)
        
            dates_auth=GetAuthorsDates(' '.join(bio_content))
            if(dates_auth):
                if(dates_auth["birth_date"]):
                    data_notices["data_auth"]["ile_en_ile_auto"]["birthDate"]=dates_auth["birth_date"]
                if(dates_auth["death_date"]):
                    data_notices["data_auth"]["ile_en_ile_auto"]["death_date"]=dates_auth["death_date"]
        
        data_notices["biblio_data"]["ile_en_ile"]["content"]={"livres":{},"sur_le_web":[]}
        for component in data_ile_en_ile_ok[auth]["productions"]:
            
            if(component!="Retour"):
                for current_content in data_ile_en_ile_ok[auth]["productions"][component]:

                        if("link" in current_content.keys()):
                            data_notices["biblio_data"]["ile_en_ile"]["content"]["sur_le_web"].append({"title":current_content["link"]["text"],"url":current_content["link"]["url"]})
                        
                        if("text" in current_content.keys()):
                            if component not in data_notices["biblio_data"]["ile_en_ile"]["content"]["livres"].keys():
                                data_notices["biblio_data"]["ile_en_ile"]["content"]["livres"][component]=[]
                            data_notices["biblio_data"]["ile_en_ile"]["content"]["livres"][component].append(current_content["text"])
        annoteted_bio=[]
        for content in bio_content:
            content0=pers_processor.replace_keywords(content)
            content1=loc_processor.replace_keywords(content0)
            annoteted_bio.append(content1)
             
           
        data_notices["bio_data"]["ile_en_ile"]["bio_content"]=annoteted_bio
        data_notices["bio_data"]["ile_en_ile"]["hand"]=writer_bio
        
    if(auth in data_spla_ok.keys()):
        
        data_notices["data_auth"]["spla_auto"]={}
        data_notices["data_auth"]["spla"]={}
        data_notices["bio_data"]["spla"]={}
        
        
        if(data_notices["author_name"] is None and "nom auteur" in data_spla_ok[auth].keys()):
            data_notices["author_name"]=data_spla_ok[auth]["nom auteur"]
        if("desc" in data_spla_ok[auth].keys()):
            if("content" in data_spla_ok[auth]["desc"].keys()):
                
                data_notices["bio_data"]["spla"]["ref"]=data_spla_ok[auth]["lien"]

                bio_content=data_spla_ok[auth]["desc"]["content"].encode('latin-1').decode("utf-8")
                if(len(bio_content)>0):
                    annotated0=pers_processor.replace_keywords(bio_content)
                    annotated1=loc_processor.replace_keywords(annotated0)
                    
                    data_notices["bio_data"]["spla"]["bio_content"]=[annotated1]
                    
                    dates_auth=GetAuthorsDates(' '.join(bio_content))
                    if(dates_auth):
                        if(dates_auth["birth_date"]):
                            data_notices["data_auth"]["spla_auto"]["birthDate"]=dates_auth["birth_date"]
                        if(dates_auth["death_date"]):
                            data_notices["data_auth"]["spla_auto"]["death_date"]=dates_auth["death_date"]
                    
                activity=data_spla_ok[auth]["activiés"] ######### TO PARSE
                if(activity):
                    
                    data_notices["data_auth"]["spla"]["activity"]=activity
                if "webpage" in data_spla_ok[auth].keys():
                    
        
                    data_notices["biblio_data"]["spla"]={}
                    data_notices["biblio_data"]["spla"]["ref"]=data_spla_ok[auth]["lien"]
                    data_notices["biblio_data"]["spla"]["content"]={"sur_le_web":[]}
                    data_notices["biblio_data"]["spla"]["content"]["sur_le_web"].append({"title":data_spla_ok[auth]["webpage"]["title"],"url":data_spla_ok[auth]["webpage"]["url"]})
                if "country" in data_spla_ok[auth].keys():
                    data_notices["data_auth"]["spla"]["country"]=data_spla_ok[auth]["country"]
                    
                if("lang" in data_spla_ok[auth]["desc"].keys()):
                    
                    data_notices["data_auth"]["spla"]["lang"]=data_spla_ok[auth]["desc"]["lang"]
                    
    print("-------------------------")
#    try:
    if(len(data_notices["biblio_data"].keys())>0 or len(data_notices["bio_data"].keys())>0 or len(data_notices["data_auth"].keys())>0 ):
        result=get_CompleteNotice(data_notices)
        str_res=prettify(result)
        myfile = open("C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/tei corpus2/notice_"+id_auth+".xml", "w")
        myfile.write(str_res)
        myfile.close()
#    except:
#        print("PB DURING SAVING Notice")


            