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

parser = argparse.ArgumentParser()
parser.add_argument("--annot_file", default="./preproc_fallDown/ava_v1.0_extend_annot.csv",
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

def mvkframe(video_id:str, time_id:str):
    outpath = os.path.join(outdir_keyframes, video_id)
    mkdir_p(oupath)
    datapath = os.path.join(datadir_keyframes, video_id)
    datapath = os.path.join((datapath, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":img_suffix})
    werror = subprocess.call("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        sys.exit("ERROR. %(video_id)s %(time_id)s frame copy failed. Exit."%{"video_id":video_id, "time_id":time_id})

def mvclip(video_id:str, time_id:str):
    outpath = os.path.join(outdir_clips, video_id)
    mkdir_p(oupath)
    datapath = os.path.join(datadir_clips, video_id)
    datapath = os.path.join((datapath, "%(time_id)s%(suffix)s"%{"time_id":time_id, "suffix":img_suffix})
    werror = subprocess.call("cp %(datapath)s %(outpath)s"%{"datapath":datapath, "outpath":outpath} , shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        sys.exit("ERROR. %(video_id)s %(time_id)s clip copy failed. Exit."%{"video_id":video_id, "time_id":time_id})

def mv():
    files = read_csv(annotfile)
    for i in files:
        video_id = i[0]
        time_id = i[1]
        mvkframe(video_id, time_id)
        mvclip(video_id, time_id)

if __name__ == '__main__':
    print("Moveing.")
    mv()