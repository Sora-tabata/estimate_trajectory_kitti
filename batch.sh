#!/bin/sh


dir_path="/home/sora-lab/dataset/data_kitti/*"
dirs=`find $dir_path -maxdepth 0 -type d`

for dir in $dirs;
do
    echo $dir
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    echo $DIR_NAME
    sudo cp $dir/OUTPUT_ORBSLAM/1.txt $dir/KeyFrameTrajectory.txt
    sudo cp $dir/OUTPUT_DROIDSLAM/poses_1.npy $dir/poses.npy
    sudo cp $dir/OUTPUT_DROIDSLAM/tstamps_1.npy $dir/tstamps.npy
done
