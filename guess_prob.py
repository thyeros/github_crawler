import re
import csv
import os
import string

valid_chars = "-_.() %s%s" % (string.ascii_letters, string.digits)

prob_dict = {}
sample_dict = {}
stat_dict={}

def cleanse_str(test):
    test = test.strip()
    test = test.replace("v1","v_one");
    test = test.replace("v2","v_two");
    test = test.replace('-','');
    test = test.replace('_','');
    test = test.replace('(','');
    test = test.replace(')','');
    test = ''.join(test.split())
    test = test.lower()
    return test

def create_sample():
    os.system("mkdir -p samples")

    with open("../prob_list.csv") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        for row in csv_reader:
            number = row[0]
            name = row[1]

            sample_dict[number] = "samples/"+number;

            cmd = "mkdir -p "+sample_dict[number]
            #print cmd      
            os.system(cmd)

            name = cleanse_str(name)

            stat_dict[number] = 0
            prob_dict[name] = number
            

            # prob_dict[number] = number


def guess_by_name(curname): 
    key = curname 
    if key in prob_dict:
        return prob_dict[key]

    match = re.search(r"([a-z]+)$", curname)
    if match:
        key = match.group(1).strip()
        if key in prob_dict:
            return prob_dict[key]
 
    match = re.search(r"^([a-z]+)", curname)
    if match:
        key = match.group(1).strip()
        if key in prob_dict:
            return prob_dict[key]

    return ""
 

def guess_by_number(curname):
    key = curname 
    if key in prob_dict:
        return prob_dict[key]

    match = re.search(r"(\d+)$", curname)
    if match:
        key = str(int(match.group(1).strip()))
        if key in prob_dict:
            return prob_dict[key]
 
    match = re.search(r"^(\d+).*", curname)
    if match:
        key = str(int(match.group(1).strip()))
        if key in prob_dict:
            return prob_dict[key]

    return ""

def ignore_by_name(curname):
    match = re.search(r"test", curname)   
    if match:
        return True
    return False

create_sample()

ext_dic = {".cpp":1, ".c":2, ".hpp":3, ".h":4, ".java":11, ".js":12, ".py":21, ".go":31}
num_tested = 0
num_mapped = 0;

f = open("../file_list.txt", "r")
for line in f:
    test = line.strip()
    curext = os.path.splitext(test)[1]

    if curext not in ext_dic:
        continue
    

    test = cleanse_str(test)
    

    #filename
    curbase = os.path.basename(test);
    curbase = os.path.splitext(curbase)[0]
    curbase = curbase.replace('.','')
    curbase = ''.join(c for c in curbase if c in valid_chars)

    #remove filename and check dir
    curdir = os.path.basename(os.path.dirname(test)) 
    curdir = curdir.replace('.','')

    #remove filename and check dir
    prvdir = os.path.basename(os.path.dirname(os.path.dirname(test)))
    prvdir = prvdir.replace('.','')    

    print("======{}:{}:{}:{}".format(curbase, curdir, prvdir, test))   


    if(ignore_by_name(curdir) or ignore_by_name(curbase)):
        continue


    cur_dict = {} 
    
    prob_num = guess_by_name(curbase)
    if prob_num is not "":
        cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1

    prob_num = guess_by_number(curbase)
    if prob_num is not "":
        cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1


    if len(cur_dict) == 0:
        prob_num = guess_by_name(curdir)
        if prob_num is not "":
            cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1

        prob_num = guess_by_name(prvdir)
        if prob_num is not "":
            cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1

        prob_num = guess_by_number(curdir)
        if prob_num is not "":
            cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1

        prob_num = guess_by_number(prvdir)
        if prob_num is not "":
            cur_dict[prob_num] = cur_dict.get(prob_num, 0) + 1

    num_tested = num_tested+1

    if len(cur_dict) == 0:
        print ("{} {}".format("??", line))
    elif len(cur_dict) == 1:
        num_mapped = num_mapped+1
        for key in cur_dict:
            print ("{} {}".format(key, line))

            cmd = "ln -sf \"../../"+line.strip()+"\" "+sample_dict[key]+"/"+str(stat_dict[key])+curext
            print(cmd)      
            os.system(cmd)

            stat_dict[key] = stat_dict[key] + 1

    else:
        for key in cur_dict:
            print ("!!{} {}".format(key, line))
 
print (num_mapped,"/",num_tested)

for key in sorted(stat_dict):
    print ("{} {}".format(key, stat_dict[key]))

