#----------------------------------------------------#
#Path: /script/gen_keyframe.py
#Discription: Generate preannotated data using darknet yolov2
#Dependency: darknet yolo
#Extra: Refactored from darknet.py from github.com/pjreddie/darknet
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#
from ctypes import *
import math
import random
import subprocess
import argparse
from parsejson import read_csv
import json
from cv2 import imread
import warnings

#Parse command line argument
parser = argparse.ArgumentParser()
parser.add_argument("--output_dir", default="./preproc_fallDown", help="Output directory.")
parser.add_argument("--sub_dir", default="fall1", help="Subdirectory.")
#User input port number.
parser.add_argument("--port", default="10800", help="Opened port number to hosted files.")

FLAGS = parser.parse_args()

outdir = FLAGS.output_dir
PORT = FLAGS.port
sub_dir = FLAGS.sub_dir

#Keyframe output path ./preproc_fallDown/keyframes
outdir_keyframes = os.path.join(outdir, "keyframes")
outdir_preannotxt = os.path.join(outdir, "%(sub)s.txt"%{"sub": sub_dir})
#Initial csv path ./preproc_fallDown/ava_v1.0_extend.csv
out_csv = os.path.join(outdir, "ava_v1.0_extend.csv)"

img_suffix = ".jpg"
ip = "10.0.14.49"

def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]

    

#lib = CDLL("/home/pjreddie/documents/darknet/libdarknet.so", RTLD_GLOBAL)
#lib = CDLL("libdarknet.so", RTLD_GLOBAL)
lib = CDLL("../darknet/libdarknet.so", RTLD_GLOBAL)
lib.network_width.argtypes = [c_void_p]
lib.network_width.restype = c_int
lib.network_height.argtypes = [c_void_p]
lib.network_height.restype = c_int

predict = lib.network_predict
predict.argtypes = [c_void_p, POINTER(c_float)]
predict.restype = POINTER(c_float)

set_gpu = lib.cuda_set_device
set_gpu.argtypes = [c_int]

make_image = lib.make_image
make_image.argtypes = [c_int, c_int, c_int]
make_image.restype = IMAGE

get_network_boxes = lib.get_network_boxes
get_network_boxes.argtypes = [c_void_p, c_int, c_int, c_float, c_float, POINTER(c_int), c_int, POINTER(c_int)]
get_network_boxes.restype = POINTER(DETECTION)

make_network_boxes = lib.make_network_boxes
make_network_boxes.argtypes = [c_void_p]
make_network_boxes.restype = POINTER(DETECTION)

free_detections = lib.free_detections
free_detections.argtypes = [POINTER(DETECTION), c_int]

free_ptrs = lib.free_ptrs
free_ptrs.argtypes = [POINTER(c_void_p), c_int]

network_predict = lib.network_predict
network_predict.argtypes = [c_void_p, POINTER(c_float)]

reset_rnn = lib.reset_rnn
reset_rnn.argtypes = [c_void_p]

load_net = lib.load_network
load_net.argtypes = [c_char_p, c_char_p, c_int]
load_net.restype = c_void_p

do_nms_obj = lib.do_nms_obj
do_nms_obj.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

do_nms_sort = lib.do_nms_sort
do_nms_sort.argtypes = [POINTER(DETECTION), c_int, c_int, c_float]

free_image = lib.free_image
free_image.argtypes = [IMAGE]

letterbox_image = lib.letterbox_image
letterbox_image.argtypes = [IMAGE, c_int, c_int]
letterbox_image.restype = IMAGE

load_meta = lib.get_metadata
lib.get_metadata.argtypes = [c_char_p]
lib.get_metadata.restype = METADATA

load_image = lib.load_image_color
load_image.argtypes = [c_char_p, c_int, c_int]
load_image.restype = IMAGE

rgbgr_image = lib.rgbgr_image
rgbgr_image.argtypes = [IMAGE]

predict_image = lib.network_predict_image
predict_image.argtypes = [c_void_p, IMAGE]
predict_image.restype = POINTER(c_float)

def classify(net, meta, im):
    out = predict_image(net, im)
    res = []
    for i in range(meta.classes):
        res.append((meta.names[i], out[i]))
    res = sorted(res, key=lambda x: -x[1])
    return res

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im = load_image(image, 0, 0)
    num = c_int(0)
    pnum = pointer(num)
    predict_image(net, im)
    dets = get_network_boxes(net, im.w, im.h, thresh, hier_thresh, None, 0, pnum)
    num = pnum[0]
    if (nms): do_nms_obj(dets, num, meta.classes, nms);

    res = []
    for j in range(num):
        for i in range(meta.classes):
            if dets[j].prob[i] > 0:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i], (b.x, b.y, b.w, b.h)))
    res = sorted(res, key=lambda x: -x[1])
    free_image(im)
    free_detections(dets, num)
    return res
    
def wirteDetect(net, meta):
    ls = read_csv(out_csv)
    resultlst = []
    for i in ls:
        temp = []
        vidoe_id = i[0]
        time_id = i[1]
        if vidoe_id != sub_dir:
            continue
        fl = os.path.join(outdir_keyframes, vidoe_id)
        fl = os.path.join(fl, "%(time_id)s%(suffix)s"%{"time_id": time_id, "suffix": img_suffix})
        result = detect(net, meta, fl)
        result = result.replace("(", "[").replace(")", "]").replace("'", "\"")
        result = json.loads(result)
        temp.append(vidoe_id)
        temp.append(time_id)
        im = cv2.imread(fl)
        width, height, _ = im.shape
        temp0 = []
        for j in result:
            if j[1] < 0.5:
                warnings.warn("WARNING. %(vidoe_id)s %(time_id)s bbox %(bbox)s is not qualified"%{
                                            "vidoe_id": vidoe_id, 
                                            "time_id": time_id, 
                                            "bbox": j[0]})
            temp1 = []
            temp1.append(i[2][0] / width)
            temp1.append(i[2][1] / height)
            temp0.append(temp1)
            temp2 = []
            temp2.append((i[2][2] + i[2][0]) / width)
            temp2.append((i[2][3] + i[2][1]) / height)
            temp0.append(temp2)
        temp.append(temp0)

    for i in temp:
        vidoe_id = i[0]
        time_id = i[1]
        url = "http://%(ip)s:%(port)s/%(video_id)s/%(time_id)s%(suffix)s"%{
                                            "ip" : ip,
                                            "port": PORT,
                                            "video_id": video_id,
                                            "time_id": time_id,
                                            "suffix": img_suffix}
        fl = os.path.join(outdir_keyframes, vidoe_id)
        fl = os.path.join(fl, "%(time_id)s%(suffix)s"%{"time_id": time_id, "suffix": img_suffix})
        im = cv2.imread(fl)
        width, height, _ = im.shape
        dict = {}
        dict["content"] = url
        dict["annotation"] = []
        dict["extras"] = "null"

        dict1 = {}
        dict1["label"] = "0"
        dict1["imageWidth"] = width
        dict1["imageHeight"] = height
        dict1["points"] = i[2]

        dict["annotation"].append(dict1)
        with open(outdir_preannotxt, "a") as ftxt:
            str = json.dumps(dict)
            ftxt.write(str + "\n")

if __name__ == "__main__":
    net = load_net("../darknet/cfg/tiny-yolo.cfg", "../darknet/tiny-yolo.weights", 0)
    meta = load_meta("../darknet/cfg/coco.data")
    wirteDetect(net, meta)

    

