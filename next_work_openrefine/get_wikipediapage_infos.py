# -*- coding: utf-8 -*-
"""
Created on Mon Feb  1 13:31:11 2021

@author: Celian
"""
from bs4 import BeautifulSoup
import requests
import re
import json

import csv


def load_page(url):
    en_rq=requests.get(url)
    return en_rq.text

file='C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/data_for_wiki_info.csv'
list_clean_spla_id={}
wikidata_res=[]
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        print(row)
        current={header[i]:row[i] for i  in range(len(header))}
        wikidata_res.append(current)
        
        

file='C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/wiki_structure.csv'
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        print(row)
        current={header[i]:row[i] for i  in range(len(header))}
        
lang_list=["en","fr","ht"]
header=["url","lang","entity","nb_redirects","nb_view_month","page_creator","nb_edit","creation_date_row","last_modif_date"]
data_final=[header]
for row in wikidata_res:
    for lang in lang_list:
        key="wikipage_"+lang
        url=row[key]
        if(url!="#N/A"):
           entity=url.replace("https://"+lang+".wikipedia.org/wiki/","")
           print(entity)
           print(lang)
           info_url="https://"+lang+".wikipedia.org/w/index.php?title="+entity+"&action=info"
           
           current=[url,lang,entity,0,0,"",0,"",""]
           info_page=load_page(info_url)
           
           soup = BeautifulSoup(info_page)
           
           found_first_table=soup.find("h2", {"id": "mw-pageinfo-header-basic"})
           found_second_table=soup.find("h2", {"id": "mw-pageinfo-header-edits"})
           
           if(found_first_table):
               print("-found first")
               redirects_row=soup.find("tr",{"id":"mw-pageinfo-visiting-watchers"})
               if(redirects_row):
                   redirects=redirects_row.findAll("td")[1].get_text()
                   current[3]=redirects
               nb_view_30_row=soup.find("tr",{"id":"mw-pvi-month-count"})
               if nb_view_30_row:
                   nb_view_30=nb_view_30_row.findAll("td")[1].get_text()
                   current[4]=nb_view_30
           if(found_second_table):
                print("-found second")
                page_creator_row=soup.find("tr",{"id":"mw-pageinfo-firstuser"})
                if page_creator_row:
                    page_creator=page_creator_row.findAll("td")[1].get_text()
                    current[5]=page_creator
                nb_edits_row=soup.find("tr",{"id":"mw-pageinfo-edits"})
                if nb_edits_row:
                    nb_edits=nb_edits_row.findAll("td")[1].get_text()
                    current[6]=nb_edits
                creation_date_row=soup.find("tr",{"id":"mw-pageinfo-firsttime"})
                if creation_date_row:
                    creation_date=creation_date_row.findAll("td")[1].get_text()
                    current[7]=creation_date
                    
                last_modif_date_row=soup.find("tr",{"id":"mw-pageinfo-lasttime"})
                if last_modif_date_row:
                    last_modif_date=last_modif_date_row.findAll("td")[1].get_text()
                    current[8]=last_modif_date
          
           data_final.append(current)



with open('C:/Users/Celian/Desktop/lifranum_carto/next_work_openrefine/data_wiki_info_final.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    for row in data_final:
        spamwriter.writerow(row)