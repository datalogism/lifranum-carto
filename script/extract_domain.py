# -*- coding: utf-8 -*-
"""
Created on Mon Jan 27 13:23:20 2020

@author: Celian
"""

from urllib import parse
import csv




d=[]
file='C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/liens.csv'
with open(file, encoding='utf-8') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=';')
    header=next(readCSV)
    for row in readCSV:
        new=[]
        url=parse.urlsplit(row[1])        
        new.append([row[0],row[1],url.netloc,row[2]])
        d.append(new)
        
with open('C:/Users/Celian/Desktop/M2 HUMANUM/PROJET/lifranum_carto/data/liens_domain.csv', 'w', newline='', encoding="utf-8") as csvfile:
    spamwriter = csv.writer(csvfile, delimiter=';',
                            quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    spamwriter.writerow(['Source', 'Target','Target2' 'Type'])
    for row in d:
        spamwriter.writerow(row[0])

