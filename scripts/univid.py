#----------------------------------------------------#
#Path: /script/vid.py
#Discription: video format and encode unify and get rid of audio stream
#Dependency: ffprobe
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#imports
from comutil import *
import copy
#universally unique identifiers
import uuid

parser = argparse.ArgumentParser()
#Use reletive path
#input Video path ./vid_fallDown
parser.add_argument("--video_dir", default="./vid_fallDown", help="Videos source path.")

FLAGS = parser.parse_args()

videodir = FLAGS.video_dir

#Set default container, default mp4
vid_suffix = ".mp4"
#set default codec, default h.264
vid_codec = "libx264"

#----------------------------------------------------#
#Chaneg a single video file to codec h.264
#Chaneg container to mp4
#----------------------------------------------------#
#No output
#----------------------------------------------------#
def gen_file(filedir: str, videodir: str):
    #Generate unique video id
    filedir = os.path.join(videodir, filedir)
    video_id = str(uuid.uuid1()).split('-')[0]
    cache_file = os.path.join(videodir, "%(video_id)s%(vid_suffix)s"% {"video_id": video_id, "vid_suffix":vid_suffix})
    #No audio needed.
    command = "ffmpeg -i %(video_file)s -vcodec %(vid_codec)s -an %(cache_file)s"% {
                "video_file": filedir, 
                "cache_file": cache_file, 
                "vid_codec": vid_codec}
    print(command)
    werror = subprocess.call(command, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror != 0:
        sys.exit("ERROR. Decode file %(filedir)s failed."%{"filedir": filedir})
    werror = subprocess.call("rm -f %(filedir)s"%{"filedir": filedir}, shell = True)
    if werror != 0:
        warnings.warn("WARNING. Remove file %(filedir)s failed. Please remove by hand."%{"filedir": filedir})

#----------------------------------------------------#
#Get a list of video names inside a specific dir.
#----------------------------------------------------#
#videodir: directory that maay conatin video files.
#----------------------------------------------------#
#List: list of video file pathes. [[str]]
#----------------------------------------------------#
def gen_vidList(videodir: str) -> list: 
    # Auto exit check
    videos = subprocess.check_output("ls %(videodir)s" %{"videodir": videodir}, shell=True)
    #Last item in list is ""
    videos = videos.decode('utf8')
    videos = videos.split('\n')
    List = []
    for i in videos:
        temp = []
        temppath = os.path.join(videodir, i)
        if check_vid(temppath):
            temp.append(copy.deepcopy(i))
            List.append(copy.deepcopy(temp))
    return List

#----------------------------------------------------#
#Main call
#----------------------------------------------------#
#List: list of full file name of videos
#List: directory that maay conatin video files.
#----------------------------------------------------#
#No output argument
#----------------------------------------------------#
def unify_vid(List: list, videodir: str):
    for i in List:
        gen_file(i[0], videodir)

#----------------------------------------------------#
#Main
#----------------------------------------------------#
if __name__ == '__main__':
    bshfile = os.path.join(videodir, "copy_file_in.sh")
    subprocess.call("sh %(bshfile)s" % {"bshfile": bshfile}, shell = True)
    print("Generating video list.")
    vidlist = gen_vidList(videodir)
    print("Decode encode videos.")
    unify_vid(vidlist, videodir)