#!/bin/sh

conda activate colmap0
dir_path="/home/sora-desktop/dataset/data_kitti/*"
dirs=`find $dir_path -maxdepth 0 -type d`

for dir in $dirs;
do
    echo $dir
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    echo $DIR_NAME
    cp $dir/OUTPUT_DROIDSLAM/poses_1.npy $dir/poses.npy
    cp $dir/OUTPUT_DROIDSLAM/tstamps_1.npy $dir/tstamps.npy
    mkdir $dir/output
    mkdir $dir/output/opted
    rm -rf image_2
    rm -rf image_3
    rm -rf matches
    rm -rf exif
    rm -rf undistorted
    rm -rf features
    rm -rf reports
done
for dir in $dirs;
do
    cd $dir
    python /home/sora-desktop/Documents/estimate_trajectory_kitti/main.py &
done
wait