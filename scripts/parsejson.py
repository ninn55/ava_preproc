import argparse
import json
import csv
import warnings
import sys

#Parse command line argument
parser = argparse.ArgumentParser()

parser.add_argument("--annot_file", default="./preproc_fallDown/ava_v1.0_extend_annot.csv", help="Anotation file path.")
parser.add_argument("--json_file", default="./demo/demo_out.json", help="Json file path.")
#Image file sub dir
parser.add_argument("--sub_dir", default="fall1", help="Subdirectory.")

FLAGS = parser.parse_args()

annot_file = FLAGS.annot_file
json_file = FLAGS.json_file
sub_dir = FLAGS.sub_dir

img_suffix = ".jpg"

#----------------------------------------------------#
#Read CSV file and parse it to dict
#{(video_id, time_id):[]}
#----------------------------------------------------#
def read_csv() -> dict:
    with open(annot_file, 'r') as f:
        dic = {}
        reader = list(csv.reader(f))
        for i in range(len(reader):
            temp = (i[0], i[1])
            if temp in dic.keys():
                warnings.warn("WARNING. Keys %(temp)s already parsed."%{"temp": temp})
            dic[temp] = []
    return dic

#----------------------------------------------------#
#Took dictionary input and save it to csv file
#----------------------------------------------------#
def write_csv(Lst: list):
    wcode = subprocess.call("ls %s*"% annot_file, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if wcode == 0:
        warnings.warn("WARNING csv file already exist, romve first.")
        werror = subprocess.call("rm -f %(txtfile)s"%{"txtfile": annot_file}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
        if werror != 0:
            sys.exit("ERROR. File %(txtfile)s removal failed. Please remove manully"%{"txtfile": annot_file})
        
        #Open and write file
        with open(annot_file, 'w') as filecsv:
            wr = csv.writer(filecsv)
            for i in Lst:
                wr.writerow(i)

#----------------------------------------------------#
#Read json and output essential info in a list
#[[video_id, time_id, cord0, cord1, cord2, cord3, annot_id], []]
#----------------------------------------------------#
def read_json() -> list:
    with open(json_file) as f:
        outlst = []
        while 1:
            temp = f.readline()
            if temp = "":
                break
            temp = json.loads(temp)
            if not temp["content"].endswith(img_suffix):
                sys.exit("ERROR. %(file)s is not a image."%{"file": temp})
            kf = temp["content"].split('/')[-1]
            video_id = sub_dir
            time_id = kf.split('.')[0]
            if temp["metadata"]["evaluation"] != 'CORRECT':
                warning.warn("WARNING. %(video_id)s %(time_id)s is not evaluated" % ("video_id": video_id, "time_id": time_id))
            for j in temp["annotation"]:
                lst = [j["points"][0][0], j["points"][0][1], j["points"][2][0], j["points"][2][1]]
                for i in j["label"]:
                    lst.append(i)
                    outlst.append(lst)
    return outlst

#----------------------------------------------------#
#Add list of essential info to list
#----------------------------------------------------#
def parse_json(csv_dic: dict, json_dic: dict) -> list:
    pass

#----------------------------------------------------#
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    print("Gnerate csv file.")
    write_csv(read_json())