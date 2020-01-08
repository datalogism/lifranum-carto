# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 12:28:17 2020

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

file='C:/Users/Celian/Desktop/lifranum_carto/data/spla_haiti_final.json'

with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
corpus_haiti_spla=[]
for d in data:
    if("country" in d.keys() and d["country"]=="Haiti"):
        corpus_haiti_spla.append(d)
    if("desc" in d.keys() and "content" in d["desc"].keys() and "haiti" in d["desc"]["content"].lower()):
        corpus_haiti_spla.append(d)
list_author_spla=list(set([d['nom auteur'] for d in corpus_haiti_spla if d['nom auteur']!=""]))
list_author_spla_norm=["_".join(normalize_names(n)) for n in list_author_spla]

#### ILE EN ILE FILE

file='C:/Users/Celian/Desktop/lifranum_carto/data/ile_en_ile.json'

with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
corpus_haiti_ile_en_ile=[]
type_prod=[]
for d in data.keys():
    corpus_haiti_ile_en_ile.append(d)
    
    type_prod=type_prod+list(data[d]["productions"].keys())
list_author_ile_en_ile_norm=["_".join(normalize_names(n)) for n in corpus_haiti_ile_en_ile]

# COTE CORPUS
corpus_haiti_cote=[]
import csv
file='C:/Users/Celian/Desktop/lifranum_carto/data/Corpus_Haitiv3.csv'
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        current={header[i]:row[i] for i  in range(len(header))}
        current["URL"]=current["URL"][0:len(current["URL"])-1]
        corpus_haiti_cote.append(current)
list_url_cote=list(set([d['URL'] for d in corpus_haiti_cote if d['URL']!=""]))
list_author_cote=list(set([d['Auteur'] for d in corpus_haiti_cote if d['Auteur']!=""]))
list_author_cote_norm=["_".join(normalize_names(n)) for n in list_author_cote]
both=set(list_author_ile_en_ile_norm).intersection(set(list_author_cote_norm))


all_authors=set(list(list_author_spla_norm+list_author_cote_norm+list_author_ile_en_ile_norm))
       
with open('C:/Users/Celian/Desktop/lifranum_carto/data/list_authors.json', 'w') as outfile:
     json.dump(list(all_authors), outfile)

import csv
from operator import getitem
typo=list(set([k.lower() for k in type_prod]))
with open('C:/Users/Celian/Desktop/lifranum_carto/data/list_typo.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    for t in typo:    
        spamwriter.writerow([t])
