file_path_merged = "C:\\lokal_\\MyApps\\owascrp\\Outputs\\Merged\\";
file_path = "C:\\lokal_\\MyApps\\owascrp\\Outputs\\";

#file_path = "/home/user/Projects/owascrp/Outputs/";

header = 1
first_auction = 162
last_auction = 163


fout=open(file_path_merged+"owa_merged_"+str(first_auction)+ "_" + str(last_auction)+".csv","a")
for num in range(first_auction,last_auction+1):
    row_num = 0
 #   for line in open(file_path+"MapAuctionSaleNo."+str(num)+".csv"):
    for line in open(file_path+"MapAuctionSaleNo."+str(num)+".csv"):
        print(row_num)
        
        # Nur den Header beim ersten File mitnehmen, danach wird einfach die Reihe übersprungen
        if header == 1:
            fout.write(line)    
            header = 0
            row_num += 1
            
        else:
            if row_num == 0:
                row_num += 1
            else:
                fout.write(line) 
                row_num += 1
                
fout.close()



