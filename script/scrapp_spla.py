# -*- coding: utf-8 -*-
"""
Created on Sat Nov  2 01:28:55 2019

@author: Celian
"""


import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import json
from bs4 import BeautifulSoup as bs
import time


def init_driver():
 
     # initiate the driver:
     driver = webdriver.Firefox(executable_path ='C:/Users/Celian/Selenium/geckodriver.exe')
 
     # set a default wait time for the browser [5 seconds here]:
     driver.wait = WebDriverWait(driver, 5)
 
     return driver

def close_driver(driver):
 
    driver.close()
 
    return

data=[]

driver = init_driver()
driver.get("http://www.spla.pro/fr/liste.personne.html?no_rub=5&fbclid=IwAR0EcB7kIP_aatWelXw_fFbvlVVUoiakGI4qTZ_FqDB2cnq5D77D6tZ2C4Y&page=152")


next_exist=driver.find_element_by_class_name("more")
while next_exist:
    driver.find_element_by_class_name("more").click()    
    page_source = driver.page_source  

    soup = bs(page_source,'lxml') 
    item_list=soup.find_all("div", class_='blocksitgrid')
    for i in item_list:
    
        link = i.find("a", href=True)
        link_href=link["href"]
                
        details=i.find("div", {"class":"affcol-details"})
        nom=details.find("h2").get_text()
        activite=details.find("div", {"class":"soustitre"})
        data_auteur={"lien":link_href,"nom auteur":nom,"activiés":activite}
        data.append(data_auteur)
        next_exist=driver.find_element_by_class_name("more")
for d in data:
    if d['activiés']:
        try:
            d['activiés']=d['activiés'].get_text()
        except:
            print("ok")
    else:
        d['activiés']=""
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/spla_haiti1.json'

with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)



with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
import requests

for d in data:
    
        if("get_info_done" not in d.keys() or d["get_info_done"]==0):
            try:
                r  = requests.get(d["lien"])
                id_pers=d["lien"].split(".")[-2]
                data_c = r.text
                soup = bs(data_c)
                d["get_info_done"]=1
                try:
                    country=soup.find("div", {'class':'img-drapo'}).find("a")
                    d["country"]=country.get_text()
                except:
                    print("pas pays")
                try:
                    referenced_as=soup.findall("a")
                    ref_list=[]
                    for link in referenced_as:
                        ref_list.append(link.get_text())
                    print(ref_list)
                    d["ref_list"]=ref_list
                except:
                    print("pas pays")
            except:
                print("conn refused")                
                d["get_info_done"]=0
        
        if("get_info_done_2" not in d.keys() or d["get_info_done_2"]==0):
            try:
                desc_link=("http://www.spla.pro/inc/fiche_descriptions_ajax.php?type=personne&no="+str(id_pers))
                r  = requests.get(desc_link)
                
                d["get_info_done_2"]=1
                data_c = r.text
                soup = bs(data_c)      
                every_desc=soup.find("div")
                current_desc={}
                try:
                    lang=every_desc.find("h4").get_text()
                    current_desc["lang"]=lang
                except:
                    print("pas de langue")
                try:
                    desc_content=every_desc.find("p").get_text()
                    current_desc["content"]=desc_content
                except:
                    print("pas de desc for lang")
                if(len(current_desc.keys())>0):        
                    d["desc"]=current_desc
            except:
                
                d["get_info_done_2"]=0
                print("pas de desc")

        
    
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/spla_haiti3.json'

with open(file, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
        
    