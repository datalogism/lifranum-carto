# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 15:27:38 2021

@author: Celian
"""
import csv
file='C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/base_auteurs_last_enriched.csv'
list_clean_spla_id={}
wikidata_res=[]
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        
        current={header[i]:row[i] for i  in range(len(header))}
        wikidata_res.append(current)
        if(row[5]!=""):
            print(row[5])
            current="http://www.spla.pro/fiche.personne."+row[5]+".html"
            list_clean_spla_id[current]=row[5]
 
import json         
file='C:/Users/Celian/Desktop/lifranum_carto/data/spla_haiti_final.json'

with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
    
for d in data:
    if(d["lien"] in list_clean_spla_id.keys()):
        if("webpage" in d.keys()):
            print(list_clean_spla_id[d["lien"]],";",d["webpage"]["url"])
        
        
        