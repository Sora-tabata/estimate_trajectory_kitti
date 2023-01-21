#!/bin/sh


dir_path="/home/sora-lab/dataset/kitti/*"
dirs_=`find $dir_path -maxdepth 0 -type d`
for dir in $dirs_;
do
    dir_path=`echo "$dir/*"`
    dirs=`find $dir_path -maxdepth 0 -type d`
    for dir in $dirs;
    do
        echo $dir
        cd $dir
        CURRENT=$(cd $(dirname $0);pwd)
        DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
        echo $DIR_NAME
        cd $dir
        cd $dir/images
        python /home/sora-lab/Documents/estimate_trajectory_kitti/rename.py
        cp -r $dir/images $dir/image_0
    done
done
'''
for i in `seq 0 9`;
do
    for dir in $dirs;
    do
        echo $dir
        cd $dir
        CURRENT=$(cd $(dirname $0);pwd)
        DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
        echo $DIR_NAME
        cd /ORB_SLAM3
        ./Examples/Monocular/mono_kitti Vocabulary/ORBvoc.txt Examples/Monocular/KITTI00.yaml $dir
        cp KeyFrameTrajectory.txt $dir/OUTPUT_ORBSLAM/$i.txt
    done
done
'''