#----------------------------------------------------#
#Path: /script/hostraw.py
#Discription: host images for annotation and processing
#Dependency: unix netstat, grep
#Extra: info from john carter at stackoverflow.com and tecmint.com
#License: Unknown
#Coder: NiuWenxu
#Contact: wniu@connect.ust.hk
#----------------------------------------------------#

#imports
import http.server
import socketserver
import os
import warnings
import argparse
import subprocess
import sys

#Parse command line argument
parser = argparse.ArgumentParser()

#User input port number.
parser.add_argument("--port", default="10800", help="Opened port number to hosted files.")
#Image file sub dir
parser.add_argument("--sub_dir", default="fall1", help="Subdirectory.")
#Generated key frame dir
parser.add_argument("--frame_dir", default="./preproc_fallDown/keyframes", help="Hosted key frames dir.")

FLAGS = parser.parse_args()

PORT = FLAGS.port
keyframedir = FLAGS.frame_dir
subdir = FLAGS.sub_dir

#Preset argu
txt_suffix = ".txt"
img_suffix = ".jpg"
host_ip = "10.0.14.49"
txt_name = "imgs"

#----------------------------------------------------#
#Check port availability
#----------------------------------------------------#
def check_port():
    werror = subprocess.call("sudo netstat -lntup|grep \":%(port)s\"" % {"port": PORT}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror == 0:
        sys.exit("ERROR, port %(port)s taken. Please change port number"%{"port": PORT})

#----------------------------------------------------#
#Generate txt file for dataturks
#----------------------------------------------------#
def gen_txt():
    #Check dir status
    ls = os.listdir()
    if len(ls) == 0:
        sys.exit("ERROR, Subdir is empty.")
    
    txtfile = "%(txt_name)s%(txt_suffix)s" % {"txt_suffix": txt_suffix, "txt_name": txt_name}

    #Delete existing txt file
    werror = subprocess,call("ls %(txtfile)s*"%{"txtfile": txtfile}, shell = True, stderr = subprocess.DEVNULL, stdout = subprocess.DEVNULL)
    if werror == 0:
        warnings.warn("WARNING. File %(txtfile)s exist, remove first."%{"txtfile": txtfile})
        werror = subprocess.call("rm -f %(txtfile)s"%{"txtfile": txtfile})
        if werror != 0:
            sys.exit("ERROR. File %(txtfile)s removal failed. Please remove manully"%{"txtfile": txtfile}))

    #Generate txt file
    with open(txtfile, 'w') as f:
        for i in ls:
            if not i.endswith(img_suffix):
                continue
            temp = "http://%(host_ip)s:%(port)s/%(name)s\n" % {"host_ip": host_ip, "port": PORT, "name": i}
            f.write(temp)

#----------------------------------------------------#
#Main call
#----------------------------------------------------#
if __name__ == '__main__':
    print("Checking port.")
    check_port()
    os.chdir(os.path.join(keyframedir, subdir))
    print("Gen txt file")
    gen_txt()

    print("Start http server.")
    Handler = http.server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", PORT), Handler)
    print("Serving at port %(port)s. In %(dir)s"%{"port": PORT, "dir": os.path.join(keyframedir, subdir)})
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd:server_close()