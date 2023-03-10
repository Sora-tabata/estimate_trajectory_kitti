import json
import cv2
import numpy as np
from scipy import integrate, signal, interpolate
import matplotlib.pyplot as plt
import matplotlib
import matplotlib as mpl
import csv
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation
import math
import glob
from init import Init
import orbslam_eva
from make_testlist import MakeTestList
MakeTestList().exportFile()


class CalcTraj():
    def __init__(self):
        a = Init()
        self.n_frame = a.n_frame
        self.Nx = a.Nx
        self.ground_time = a.ground_time
        self.ground_data = a.ground_data

    @staticmethod
    def rotationMatrixToEulerAngles(self, R):
        sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

        singular = sy < 1e-6

        if not singular:
            pitch = math.atan2(R[2, 1], R[2, 2])
            roll = math.atan2(-R[2, 0], sy)
            yaw = math.atan2(R[1, 0], R[0, 0])
        else:
            pitch = math.atan2(-R[1, 2], R[1, 1])
            roll = math.atan2(-R[2, 0], sy)
            yaw = 0

        return np.array([-roll, -pitch, yaw])

    def calcGroundTruth(self, ground_time, res_time, ground_data):
        time = self.Nx
        data= orbslam_eva.gen_data(ground_time, res_time, ground_data)[1]
        ground_R = np.asarray(orbslam_eva.get_R(data)).T
        ground_points = np.asarray(orbslam_eva.get_coo(data))
        #print(ground_R.shape)
        l = np.zeros(self.n_frame-1)
        L = 0
        distance = []
        #print(ground_points.shape)
        for n in range(self.n_frame-1):
            l[n] = np.sqrt(
                (ground_points[0][n + 1] - ground_points[0][n]) ** 2 +  (ground_points[1][n + 1] - ground_points[1][n]) ** 2 + (ground_points[2][n + 1] - ground_points[2][n]) ** 2)
            L = L + l[n]
            distance.append(L)
        R_ = np.identity(3)
        eul = []
        for i in range(len(time)):
            eul.append([CalcTraj.rotationMatrixToEulerAngles(self, np.array(R_).T @ np.array(ground_R[i]))])
            R_ = ground_R[i]
        r1 = np.zeros(self.n_frame)
        p1 = np.zeros(self.n_frame)
        ya1 = np.zeros(self.n_frame)
        r1_ = np.rad2deg(np.cumsum(np.array(eul).T[0]))
        p1_ = np.rad2deg(np.cumsum(np.array(eul).T[1]))
        ya1_ = np.rad2deg(np.cumsum(np.array(eul).T[2]))
        for i in range(self.n_frame):
            r1[i] = ya1_[i] #% 360 - 180
            p1[i] = p1_[i] #% 360 - 180
            ya1[i] = r1_[i]

        return L, ground_points[0], ground_points[2], ground_points[1], r1 - r1[0], p1 - p1[0], ya1 - ya1[0]

    
    

    def calcOrbslam(self, groundtruth, L):
        ground_time = self.ground_time
        ground_data = self.ground_data
        groundtruth = CalcTraj().calcGroundTruth(ground_time, Init().L0, ground_data)
        
        time = self.Nx
        t_orb = L[:, 0]  # /1000000000
        x_orb = L[:, 3]
        y_orb = L[:, 1]
        z_orb = -L[:, 2]
        q0 = L[:, 4]#7
        q1 = L[:, 5]#6
        q2 = L[:, 6]#4
        q3 = L[:, 7]#5
        r1 = np.zeros(len(q0))
        p1 = np.zeros(len(q0))
        ya1 = np.zeros(len(q0))
        for i in range(len(q0)):
            r1[i] = np.rad2deg(
                np.arctan(2 * (q0[i] * q1[i] + q2[i] * q3[i]) / (q0[i] ** 2 - q1[i] ** 2 - q2[i] ** 2 + q3[i] ** 2)))
            p1[i] = np.rad2deg(np.arcsin(2 * (q0[i] * q2[i] - q1[i] * q3[i])))
            ya1[i] = np.rad2deg(
                np.arctan(2 * (q0[i] * q3[i] + q2[i] * q1[i]) / (q0[i] ** 2 + q1[i] ** 2 - q2[i] ** 2 - q3[i] ** 2)))
        
        q0_ = interpolate.interp1d(t_orb, L[:, 4], kind="linear",fill_value="extrapolate")(time)#7##5
        q1_ = interpolate.interp1d(t_orb, L[:, 5], kind="linear",fill_value="extrapolate")(time)#6##6
        q2_ = interpolate.interp1d(t_orb, L[:, 6], kind="linear",fill_value="extrapolate")(time)#4##7
        q3_ = interpolate.interp1d(t_orb, L[:, 7], kind="linear",fill_value="extrapolate")(time)#5##4
        
        R = []
        R_ = np.identity(3)
        eul = []
        for i in range(len(time)):
            R.append([[q0_[i] ** 2 + q1_[i] ** 2 - q2_[i] ** 2 - q3_[i] ** 2, 2 * (q1_[i] * q2_[i] - q0_[i] * q3_[i]),
                    2 * (q0_[i] * q2_[i] + q1_[i] * q3_[i])],
                    [2 * (q0_[i] * q3_[i] + q1_[i] * q2_[i]), q0_[i] ** 2 - q1_[i] ** 2 + q2_[i] ** 2 - q3_[i] ** 2,
                    2 * (-q0_[i] * q1_[i] + q2_[i] * q3_[i])],
                    [2 * (q1_[i] * q3_[i] - q0_[i] * q2_[i]), 2 * (q2_[i] * q3_[i] + q0_[i] * q1_[i]),
                    q0_[i] ** 2 - q1_[i] ** 2 - q2_[i] ** 2 + q3_[i] ** 2]])
            eul.append([CalcTraj.rotationMatrixToEulerAngles(self, np.array(R_).T @ np.array(R[i]))])
            R_ = R[i]
        
        r1 = np.zeros(self.n_frame)
        p1 = np.zeros(self.n_frame)
        ya1 = np.zeros(self.n_frame)
        #???????????????
        #print(np.array(eul).T[0])
        #R4 = R3 @ np.linalg.inv(R3)
        r1_ = np.rad2deg(np.cumsum(np.array(eul).T[0]))
        p1_ = np.rad2deg(np.cumsum(np.array(eul).T[1]))
        ya1_ = np.rad2deg(np.cumsum(np.array(eul).T[2]))
        for i in range(self.n_frame):
            r1[i] = -p1_[i]
            p1[i] = (ya1_[i] - 180)
            ya1[i] = r1_[i]

        
        
        
        #f1 = interpolate.interp1d(t_orb, r1, kind="linear", fill_value=(r1[0], r1[len(r1)-1]),bounds_error=False)#(r1[0], r1[len(r1)-1])
        #f2 = interpolate.interp1d(t_orb, ya1, kind="linear", fill_value=(ya1[0], ya1[len(ya1)-1]),bounds_error=False)
        #f3 = interpolate.interp1d(t_orb, p1, kind="linear", fill_value=(p1[0], p1[len(p1)-1]),bounds_error=False)
        f4 = interpolate.interp1d(t_orb, x_orb, kind="linear", fill_value="extrapolate")
        f5 = interpolate.interp1d(t_orb, y_orb, kind="linear", fill_value="extrapolate")
        f6 = interpolate.interp1d(t_orb, z_orb, kind="linear", fill_value="extrapolate")
        #r1_re = f1(time)
        #ya1_re = -f3(time)
        #p1_re = f2(time)
        
        x_re = f4(time)
        y_re = f5(time)
        z_re = f6(time)
        l_orb = np.zeros(len(time))
        L_orb = 0
        distance = []
        #print(np.array(x_re).shape, "len")
        for n in range(len(x_re)-1):
            l_orb[n] = np.sqrt((x_re[n + 1] - x_re[n]) ** 2 + (y_re[n + 1] - y_re[n]) ** 2 + (z_re[n + 1] - z_re[n]) ** 2)
            L_orb = L_orb + l_orb[n]
            distance.append(L_orb)

        k_v=groundtruth[0]/L_orb
        x_vf = x_re * k_v
        y_vf = y_re * k_v
        z_vf = z_re * k_v

        x_ = np.vstack([y_vf, x_vf, z_vf]).T
        y_ = np.vstack([groundtruth[1], groundtruth[2], groundtruth[3]]).T
        y__ = y_.copy()
        x_ = x_ - x_.mean(axis=0)
        y_ = y_ - y_.mean(axis=0)
        
        U, S, VT = np.linalg.svd(y_.T @ x_)
        R__ = U @ VT
        R_det = np.linalg.det(R__)
        sigma = np.array([[1, 0, 0], [0, 1, 0], [0, 0, R_det]])
        R = U @ sigma @ VT
        x_ = (R @ x_.T).T

        #x_[:, 0], x_[:, 1], z_vf-z_vf[0], r1_re, p1_re, ya1_re, t_orb, x_re, y_re, z_re, k_v, np.array(distance)*k_v
        #y_vf-y_vf[0], x_vf-x_vf[0], z_vf-z_vf[0], r1_re, p1_re, ya1_re, t_orb, x_re, y_re, z_re, k_v, np.array(distance)*k_v
        #y_vf-y_vf[0], x_vf-x_vf[0], z_vf-z_vf[0], r1-r1[0], p1-p1[0], ya1-ya1[0], t_orb, x_re, y_re, z_re, k_v, np.array(distance)*k_v,x_[:, 0]+y__.mean(axis=0)[0], x_[:, 1]+y__.mean(axis=0)[1], x_[:, 2]+y__.mean(axis=0)[2]
        return y_vf, x_vf, z_vf, r1, p1, ya1, t_orb, x_re, y_re, z_re, k_v, np.array(distance)*k_v,x_[:, 0]+y__.mean(axis=0)[0], x_[:, 1]+y__.mean(axis=0)[1], x_[:, 2]+y__.mean(axis=0)[2]
    
    def calcOpensfm(self, groundtruth, json_file):
        ground_time = self.ground_time
        ground_data = self.ground_data
        groundtruth = CalcTraj().calcGroundTruth(ground_time, Init().L0, ground_data)
        
        time = self.Nx
        json_object = json.load(json_file)
        f = open('test_list.txt', 'r')
        name_data = f.read().splitlines()
        f.close()

        roll_est = np.zeros(len(name_data))
        pitch_est = np.zeros(len(name_data))
        yaw_est = np.zeros(len(name_data))
        x_est = np.zeros(len(name_data))
        y_est = np.zeros(len(name_data))
        z_est = np.zeros(len(name_data))
        list = np.array(range(len(name_data)))

        for i, j in zip(list, name_data):
            try:
                roll_est[i] = json_object[0]["shots"][j]["rotation"][0]
                pitch_est[i] = json_object[0]["shots"][j]["rotation"][1]
                yaw_est[i] = json_object[0]["shots"][j]["rotation"][2]
                x_est[i] = json_object[0]["shots"][j]["translation"][0]
                y_est[i] = json_object[0]["shots"][j]["translation"][1]
                z_est[i] = json_object[0]["shots"][j]["translation"][2]
            except KeyError:
                #print("???????????????", i, j)
                continue
        #print(roll_est[0], pitch_est[0], yaw_est[0])
        t = np.vstack([x_est, y_est, z_est]).T
        R3 = []
        for i in range(len(name_data)):
            R3.append(np.array(cv2.Rodrigues(np.array([roll_est[i], pitch_est[i], yaw_est[i]]))[0]).T)
        xyz = []
        for i in range(len(name_data)):
            xyz.append(-np.dot(np.array(R3[i]).T.T, t[i]))
        x_sfm = np.array(xyz)[:, 0]
        y_sfm = np.array(xyz)[:, 1]
        z_sfm = np.array(xyz)[:, 2]
        l_sfm = np.zeros(len(name_data)-1)
        L_sfm = 0
        distance = []
        for n in range(len(name_data)-1):
            l_sfm[n] = np.sqrt(
                (x_sfm[n + 1] - x_sfm[n]) ** 2 + (y_sfm[n + 1] - y_sfm[n]) ** 2 + (z_sfm[n + 1] - z_sfm[n]) ** 2)
            L_sfm = L_sfm + l_sfm[n]
            distance.append(L_sfm)
        k_sfm = groundtruth[0] / L_sfm
        y_ = np.vstack([groundtruth[2], groundtruth[1], groundtruth[3]]).T
        x_ = k_sfm*np.vstack([x_sfm[:], y_sfm[:], z_sfm[:]]).T  # colmap
        x__ = x_.copy()
        y__ = y_.copy()
        x_ = x_ - x_.mean(axis=0)  # genten
        y_ = y_ - y_.mean(axis=0)


        U, S, VT = np.linalg.svd(y_.T @ x_)
        R__ = U @ VT
        R_det = np.linalg.det(R__)
        sigma = np.array([[1, 0, 0], [0, 1, 0], [0, 0, R_det]])
        R = U @ sigma @ VT
        x_ = (R @ x_.T).T
        r1 = np.zeros(len(name_data))
        p1 = np.zeros(len(name_data))
        ya1 = np.zeros(len(name_data))
        #???????????????

        #R4 = R3 @ np.linalg.inv(R3)
        for i in range(len(name_data)):
            eul = np.rad2deg(CalcTraj.rotationMatrixToEulerAngles(self, R3[i]))
            r1[i] = -eul[0]
            p1[i] = eul[1] - 90
            ya1[i] = -eul[2]
        R_ = []
        #x__[:, 0]-x__[:, 0][0], x__[:, 1]-x__[:, 1][0], r1-r1[0], p1-p1[0],ya1-ya1[0], t*k_sfm, R3,k_sfm*np.array(xyz), R_, x_[:, 2]-x_[:, 2][0], np.array(distance)*k_sfm, x_[:, 1]+y__.mean(axis=0)[1], x_[:, 0]+y__.mean(axis=0)[0]
        return x__[:, 0], x__[:, 1], r1, p1,ya1, t*k_sfm, R3,k_sfm*np.array(xyz), R_, x_[:, 2], np.array(distance)*k_sfm, x_[:, 1]+y__.mean(axis=0)[1], x_[:, 0]+y__.mean(axis=0)[0]

    
    def calcDroidslam(self, groundtruth, L):
        time = self.Nx
        #quotient = len(groundtruth[0]) // len(time)
        #remainder = len(groundtruth[0]) % len(time)
        t_orb = L[:, 0]
        '''
        q0 = interpolate.interp1d(t_orb, L[:, 4], kind="quadratic",fill_value="extrapolate")(time)#7##5
        q1 = interpolate.interp1d(t_orb, L[:, 7], kind="quadratic",fill_value="extrapolate")(time)#6##6
        q2 = interpolate.interp1d(t_orb, L[:, 6], kind="quadratic",fill_value="extrapolate")(time)#4##7
        q3 = interpolate.interp1d(t_orb, L[:, 5], kind="quadratic",fill_value="extrapolate")(time)#5##4
        '''

        t_x = L[:, 1]
        t_y = L[:, 2]
        t_z = L[:, 3]
        
        q0 = L[:, 4]
        q1 = L[:, 7]
        q2 = L[:, 6]
        q3 = L[:, 5]

        R = []
        for i in range(len(L)):
            R.append([[q0[i] ** 2 + q1[i] ** 2 - q2[i] ** 2 - q3[i] ** 2, 2 * (q1[i] * q2[i] - q0[i] * q3[i]),
                    2 * (q0[i] * q2[i] + q1[i] * q3[i])],
                    [2 * (q0[i] * q3[i] + q1[i] * q2[i]), q0[i] ** 2 - q1[i] ** 2 + q2[i] ** 2 - q3[i] ** 2,
                    2 * (-q0[i] * q1[i] + q2[i] * q3[i])],
                    [2 * (q1[i] * q3[i] - q0[i] * q2[i]), 2 * (q2[i] * q3[i] + q0[i] * q1[i]),
                    q0[i] ** 2 - q1[i] ** 2 - q2[i] ** 2 + q3[i] ** 2]])
        R3 = R.copy()
        t = np.vstack([t_z, t_y, t_x]).T
        #t = np.vstack([t_z, t_y, t_x]).T
        xyz = []
        for i in range(len(L)):
            xyz.append(-np.dot(np.array(R[i]).T, t[i]))
        xyz = np.array(xyz)
        new_t = []
        for i in t_orb:
            try:
                new_t.append(time[int(i)])
            except:
                new_t = t_orb
                break
        x_droid = interpolate.interp1d(new_t, xyz[:, 0], kind="linear",fill_value="extrapolate")(time)#7##5
        y_droid = interpolate.interp1d(new_t, xyz[:, 1], kind="linear",fill_value="extrapolate")(time)#7##5
        z_droid = interpolate.interp1d(new_t, xyz[:, 2], kind="linear",fill_value="extrapolate")(time)#7##5
        '''
        x_droid = xyz[:, 0]
        y_droid = xyz[:, 1]
        z_droid = xyz[:, 2]
        '''
        t_ = np.vstack([z_droid, x_droid, y_droid]).T
        t__ = np.vstack([x_droid, y_droid, z_droid]).T
        l_sfm = np.zeros(len(time)-1)
        L_sfm = 0
        distance = []

        for n in range(len(time)-1):
            l_sfm[n] = np.sqrt(
                (x_droid[n + 1] - x_droid[n]) ** 2 + (y_droid[n + 1] - y_droid[n]) ** 2 + (z_droid[n + 1] - z_droid[n]) ** 2)
            L_sfm = L_sfm + l_sfm[n]
            distance.append(L_sfm)
        k_sfm = groundtruth[0] / L_sfm
        y_ = np.vstack([groundtruth[2], groundtruth[1], groundtruth[3]]).T
        y__ = y_.copy()
        x_ = k_sfm*np.vstack([z_droid[:], x_droid[:], y_droid[:]]).T  # colmap
        x__ = x_.copy()
        #x_ = k_sfm*np.vstack([z_droid[:], y_droid[:], x_droid[:]]).T
        x_ = x_ - x_.mean(axis=0)  # genten
        y_ = y_ - y_.mean(axis=0)
        U, S, VT = np.linalg.svd(y_.T @ x_)
        R__ = U @ VT
        R_det = np.linalg.det(R__)
        sigma = np.array([[1, 0, 0], [0, 1, 0], [0, 0, R_det]])
        R = U @ sigma @ VT
        x_ = (R @ x_.T).T
        #droid_x = interpolate.interp1d(t_orb*(1/14), x_[:, 0], kind="linear",fill_value="extrapolate")(time)#7##5
        #droid_y = interpolate.interp1d(t_orb*(1/14), x_[:, 1], kind="linear",fill_value="extrapolate")(time)#7##5
        '''
        q0_ = interpolate.interp1d(t_orb, L[:, 5], kind="linear",fill_value="extrapolate")(time)#7##5
        q1_ = interpolate.interp1d(t_orb, L[:, 6], kind="linear",fill_value="extrapolate")(time)#6##6
        q2_ = interpolate.interp1d(t_orb, L[:, 7], kind="linear",fill_value="extrapolate")(time)#4##7
        q3_ = interpolate.interp1d(t_orb, L[:, 4], kind="linear",fill_value="extrapolate")(time)#5##4
        
        R1 = []
        R_ = np.identity(3)
        eul = []
        for i in range(len(time)):
            R1.append([[q0_[i] ** 2 + q1_[i] ** 2 - q2_[i] ** 2 - q3_[i] ** 2, 2 * (q1_[i] * q2_[i] - q0_[i] * q3_[i]),
                    2 * (q0_[i] * q2_[i] + q1_[i] * q3_[i])],
                    [2 * (q0_[i] * q3_[i] + q1_[i] * q2_[i]), q0_[i] ** 2 - q1_[i] ** 2 + q2_[i] ** 2 - q3_[i] ** 2,
                    2 * (-q0_[i] * q1_[i] + q2_[i] * q3_[i])],
                    [2 * (q1_[i] * q3_[i] - q0_[i] * q2_[i]), 2 * (q2_[i] * q3_[i] + q0_[i] * q1_[i]),
                    q0_[i] ** 2 - q1_[i] ** 2 - q2_[i] ** 2 + q3_[i] ** 2]])
            eul.append([CalcTraj.rotationMatrixToEulerAngles(self, np.array(R_).T @ np.array(R1[i]))])
            R_ = R1[i]
        
        r1 = np.zeros(self.n_frame)
        p1 = np.zeros(self.n_frame)
        ya1 = np.zeros(self.n_frame)
        #???????????????
        #print(np.array(eul).T[0])
        #R4 = R3 @ np.linalg.inv(R3)
        r1_ = np.rad2deg(np.cumsum(np.array(eul).T[0]))
        p1_ = np.rad2deg(np.cumsum(np.array(eul).T[1]))
        ya1_ = np.rad2deg(np.cumsum(np.array(eul).T[2]))
        for i in range(self.n_frame):
            r1[i] = -p1_[i]
            p1[i] = -(ya1_[i] - 180)
            ya1[i] = r1_[i]
        '''
        q0 = L[:, 4]#7
        q1 = L[:, 7]#6
        q2 = L[:, 6]#4
        q3 = L[:, 5]#5
        r1_ = np.zeros(len(q0))
        p1_ = np.zeros(len(q0))
        ya1_ = np.zeros(len(q0))
        for i in range(len(q0)):
            r1_[i] = np.rad2deg(
                np.arctan(2 * (q0[i] * q1[i] + q2[i] * q3[i]) / (q0[i] ** 2 - q1[i] ** 2 - q2[i] ** 2 + q3[i] ** 2)))
            p1_[i] = np.rad2deg(np.arcsin(2 * (q0[i] * q2[i] - q1[i] * q3[i])))
            ya1_[i] = np.rad2deg(
                np.arctan(2 * (q0[i] * q3[i] + q2[i] * q1[i]) / (q0[i] ** 2 + q1[i] ** 2 - q2[i] ** 2 - q3[i] ** 2)))
        f1 = interpolate.interp1d(new_t, r1_, kind="linear", fill_value=(r1_[0], r1_[len(r1_)-1]),bounds_error=False)#(r1[0], r1[len(r1)-1])
        f2 = interpolate.interp1d(new_t, ya1_, kind="linear", fill_value=(ya1_[0], ya1_[len(ya1_)-1]),bounds_error=False)
        f3 = interpolate.interp1d(new_t, p1_, kind="linear", fill_value=(p1_[0], p1_[len(p1_)-1]),bounds_error=False)
        r1 = -f1(time)
        ya1 = f3(time)
        p1 = -f2(time)
        #-(x__[:, 0]-x__[:, 0][0]), x__[:, 1]-x__[:, 1][0], x__[:, 2]-x__[:, 2][0],r1-r1[0], p1-p1[0], ya1-ya1[0], t_*k_sfm, t__*k_sfm, R3, x_, np.array(distance)*k_sfm,x_[:, 1]+y__.mean(axis=0)[1], x_[:, 0]+y__.mean(axis=0)[0], x_[:, 2]-y__.mean(axis=0)[2]
        
        R_ = np.identity(3)
        eul = []
        for i in range(len(L)):
            eul.append([CalcTraj.rotationMatrixToEulerAngles(self, np.array(R_).T @ np.array(R3[i]))])
            R_ = R3[i]

        r1 = np.zeros(len(L))
        p1 = np.zeros(len(L))
        ya1 = np.zeros(len(L))
        r1_ = np.rad2deg(np.cumsum(np.array(eul).T[0]))
        p1_ = np.rad2deg(np.cumsum(np.array(eul).T[1]))
        ya1_ = np.rad2deg(np.cumsum(np.array(eul).T[2]))
        for i in range(len(L)):
            r1[i] = (ya1_[i] - 180)#p1_[i]
            p1[i] = p1_[i]#(ya1_[i] - 180)
            ya1[i] = r1_[i]
        
        f1 = interpolate.interp1d(new_t, r1, kind="linear", fill_value=(r1[0], r1[len(r1)-1]),bounds_error=False)#(r1[0], r1[len(r1)-1])
        f3 = interpolate.interp1d(new_t, ya1, kind="linear", fill_value=(ya1[0], ya1[len(ya1)-1]),bounds_error=False)
        f2 = interpolate.interp1d(new_t, p1, kind="linear", fill_value=(p1[0], p1[len(p1)-1]),bounds_error=False)
        r1 = f1(time)
        p1 = f2(time)
        ya1 = f3(time)
        
        return -(x__[:, 0]), x__[:, 1], x__[:, 2],r1, p1, ya1, t_*k_sfm, t__*k_sfm, R3, x_, np.array(distance)*k_sfm,x_[:, 1]+y__.mean(axis=0)[1], x_[:, 0]+y__.mean(axis=0)[0], x_[:, 2]-y__.mean(axis=0)[2]

