#!/bin/sh


dir_path="/mnt/source/dataset/data_kitti/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for i in `seq 0 9`;
do
    for dir in $dirs;
    do
        echo $dir
        cd $dir
        CURRENT=$(cd $(dirname $0);pwd)
        DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
        echo $DIR_NAME
        mkdir $dir/OUTPUT_ORBSLAM
        cd /ORB_SLAM3
        ./Examples/Monocular/mono_kitti Vocabulary/ORBvoc.txt Examples/Monocular/KITTI03.yaml $dir
        cp KeyFrameTrajectory.txt $dir/OUTPUT_ORBSLAM/$i.txt
    done
done