#----------------------------------------------------#
#Path: /script/gen_keyframe.py
#Discription: Generate key frames and csv used for latter annotation
#Dependency: FFMPEG FFPROBE Git
#Extra: Refactored from extract_keyframe.py from github.com/kevinlin311tw/ava-dataset-tool
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
from comutil import *

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
#default genkeyframe suffix
img_suffix = ".jpg"
#Frame interval in seconds
interval = 1
#Clip length
clip_length = 3 # seconds
#Clip padding
clip_time_padding = 1.0 # seconds

#----------------------------------------------------#
#Extract a single frame from video file using ffmpeg
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
#videofile        |  Full file path
#video_id         |  Video id, file name with no extension
#vidduration    |  Dictionary of video, video_id:video_duration, str:int
#time_id          |  Count from start of the video in second
#outdir_keyframes |  Full keyframe output path
#----------------------------------------------------#
#outpath          |  Full path of output video
#----------------------------------------------------#
@log_on_error(logging.ERROR, "'[video_id:s]''[time_id:s]' keyframe failed to generate",
             on_exceptions = GenFailed, reraise = True, logger=globallogger)
@log_on_error(logging.DEBUG, "'[video_id:s]''[time_id:s]' clips too long for video",
             on_exceptions = ExcessVideoDuration, reraise = False, logger=globallogger)
