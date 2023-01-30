from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
from calc_traj import CalcTraj
from init import Init
from calc_RT__ import CalcRT
from optimize_traj7 import OptimizeTraj
import numpy as np
from equalize_est import Equalize
import os
import csv


class CalcRMSE():
    def __init__(self):
        a = Init()
        self.L0 = a.L0
        self.json_file0 = a.json_file0
        self.droid = a.droid
        self.ground_time = a.ground_time
        self.ground_data = a.ground_data
        self.groundtruth = CalcTraj().calcGroundTruth(self.ground_time, self.L0, self.ground_data)
        self.opensfm = CalcTraj().calcOpensfm(self.groundtruth, self.json_file0)
        self.droidslam = CalcTraj().calcDroidslam(self.groundtruth, self.droid)
        self.optimized = OptimizeTraj().calcOptimizeTraj()
        if (len(self.L0) == 0):
            self.orbslam = self.droidslam
        else:
            self.orbslam = CalcTraj().calcOrbslam(self.groundtruth, self.L0)
        self.equalizedDROID = Equalize().averagedSLAM(a.droid0, a.droid1, a.droid2, a.droid3, a.droid4, a.droid5, a.droid6, a.droid7, a.droid8, a.droid9, 'DROIDSLAM')

        if (len(a.L) == 0):
            self.equalizedORB = self.equalizedDROID
        else:
            self.equalizedORB = Equalize().averagedSLAM(a.L0, a.L1, a.L2, a.L3, a.L4, a.L5, a.L6, a.L7, a.L8, a.L9, 'ORBSLAM')

    def calc_RMSE(self):
        '''
        rmse_orb_x = np.sqrt(mean_squared_error(self.orbslam[12], self.groundtruth[1]))
        rmse_orb_y = np.sqrt(mean_squared_error(self.orbslam[13], self.groundtruth[2]))
        rmse_sfm_x = np.sqrt(mean_squared_error(self.opensfm[11], self.groundtruth[1]))
        rmse_sfm_y = np.sqrt(mean_squared_error(self.opensfm[12], self.groundtruth[2]))
        rmse_droid_x = np.sqrt(mean_squared_error(self.droidslam[11], self.groundtruth[1]))
        rmse_droid_y = np.sqrt(mean_squared_error(self.droidslam[12], self.groundtruth[2]))
        rmse_opt_x = np.sqrt(mean_squared_error(self.optimized[0], self.groundtruth[1]))
        rmse_opt_y = np.sqrt(mean_squared_error(self.optimized[1], self.groundtruth[2]))
        '''

        rmse_orb_x = mean_absolute_error(self.orbslam[12], self.groundtruth[1])
        rmse_orb_y = mean_absolute_error(self.orbslam[13], self.groundtruth[2])
        rmse_sfm_x = mean_absolute_error(self.opensfm[11], self.groundtruth[1])
        rmse_sfm_y = mean_absolute_error(self.opensfm[12], self.groundtruth[2])
        rmse_droid_x = mean_absolute_error(self.droidslam[11], self.groundtruth[1])
        rmse_droid_y = mean_absolute_error(self.droidslam[12], self.groundtruth[2])
        rmse_opt_x = mean_absolute_error(self.optimized[0], self.groundtruth[1])
        rmse_opt_y = mean_absolute_error(self.optimized[1], self.groundtruth[2])

        rmse_orb = (rmse_orb_x + rmse_orb_y)/2
        rmse_sfm = (rmse_sfm_x + rmse_sfm_y)/2
        rmse_droid = (rmse_droid_x + rmse_droid_y)/2
        rmse_opt = (rmse_opt_x + rmse_opt_y)/2
        print(os.getcwd())
        print("RMSE_ORB-SLAM2", rmse_orb)
        print("RMSE_OpenSfM", rmse_sfm)
        print("RMSE_DROID-SLAM", rmse_droid)
        print("RMSE_Optimized", rmse_opt)

        return rmse_orb, rmse_sfm, rmse_droid, rmse_opt
    
    def calc_eva(self):
        a = self.calc_RMSE()
        rmse_orb = a[0]
        rmse_sfm = a[1]
        rmse_droid = a[2]
        rmse_opt = a[3]

        '''
        rmse_orb_roll = np.sqrt(mean_squared_error(self.orbslam[3]-np.median(self.orbslam[3]), self.groundtruth[4]-np.median(self.groundtruth[4])))
        rmse_orb_pitch = np.sqrt(mean_squared_error(self.orbslam[4]-np.median(self.orbslam[4]), self.groundtruth[5]-np.median(self.groundtruth[5])))
        rmse_orb_yaw = np.sqrt(mean_squared_error(self.orbslam[5]-np.median(self.orbslam[5]), self.groundtruth[6]-np.median(self.groundtruth[6])))

        rmse_sfm_roll = np.sqrt(mean_squared_error(self.opensfm[2]-np.median(self.opensfm[2]), self.groundtruth[4]-np.median(self.groundtruth[4])))
        rmse_sfm_pitch = np.sqrt(mean_squared_error(self.opensfm[3]-np.median(self.opensfm[3]), self.groundtruth[5]-np.median(self.groundtruth[5])))
        rmse_sfm_yaw = np.sqrt(mean_squared_error(self.opensfm[4]-np.median(self.opensfm[4]), self.groundtruth[6]-np.median(self.groundtruth[6])))

        rmse_droid_roll = np.sqrt(mean_squared_error(self.droidslam[3]-np.median(self.droidslam[3]), self.groundtruth[4]-np.median(self.groundtruth[4])))
        rmse_droid_pitch = np.sqrt(mean_squared_error(self.droidslam[4]-np.median(self.droidslam[4]), self.groundtruth[5]-np.median(self.groundtruth[5])))
        rmse_droid_yaw = np.sqrt(mean_squared_error(self.droidslam[5]-np.median(self.droidslam[5]), self.groundtruth[6]-np.median(self.groundtruth[6])))

        rmse_opt_roll = np.sqrt(mean_squared_error(self.optimized[3]-np.median(self.optimized[3]), self.groundtruth[4]-np.median(self.groundtruth[4])))
        rmse_opt_pitch = np.sqrt(mean_squared_error(self.optimized[4]-np.median(self.optimized[4]), self.groundtruth[5]-np.median(self.groundtruth[5])))
        rmse_opt_yaw = np.sqrt(mean_squared_error(self.optimized[5]-np.median(self.optimized[5]), self.groundtruth[6]-np.median(self.groundtruth[6])))
        '''
        rmse_orb_roll = mean_absolute_error(self.orbslam[3]-np.median(self.orbslam[3]), self.groundtruth[4]-np.median(self.groundtruth[4]))
        rmse_orb_pitch = mean_absolute_error(self.orbslam[4]-np.median(self.orbslam[4]), self.groundtruth[5]-np.median(self.groundtruth[5]))
        rmse_orb_yaw = mean_absolute_error(self.orbslam[5]-np.median(self.orbslam[5]), self.groundtruth[6]-np.median(self.groundtruth[6]))

        rmse_sfm_roll = mean_absolute_error(self.opensfm[2]-np.median(self.opensfm[2]), self.groundtruth[4]-np.median(self.groundtruth[4]))
        rmse_sfm_pitch = mean_absolute_error(self.opensfm[3]-np.median(self.opensfm[3]), self.groundtruth[5]-np.median(self.groundtruth[5]))
        rmse_sfm_yaw = mean_absolute_error(self.opensfm[4]-np.median(self.opensfm[4]), self.groundtruth[6]-np.median(self.groundtruth[6]))

        rmse_droid_roll = mean_absolute_error(self.droidslam[3]-np.median(self.droidslam[3]), self.groundtruth[4]-np.median(self.groundtruth[4]))
        rmse_droid_pitch = mean_absolute_error(self.droidslam[4]-np.median(self.droidslam[4]), self.groundtruth[5]-np.median(self.groundtruth[5]))
        rmse_droid_yaw = mean_absolute_error(self.droidslam[5]-np.median(self.droidslam[5]), self.groundtruth[6]-np.median(self.groundtruth[6]))

        rmse_opt_roll = mean_absolute_error(self.optimized[3]-np.median(self.optimized[3]), self.groundtruth[4]-np.median(self.groundtruth[4]))
        rmse_opt_pitch = mean_absolute_error(self.optimized[4]-np.median(self.optimized[4]), self.groundtruth[5]-np.median(self.groundtruth[5]))
        rmse_opt_yaw = mean_absolute_error(self.optimized[5]-np.median(self.optimized[5]), self.groundtruth[6]-np.median(self.groundtruth[6]))
        

        cwd = os.getcwd()
        tra = [[cwd ,rmse_orb, rmse_sfm, rmse_droid, rmse_opt]]
        roll = [[cwd, rmse_orb_roll, rmse_sfm_roll, rmse_droid_roll, rmse_opt_roll]]
        pitch = [[cwd, rmse_orb_pitch, rmse_sfm_pitch, rmse_droid_pitch, rmse_opt_pitch]]
        yaw = [[cwd, rmse_orb_yaw, rmse_sfm_yaw, rmse_droid_yaw, rmse_opt_yaw]]

        f1 = open('/home/sora-lab/Desktop/kitti_csv/tra.csv', mode="a", newline="")
        writer1 = csv.writer(f1)
        for data in tra:
            writer1.writerow(data)
        f1.close()

        f2 = open('/home/sora-lab/Desktop/kitti_csv/roll.csv', mode="a", newline="")
        writer2 = csv.writer(f2)
        for data in roll:
            writer2.writerow(data)
        f2.close()

        f3 = open('/home/sora-lab/Desktop/kitti_csv/pitch.csv', mode="a", newline="")
        writer3 = csv.writer(f3)
        for data in pitch:
            writer3.writerow(data)
        f3.close()

        f4 = open('/home/sora-lab/Desktop/kitti_csv/yaw.csv', mode="a", newline="")
        writer4 = csv.writer(f4)
        for data in yaw:
            writer4.writerow(data)
        f4.close()


CalcRMSE().calc_eva()