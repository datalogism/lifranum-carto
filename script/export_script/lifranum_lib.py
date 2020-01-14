# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 23:59:39 2020

@author: Celian
"""
import csv
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
import datetime
from lxml import etree
from xml.dom import minidom
from xml.etree import ElementTree

import unicodedata
import spacy

from spacy_lefff import LefffLemmatizer, POSTagger
nlp=spacy.load('fr_core_news_sm')

spacy_nlp = spacy.load('fr_core_news_sm')
french_lemmatizer = LefffLemmatizer()
spacy_nlp.add_pipe(french_lemmatizer, name='lefff')



from spacy.matcher import Matcher
from date_extractor import extract_dates

def GetAuthorsDates(txt):
    txt_clean=txt.lower()
    dates = extract_dates(txt_clean)

    
    doc = spacy_nlp(txt_clean)
  
    matcher = Matcher(spacy_nlp.vocab)
    ruled=False
    for d in dates:
        if d:
            ruled=True
            pattern = [{"LEMMA": "naître"},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}},{"TEXT":str(d.year)},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}}]
            matcher.add("birth_date_"+str(d), None, pattern)
            pattern = [{"LEMMA": "naissance"},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}},{"TEXT":str(d.year)},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}}]
            matcher.add("birth_date2_"+str(d), None, pattern)
            pattern = [{"LEMMA": "mourir"},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}},{"TEXT":str(d.year)},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}}]
            matcher.add("death_date_"+str(d), None, pattern)
            pattern = [{"LEMMA": "décéder"},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}},{"TEXT":str(d.year)},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}}]
            matcher.add("death_date2_"+str(d), None, pattern)
            pattern = [{"LEMMA": "mort"},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}},{"TEXT":str(d.year)},{"OP":"*","POS":{"NOT_IN":["PUNCT"]}}]
            matcher.add("death_date3_"+str(d), None, pattern)
    matches = matcher(doc)
    
    resp={"birth_date":None,"death_date":None}
    found_dates={"birth_date":[],"death_date":[]}
    if ruled:
        for match_id, start, end in matches:
            if match_id:
                string_id = spacy_nlp.vocab.strings[match_id] 
                splitted=string_id.split("_")
                if("birth" in string_id):
                    found_dates["birth_date"].append(splitted[-1])
                if("death" in string_id):
                    found_dates["death_date"].append(splitted[-1])
    found_dates["birth_date"]=list(set(found_dates["birth_date"]))
    found_dates["death_date"]=list(set(found_dates["death_date"]))
    if(len(found_dates["birth_date"])==1):
        resp["birth_date"]=found_dates["birth_date"][0]
    if(len(found_dates["death_date"])==1):
        resp["death_date"]=found_dates["death_date"][0]
    
    return resp


def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')
def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ElementTree.tostring(elem, encoding= 'utf-8', method='xml')
    reparsed = minidom.parseString(rough_string)
    txt= reparsed.toprettyxml(indent="  ")
    txt2=txt.replace('<?xml version="1.0" ?>','<?xml version="1.0" encoding="UTF-8"?>')
    return txt2

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
			new_div=SubElement(text,"div")
			new_div.set("subtype",list_name.lower())
			if(list_name=="sur_le_web"):
				new_list=SubElement(new_div,"list")
				for itt in data["biblio_data"][biblio_k]["content"][list_name]:
					item = SubElement(new_list,"item")
					item.text=itt["title"]
					item.set("ref",itt["url"])
			else:
				for prod_k in data["biblio_data"][biblio_k]["content"][list_name].keys():    
					new_list=SubElement(new_div,"list")
					new_list.set("subtype",prod_k.lower())
					current_prod=data["biblio_data"][biblio_k]["content"][list_name][prod_k]
					for prod in current_prod:
						item = SubElement(new_list,"item")    
						item.text=prod
                 
	return root


def get_BioAuthors(data):
   # data=data_bio
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
        if "bio_content" in data["bio_data"][bio_k].keys():
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
                
                text.append(ElementTree.fromstring('<p>'+row+"</p>"))
    #            p.text=row2
        return root


def get_FicheAuthors(data):
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
	title.text ="Fiche Auteur de "+data["author_name"] ###################
	for auth in data["file_authors"]:
		author=SubElement(titleStmt,"author")
		author.text=auth["auth_name"]
	
	publicationStmt=SubElement(fileDesc,"publicationStmt")
	for auth in data["file_authors"]:
		author=SubElement(publicationStmt,"org_name")
		author.text=auth["org_name"]
	date=SubElement(publicationStmt,"date")
	date.text =generated_on
	content=SubElement(root,"text")
	list_pers=SubElement(content,"listPerson")
	pers=SubElement(list_pers,"person")
	pers.set("id",id_auth+"_fiche_auteur")
	pers.set("id",id_auth)
	if("viaf" in data["data_auth"].keys() and "gender" in data["data_auth"]["viaf"].keys()):
		if(data["data_auth"]["viaf"]["gender"] and data["data_auth"]["viaf"]["gender"] != None):
			gender=SubElement(pers,"gender")
			gender.set("source","viaf")
			gender.text=data["data_auth"]["viaf"]["gender"]
	if("bnf" in data["data_auth"].keys() and "gender" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["gender"] and data["data_auth"]["bnf"]["gender"] != None):
			gender=SubElement(pers,"gender")
			gender.set("source","bnf")
			gender.text=data["data_auth"]["viaf"]["gender"]
	if("bnf" in data["data_auth"].keys() and "name" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["name"] and data["data_auth"]["bnf"]["name"] != None):
			surname=SubElement(pers,"surname")
			surname.set("source","bnf")
			surname.text=data["data_auth"]["bnf"]["name"]
	if("bnf" in data["data_auth"].keys() and "family_name" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["family_name"] and data["data_auth"]["bnf"]["family_name"] != None):
			surname=SubElement(pers,"forename")
			surname.set("source","bnf")
			surname.text=data["data_auth"]["bnf"]["family_name"]
	if("bnf" in data["data_auth"].keys() and "id_bnf" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["id_bnf"]):
			id_no=SubElement(pers,"idno")
			id_no.set("type","BNF")
			splitted=data["data_auth"]["bnf"]["id_bnf"].split("/")
			id_no.text=splitted[-1]
			id_no_content=SubElement(id_no,"g")
			id_no_content.set("ref",data["data_auth"]["bnf"]["id_bnf"])
	if("bnf" in data["data_auth"].keys() and "id_viaf" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["id_viaf"]):
			id_no=SubElement(pers,"idno")
			id_no.set("type","VIAF")
			splitted=data["data_auth"]["bnf"]["id_viaf"].split("/")
			id_no.text=splitted[-1]
			id_no_content=SubElement(id_no,"g")
			id_no_content.set("ref",data["data_auth"]["bnf"]["id_viaf"])
	if("bnf" in data["data_auth"].keys() and "id_dbpedia" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["id_dbpedia"]):
			id_no=SubElement(pers,"idno")
			id_no.set("type","VIAF")
			splitted=data["data_auth"]["bnf"]["id_dbpedia"].split("/")
			id_no.text=splitted[-1]
			id_no_content=SubElement(id_no,"g")
			id_no_content.set("ref",data["data_auth"]["bnf"]["id_dbpedia"])
	if("viaf" in data["data_auth"].keys() and "birth_date" in data["data_auth"]["viaf"].keys()):
		if(data["data_auth"]["viaf"]["birth_date"]):
			birth=SubElement(pers,"birth")
			birth.set("source","viaf")
			birth_date=SubElement(birth,"date")
			birth_date.text=data["data_auth"]["viaf"]["birth_date"]
	if("viaf" in data["data_auth"].keys() and "death_date" in data["data_auth"]["viaf"].keys()):
		if(data["data_auth"]["viaf"]["death_date"]):
			death=SubElement(pers,"death")
			death.set("source","viaf")
			death_date=SubElement(death,"date")
			death_date.text=data["data_auth"]["viaf"]["death_date"]
	if("ile_en_ile_auto" in data["data_auth"].keys() and "birth_date" in data["data_auth"]["ile_en_ile_auto"].keys()):
		if(data["data_auth"]["ile_en_ile_auto"]["birth_date"]):
			birth=SubElement(pers,"birth")
			birth.set("source","ile_en_ile_auto")
			birth_date=SubElement(birth,"date")
			birth_date.text=data["data_auth"]["ile_en_ile_auto"]["birth_date"]
	if("ile_en_ile_auto" in data["data_auth"].keys() and "death_date" in data["data_auth"]["ile_en_ile_auto"].keys()):
		if(data["data_auth"]["ile_en_ile_auto"]["death_date"]):
			death=SubElement(pers,"death")
			death.set("source","ile_en_ile_auto")
			death_date=SubElement(death,"date")
			death_date.text=data["data_auth"]["ile_en_ile_auto"]["death_date"]
	if("spla_auto" in data["data_auth"].keys() and "birth_date" in data["data_auth"]["spla_auto"].keys()):
		if(data["data_auth"]["spla_auto"]["birth_date"]):
			birth=SubElement(pers,"birth")
			birth.set("source","spla_auto")
			birth_date=SubElement(birth,"date")
			birth_date.text=data["data_auth"]["spla_auto"]["birth_date"]
	if("spla_auto" in data["data_auth"].keys() and "death_date" in data["data_auth"]["spla_auto"].keys()):
		if(data["data_auth"]["spla_auto"]["death_date"]):
			death=SubElement(pers,"death")
			death.set("source","spla_auto")
			death_date=SubElement(death,"date")
			death_date.text=data["data_auth"]["spla_auto"]["death_date"]
	if("bnf" in data["data_auth"].keys() and "lang" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["lang"]):
			lang=SubElement(pers,"language")
			lang.set("source","bnf")
			lang.text=data["data_auth"]["bnf"]["lang"]
	if("spla" in data["data_auth"].keys() and "lang" in data["data_auth"]["spla"].keys()):
		if(data["data_auth"]["spla"]["lang"]):
			lang=SubElement(pers,"language")
			lang.set("source","spla")
			lang.text=data["data_auth"]["spla"]["lang"]
	if("spla" in data["data_auth"].keys() and "country" in data["data_auth"]["spla"].keys()):
		if(data["data_auth"]["spla"]["country"]):
			country=SubElement(pers,"country")
			country.set("source","spla")
			country.text=data["data_auth"]["spla"]["country"]
	if("bnf" in data["data_auth"].keys() and "country" in data["data_auth"]["bnf"].keys()):
		if(data["data_auth"]["bnf"]["country"]):
			country=SubElement(pers,"language")
			country.set("source","bnf")
			country.text=data["data_auth"]["bnf"]["country"]
	if("viaf" in data["data_auth"].keys() and "occupations" in data["data_auth"]["viaf"].keys()):
		if(data["data_auth"]["viaf"]["occupations"]):
			for occ in data["data_auth"]["viaf"]["occupations"]:
				profession=SubElement(pers,"profession")
				profession.set("source","viaf")
				profession.text=occ
	if("spla" in data["data_auth"].keys() and "activity" in data["data_auth"]["spla"].keys()):
		if(data["data_auth"]["spla"]["activity"]):
			profession=SubElement(pers,"profession")
			profession.set("source","spla")
			profession.text=data["data_auth"]["spla"]["activity"]
	return root

				
def get_Masters(data):
	id_auth= strip_accents('_'.join(normalize_names(data["author_name"])))
	root = Element('master')
	root.set('xmlns:xi', 'http://www.w3.org/2001/XInclude')
	root.set('xml:lang', 'fr')
	root.set('xml:id',id_auth+'_master_auteur') ###################
	for file in data["data_files"]:
		ref=SubElement(root,"xi:include")
		ref.set("ref",file)
	return root
    
	