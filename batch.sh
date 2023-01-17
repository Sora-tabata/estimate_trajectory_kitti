#!/bin/sh

conda activate colmap0
dir_path="/home/sora-desktop/dataset/kitti/00/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for dir in $dirs;
do
    cd $dir
    cp $dir/OUTPUT_ORBSLAM/0.txt $dir/KeyFrameTrajectory.txt
done
for dir in $dirs;
do
    cd $dir
    python /home/sora-desktop/Documents/estimate_trajectory_kitti/main.py &
done
wait
for dir in $dirs;
do
    echo $dir
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    echo $DIR_NAME
    cp $dir/output/opted/trajectory.png /home/sora-desktop/Desktop/tra/$DIR_NAME.png
done
