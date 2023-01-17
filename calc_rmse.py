from sklearn.metrics import mean_squared_error
import numpy as np
from calc_traj import CalcTraj
from init import Init
from calc_RT__ import CalcRT
from optimize_traj7 import OptimizeTraj
import numpy as np
from equalize_est import Equalize
import os


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
        rmse_orb_x = np.sqrt(mean_squared_error(self.orbslam[0], self.groundtruth[1]))
        rmse_orb_y = np.sqrt(mean_squared_error(self.orbslam[1], self.groundtruth[2]))
        rmse_sfm_x = np.sqrt(mean_squared_error(self.opensfm[0], self.groundtruth[1]))
        rmse_sfm_y = np.sqrt(mean_squared_error(self.opensfm[1], self.groundtruth[2]))
        rmse_droid_x = np.sqrt(mean_squared_error(self.droidslam[0], self.groundtruth[1]))
        rmse_droid_y = np.sqrt(mean_squared_error(self.droidslam[1], self.groundtruth[2]))
        rmse_opt_x = np.sqrt(mean_squared_error(self.optimized[0], self.groundtruth[1]))
        rmse_opt_y = np.sqrt(mean_squared_error(self.optimized[1], self.groundtruth[2]))

        rmse_orb = (rmse_orb_x + rmse_orb_y)/2
        rmse_sfm = (rmse_sfm_x + rmse_sfm_y)/2
        rmse_droid = (rmse_droid_x + rmse_droid_y)/2
        rmse_opt = (rmse_opt_x + rmse_opt_y)/2
        print(os.getcwd())
        print("RMSE_ORB-SLAM2", rmse_orb)
        print("RMSE_OpenSfM", rmse_sfm)
        print("RMSE_DROID-SLAM", rmse_droid)
        print("RMSE_Optimized", rmse_opt)

CalcRMSE().calc_RMSE()