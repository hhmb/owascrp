# -*- coding: utf-8 -*-
"""
Created on Wed Jun 24 16:46:20 2015

@author: mbaumgar
"""


from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd

r = requests.get("http://www.oldworldauctions.com/archives.asp")
owa_archive_txt = r.text
owa_archive_soup = BeautifulSoup(owa_archive_txt)
#print(owa_archive_soup.prettify())





####################################
#  get link-array
####################################
archive_price_links =[]
for link in owa_archive_soup.find_all('a'):
    if 'archives/prices' in link.get('href'):
       archive_price_links.append('http://www.oldworldauctions.com/'+link.get('href'))


#print(archive_price_links[0])

####################################
#  loop links
####################################

r = requests.get(archive_price_links[0]) # iterate array !!
owa_archive_price_txt = r.text
owa_archive_price_soup = BeautifulSoup(owa_archive_price_txt)


####################################
#  get lots
####################################

archive_lots_links =[]
archive_lots_links_counter = 0
curr_status = 200
data_frame = None
 

for link in owa_archive_price_soup.find_all('a'):
    if 'detail/' in link.get('href'):
        archive_lots_links.append('http://www.oldworldauctions.com/archives/'+link.get('href'))

#print(archive_lots_links[0])
r = requests.get(archive_lots_links[0]) # iterate array !!
owa_archive_lot_txt = r.text
owa_archive_lot_soup = BeautifulSoup(owa_archive_lot_txt)

#print(owa_archive_lot_soup.prettify())
a = str(owa_archive_lot_soup.findAll("img", "imgSpec"))

mo =  re.search(r"http://www.*jpg",a)
print("Current Lot %s" % mo.group())