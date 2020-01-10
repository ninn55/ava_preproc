#----------------------------------------------------#
#Path: /script/gen_clip.py
#Discription: Generate video clips from csv, used for latter annotation
#Dependency: FFMPEG,  Git
#Extra: Refactored from extract_keyframe.py from github.com/kevinlin311tw/ava-dataset-tool
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
from genkeyframe import *

#Clips output path ./preproc_fallDown/clips
outdir_clips = os.path.join(outdir, "clips")

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
@log_on_error(logging.ERROR, "CSV file '[out_csv:s]' not found.", 
            on_exceptions = (FileNOTFound, FileExistsError), reraise = True , logger=globallogger)
def write_clips(frameloc:list, usecsv: bool, out_csv: str, vid_suffix: str, vidduration: dict, outdir_clips: str):
    #Input check
    if usecsv: 
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode != 0:
            #sys.exit("ERROR csv file in %(csv)s donot exist. CODE $(error)s"% {"csv": out_csv, "error": wcode})
            raise FileNOTFound

    if usecsv:
        #overwrite input list
        frameloc = read_csv(out_csv)

    #Call get_clips individually
    for i in frameloc:
        video_id = i[0]
        time_id = i[1]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        temp = get_clips(videofile, video_id, vidduration, time_id, outdir_clips)

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
@log_on_error(logging.ERROR, "'[video_id:s]''[time_id:s]' clip failed to generate",
             on_exceptions = GenFailed, reraise = True, logger=globallogger)
@log_on_error(logging.DEBUG, "'[video_id:s]''[time_id:s]' clips too long for video",
             on_exceptions = ExcessVideoDuration, reraise = False, logger=globallogger)
@log_on_end(logging.INFO, "'[result:s]' Generated.", logger=globallogger)
def get_clips(videofile: str, video_id: str, vidduration: dict, time_id: str, outdir_clips: str):
    outdir_folder = os.path.join(outdir_clips, video_id)
    mkdir_p(outdir_folder)

    clip_start = float(int(time_id)) - clip_time_padding - float(clip_length) / 2
    if clip_start < 0:
        #clip_start = 0
        #warnings.warn("WARNING. %(video_id)s %(time_id)s clip too long for video file."%{"video_id":video_id, "time_id":time_id})
        raise ExcessVideoDuration
    clip_end = float(int(time_id)) + float(clip_length) / 2
    if clip_end > vidduration[video_id]:
        #clip_end = vidduration[video_id]
        #warnings.warn("WARNING. %(video_id)s %(time_id)s clip too long for video file."%{"video_id":video_id, "time_id":time_id})
        raise ExcessVideoDuration

    outpath_clip = os.path.join(outdir_folder, '%d%s' % (int(time_id), vid_suffix))
    werror = subprocess.call("ls %(outpath)s*" % {'outpath': outpath_clip}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    #werror = 1
    if werror != 0:
        #Generate clips
        ffmpeg_command = 'ffmpeg -hide_banner -loglevel panic -i %(videopath)s -ss %(start_timestamp)s -g 1 -force_key_frames 0 -to %(end_timestamp)s %(outpath)s' % {
                          'start_timestamp': hou_min_sec(clip_start * 1000),
                          'end_timestamp': hou_min_sec(clip_end * 1000),
                          'videopath': videofile,
                          'outpath': outpath_clip}
        #print(ffmpeg_command)
        globallogger.log(logging.DEBUG, ffmpeg_command)
        werror = subprocess.call(ffmpeg_command, shell=True)
        #Add exit code check
        if werror != 0:
            #sys.exit("ERROR ffmpeg write frame fail. CODE %(error)s" % {"error": code})
            globallogger.log(logging.ERROR, "Failed code %(code)s"%{"code":str(werror)})
            raise GenFailed
    else:
        #warnings.warn("WARNING. Frame file already exist.")
        globallogger.log(logging.INFO, "File %(file)s already exist. Skip."%{"file": outpath_clip})
    return outpath_clip

#----------------------------------------------------#
#Cleanup clips generated by this script
#----------------------------------------------------#
#outdir_clips Clips output path
#----------------------------------------------------#
@log_on_start(logging.WARNING, "CLEANING", logger = globallogger)
def clean_clips(outdir_clips: str):
    #CAUTION BEFORE CALLING
    warnings.warn("CLEANING CAUTION")
    werror = subprocess.call("rm -r %(outdir_clips)s/"% {"outdir_clips": outdir_clips}, shell = True)

#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    if con:
        print("Cleaning project.")
        clean_clips(outdir_clips)

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