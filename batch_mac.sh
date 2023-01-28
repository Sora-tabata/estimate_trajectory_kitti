#!/bin/sh
#source /home/sora-desktop/anaconda3/etc/profile.d/conda.sh
conda activate est




dir_path="/Volumes/PortableSSD/kitti/00/*"
dirs=`find $dir_path -maxdepth 0 -type d`

for dir in $dirs;
do
    echo $dir
    cd $dir
    CURRENT=$(cd $(dirname $0);pwd)
    DIR_NAME=`echo ${dir} | awk -F "/" '{ print $NF }'`
    echo ${DIR_NAME}
    cd $dir
    python /Users/sora-mac/Documents/estimate_trajectory_kitti/calc_rmse.py
    rm -rf /Users/sora-mac/Pictures/kitti_output/$DIR_NAME
    cp -r $dir/output/opted /Users/sora-mac/Pictures/kitti_output/$DIR_NAME
done