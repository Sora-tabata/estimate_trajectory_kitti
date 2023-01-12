#!/bin/sh
#source /home/sora-desktop/anaconda3/etc/profile.d/conda.sh
conda activate droidenv



#cd /home/sora-desktop/ORB_SLAM3
dir_path="/home/sora-lab/dataset/data_kitti/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for i in `seq 0 9`;
do
    for dir in $dirs;
    do
        echo $dir
        cd $dir
        mkdir $dir/OUTPUT_DROIDSLAM
    done
    cd /home/sora-lab/DROID-SLAM
    for dir in $dirs;
    do
        python demo.py --imagedir=$dir/image_0 --calib=calib/03.txt --reconstruction_path=kitti --image_size=[376,1241] --stride=1 --disable_vis
    done
    for dir in $dirs;
    do
        cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
        cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
    done
done
