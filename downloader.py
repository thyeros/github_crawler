import csv
import os


with open('repositories.csv', newline='') as csvfile:
    gitreader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in gitreader:        
        cmd = "wget "+row[4]+" -O ./"+row[1]+"_"+row[2]+".zip"
        print(cmd)
        os.system(cmd)
