# ava_data_preproc

A WIP tool set for data set generation. Specifically for ava dataset.

Design of this tool set is keeping labeling new video recognition data in mind. The external tools include 

## Directory structure

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

## Block diagram

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

## How to

1. Run front_endofline.sh;
2. (Optional) Pre-annotate data with darknet;
3. Host images(simple http server or image host);
4. Annotate with dataturks, export data;
5. Run back_endofline.sh;

TODO: 
    __call__ to implement generation
    subprocess.popen to multiprocess
    finish log decrator