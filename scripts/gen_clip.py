#----------------------------------------------------#
#Path: /script/gen_clip.py
#Discription: Generate video clips from csv, used for latter annotation
#Dependency: FFMPEG
#Extra: Refactored from extract_keyframe.py from github.com/kevinlin311tw/ava-dataset-tool
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
from gen_keyframe import mkdir_p, gen_vidList, gen_vidduration, gen_basecsv
import os
import subprocess
import sys
import csv
import warnings
import argparse

#Parse command line argument
parser = argparse.ArgumentParser()
#Use reletive path
#input Video path ./vid_fallDown
parser.add_argument("--video_dir", default="./vid_fallDown", help="Videos source path.")
parser.add_argument("--output_dir", default="./preproc_fallDown", help="Output directory.")
parser.add_argument("--clean", default="", help="Clean directory or not.")

FLAGS = parser.parse_args()

videodir = FLAGS.video_dir
outdir = FLAGS.output_dir
con = FLAGS.clean

#Initial csv path ./preproc_fallDown/ava_v1.0_extend.csv
out_csv = os.path.join(outdir, "ava_v1.0_extend.csv")
#Clips output path ./preproc_fallDown/clips
outdir_clips = os.path.join(outdir, "clips")
#Change clean condition to bool
con = bool(con)

#Video suffix, default mp4
vid_suffix = ".mp4"
clip_length = 3 # seconds
clip_time_padding = 1.0 # seconds

def rd_basecsv(out_csv: str)->list:
    with open(out_csv, 'r') as filecsv:
        #overwrite input list
        frameloc = list(csv.reader(filecsv))
    return frameloc

def write_clips(frameloc:list, usecsv: bool, out_csv: str, vid_suffix: str, vidduration: dict, outdir_clips: str):
    #Input check
    if usecsv: 
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode != 0:
            sys.exit("ERROR csv file in %(csv)s donot exist. CODE $(error)s"% {"csv": out_csv, "error": wcode})
    else:
        if len(frameloc) == 0:
            sys.exit("ERROR directory donnot contain any video. CODE 3")

    if usecsv:
        #overwrite input list
        frameloc = rd_basecsv(out_csv)

    for i in frameloc:
        video_id = i[0]
        fl = i[1]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        temp = get_clips(videofile, video_id, vidduration, fl, outdir_clips)

def get_clips(videofile, video_id, vidduration, time_id, outdir_clips):
    #Input check
    if vidduration[video_id] - time_id <= (clip_length + clip_time_padding):
        warnings.warn("Clip too long for video file.")
        return
        
    outdir_folder = os.path.join(outdir_clips, video_id)
    mkdir_p(outdir_folder)
    clip_start = time_id - clip_time_padding - float(clip_length) / 2
    if clip_start < 0:
        clip_start = 0
    clip_end = time_id + float(clip_length) / 2
    outpath_clip = os.path.join(outdir_folder, '%d.%s' % (int(time_id), vid_suffix))

    ffmpeg_command = 'rm %(outpath)s;  \
                      ffmpeg -ss %(start_timestamp)s -i \
                      %(videopath)s -g 1 -force_key_frames 0 \
                      -t %(clip_length)d %(outpath)s' % {
                          'start_timestamp': hou_min_sec(clip_start * 1000),
                          # 'end_timestamp': hou_min_sec(clip_end * 1000),
                          'clip_length': clip_length + clip_time_padding,
                          'videopath': videofile,
                          'outpath': outpath_clip}
    subprocess.call(ffmpeg_command, shell=True)

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
    subprocess.call("sh vid_fallDown/copy_file_in.sh", shell = True)
    videolist = gen_vidList(videodir, vid_suffix)
    vidduration = gen_vidduration(videodir, videolist, vid_suffix)
    frameloc = gen_basecsv(videodir, videolist, vidduration, True, interval, out_csv)
    write_clips(frameloc, True, out_csv, vid_suffix, vidduration, outdir_clips)