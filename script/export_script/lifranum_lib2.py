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



def get_CompleteNotice(datas):
    id_auth= strip_accents('_'.join(normalize_names(datas["author_name"])))
    generated_on = str(datetime.datetime.now())[0:10]
    root = Element('TEI')
    root.set('xmlns:xi', 'http://www.w3.org/2001/XInclude')
    root.set('xml:lang', 'fr')
    root.set('xml:id',id_auth+"_notice") ###################
    teiHeader=SubElement(root,"teiHeader")
    fileDesc=SubElement(teiHeader,"fileDesc")
    titleStmt=SubElement(fileDesc,"titleStmt")
    title=SubElement(titleStmt,"title")
    title.text ="Notice de "+datas["author_name"] ###################
    for auth in datas["file_authors"]:
        author=SubElement(titleStmt,"author")
        author.text=auth["auth_name"]
    
    publicationStmt=SubElement(fileDesc,"publicationStmt")
    for auth in datas["file_authors"]:
        author=SubElement(publicationStmt,"org_name")
        author.text=auth["org_name"]
    date=SubElement(publicationStmt,"date")
    date.text =generated_on
    sourceDesc=SubElement(fileDesc,"sourceDesc")
    sourceDesc.text="Données issues de sources d'autorités et de répétoire web"
    n=1
    if("data_auth" in datas.keys()):
        data=datas["data_auth"]
        Div_fiche_autorite=SubElement(root,"div")
        Div_fiche_autorite.set("xml:id",id_auth+"_fiche_autorite")
        Div_fiche_autorite.set("n",str(n))
        person=SubElement(Div_fiche_autorite,"person")
        person.set("ana",id_auth)

        ## SEX
        person.set("sex","na")
        if("viaf" in data.keys() and "gender" in data["viaf"].keys()):
            if(data["viaf"]["gender"] and data["viaf"]["gender"] != None):
                person.set("sex",data["viaf"]["gender"])
        if("bnf" in data.keys() and "gender" in data["bnf"].keys()):
            if(data["bnf"]["gender"] and data["bnf"]["gender"] != None):
                person.set("sex",data["viaf"]["gender"])

        ## NAME SURNAME
        persName=None
        if("bnf" in data.keys() and "name" in data["bnf"].keys()):
            if(data["bnf"]["name"] and data["bnf"]["name"] != None):
                if(persName is None):
                    persName=SubElement(person,"persName")
                surname=SubElement(persName,"surname")
                surname.set("source","bnf")
                surname.text=data["bnf"]["name"]

        ## FAMILY NAME
        if("bnf" in data.keys() and "family_name" in data["bnf"].keys()):
            if(data["bnf"]["family_name"] and data["bnf"]["family_name"] != None):
                if(persName is None):
                    persName=SubElement(person,"persName")
                surname=SubElement(persName,"forename")
                surname.set("source","bnf")
                surname.text=data["bnf"]["family_name"]
                
        ### IF no distinctions
        if(persName is None):
            persName=SubElement(person,"persName")
            persName.text=datas["author_name"]


        ##BNF
        if("bnf" in data.keys() and "id_bnf" in data["bnf"].keys()):
            if(data["bnf"]["id_bnf"]):
                id_no=SubElement(person,"idno")
                id_no.set("type","BNF")
                splitted=data["bnf"]["id_bnf"].split("/")
                id_no.text=splitted[-1]
                id_no_content=SubElement(id_no,"g")
                id_no_content.set("ref",data["bnf"]["id_bnf"])

        ## VIAF
        if("bnf" in data.keys() and "id_viaf" in data["bnf"].keys()):
            if(data["bnf"]["id_viaf"]):
                id_no=SubElement(person,"idno")
                id_no.set("type","VIAF")
                splitted=data["bnf"]["id_viaf"].split("/")
                id_no.text=splitted[-1]
                id_no_content=SubElement(id_no,"g")
                id_no_content.set("ref",data["bnf"]["id_viaf"])
        ## DBPEDIA
        if("bnf" in data.keys() and "id_dbpedia" in data["bnf"].keys()):
            if(data["bnf"]["id_dbpedia"]):
                id_no=SubElement(person,"idno")
                id_no.set("type","VIAF")
                splitted=data["bnf"]["id_dbpedia"].split("/")
                id_no.text=splitted[-1]
                id_no_content=SubElement(id_no,"g")
                id_no_content.set("ref",data["bnf"]["id_dbpedia"])
        # BIRTHDATE
        if("viaf" in data.keys() and "birth_date" in data["viaf"].keys()):
            if(data["viaf"]["birth_date"]):
                birth=SubElement(person,"birth")
                birth.set("source","viaf")
                birth_date=SubElement(birth,"date")
                birth_date.text=data["viaf"]["birth_date"]
        if("spla_auto" in data.keys() and "birth_date" in data["spla_auto"].keys()):
            if(data["spla_auto"]["birth_date"]):
                birth=SubElement(person,"birth")
                birth.set("source","spla_auto")
                birth_date=SubElement(birth,"date")
                birth_date.text=data["spla_auto"]["birth_date"]
        if("ile_en_ile_auto" in data.keys() and "birth_date" in data["ile_en_ile_auto"].keys()):
            if(data["ile_en_ile_auto"]["birth_date"]):
                birth=SubElement(person,"birth")
                birth.set("source","ile_en_ile_auto")
                birth_date=SubElement(birth,"date")
                birth_date.text=data["ile_en_ile_auto"]["birth_date"]

        # DEATHDATE
        if("viaf" in data.keys() and "death_date" in data["viaf"].keys()):
            if(data["viaf"]["death_date"]):
                death=SubElement(person,"death")
                death.set("source","viaf")
                death_date=SubElement(death,"date")
                death_date.text=data["viaf"]["death_date"]
        
        if("ile_en_ile_auto" in data.keys() and "death_date" in data["ile_en_ile_auto"].keys()):
            if(data["ile_en_ile_auto"]["death_date"]):
                death=SubElement(person,"death")
                death.set("source","ile_en_ile_auto")
                death_date=SubElement(death,"date")
                death_date.text=data["ile_en_ile_auto"]["death_date"]

        if("spla_auto" in data.keys() and "death_date" in data["spla_auto"].keys()):
            if(data["spla_auto"]["death_date"]):
                death=SubElement(person,"death")
                death.set("source","spla_auto")
                death_date=SubElement(death,"date")
                death_date.text=data["spla_auto"]["death_date"]
        ## LANG
        list_lang=[]
        langKnowledge=None
        if("bnf" in data.keys() and "lang" in data["bnf"].keys()):
            if(data["bnf"]["lang"] and data["bnf"]["lang"] not in list_lang):
                if(langKnowledge==None):
                    langKnowledge=SubElement(person,"langKnowledge")

                lang=SubElement(langKnowledge,"langKnown")
                lang.set("source","bnf")
                lang.text=data["bnf"]["lang"]
                list_lang.append(data["bnf"]["lang"])
        if("spla" in data.keys() and "lang" in data["spla"].keys()):
            if(data["spla"]["lang"] and data["spla"]["lang"] not in list_lang):
                if(langKnowledge==None):
                    langKnowledge=SubElement(person,"langKnowledge")
                lang=SubElement(langKnowledge,"langKnown")
                lang.set("source","spla")
                lang.text=data["spla"]["lang"]
                list_lang.append(data["spla"]["lang"])

        #RESIDENCE
        if("spla" in data.keys() and "country" in data["spla"].keys()):
            if(data["spla"]["country"]):
                residence=SubElement(person,"residence")
                placeName=SubElement(residence,"placeName")
                country=SubElement(placeName,"country")
                country.set("source","spla")
                country.text=data["spla"]["country"]
        if("bnf" in data.keys() and "country" in data["bnf"].keys()):
            if(data["bnf"]["country"]):
                residence=SubElement(person,"residence")
                placeName=SubElement(residence,"placeName")
                country=SubElement(placeName,"country")
                country.set("source","bnf")
                country.text=data["bnf"]["country"]

        ## OCCUPATION
        list_occup=[]
        if("viaf" in data.keys() and "occupations" in data["viaf"].keys()):
            if(data["viaf"]["occupations"]):
                for occ in data["viaf"]["occupations"]:
                    if( occ not in list_occup):
                        occupation=SubElement(person,"occupation")
                        occupation.set("source","viaf")
                        occupation.text=occ
                        list_occup.append(occ)
        if("spla" in data.keys() and "activity" in data["spla"].keys()):
            if(data["spla"]["activity"]):
                if("," in data["spla"]["activity"]):
                    activities=data["spla"]["activity"].split(",")
                    for occ in activities:
                        if( occ not in list_occup):
                            occupation=SubElement(person,"occupation")
                            occupation.set("source","spla")
                            occupation.text=occ
                            list_occup.append(occ)
                else:
                    if( data["spla"]["activity"] not in list_occup):
                        occupation=SubElement(person,"occupation")
                        occupation.set("source","spla")
                        occupation.text=data["spla"]["activity"]
                        list_occup.append(data["spla"]["activity"])

        if("viaf" in data.keys() and "co_authors" in data["viaf"].keys()):
            if(data["viaf"]["co_authors"] and len(data["viaf"]["co_authors"])>0):
                listPerson=SubElement(person,"listPerson")
                listPerson.set("type","co_authors")
                listPerson.set("source","viaf")
                for occ in data["viaf"]["co_authors"]:
                    person2=SubElement(listPerson,"person")
                    person2.set(ana,"viaf")
                    ana_occ=strip_accents('_'.join(normalize_names(occ["name"])))
                    person2.set("ana",ana_occ)
                    persName2=SubElement(person2,"persName")
                    persName2.text(occ["name"])

        return root
        
