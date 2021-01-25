# -*- coding: utf-8 -*-
"""
Created on Mon Jan 25 12:29:19 2021

@author: Celian
"""
import json
test_list=["agnant","alexis_jacques-stephen","anglade","apollon","attoumani","auguste","augustin","baco","barthelemy","batraville","beauge-rosier","belance","belin","bellegarde","benjamin","berrouet-oriol","bloncourt","bourjolly","brierre","brouard","calvin","camille","capecia","casseus","castera","cave","chancy","charles_christophe","charles_jean-claude","charlier_jacques","chassagne","chauvet","chenet","clitandre","colimon-hall","comhaire-sylvain","constant","dabel","dalembert","danticat","davertige","deita","depestre","desquiron","desrosiers","dominique","dorsinville_max","dorsinville_roger","duccha","edouard","ejen","exavier","faubert","fievre","fignole","fombrun","fouche","franketienne","franz","gaillard","gaillard-vante","guerin","innocent_antoine","jean","klang","laferriere","bogart","lahens","laleau","laraque","large","laroche","laroche_maximilien","lauture","legagneur","lemoine","leonidas","lespes","lherisson_farah-martine","magloire-saint-aude","mars","martelly","mathieu","maurouard","metellus","milce","monnin","morisolewa","morisseau_roland","narcisse","noel","ollivier","orcel","papillon_ileus","papillon_margaret","paret","pasquet_fabienne","pasquet_jean-marc","paul","pean","phelps","philoctete","pierre_claude","pierre-dahomey","poujol-oriol","price-mars","prophete_emmelie","regis","renaud","roumain","roumer","saint-amand","saint-eloi","scott","sixto","soeuf-elbadawi","suprice","surena","tavernier","theard","thoby-marcelin","trouillot_evelyne","trouillot_lyonel","valcin","victor_gary","vilaire","voltaire-marcelin","amerique","desrivieres","dovilas","etienne","jacquet","kauss","labuchin","lafortune","aupont","magloire_nadine","manigat"]
file='C:/Users/Celian/Desktop/lifranum_carto/data/ile_en_ile.json'

with open(file, encoding='utf-8') as json_file:
    data = json.load(json_file)
    
names=list(data.keys())
data[names[0]]["url"].replace("http://ile-en-ile.org/","").replace("/","")
