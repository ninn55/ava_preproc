#----------------------------------------------------#
#Path: /script/comutil.py
#Discription: Common utility functions
#Dependency: None
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
#common imports
import argparse
import csv
import json
import logging
import os
import subprocess
import sys
import warnings

from libs.decorator import log_on_end, log_on_error, log_on_start
from usrexception import *

#Logger definition

#Default log files path
logfilepath = "./logs"
logfiledebug = "debug.log"
logfileinfo = "info.log"
logfileerror = "error.log"

# Mkae logger dir if not exist
mkdir_p(logfilepath)
globallogger = logging.getLogger("globallogger")
#Global log level change for deployment.
globallogger.setLevel(logging.DEBUG)

#DEbug level handler
debughandler = logging.FileHandler(os.path.join(logfilepath, logfiledebug))
debughandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(funcName)s - %(message)s"))

#Info level handler
infohandler = logging.FileHandler(os.path.join(logfilepath, logfileinfo))
infohandler.setLevel(logging.INFO)
infohandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(filename)s[:%(lineno)s] - %(funcName)s - %(message)s"))

#Error level handler
errorhandler = logging.FileHandler(os.path.join(logfilepath, logfileerror))
errorhandler.setLevel(logging.ERROR)
errorhandler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(process)d[:%(thread)d] - %(filename)s[:%(lineno)s] - %(funcName)s - %(message)s"))

#Add handlers to global logger
globallogger.addHandler(debughandler)
globallogger.addHandler(infohandler)
globallogger.addHandler(errorhandler)

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
#@log_on_start(logging.DEBUG, "Make directory '[path:s]'", logger = globallogger)
@log_on_end(logging.INFO, "Make directory '[path:s]' successful", logger = globallogger)
@log_on_error(logging.ERROR, "Make directory '[path:s]' failed, use python version 2.5 above",
                on_exceptions = OSError, reraise = True, logger=globallogger)
def mkdir_p(path: str):
    #try:
    _supermakedirs(path, 0o775) # Supporting Python 2 & 3
    #except OSError: # Python >2.5
    #    pass          

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

@log_on_start(logging.DEBUG, "Running '[usrcmd:s]'", logger = globallogger)
@log_on_end(logging.INFO, "Running '[usrcmd:s]' successful", logger = globallogger)
@log_on_error(logging.INFO, "Error ocuured when running '[usrcmd:s]'",
                on_exceptions = (ShellError), reraise = False, logger = globallogger)
def call_p(usrcmd: str):
    werror = subprocess.call(usrcmd, shell = True , stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        raise ShellError
    return werror

@log_on_error(logging.INFO, "Error ocuured when running '[usrcmd:s]'",
                on_exceptions = (ShellError, subprocess.CalledProcessError), reraise = False, logger = globallogger)
def checkoutput_p(usrcmd: str):
    werror = subprocess.check_output(usrcmd, shell = True , stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    return werror

#----------------------------------------------------#
#Read base CSV file and parse it to set
#{(video_id, time_id):[]}
#----------------------------------------------------#
#@log_on_start(logging.DEBUG, "Starting read csv file '[fl:s]'", logger = globallogger)
@log_on_end(logging.INFO, "Read CSV file '[fl:s]' successful", logger = globallogger)
@log_on_error(logging.ERROR, "Make directory '[path:s]' failed, use python version 2.5 and above", 
                on_exceptions = (FileNOTFound, FileNotFoundError), reraise = True, logger=globallogger)
def read_csv(fl: str) -> set:
    werror = subprocess.call("ls %(file)s*"%{"file": fl}, shell = True)
    if werror != 0:
        raise FileNOTFound 
    with open(fl, 'r') as f:
        dic = set()
        reader = list(csv.reader(f))
        for i in reader:
            temp = (i[0], i[1])
            if temp in dic:
                #warnings.warn("WARNING. Keys %(temp)s already parsed."%{"temp": temp})
                globallogger.log(logging.DEBUG, "Keys %(temp)s already parsed."%{"temp": temp})
            else:
                dic.add(temp)
    return dic

#----------------------------------------------------#
#Check a file is video or not using ffprobe.
#----------------------------------------------------#
#dir: full path or relative path to a video file.
#----------------------------------------------------#
#True for it is video.
#----------------------------------------------------#
@log_on_end(logging.DEBUG, "Starting checking file '[dir:s]' {result!r}.", logger = globallogger)
def check_vid(dir: str) -> bool:
    command  = "ffprobe %(video_dir)s" % {"video_dir": dir}
    globallogger.log(logging.DEBUG, command)
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
