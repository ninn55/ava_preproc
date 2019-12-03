#----------------------------------------------------#
#Path: /script/gen_keyframe.py
#Discription: Generate key frames and csv used for latter annotation
#Dependency: FFMPEG FFPROBE GIT
#Extra: Refactored from extract_keyframe.py from github.com/kevinlin311tw/ava-dataset-tool
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

#Keyframe output path ./preproc_fallDown/keyframes
outdir_keyframes = os.path.join(outdir, "keyframes")
#Initial csv path ./preproc_fallDown/ava_v1.0_extend.csv
out_csv = os.path.join(outdir, "ava_v1.0_extend.csv")
#Change clean condition to bool
con = bool(con)

#Video suffix, default mp4
vid_suffix = ".mp4"
#Frame interval in seconds
interval = 1

#----------------------------------------------------#
#Extract a single frame from video file using ffmpeg
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
#Input arg
#videofile        |  Full file path
#video_id         |  Video id, file name with no extension
#time_id          |  Count from start of the video in second
#outdir_keyframes |  Full keyframe output path
#----------------------------------------------------#
#Output arg
#outpath          |  Full path of output video
#----------------------------------------------------#
def get_keyframe(videofile: str, video_id: str, time_id: str, outdir_keyframes: str) -> str: 
    outdir_folder = os.path.join(outdir_keyframes, video_id)
    mkdir_p(outdir_folder)
    outpath = os.path.join(outdir_folder, '%d.jpg' % (int(time_id)))
    werror = subprocess.call("ls %(outpath)s*" % {'outpath': outpath}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    #werror = 1
    if werror != 0:
        #generat ungenerated key frames
        ffmpeg_command = 'ffmpeg -hide_banner -loglevel panic -ss %(timestamp)f -i %(videopath)s \
                          -frames:v 1 %(outpath)s' % {
                          'timestamp': float(time_id),
                          'videopath': videofile,
                          'outpath': outpath}
        print(ffmpeg_command)
        code = subprocess.call(ffmpeg_command, shell=True)
        #Add exit code check
        if code != 0:
            sys.exit("ERROR ffmpeg write frame fail. CODE %(error)s" % {"error": code})
    else:
        warnings.warn("WARNING. Frame file already exist.")
    return outpath

#----------------------------------------------------#
#Write key frames
#----------------------------------------------------#
#Input arg
#videodir           |  video file directory
#frameloc           |  2D list containing video_id and frame location
#vid_suffix         |  suffix of video
#usecsv             |  use csv file or input list directly
#outdir_keyframes   |  Keyframe output path
#out_csv            |  csv file path
#----------------------------------------------------#
#NO output arg
#----------------------------------------------------#
def write_keyframe(videodir: str, frameloc: list, vid_suffix: str, usecsv: bool, outdir_keyframes: str, out_csv: str):
    #Input check
    if usecsv: 
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode != 0:
            sys.exit("ERROR csv file in %(csv)s donot exist. CODE $(error)s"% {"csv": out_csv, "error": wcode})
    else:
        if len(frameloc) == 0:
            sys.exit("ERROR directory donnot contain any video. CODE 3")

    #parse csv file into list
    if usecsv:
        with open(out_csv, 'r') as filecsv:
            #overwrite input list
            frameloc = list(csv.reader(filecsv))

    for i in frameloc:
        video_id = i[0]
        fl = i[1]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        temp = get_keyframe(videofile, video_id, fl, outdir_keyframes)

#----------------------------------------------------#
#generate predefined csv file for this specific case
#----------------------------------------------------#
#Input arg      
#videodir       |  video file directory
#videolist      |  List of video_id(str)
#vidduration    |  Dictionary of video, video_id:video_duration, str:int
#writeindex     |  write to csv or not. bool.
#interval       |  time interval between frames
#out_csv        |  csv file output directory
#----------------------------------------------------#
#Output arg
#frameloc       |  2D list containing video_id and frame location
#----------------------------------------------------#
def gen_basecsv(videodir: str, videolist: list, vidduration: dict, writeindex: bool, interval: float, out_csv: str) -> list: 
    #Input check
    if len(videolist) != len(vidduration):
        sys.exit("ERROR inner logic error. CODE 2")
    if len(videolist) == 0 or len(vidduration) == 0:
        sys.exit("ERROR directory donnot contain any video. CODE 3")
    List = []
    for i in videolist:
        video_id = i[0] #String
        duration = vidduration[video_id] #Int
        #Discard first and last frame
        for j in range(1, duration, interval):
            temp = [video_id, str(j)]
            List.append(temp)
    
    #Write List to csv file
    if writeindex:
        #File exist check        
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode == 0:
            warnings.warn("WARNING csv file already exist, not generate.")
            return List
        #Open and write file
        with open(out_csv, 'w') as filecsv:
            wr = csv.writer(filecsv)
            for i in List:
                wr.writerow(i)
    return List
            
    
#----------------------------------------------------#
#Generate list of video 
#----------------------------------------------------#
#Input arg
#videodir:      video file directory
#vid_suffix:    suffix of video
#----------------------------------------------------#
#Output arg
#videolist:     List of video_id(str)
#----------------------------------------------------#
def gen_vidList(videodir: str, vid_suffix: str) -> list: 
    # Auto exit check
    videos = subprocess.check_output("ls %(videodir)s" %{"videodir": videodir}, shell=True)
    #Last item in list is ""
    videos = videos.decode('utf8')
    videos = videos.split('\n')
    List = []
    for i in videos:
        temp = []
        if i.endswith(vid_suffix):
            #no suffix needed
            temp.append(i.split(".")[0])
            List.append(temp)
    return List

#----------------------------------------------------#
#Generate video duration dictionary using ffprobe
#----------------------------------------------------#
#Input arg
#videodir:      video file directory
#videolist:     List of video_id(str)
#vid_suffix:    suffix of video
#----------------------------------------------------#
#Output arg
#vidduration:   Dictionary of video, video_id:video_duration, str:int
#----------------------------------------------------#
def gen_vidduration(videodir: str, videolist: list, vid_suffix: str) -> dict: 
    dic = {}
    for i in videolist:
        video_id = i[0]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        ffprobe_command = "ffprobe -i %(videofile)s \
                            -show_format -v quiet | grep duration" % {
                                "videofile": videofile}
        # Auto exit check        
        temp = subprocess.check_output(ffprobe_command, shell = True).decode("utf8")
        temp = temp.split('=')[1]
        duration = int(float(temp.split("\n")[0]))
        if video_id in dic:
            pass
        else:
            dic[video_id] = duration
    return dic

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
#Clean up key frames and CSV files generated by this script
#----------------------------------------------------#
#Input arg
#outdir_keyframes   Keyframe output path
#out_csv            csv file output directory
#----------------------------------------------------#
def clean_all(outdir_keyframes: str, out_csv: str):
    warnings.warn("CLEANING CAUTION")
    error = subprocess.call("git clean -fx", shell = True)
    error = subprocess.call("rm -r %(outdir_keyframes)s/"% {"outdir_keyframes": outdir_keyframes}, shell = True)
    
#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    if con:
        print("Cleaning project.")
        clean_all(outdir_keyframes, out_csv)
    subprocess.call("sh vid_fallDown/copy_file_in.sh", shell = True)
    print("Generating video list.")
    videolist = gen_vidList(videodir, vid_suffix)
    print("Genetating video duration")
    vidduration = gen_vidduration(videodir, videolist, vid_suffix)
    print("Generating CSV file.")
    frameloc = gen_basecsv(videodir, videolist, vidduration, True, interval, out_csv)
    print("Generating keyframes")
    write_keyframe(videodir, frameloc, vid_suffix, False, outdir_keyframes, out_csv)