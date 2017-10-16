# -*- coding: utf-8 -*-
"""
Created on Tue Oct 10 18:51:22 2017

@author: MBAUMGAR
"""


#######################
# Read list of picture pathes from file
#  remove thumb/ element from path to download large size pic (not thumb)
#  get name of pic from path
#  iterate over A, B, C pathes 
########################

import pandas as pd
import urllib 
import re


#spezifizieren Pfad der Excel Datei
path_name = "C://lokal_//MyApps//owascrp//Outputs//Merged//"
file_name = "owa_merged_116_163.csv"

#Liste in Data Frame lesen
data_raw = pd.read_csv(path_name+file_name, delimiter=";")

# ACHTUNG: OPTIONAL --- delete unwanted or done auctions 
data_raw = data_raw[data_raw["Auction_No"]>162]
#data_raw = data_raw[data_raw["Auction_No"]<117]

#Column of Pictures 
pic_path_thumb_col = data_raw["Image"]
#Column of Pictures without "Thumb/" path element
pic_path_col = pic_path_thumb_col.apply(lambda picpath: str(picpath).replace('thumbs/',''))

# -----------------------------------------------
#   Iterate the pictures in the file
# -----------------------------------------------

letter_count = 0
error_not_set = True
prefix_array = ["A", "B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S", "T", "U", "V", "W", "X", "Y", "Z"]

# Outer Loop: Counter of picpathes
for row in pic_path_col:
    print ("Current path at reading is:" + row)
    # Inner Loop: counter of prefix array
    while error_not_set: 
        letter = prefix_array[letter_count]
        letter_count += 1
        #change letter in picpath
        picpath_newletter = row.replace('A.jpg', letter + '.jpg')
            
        #get name of picture (regex means: everything after last / ) 
        curr_picname = re.search(r"[^/]*$",picpath_newletter).group()  

        # ERROR HANDLING  - Check if path exists
        req = urllib.request.Request(picpath_newletter)
        try:
            response = urllib.request.urlopen(req)
        except urllib.error.HTTPError as e:
            # do something
            print('Error code: ', e.code)
            error_not_set = False
        except urllib.error.URLError as e:
            # do something
            print('Reason: ', e.reason)
            error_not_set = False
        else:
            #path exists - save file
            #write picture
            f = open("C://lokal_//MyApps//owascrp//Outputs//Pics//" + curr_picname , 'wb')
            f.write(urllib.request.urlopen(picpath_newletter).read())
            f.close()
                
            print("Write pic number named " + curr_picname)
            
    #reset other command variables
    error_not_set = True
    letter_count = 0
    