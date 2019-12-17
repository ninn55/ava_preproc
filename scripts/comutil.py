#----------------------------------------------------#
#Path: /script/comutil.py
#Discription: Common utility functions
#Dependency: None
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
import argparse
import os
import subprocess
import csv
import sys
import warnings
import json

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def mkdir_p(path):
    try:
        _supermakedirs(path, 0o775) # Supporting Python 2 & 3
    except OSError: # Python >2.5
        pass          

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def _supermakedirs(path, mode):
    if not path or os.path.exists(path):
        return []
    (head, _) = os.path.split(path)
    res = _supermakedirs(head, mode)
    os.mkdir(path)
    os.chmod(path, mode)
    res += [path]
    return res

#----------------------------------------------------#
#Read base CSV file and parse it to set
#{(video_id, time_id):[]}
#----------------------------------------------------#
def read_csv(fl) -> set:
    with open(fl, 'r') as f:
        dic = set()
        reader = list(csv.reader(f))
        for i in reader:
            temp = (i[0], i[1])
            if temp in dic:
                warnings.warn("WARNING. Keys %(temp)s already parsed."%{"temp": temp})
            dic.add(temp)
    return dic

#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    sys.exit("ERROR. This is a common utility file. Not run directly.")