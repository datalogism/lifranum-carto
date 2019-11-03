# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 13:27:38 2019

@author: Celian
"""

import requests

viaf_id="58863888"
#https://platform.worldcat.org/api-explorer/apis/VIAF
r=requests.get("http://www.viaf.org/viaf/"+viaf_id+"/")
data=r.text