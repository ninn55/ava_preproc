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

## Dir 结构

```
* falldown
    * bbox
    * keyframes
    * clips
    * ...
* ava_data_preproc
    * scripts
        * lib
    * doc
    * ...
* darknet
    * cfg
    * data
    * ...
* ...
```

## 流程

```
+-----------+    +-----------+   +-----------+  
\ keyframes \    \   clips   \   \ hostrawimg\  Front 
+-----------+    +-----------+   +-----------+  
       
               +----------------+
               \ pre-annotation \
               +----------------+

                 +-----------+
                 \ dataturks \
                 +-----------+

+-----------+   +-----------+   +-----------+  
\ parsejson \   \ drawbbox  \   \  cpfile   \   Back
+-----------+   +-----------+   +-----------+  
```

## 关键帧提取

在根目录下，
```
python3 scripts/genkeyframe.py
```
使用方法见
```
python3 scripts/genkeyframe.py --help
```
根据AVA的定义，关键帧为真实标注的帧。在AVA中从第15分钟开始每间隔1秒取1帧，总共标注15分钟。
由于提供数据的时长，此处将视频从头到尾间隔1秒标注，舍弃第1帧与最后1帧。

关键帧的位置为`/ava_data_preproc/preproc_fallDown/keyframes/video_id/time_id.jpg`

## 生成clips

在根目录下，
```
python3 scripts/genclip.py
```
使用方法见
```
python3 scripts/genclip.py --help
```

根据ava的定义，clip位于`keyframe_time_id - clip_time_padding - clip_length / 2`与`keyframe_time_id + clip_length / 2`之间。

clips的位置为`/ava_data_preproc/preproc_fallDown/clips/video_id/frame_count.mp4`
 
或直接运行`sh front_endofline.sh`

## Host img

后续会直接使用self host的图床代替。

只依赖于python核心包，可直接执行。

* `python3 ./scripts/hostraw.py -- port <open_port>`

* `sudo netstat -lntup | grep "<port_number>"`

注：

* `nohup python3 ./scripts/hostraw.py -- port <open_port> > hostraw.log &`
* `netstat -lntup | grep ":10800"`
* `ps -ef | grep python`
* `kill -9 <process_id>`

## 预标注

见`./doc/Preannot.md`

## Dataturks

见`./doc/dataturks.md`

## 输出转码

`python3 ./scripts/parsejson.py --sub_dir <video_id> --json_file  <output dir>`

或

`sh back_endofline.sh`

## 其他

`univid.py` : 在处理之前，将所有的带标注的视频文件转码为MPEG4，去除音频流，并包装为mp4格式。
`drawbbox.py` : 将标注出的结果渲染至相应的关键帧上。 
`cpfile.py` : 将输出整理至相应的文件夹。
`comutil.py` : 一些全局公用的imports和函数。

注:
* Bare git repo 位置: `/home/wniu/ava_data_preproc/`
* AVA数据位置: `/data/video_caption_database/ava/ava/`
* 代标注数据位置: `/data/video_caption_database/XiaMen/TrainVedio/behavior_recognition/`

