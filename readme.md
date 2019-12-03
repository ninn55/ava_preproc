# ava_data_preproc

AVA数据集标注及预处理完整工具链。

## Repo clone方法：
```
git clone ssh://root@10.0.14.49/home/wniu/ava_data_preproc/
git clone /home/wniu/ava_data_preproc/
```

## 关键帧提取

在根目录下，
```
sh vid_fallDown/copy_file_in.sh
python3 scripts/gen_keyframe.py
```
根据AVA的定义，关键帧为真实标注的帧。在AVA中从第15分钟开始每间隔1秒取1帧，总共标注15分钟。
由于提供数据的时长，此处将视频从头到尾间隔1秒标注，舍弃第1帧与最后1帧。

关键帧的位置为`/ava_data_preproc/preproc_fallDown/keyframes/video_id/frame_count.jpg`

## 生成clip



注:
* Bare git repo 位置: `ssh://root@10.0.14.49/home/wniu/ava_data_preproc/`
* AVA数据位置: `/data/video_caption_database/ava/ava/`
* 代标注数据位置: `/data/video_caption_database/XiaMen/TrainVedio/behavior_recognition/`

