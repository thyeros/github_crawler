import csv
import os


with open('repositories.csv', newline='') as csvfile:
    gitreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in gitreader:        
        filename = "./"+row[1]+"_xxx_"+row[2]+".zip"

        if(os.path.isfile(filename)):     
            print(filename," already there")       
            continue

        cmd = "wget "+row[4]+" -O "+filename
        print(cmd)
        os.system(cmd)
