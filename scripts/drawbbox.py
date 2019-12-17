#----------------------------------------------------#
#Path: /script/gen_keyframe.py
#Discription: Render bbox on key frames
#Dependency: opencv
#Extra: Refactored from extract_keyframe.py from github.com/kevinlin311tw/ava-dataset-tool
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#Imports
from comutil import *
import cv2

#Parse command line argument
parser = argparse.ArgumentParser()
#Anotation file
parser.add_argument("--annot_file", default="./preproc_fallDown/ava_v1.0_extend_annot.csv",
                    help="Anotation file path.")
#Labels
parser.add_argument("--actionlist_file",
                    default="./preproc_fallDown/ava_action_list_v2.0.csv",
                    help="Action list file path.")
#Output dir
parser.add_argument("--output_dir", default="./preproc_fallDown", help="Output directory.")

FLAGS = parser.parse_args()

annotfile = FLAGS.annot_file
actionlistfile = FLAGS.actionlist_file
outdir = FLAGS.output_dir

#keyframes dir
outdir_keyframes = os.path.join(outdir, "keyframes")
# bbox output dir
outdir_bboxs = os.path.join(outdir, "bboxs")

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def load_action_name(annotations):
    csvfile = open(annotations,'r')
    reader = list(csv.reader(csvfile))
    dic = {}
    for i in range(len(reader)-1):
        temp = (reader[i+1][1],reader[i+1][2])
        dic[i+1] = temp
    return dic

#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def load_labels(annotations):
    csvfile = open(annotations,'r')
    reader = list(csv.reader(csvfile))
    dic = {}
    for i in range(len(reader)):

        if (reader[i][0],reader[i][1]) in dic:
            dic[(reader[i][0],reader[i][1])].append(i)
        else:
            templist = []
            templist.append(i)
            dic[(reader[i][0],reader[i][1])] = templist
    return reader, dic

#----------------------------------------------------#
#Draw bounding box on images
#----------------------------------------------------#
#Input argu
#anno_data      |  annotation data in format of list imported from csv
#action_name    |  labels in set import from csv
#keyfname       |  full path of frames
#video_id       |  Video id, file name with no extension
#time_id        |  Count from start of the video in second
#bbox_ids       |  Bounding box id ?
#----------------------------------------------------#
#No output argu
#----------------------------------------------------#
#Recycled from ava-dataset-tool by kevinlin311tw
#----------------------------------------------------#
def visual_bbox(anno_data, action_name, keyfname, video_id, time_id, bbox_ids):
    #print(anno_data)
    frame = cv2.imread(keyfname)
    frame_height, frame_width, channels = frame.shape
    outdir_folder = os.path.join(outdir_bboxs, video_id)
    mkdir_p(outdir_folder)
    outpath = os.path.join(outdir_folder, '%d_bbox.jpg' % (int(time_id)))
    draw_dic = {}
    for idx in bbox_ids:
        bbox = anno_data[idx][2:6]
        action_string = action_name[int(anno_data[idx][-1])]
        cv2.rectangle(frame, (int(float(bbox[0])*frame_width),int(float(bbox[1])*frame_height)), 
                (int(float(bbox[2])*frame_width),int(float(bbox[3])*frame_height)), [0,0,255], 1)
        x1 = int(float(bbox[0])*frame_width)
        y1 = int(float(bbox[1])*frame_height)

        if (x1,y1) in draw_dic:
            draw_dic[(x1,y1)] +=1
        else:
            draw_dic[(x1,y1)] = 1

        pt_to_draw = (x1,y1+20*draw_dic[(x1,y1)])          
        cv2.putText(frame, action_string[0], pt_to_draw, cv2.FONT_HERSHEY_SIMPLEX, fontScale=0.6, color=[0,255,255], thickness=1)
        draw_dic[pt_to_draw] = True
    cv2.imwrite(outpath, frame) 

#----------------------------------------------------#
#Render on bbox
#----------------------------------------------------#
def gen_bbox():
    anno_data, table = load_labels(annotfile)
    action_name = load_action_name(actionlistfile) 
    for key in sorted(table):
        video_id = key[0]
        time_id = float(key[1])    
        bbox_ids = table[key]
        outdir_folder = os.path.join(outdir_keyframes, video_id)
        fname = os.path.join(outdir_folder, '%d.jpg' % (int(time_id)))
        visual_bbox(anno_data, action_name, fname, video_id, time_id, bbox_ids)

#----------------------------------------------------#    
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    gen_bbox()