# -*- coding: utf-8 -*-
"""
Created on Sat Jun 20 17:05:35 2015

@author: Matthias

Info: Auction 115 is not readable
"""


####################################
#  import libs
####################################

from bs4 import BeautifulSoup
import requests
import re
import numpy as np
import pandas as pd

####################################
#  text_cleaner
####################################

def text_cleaner(input_text):
    input_text1 = input_text.replace("&nbsp", " ")
    input_text2 = input_text1.replace("Â", "")
    #input_text3 = input_text2.replace("\n", " ")
    return input_text2


####################################
#  df_cleaner
####################################
def df_cleaner(data_frame, col_name, list_repl, list_for):
    i = 0    
    for elem in list_repl:
        data_frame[col_name] = data_frame[col_name].str.replace(list_repl[i],list_for[i])
        i += 1        
        
####################################
#  get main page
####################################

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
#  loop links (Einzelne Auktionen)
####################################
archive_price_links_counter = 0

#Manuelle Übersteuerung des max links
archive_price_links_counter = 5

number_of_lot_links = len(archive_price_links)




while archive_price_links_counter < number_of_lot_links: 

    
    r = requests.get(archive_price_links[archive_price_links_counter]) # iterate array !!
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
    
    number_of_lot_links = len(archive_lots_links)
    
    ####################################
    #  inner loop
    ####################################
    
    #while archive_lots_links_counter < 2 and curr_status == 200:
        
    while archive_lots_links_counter < number_of_lot_links and curr_status == 200: 
        
        ####################################
        #  make soup
        ####################################
        r = requests.get(archive_lots_links[archive_lots_links_counter])  # iterate inner array !!
        
        #print("status code %s " % r.status_code)    
        curr_status = r.status_code
        
        if curr_status == 200:
            owa_archive_lot_txt = r.text
            owa_archive_lot_soup = BeautifulSoup(owa_archive_lot_txt)
            
            #reset data list
            data_list = []
            
            
            
            ####################################
            #  get text
            ####################################
            text_string = owa_archive_lot_soup.get_text(separator="\n", strip=False)
            image_string = str(owa_archive_lot_soup.findAll("img", "imgSpec"))   
            
            ####Auction
            mo =  re.search(r"Map Auction Sale No.*[0-9]\n",text_string)
            data_list.append(text_cleaner(mo.group()))
            print("Current Auction %s" % mo.group())
            curr_auction = mo.group()
            
            ####Lot
            mo =  re.search(r"Lot #[0-9]+",text_string)        
            data_list.append(text_cleaner(mo.group()))
            print("Current Lot %s" % mo.group())
            ####Image
            mo =  re.search(r"http://www.*jpg",image_string)
            data_list.append(mo.group())
            ####Title
            mo =  re.search(r"Lot #.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Estimate
            mo =  re.search(r"Estimate:.*\n.*[0]\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Sold for
            mo =  re.search(r"Sold for:.*[0]\n",text_string)
            if mo is not None:                    
                data_list.append(text_cleaner(mo.group()))
            else:
                #print("Item not sold")
                s= "-10000"
                data_list.append(text_cleaner(s))
            ####By
            mo =  re.search(r"By:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Subject
            mo =  re.search(r"Subject:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Date
            mo =  re.search(r"Date:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Publication
            mo =  re.search(r"Publication:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Condition
            mo =  re.search(r"Condition:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Color
            mo =  re.search(r"Color:.*\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            ####Size
            mo =  re.search(r"Size:.*\n.*cm\n",text_string)        
            data_list.append(text_cleaner(mo.group()))
            
            ####Text
            
            str_beg = mo.end()
            mo =  re.search(r"Search\n",text_string)
            str_end = mo.start()
            #print(text_string[str_beg:str_end])
            s = text_string[str_beg:str_end]
            data_list.append(text_cleaner(s))
            
            #add list to pandas dataframe
            #print ("Laenge %i " % len(data_list))
            
            if data_frame is None:
                data_frame = pd.DataFrame(np.array([data_list]), columns=['Auction', 'Lot', 'Image', 'Title', 'Estimate', 'Sold_For', 'By', 'Subject', 'Date', 'Publication', 'Condition', 'Color', 'Size', 'Text' ])
            else: 
                data_frame_2 = pd.DataFrame(np.array([data_list]), columns=['Auction', 'Lot', 'Image', 'Title', 'Estimate', 'Sold_For', 'By', 'Subject', 'Date', 'Publication', 'Condition', 'Color', 'Size', 'Text' ])
                #data_frame.append(data_frame_2, ignore_index=True)
                data_frame = pd.concat([data_frame, data_frame_2], ignore_index=True)
    
            
            ####################################
            #  Clean Dataframe
            ####################################     
            df_cleaner(data_frame, "Auction", ["Map Auction Sale No. ","\n","closed"], ["","",""])
            df_cleaner(data_frame, "Lot", ["Lot #"], [""])
            df_cleaner(data_frame, "Estimate", ["Estimate:","\n"], ["",""])
            df_cleaner(data_frame, "Sold_For", ["Sold for:","$","\n"], ["","",""])
            df_cleaner(data_frame, "By", ["By:","\n"], ["",""])
            df_cleaner(data_frame, "Subject", ["Subject:","\n"], ["",""])
            df_cleaner(data_frame, "Date", ["Date:","\n"], ["",""])
            df_cleaner(data_frame, "Publication", ["Publication:","\n"], ["",""])
            df_cleaner(data_frame, "Condition", ["Condition:","\r","\n"], ["","",""])
            df_cleaner(data_frame, "Color", ["Color:","\n"], ["",""])
            df_cleaner(data_frame, "Size", ["Size:","\n"], [""," "])
    
    
            #data_frame["Text"] = data_frame["Text"].str.replace("\n","")
            ####################################
            #  Splitting Frame
            ####################################        
            data_frame["Auction_No"] = data_frame["Auction"].str.split('-').str[0].str.replace(" ", "")
            data_frame["Auction_Close"] = data_frame["Auction"].str.split('-').str[1].str.replace(" ", "")
            
            data_frame["Estimate_Low"] = data_frame["Estimate"].str.split('-').str[0].str.replace(" ", "")
            data_frame["Estimate_High"] = data_frame["Estimate"].str.split('-').str[1].str.replace(" ", "")
            
            data_frame["Date_Low"] = data_frame["Date"].str.split('-').str[0].str.replace(" ", "")
            data_frame["Date_High"] = data_frame["Date"].str.split('-').str[1].str.replace(" ", "")
            
            data_frame["Size_Inches"] = data_frame["Size"].str.split('inches').str[0].str.replace(" ", "")
            data_frame["Size_Cm"] = data_frame["Size"].str.split('inches').str[1].str.replace("cm", "").str.replace(" ", "")         
            
            data_frame["Size_Cm_W"] = data_frame["Size_Cm"].str.split('x').str[0]        
            data_frame["Size_Cm_H"] = data_frame["Size_Cm"].str.split('x').str[1] 
          
            ####################################
            #  Formatting numbers
            ####################################  
            df_cleaner(data_frame, "Estimate_Low", [",","$"], ["",""])
            df_cleaner(data_frame, "Estimate_High",  [",","$"], ["",""])
            df_cleaner(data_frame, "Sold_For", [",","$"], ["",""])
            
            #increase counter
            archive_lots_links_counter += 1
            
            print("Finished lot %i of %i, that is %f percent" %(archive_lots_links_counter, number_of_lot_links, float(archive_lots_links_counter*100.00/number_of_lot_links*1.00)))
            
    
    
    #print("Counter at inner loop finish: %i" % archive_lots_links_counter)
    file_path = "/home/user/Projects/owascrp/Outputs/";    
    #file_path = "/home/user/Projects/Owa_Scrape/Outputs/";
    
    file_path_logs = "/home/user/Projects/owascrp/Outputs/Logs/";    
    #file_path_logs = "/home/user/Projects/Owa_Scrape/Outputs/Logs/";
    
    data_frame.to_csv(file_path + curr_auction.replace(" ", "")[0:20] +".csv", sep=';', encoding='utf-8')
    
    ####################################
    #  Create Logfile for auction_scrape
    ####################################
    log_text = "Log-File: \n -------------------------------------- \n"
    for col in data_frame.columns:
          log_text = log_text + "Von % i Werten %i Null-Werte in Spalte %s \n" %(len(data_frame[col]), sum(pd.isnull(data_frame[col])), col)
          
          
    with open(file_path_logs + curr_auction.replace(" ", "")[0:20] +".log", "w") as text_file:
        text_file.write(log_text)
        
    #increase counter
    archive_price_links_counter += 1    
        
####################################
#  End Loop
####################################    
