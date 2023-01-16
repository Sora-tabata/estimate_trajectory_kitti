#!/bin/sh


dir_path="/home/sora-lab/dataset/kitti/00/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for dir in $dirs;
do
    #cp -r $dir/images $dir/image_0
    cd $dir
    cp -r $dir/images $dir/image_1
    sudo rm -rf $dir/image_0
    cp -r $dir/image_1 $dir/image_0
    cd $dir/image_0
    python /home/sora-lab/Documents/estimate_trajectory_kitti/rename.py
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