#!/bin/sh

conda activate colmap0
dir_path="/home/sora-lab/dataset/data_kitti/*"
dirs=`find $dir_path -maxdepth 0 -type d`

for dir in $dirs;
do
    echo $dir
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    echo $DIR_NAME
    cp $dir/KeyFrameTrajectory.txt
    cp $dir/reconstruction
    rm -rf image_2
    rm -rf image_3
    rm -rf matches
    rm -rf exif
    rm -rf 
done