#!/bin/sh
#source /home/sora-desktop/anaconda3/etc/profile.d/conda.sh
conda activate droidenv


'''
#cd /home/sora-desktop/ORB_SLAM3
dir_path="/home/sora-lab/dataset/kitti/00/*"
dirs=`find $dir_path -maxdepth 0 -type d`
for i in `seq 0 9`;
do
    cd /home/sora-lab/DROID-SLAM
    for dir in $dirs;
    do
        python demo.py --imagedir=$dir/image_0 --calib=calib/00.txt --reconstruction_path=kitti --image_size=[376,1241] --stride=1 --disable_vis
    
        cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
        cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
    done
done
'''

#!/bin/sh

dir_path="/home/sora-lab/dataset/kitti/*"
dirs_=`find $dir_path -maxdepth 0 -type d`
for dir in $dirs_;
do
    dir_path=`echo "$dir/*"`
    dirs=`find $dir_path -maxdepth 0 -type d`
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
    echo $DIR_NAME
    if [ $DIR_NAME = 00 ] || [ $DIR_NAME = 01 ] || [ $DIR_NAME = 02 ]; then
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
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
        done
    done
    fi
    if [ $DIR_NAME = 03 ];
    then
    for i in `seq 0 9`;
    do
        for dir in $dirs;
        do
            echo $dir
            cd $dir
            CURRENT=$(cd $(dirname $0);pwd)
            DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
            echo $DIR_NAME
            cd cd ~/DROID-SLAM/
            python demo.py --imagedir=$dir/image_0 --calib=$dir/calib.txt --reconstruction_path=kitti --image_size=[375,1242] --stride=1 --disable_vis
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
        done
    done
    fi
    if [ $DIR_NAME = 04 ] || [ $DIR_NAME = 05 ] || [ $DIR_NAME = 06 ] || [ $DIR_NAME = 07 ] || [ $DIR_NAME = 08 ] || [ $DIR_NAME = 09 ] || [ $DIR_NAME = 10 ];
    then
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
            python demo.py --imagedir=$dir/image_0 --calib=$dir/calib.txt --reconstruction_path=kitti --image_size=[370,1226] --stride=1 --disable_vis
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/tstamps.npy $dir/OUTPUT_DROIDSLAM/tstamps_$i.npy
            cp /home/sora-lab/DROID-SLAM/reconstructions/kitti/poses.npy $dir/OUTPUT_DROIDSLAM/poses_$i.npy
        done
    done
    fi


done