@log_on_end(logging.INFO, "'[result:s]' Generated.", logger=globallogger)
def get_keyframe(videofile: str, video_id: str, vidduration: dict,time_id: str, outdir_keyframes: str) -> str: 
    outdir_folder = os.path.join(outdir_keyframes, video_id)
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

    outpath = os.path.join(outdir_folder, '%(time_id)d%(suffix)s' % {"time_id": int(time_id), "suffix": img_suffix})
    werror = subprocess.call("ls %(outpath)s*" % {'outpath': outpath}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    #werror = 1
    if werror != 0:
        #generat ungenerated key frames
        ffmpeg_command = 'ffmpeg -hide_banner -loglevel panic -ss %(timestamp)f -i %(videopath)s \
                          -frames:v 1 %(outpath)s' % {
                          'timestamp': float(time_id),
                          'videopath': videofile,
                          'outpath': outpath}
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
        globallogger.log(logging.INFO, "File %(file)s already exist. Skip."%{"file": outpath})
    return outpath

#----------------------------------------------------#
#Write key frames
#----------------------------------------------------#
#videodir           |  video file directory
#frameloc           |  2D list containing video_id and frame location
#vid_suffix         |  suffix of video
#usecsv             |  use csv file or input list directly
#outdir_keyframes   |  Keyframe output path
#out_csv            |  csv file path
#----------------------------------------------------#
#NO output arg
#----------------------------------------------------#
@log_on_error(logging.ERROR, "CSV file '[out_csv:s]' not found.", 
            on_exceptions = (FileNOTFound, FileExistsError), reraise = True , logger=globallogger)
def write_keyframe(videodir: str, frameloc: list, vidduration: dict, vid_suffix: str, usecsv: bool, outdir_keyframes: str, out_csv: str):
    #Input check
    if usecsv: 
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode != 0:
            #sys.exit("ERROR csv file in %(csv)s donot exist. CODE $(error)s"% {"csv": out_csv, "error": wcode})
            raise FileNOTFound

    #parse csv file into list
    if usecsv:
        #overwrite input list
        frameloc = read_csv(out_csv)

    for i in frameloc:
        video_id = i[0]
        time_id = i[1]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        temp = get_keyframe(videofile, video_id, vidduration, time_id, outdir_keyframes)

#----------------------------------------------------#
#generate predefined csv file for this specific case
#return list [[video_id, time_id]]similar to comutil.read_csv{(video_id, time_id)}
#----------------------------------------------------#  
#videodir       |  video file directory
#videolist      |  List of video_id(str)
#vidduration    |  Dictionary of video, video_id:video_duration, str:int
#writeindex     |  write to csv or not. bool.
#interval       |  time interval between frames
#out_csv        |  csv file output directory
#----------------------------------------------------#
#frameloc       |  2D list containing video_id and frame location
#----------------------------------------------------#
@log_on_error(logging.FATAL, "Inner logic error", 
            on_exceptions = InnerLogicError, reraise=True, logger=globallogger) 
@log_on_end(logging.INFO, "base csv generated")
def gen_basecsv(videodir: str, videolist: list, vidduration: dict, writeindex: bool, interval: float, out_csv: str) -> list: 
    List = []
    for i in videolist:
        video_id = i[0] #String
        duration = vidduration[video_id] #Int
        #Discard first and last frame
        #Change this block if specific frames is requested.
        #May not be global
        start_id = 1
        end_id = duration
        for j in range(start_id, end_id, interval):
            if j > duration or start_id < 0 or end_id < 0 or start_id >= end_id:
                #sys.exit("ERROR inner logic error. CODE 2")
                raise InnerLogicError
            temp = [video_id, str(j)]
            List.append(temp)
    
    #Write List to csv file
    if writeindex:
        #File exist check        
        wcode = subprocess.call("ls %s*"% out_csv, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if wcode == 0:
            #warnings.warn("WARNING csv file already exist, not generate.")
            globallogger.log(logging.DEBUG, "csv file already exist, not generate.")
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
#videodir:      video file directory
#vid_suffix:    suffix of video
#----------------------------------------------------#
#videolist:     List of video_id(str)
#----------------------------------------------------#
@log_on_end(logging.INFO, "video list generated", logger=globallogger)
@log_on_error(logging.ERROR, "Folder '[videodir:s]' does nor contain any video file or not being read.",
            on_exceptions=FileNOTFound, reraise=True, logger=globallogger)
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
    if len(List) == 0:
        raise FileNOTFound
    return List

#----------------------------------------------------#
#Generate video duration dictionary using ffprobe
#----------------------------------------------------#
#videodir:      video file directory
#videolist:     List of video_id(str)
#vid_suffix:    suffix of video
#----------------------------------------------------#
#vidduration:   Dictionary of video, video_id:video_duration, str:int
#----------------------------------------------------#
@log_on_end(logging.INFO, "Video duration dictionary generated.", logger=globallogger)
@log_on_error(logging.ERROR, "Inner logic error", 
            on_exceptions=(subprocess.CalledProcessError, InnerLogicError), 
            reraise=True, logger=globallogger)
def gen_vidduration(videodir: str, videolist: list, vid_suffix: str) -> dict: 
    dic = {}
    for i in videolist:
        video_id = i[0]
        videofile = os.path.join(videodir, "%(video_id)s%(suf)s"%{"video_id": video_id, "suf": vid_suffix})
        ffprobe_command = "ffprobe -i %(videofile)s \
                            -show_format -v quiet | grep duration" % {
                                "videofile": videofile}
        globallogger.log(logging.DEBUG, ffprobe_command)
        # Auto exit check        
        temp = subprocess.check_output(ffprobe_command, shell = True).decode("utf8")
        temp = temp.split('=')[1]
        duration = int(float(temp.split("\n")[0]))
        if video_id in dic:
            pass
        else:
            dic[video_id] = duration
    if len(dic) == 0 or len(dic) != len(videolist):
        raise InnerLogicError
    return dic

#----------------------------------------------------#
#Clean up key frames and CSV files generated by this script
#----------------------------------------------------#
#outdir_keyframes   Keyframe output path
#out_csv            csv file output directory
#----------------------------------------------------#
@log_on_start(logging.WARNING, "CLEANING", logger = globallogger)
def clean_keyframes(outdir_keyframes: str, out_csv: str):
    #warnings.warn("CLEANING CAUTION")
    werror = subprocess.call("git clean -fx", shell = True)
    werror = subprocess.call("rm -r %(outdir_keyframes)s/"% {"outdir_keyframes": outdir_keyframes}, shell = True)
    
#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    if con:
        clean_keyframes(outdir_keyframes, out_csv)

    bshfile = os.path.join(videodir, "copy_file_in.sh")
    subprocess.call("sh %(bshfile)s" % {"bshfile": bshfile}, shell = True)
    print("Generating video list.")
    videolist = gen_vidList(videodir, vid_suffix)
    print("Genetating video duration")
    vidduration = gen_vidduration(videodir, videolist, vid_suffix)
    print("Generating CSV file.")
    frameloc = gen_basecsv(videodir, videolist, vidduration, True, interval, out_csv)
    print("Generating keyframes")
    write_keyframe(videodir, frameloc, vidduration, vid_suffix, False, outdir_keyframes, out_csv)