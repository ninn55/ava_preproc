import sys
sys.path.insert(1, '../darknet/python')
from darknet import load_net, load_meta, detect

net = load_net("../darknet/cfg/yolov2.cfg", "../darknet/yolov2.weights", 0)
meta = load_meta("../darknet/cfg/coco.data")
r = detect(net, meta, "../darknet/data/dog.jpg")
r2 = detect(net, meta, "../darknet/data/person.jpg")
print(r)
print(r2)