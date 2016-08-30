file_path_merged = "/home/user/Projects/owascrp/Outputs/Merged/";
file_path = "/home/user/Projects/owascrp/Outputs/";

#file_path = "/home/user/Projects/owascrp/Outputs/";

header = 1

fout=open(file_path_merged+"owa_merged.csv","a")
for num in range(116,154):
    row_num = 0
    for line in open(file_path+"MapAuctionSaleNo."+str(num)+".csv"):
        print(row_num)
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



