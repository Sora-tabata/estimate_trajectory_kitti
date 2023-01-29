#!/bin/sh
conda activate droidenv
dir_path="/media/sora-desktop/PortableSSD/kitti/00/*"
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
        cd ~/DROID-SLAM/
        python demo.py --imagedir=$dir/image_0 --calib=$dir/calib.txt --reconstruction_path=kitti --image_size=[376,1241] --stride=1 --disable_vis
        cp /home/sora-desktop/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
        cp /home/sora-desktop/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
    done
done