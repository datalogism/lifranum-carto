# -*- coding: utf-8 -*-
"""
Created on Mon Jan 18 15:33:33 2021

@author: Celian

"""
import csv
from rdflib.graph import Graph


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

file='C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/wikidata_id_list.csv'
list_id_wiki=[]
corpus_wikidata=[]
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        current={header[i]:row[i] for i  in range(len(header))}
        try:
            current["Nom"]=current["\ufeffNom"].encode("latin-1").decode("utf-8")
        except:
            current["Nom"]=current["\ufeffNom"]
        current["normalized"]="_".join(normalize_names(current["Nom"]))
        if(row[1!=""]):
            list_id_wiki.append(row[1])
        corpus_wikidata.append(current)

file='C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/ResultWikidataRequest.csv'
wikidata_res=[]
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        wikidata_res.append(row[0].replace("http://www.wikidata.org/entity/",""))
common=list(set(wikidata_res).intersection(list_id_wiki))
len(common)


import requests
import time
url="https://query.wikidata.org/bigdata/namespace/wdq/sparql"

for current in corpus_wikidata:
    id_clean=current["Wiki_ID"]
    if(current['wikipage_en']=="" and  current['wikipage_fr']=="" and current['wikipage_ht']==""):
        current["search"]=True    
    
    if "search" not in list(current.keys()):
        current["search"]=True
    if(id_clean !="" and current["search"]==True):
        
        time.sleep(5)
        print("search for wikipages of id :",id_clean)
        query="""SELECT ?article WHERE {?article schema:about <http://www.wikidata.org/entity/"""+id_clean+""">; schema:isPartOf ?wiki FILTER(?wiki IN(<https://fr.wikipedia.org/>, <https://en.wikipedia.org/>, <https://ht.wikipedia.org/>)) }"""
        r = requests.get(url, params = {'format': 'json', 'query': query})
        
        try:
            data = r.json()
            vars_found=data["head"]["vars"]
            res=data["results"]["bindings"]
            if(len(data["results"]["bindings"])>0):    
                for art in res:
                    current_url=art['article']['value']
                    if('en.wikipedia.org' in current_url):
                        current["wikipage_en"]=current_url
                    if('fr.wikipedia.org' in current_url):
                        current["wikipage_fr"]=current_url
                    if('ht.wikipedia.org' in current_url):
                        current["wikipage_ht"]=current_url    
            current["search"]=False
        except:
            print("PB")
            current["search"]=True
    else:
        current["search"]=False
    
    

wikipages_content=[]
def load_page(url):
    en_rq=requests.get(url)
    return en_rq.text

from bs4 import BeautifulSoup
lang_list=["en","fr","ht"]
for row in corpus_wikidata:
    for lang in lang_list:
        url=row["wikipage_"+lang]
        if(url!=""):
            time.sleep(2)
            print(url)
            fr_rq=load_page(url)
            soup = BeautifulSoup(fr_rq)
            current={"wiki_id":"","wiki_url":"","wiki_content":"","lang":lang}
            content=soup.find("div", {"id": "bodyContent"})
            text=content.get_text()
            print(len(text))
            if(len(text)>0):
                current["wiki_id"]=row["Wiki_ID"]
                current["wiki_url"]=row["wikipage_"+lang]
                current["wiki_content"]=text
                row["wikipage_"+lang+"_len"]=len(text)
                wikipages_content.append(current)

import pandas as pd
wikipages_content_df = pd.DataFrame(wikipages_content)
wikipages_content_df.to_csv('C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/wikipages_content.csv')

corpus_wikidata_df = pd.DataFrame(corpus_wikidata)
corpus_wikidata_df.to_csv('C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/corpus_wikidata.csv')
                
            

       
