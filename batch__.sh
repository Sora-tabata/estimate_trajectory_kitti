#!/bin/sh

conda activate colmap0
dir_path="/home/sora-lab/dataset/kitti/00/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for dir in $dirs;
do
    cd $dir
    cp $dir/OUTPUT_DROIDSLAM/poses_0.npy $dir/poses.npy
    cp $dir/OUTPUT_DROIDSLAM/tstamps_0.npy $dir/tstamps.npy
done