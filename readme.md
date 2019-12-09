# ava_data_preproc

AVA数据集标注及预处理完整工具链。

## Repo clone方法：
在10.0.14.49上：
```
git clone /home/wniu/ava_data_preproc/
```
不在服务器上
```
git clone ssh://root@10.0.14.49/home/wniu/ava_data_preproc/
```

## 关键帧提取

在根目录下，
```
python3 scripts/gen_keyframe.py
```
使用方法见
```
python3 scripts/gen_keyframe.py --help
```
根据AVA的定义，关键帧为真实标注的帧。在AVA中从第15分钟开始每间隔1秒取1帧，总共标注15分钟。
由于提供数据的时长，此处将视频从头到尾间隔1秒标注，舍弃第1帧与最后1帧。

关键帧的位置为`/ava_data_preproc/preproc_fallDown/keyframes/video_id/frame_count.jpg`

## 生成clips

在根目录下，
```
python3 scripts/gen_clip.py
```
使用方法见
```
python3 scripts/gen_clip.py --help
```
clips的位置为`/ava_data_preproc/preproc_fallDown/clips/video_id/frame_count.mp4`

## Host img

只依赖于python核心包，可直接执行。

* `python3 ./scripts/hostraw.py -- port <open_port>`

* `sudo netstat -lntup | grep "<port_number>"`

注：

* `nohup python3 ./scripts/hostraw.py -- port <open_port> > hostraw.log &`
* `netstat -lntup | grep ":10800"`
* `ps -ef | grep python`
* `kill -9 <process_id>`

## Dataturks

见`./doc/dataturks.md`

## 输出转码

`python3 ./scripts/parsejson.py --sub_dir <video_id> --json_file  <output dir>`

## 

注:
* Bare git repo 位置: `ssh://root@10.0.14.49/home/wniu/ava_data_preproc/`
* AVA数据位置: `/data/video_caption_database/ava/ava/`
* 代标注数据位置: `/data/video_caption_database/XiaMen/TrainVedio/behavior_recognition/`

