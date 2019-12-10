#----------------------------------------------------#
#Path: /script/cpfile.py
#Discription: Copy annotated file from folders
#Dependency: None
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

import subprocess
import argparse
from parsejson import read_csv
from gen_keyframe import mkdir_p
import os
import sys
import csv
import warnings
import copy

parser = argparse.ArgumentParser()
parser.add_argument("--annot_file", default="../falldown/ava_v1.0_extend_annot.csv",
                    help="Anotation file path.")

parser.add_argument("--data_dir", default="./preproc_fallDown", help="Data path.")
parser.add_argument("--output_dir", default="../falldown", help="Output path.")

FLAGS = parser.parse_args()

annotfile = FLAGS.annot_file
outdir = FLAGS.output_dir
datadir = FLAGS.data_dir

datadir_clips = os.path.join(datadir, "clips")
datadir_keyframes = os.path.join(datadir, "keyframes")

outdir_clips = os.path.join(outdir, "clips")
outdir_keyframes = os.path.join(outdir, "keyframes")

img_suffix = ".jpg"
vid_suffix = ".mp4"

def mvkframe(video_id:str, time_id:str):
    outpath = os.path.join(outdir_keyframes, video_id)
    mkdir_p(outpath)
    datapath = os.path.join(datadir_keyframes, video_id)
    datapath = os.path.join(datapath, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":img_suffix})
    print("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath})
    werror = subprocess.call("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        sys.exit("ERROR. %(video_id)s %(time_id)s frame copy failed. Exit."%{"video_id":video_id, "time_id":time_id})

def mvclip(video_id:str, time_id:str):
    outpath = os.path.join(outdir_clips, video_id)
    mkdir_p(outpath)
    datapath = os.path.join(datadir_clips, video_id)
    datapath = os.path.join(datapath, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":vid_suffix})
    print("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath})
    werror = subprocess.call("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        sys.exit("ERROR. %(video_id)s %(time_id)s clip copy failed. Exit."%{"video_id":video_id, "time_id":time_id})

def mv():
    files = read_csv(annotfile)
    delunvalid(unvalidframes(files))
    files = read_csv(annotfile)
    for i in files:
        video_id = i[0]
        time_id = i[1]
        mvkframe(video_id, time_id)
        mvclip(video_id, time_id)

def unvalidframes(annot_csv: set) -> set:
    dic = set()
    for i in annot_csv:
        video_id = i[0]
        time_id = i[1]
        datapath = os.path.join(datadir_keyframes, video_id)
        datapath = os.path.join(datapath, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":img_suffix})
        werror = subprocess.call("ls %(datapath)s*"%{"datapath":datapath} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        datapath1 = os.path.join(datadir_clips, video_id)
        datapath1 = os.path.join(datapath1, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":vid_suffix})
        werror1 = subprocess.call("ls %(datapath)s*"%{"datapath":datapath1} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if werror != 0 or werror1 != 0:
            temp = (video_id, time_id)
            if temp not in dic:
                dic.add(temp)
    return dic

def delunvalid(dic: set):
    with open(annotfile, 'r') as f:
        reader = list(csv.reader(f))
    temp = copy.deepcopy(reader)
    for i in range(len(reader)):
        if (reader[i][0], reader[i][1]) in dic:
            warnings.warn("WARNING. Delete unvlid data %(video_id)s %(time_id)s"%{"video_id": reader[i][0], "time_id": reader[i][1]})
            temp.remove(reader[i])
    #print(temp)
    with open(annotfile, 'w') as f:
        wr = csv.writer(f)
        for i in temp:
            wr.writerow(i)
    print("Write successful.")
        
if __name__ == '__main__':
    print("Moveing.")
    mv()