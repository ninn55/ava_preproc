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
from logging import DEBUG, ERROR, INFO
from libs.decorator import log_on_start, log_on_end, log_on_error

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
#Check a file is video or not using ffprobe.
#----------------------------------------------------#
#dir: full path or relative path to a video file.
#----------------------------------------------------#
#True for it is video.
#----------------------------------------------------#
def check_vid(dir: str) -> bool:
    command  = "ffprobe %(video_dir)s" % {"video_dir": dir}
    werror = subprocess.call(command, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror == 0:
        return True
    else:
        return False

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def hou_min_sec(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000 * 60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000 * 60 * 60))
    return "%d:%d:%d" % (hours, minutes, seconds)

#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    sys.exit("This is a common utility file. Not run directly.")