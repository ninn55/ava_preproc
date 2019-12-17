# Pre-annotated image using darknet YOLO

```
git clone https://github.com/pjreddie/darknet.git
```

## 编译Darknet

使用darknet yolov2进行预标注。

* `git clone https://github.com/pjreddie/darknet.git`
* `cd darknet`
* `git config --bool core.bare true`

* `git clone ssh://root@10.0.14.49/home/wniu/darknet`

确认cuda安装:

* `nvcc --version`
* `nvidia-smi`
* `which nvcc`

确认cudnn安装:

* `cd <cuda_dir>/lib64`
* `ls | grep cudnn`

确认opencv安装：

* `cd /usr/local/lib64`
* `ls -a | grep opencv`

makefile配置:

```
GPU = 1
CUDNN = 1
OPENCV = 1
```

详见: CUDA Compiler Driver NVCC Reference guide(TRM-06721-001) 4.2.7.3
* 10.0.14.49 使用1080TI，为Pascal架构。
    * virtual architecture使用compute_60/61/62
    * GPU feature list使用sm_60/61/62

ARCH= -gencode arch=compute_30,code=sm_30 \
      -gencode arch=compute_35,code=sm_35 \
      -gencode arch=compute_60,code=[sm_60,compute_60] \
      -gencode arch=compute_61,code=[sm_61,compute_61] \
      -gencode arch=compute_62,code=[sm_52,compute_62]

* `make`

* `wget https://pjreddie.com/media/files/yolov2.weights`

## pre annotate

注：
将`../darknet/cfg/coco.data`中：
```
names = data/coco.names
```
变为：
```
names = ../darknet/data/coco.names
```

依赖于opencv。请于相应环境中编译。

```
python3 ./scripts/darknet.py
```

将输出`./preproc_fallDown/ava_preannot.json`输入dataturks的pre annotated类型。

## opencv config error

Make error fix

```
Package opencv was not found in the pkg-config search path.
Perhaps you should add the directory containing `opencv.pc'
to the PKG_CONFIG_PATH environment variable
```

在10.0.14.49上opencv位于`/usr/local/lib64` and `/usr/local/include`.
将一下内容添加至`opencv.pc`。并放到`/usr/share/pkgconfig`
```
prefix = /usr/local
exec_prefix = $(prefix)
includedir = $(prefix)/include
libdir = $(exec_prefix)/lib64

Name: opencv
Description: The opencv library
Version: 3.4.0
Cflags: -I$(includedir)/opencv -I$(includedir)/opencv2
Libs: -L$(libdir) -lopencv_calib3d -lopencv_imgproc -lopencv_highgui -lopencv_core -lopencv_imgcodecs -lopencv_videoio
```

./darknet detector test cfg/coco.data cfg/yolov2.cfg weight/yolov2.weights -dont_show <data/>train.txt > result.txt
