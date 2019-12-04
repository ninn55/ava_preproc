import json
import cv2

parser = argparse.ArgumentParser()
parser.add_argument("--annot_file", default="./preproc_fallDown/ava_v1.0_extend.csv",
                    help="Anotation file path.")
parser.add_argument("--actionlist_file",
                    default="ava_action_list_v2.0.csv",
                    help="Action list file path.")
parser.add_argument("--output_dir", default="./preproc/train", help="Output path.")

FLAGS = parser.parse_args()

annotfile = FLAGS.annot_file
actionlistfile = FLAGS.actionlist_file
outdir = FLAGS.output_dir

outdir_clips = os.path.join(outdir, "clips")
outdir_keyframes = os.path.join(outdir, "keyframes")
outdir_bboxs = os.path.join(outdir, "bboxs")

clip_length = 3 # seconds
clip_time_padding = 1.0 # seconds

def visual_bbox(anno_data, action_name, keyfname, video_id, time_id, bbox_ids):
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


        