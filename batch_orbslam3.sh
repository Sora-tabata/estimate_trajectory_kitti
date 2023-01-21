#!/bin/sh

'''
dir_path="/mnt/source/dataset/03only/*"
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
'''

dir_path4="/mnt/source/dataset/kitti/*"
dirs_4=`find $dir_path4 -maxdepth 0 -type d`

for dir4 in $dirs_4;
do
    for i in `seq 0 9`;
    do
        dir_path3=`echo "$dir4/*"`
        dirs3=`find $dir_path3 -maxdepth 0 -type d`
        for dir__ in $dirs3;
        do
            echo $dir__
            cd $dir__
            CURRENT=$(cd $(dirname $0);pwd)
            DIR_NAME=`echo "$CURRENT" | sed -e 's/.*\/\([^\/]*\)$/\1/'`
            echo $DIR_NAME
            cd $dir__
            cd /ORB_SLAM3
            ./Examples/Monocular/mono_kitti Vocabulary/ORBvoc.txt $dir__/KITTI.yaml $dir__
            cp KeyFrameTrajectory.txt $dir__/OUTPUT_ORBSLAM/$i.txt
        done
    done
done