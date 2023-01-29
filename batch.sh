#!/bin/sh

conda activate colmap0
dir_path="/media/sora-desktop/PortableSSD/kitti/*"
dirs_=`find $dir_path -maxdepth 0 -type d`
for dir_ in $dirs_;
do
    dir_path=`echo "$dir_/*"`
    dirs=`find $dir_path -maxdepth 0 -type d`
    for dir in $dirs;
    do  
        echo $dir
        cd $dir
        rm -rf $dir/output
        mkdir $dir/output
        mkdir $dir/output/opted
        #cp $dir/OUTPUT_ORBSLAM/0.txt $dir/KeyFrameTrajectory.txt
        #cp $dir/OUTPUT_DROIDSLAM/poses_0.npy $dir/poses.npy
        #cp $dir/OUTPUT_DROIDSLAM/tstamps_0.npy $dir/tstamps.npy
        python /home/sora-desktop/Documents/estimate_trajectory_kitti/calc_rmse.py #&
    done
    #wait
done
dir_path="/media/sora-desktop/PortableSSD/kitti/*"
dirs_=`find $dir_path -maxdepth 0 -type d`
for dir_ in $dirs_;
do
    cd $dir_
    CURRENT_=$(cd $(dirname $0);pwd)
    DIR_NAME_=`echo "$CURRENT_" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    dir_path=`echo "$dir_/*"`
    dirs=`find $dir_path -maxdepth 0 -type d`
    for dir in $dirs;
    do 
        cd $dir
        CURRENT=$(cd $(dirname $0);pwd)
        DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
        
        dir_name=`echo "$DIR_NAME_-$DIR_NAME"`
        rm -rf /home/sora-desktop/Desktop/kitti_output/$dir_name
        mkdir /home/sora-desktop/Desktop/kitti_output/$dir_name
        cp -r $dir/output/opted /home/sora-desktop/Desktop/kitti_output/$dir_name/png
    done
done
