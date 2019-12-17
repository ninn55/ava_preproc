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
from gen_keyframe import *

#Initial csv path ./preproc_fallDown/ava_v1.0_extend.csv
out_csv = os.path.join(outdir, "ava_v1.0_extend.csv")
#Clips output path ./preproc_fallDown/clips
outdir_clips = os.path.join(outdir, "clips")
#Change clean condition to bool
con = bool(con)

#Video suffix, default mp4
vid_suffix = ".mp4"
#Clip length
clip_length = 3 # seconds
#Clip padding
clip_time_padding = 1.0 # seconds
#Timr interval between key frames
interval = 1

#----------------------------------------------------#
#Read generated csv 
#----------------------------------------------------#
#out_csv    csv file path
#----------------------------------------------------#
#frameloc    2D list containing video_id and frame location
#----------------------------------------------------#
def rd_basecsv(out_csv: str)->list:
    with open(out_csv, 'r') as filecsv:
        #overwrite input list
        frameloc = list(csv.reader(filecsv))
    return frameloc

#----------------------------------------------------#
#Write clips
#----------------------------------------------------#
#frameloc       |  2D list containing video_id and frame location
#usecsv         |  use csv file or input list directly
#out_csv        |  csv file path
#vid_suffix     |  suffix of video
#vidduration    |  Dictionary of video, video_id:video_duration, str:int
#outdir_clips   |  Clips output path
#----------------------------------------------------#
#NO Output
#----------------------------------------------------#
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

    #Call get_clips individually
    for i in frameloc:
        video_id = i[0]
        fl = i[1]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        temp = get_clips(videofile, video_id, vidduration, fl, outdir_clips)

#----------------------------------------------------#
#Write clips
#----------------------------------------------------#
#videofile      |  Full file path 
#video_id       |  Video id, file name with no extension
#vidduration    |  Dictionary of video, video_id:video_duration, str:int
#time_id        |  Count from start of the video in second
#outdir_clips   |  Clips output path
#----------------------------------------------------#
#NO Output argu
#----------------------------------------------------#
def get_clips(videofile: str, video_id: str, vidduration: dict, time_id: str, outdir_clips: str):
    #Input check
    #Debug
    #print(int(vidduration[video_id]) - int(time_id))
    #if int(vidduration[video_id]) - int(time_id) <= (clip_length + clip_time_padding):
    #    warnings.warn("Clip too long for video file.")
    #    return
    
    outdir_folder = os.path.join(outdir_clips, video_id)
    mkdir_p(outdir_folder)
    clip_start = float(int(time_id)) - clip_time_padding - float(clip_length) / 2
    if clip_start < 0:
        #clip_start = 0
        warnings.warn("WARNING. %(video_id)s %(time_id)s clip too long for video file."%{"video_id":video_id, "time_id":time_id})
        return
    clip_end = float(int(time_id)) + float(clip_length) / 2
    if clip_end > vidduration[video_id]:
        #clip_end = vidduration[video_id]
        warnings.warn("WARNING. %(video_id)s %(time_id)s clip too long for video file."%{"video_id":video_id, "time_id":time_id})
        return
    outpath_clip = os.path.join(outdir_folder, '%d%s' % (int(time_id), vid_suffix))

    werror = subprocess.call("ls %(outpath)s*" % {'outpath': outpath_clip}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    #werror = 1
    if werror != 0:
        #Generate clips
        ffmpeg_command = 'ffmpeg -hide_banner -loglevel panic -i %(videopath)s -ss %(start_timestamp)s -g 1 -force_key_frames 0 -to %(end_timestamp)s %(outpath)s' % {
                          'start_timestamp': hou_min_sec(clip_start * 1000),
                          'end_timestamp': hou_min_sec(clip_end * 1000),
                          #'clip_length': clip_length + clip_time_padding,
                          'videopath': videofile,
                          'outpath': outpath_clip}
        print(ffmpeg_command)
        code = subprocess.call(ffmpeg_command, shell=True)
        #Add exit code check
        if code != 0:
            sys.exit("ERROR ffmpeg write frame fail. CODE %(error)s" % {"error": code})
    else:
        warnings.warn("WARNING. Frame file already exist.")

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
#Cleanup clips generated by this script
#----------------------------------------------------#
#outdir_clips Clips output path
#----------------------------------------------------#
def clean(outdir_clips: str):
    warnings.warn("CLEANING CAUTION")
    error = subprocess.call("rm -r %(outdir_clips)s/"% {"outdir_clips": outdir_clips}, shell = True)

#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    if con:
        print("Cleaning project.")
        clean(outdir_clips)

    bshfile = os.path.join(videodir, "copy_file_in.sh")
    subprocess.call("sh %(bshfile)s" % {"bshfile": bshfile}, shell = True)
    print("Generating video list.")
    videolist = gen_vidList(videodir, vid_suffix)
    print("Genetating video duration")
    vidduration = gen_vidduration(videodir, videolist, vid_suffix)
    print("Generating CSV file.")
    frameloc = gen_basecsv(videodir, videolist, vidduration, True, interval, out_csv)
    print("Generating clips")
    write_clips(frameloc, True, out_csv, vid_suffix, vidduration, outdir_clips)