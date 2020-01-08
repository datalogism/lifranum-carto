# -*- coding: utf-8 -*-
"""
Created on Sat Jan  4 13:46:44 2020

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
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="  ")

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

def AnnotateText(txt):
    current_doc = nlp(txt)
    tempo_text=txt
    done=[]
    for entity in current_doc.ents:
        if(entity.label_=="ORG"):
            token="<orgName source='auto_spacy'>"+entity.text+"</orgName>"
        if(entity.label_=="PER"):
            token="<persName source='auto_spacy'>"+entity.text+"</persName>"
        if(entity.label_=="LOC"):
            token="<placeName source='auto_spacy'>"+entity.text+"</<placeName>"
        if token and entity.text not in done:
                tempo_text=tempo_text.replace(entity.text,token)
                done.append(entity.text)
    return tempo_text

def GetGeoloc(place_name):
    locator = Nominatim(user_agent="myGeocoder")
    location = locator.geocode(place_name)
    return [location.latitude, location.longitude]
 
def get_BioAuthors(data):
    id_auth= strip_accents('_'.join(normalize_names(data["author_name"])))
    generated_on = str(datetime.datetime.now())[0:10]
    root = Element('TEI')
    root.set('xmlns:xi', 'http://www.w3.org/2001/XInclude')
    root.set('xml:lang', 'fr')
    root.set('xml:id',id_auth+'_bio_auteur') ###################
    teiHeader=SubElement(root,"teiHeader")
    fileDesc=SubElement(teiHeader,"fileDesc")
    titleStmt=SubElement(fileDesc,"titleStmt")
    title=SubElement(titleStmt,"title")
    title.text ="Biographies de"+data["author_name"] ###################
    for auth in data["file_authors"]:
        author=SubElement(titleStmt,"author")
        author.text=auth["auth_name"]
    
    publicationStmt=SubElement(fileDesc,"publicationStmt")
    for auth in data["file_authors"]:
        author=SubElement(publicationStmt,"org_name")
        author.text=auth["org_name"]
   
    date=SubElement(publicationStmt,"date")
    date.text =generated_on
    
    for bio_k in data["bio_data"].keys():
        
        text=SubElement(root,"text")
        text.set('xml:id', id_auth+'_bio_auteur_'+bio_k) ################### ID AUTEUR
        text.set('ref', data["bio_data"][bio_k]["ref"]) ################### URL ILE EN ILE
        if "hand" in data["bio_data"][bio_k].keys() and data["bio_data"][bio_k]["hand"]!="":
            text.set('hand',data["bio_data"][bio_k]["hand"] ) ################### WRITEN BY
    
    
        ####################################### SI PHOTO
        # p1=SubElement(text,"p")
        # figure=SubElement(text,"figure")
        # figure_head=SubElement(figure,"head")
        # figure_head.text="portrait de l'auteur"
        # figure_graphic=SubElement(figure,"graphic")
        # figure_head.text="portrait de l'auteur"
        # url="" #######################################
        # figure_graphic.set('url', url) #######################################
        for row in data["bio_data"][bio_k]["bio_content"]:
        ############### FOR EACH PARAPH
#            row2=AnnotateText(row)
            p=SubElement(text,"p")
            p.text=row
            p.text=row2
        return prettify(root)

def get_BiblioAuthors(data):
	id_auth= strip_accents('_'.join(normalize_names(data["author_name"])))
	generated_on = str(datetime.datetime.now())[0:10]
	root = Element('TEI')
	root.set('xmlns:xi', 'http://www.w3.org/2001/XInclude')
	root.set('xml:lang', 'fr')
	root.set('xml:id',id_auth+'_biblio_auteur') ###################
	teiHeader=SubElement(root,"teiHeader")
	fileDesc=SubElement(teiHeader,"fileDesc")
	titleStmt=SubElement(fileDesc,"titleStmt")
	title=SubElement(titleStmt,"title")
	title.text ="Contenus associés à "+data["author_name"] ###################
	for auth in data["file_authors"]:
		author=SubElement(titleStmt,"author")
		author.text=auth["auth_name"]

	publicationStmt=SubElement(fileDesc,"publicationStmt")
	for auth in data["file_authors"]:
		author=SubElement(publicationStmt,"org_name")
		author.text=auth["org_name"]

	date=SubElement(publicationStmt,"date")
	date.text =generated_on


	for biblio_k in data["biblio_data"].keys():
		text=SubElement(root,"div")
		text.set('xml:id', id_auth+'_biblio_auteur_'+biblio_k) ################### ID AUTEUR
		text.set('ref', data["biblio_data"][biblio_k]["ref"])
		for list_name in data["biblio_data"][biblio_k]["content"].keys():
			new_list=SubElement(text,"list")
			new_list.set("subtype",list_name.lower())
			for current_content in data["biblio_data"][biblio_k]["content"][list_name] :
				item = SubElement(new_list,"item")
				if("text" in current_content.keys()):
					item.text=current_content["text"]
				elif("link" in current_content.keys()):
					item.text=current_content["link"]["text"]
					item.set("ref",current_content["link"]["url"])
	return prettify(root)

    
file='C:/Users/Celian/Desktop/lifranum_carto/data/list_authors.json'
with open(file, encoding='utf-8') as json_file:
    list_authors = json.load(json_file)
    
file='C:/Users/Celian/Desktop/lifranum_carto/data/spla_haiti_final.json'
with open(file, encoding='utf-8') as json_file:
    data_spla0 = json.load(json_file)
data_spla_ok={}
for d in data_spla0:
    if ("_".join(normalize_names(d['nom auteur'])) in list_authors):
        data_spla_ok["_".join(normalize_names(d['nom auteur']))]=d

    
file='C:/Users/Celian/Desktop/lifranum_carto/data/ile_en_ile.json'
with open(file, encoding='utf-8') as json_file:
    data_ile_en_ile0 = json.load(json_file)
    
data_ile_en_ile_ok={}
for aut_k in data_ile_en_ile0.keys():
    if ("_".join(normalize_names(aut_k)) in list_authors):
        current= data_ile_en_ile0[aut_k]
        current["name_auth"]=aut_k
        data_ile_en_ile_ok["_".join(normalize_names(aut_k))]=current


test_text=[]
for auth in list_authors:

        
    data_bio={"author_name":None, "file_authors":[{"auth_name":"Inès Burri","org_name":"Université Jean Moulin Lyon 3"},{"auth_name":"Anaïs Chambat","org_name":"ENS Lyon"},{"auth_name":"Célian Ringwald","org_name":"Université Lyon 2"}],
      "bio_data":{}}
    data_biblio={"author_name":None, "file_authors":[{"auth_name":"Inès Burri","org_name":"Université Jean Moulin Lyon 3"},{"auth_name":"Anaïs Chambat","org_name":"ENS Lyon"},{"auth_name":"Célian Ringwald","org_name":"Université Lyon 2"}],
      "biblio_data":{}}
    id_auth= strip_accents(auth)
    if(auth in data_ile_en_ile_ok.keys()):
        data_bio["author_name"]=data_ile_en_ile_ok[auth]["name_auth"]
        data_biblio["author_name"]=data_ile_en_ile_ok[auth]["name_auth"]
        data_bio["bio_data"]["ile_en_ile"]={}
        data_biblio["biblio_data"]["ile_en_ile"]={}
        data_biblio["biblio_data"]["ile_en_ile"]["ref"]=data_ile_en_ile_ok[auth]["url"]
        data_biblio["biblio_data"]["ile_en_ile"]["content"]={}
        data_bio["bio_data"]["ile_en_ile"]["ref"]=data_ile_en_ile_ok[auth]["url"]
        bio_content=[]
        writer_bio=''
        for component in data_ile_en_ile_ok[auth]["bio"]:
            if(component[0:2]=="– "):
                writer_bio=component[3:]
            else:
                bio_content.append(component)
                test_text.append(component)
        
        for component in data_ile_en_ile_ok[auth]["productions"]:
            if(component!="Retour"):
                data_biblio["biblio_data"]["ile_en_ile"]["content"][component.lower()]=json.loads(json.dumps(data_ile_en_ile_ok[auth]["productions"][component]))
        data_bio["bio_data"]["ile_en_ile"]["bio_content"]=bio_content
        data_bio["bio_data"]["ile_en_ile"]["hand"]=writer_bio
    if(auth in data_spla_ok.keys()):
        if(data_bio["author_name"] is None and "nom auteur" in data_spla_ok[auth].keys()):
            data_bio["author_name"]=data_spla_ok[auth]["nom auteur"]
        if("desc" in data_spla_ok[auth].keys()):
            if("content" in data_spla_ok[auth]["desc"].keys()):
                data_bio["bio_data"]["spla"]={}
                data_bio["bio_data"]["spla"]["ref"]=data_spla_ok[auth]["lien"]
                data_bio["bio_data"]["spla"]["bio_content"]=[data_spla_ok[auth]["desc"]["content"].encode('latin-1').decode("utf-8")]
                print("bio_"+id_auth+".xml")
                test_text.append(data_bio["bio_data"]["spla"]["bio_content"])
#    if(len(data_bio["bio_data"].keys())):
#        result=get_BioAuthors(data_bio)
#        myfile = open("C:/Users/Celian/Desktop/lifranum_carto/data/tei corpus/bio_auteurs/bio_"+id_auth+".xml", "w")
#        myfile.write(result)
#        myfile.close()
    if(len(data_biblio["biblio_data"].keys())):
        result=get_BiblioAuthors(data_biblio)
        myfile = open("C:/Users/Celian/Desktop/lifranum_carto/data/tei corpus/biblio_auteurs/biblio_"+id_auth+".xml", "w")
        myfile.write(result)
        myfile.close()
    
