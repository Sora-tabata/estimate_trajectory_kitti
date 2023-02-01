import matplotlib.pyplot as plt
import matplotlib
plt.rcParams["font.family"] = "Times New Roman"
import matplotlib
import matplotlib as mpl
import csv
from mpl_toolkits.mplot3d import Axes3D
from scipy.spatial.transform import Rotation
import numpy as np
from calc_traj import CalcTraj
import glob
from equalize_est import Equalize

class ViewCoord():
    def __init__(self):
        pass
    #    self.N0 = np.loadtxt(glob.glob('ID*')[0], encoding="shift-jis", delimiter=',', skiprows=2, usecols=[2, 39, 40, 41])
    #    self.M0 = np.loadtxt(glob.glob('ID*')[0], encoding="shift-jis", delimiter=',', skiprows=2, usecols=[8, 9, 10, 13])
    #    self.gps_t = np.loadtxt(glob.glob('ID*')[0], encoding="shift-jis", delimiter=',', skiprows=2, usecols=[30, 31])
    #    self.L0 = np.loadtxt('KeyFrameTrajectory.txt', delimiter=' ')
    #    self.json_file0 = open('reconstruction.json', 'r')
    #    self.groundtruth = CalcTraj().calcGroundTruth(self.N0, self.M0)
    #    self.orbslam = CalcTraj().calcOrbslam(self.groundtruth, self.L0)
    #    self.opensfm = CalcTraj().calcOpensfm(self.groundtruth, self.json_file0)
    
    def showTrajectory(self, groundtruth, opensfm, orbslam, droidslam, optimized, equalizedORB, equalizedDROID):
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, traj = plt.subplots(figsize=(10, 10))
        traj.scatter(opensfm[11], opensfm[12], color="red", s=0.7, label="OpenSfM")
        #traj.scatter(orbslam[12], orbslam[13], color="green", s=0.7, label="ORB-SLAM2")
        #traj.scatter(droidslam[11], droidslam[12], color="blue", s=0.7, label="DROID-SLAM")
        traj.scatter(equalizedORB[6], equalizedORB[7], color="lightgreen", s=0.4, label="equalized ORB-SLAM2")
        traj.scatter(equalizedDROID[6], equalizedDROID[7], color="cyan", s=0.4, label="equalized DROID-SLAM")
        traj.scatter(groundtruth[1], groundtruth[2], color="black", s=0.7, label="Ground Truth")
        traj.scatter(optimized[0], optimized[1], color="magenta", s=0.1, label="Integrated")
        traj.set_aspect('equal')
        traj.legend(fancybox=False, shadow=False, edgecolor='black', fontsize=20)
        traj.set_ylabel("Depth direction [m]", fontsize=20)
        traj.set_xlabel("Lateral direction [m]", fontsize=20)
        traj.set_title("Trajectory", fontsize=20)
        plt.rcParams["font.family"] = "Times New Roman"
        #plt.xlim(375, 600)
        #plt.ylim(380, 540)
        plt.grid(True)
        plt.savefig('output/opted/trajectory.png')
        #plt.show()
    
    def showZ(self, groundtruth, opensfm, orbslam, droidslam, optimized):
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, traj = plt.subplots()
        time = CalcTraj().Nx
        #traj.plot(groundtruth[1], groundtruth[0], color="black", lw=0.5, label="Ground Truth")
        traj.plot(opensfm[10], opensfm[9][1:], color="red", lw=2, label="OpenSfM")
        #traj.plot(orbslam[11], orbslam[2][1:], color="green", lw=2, label="ORB-SLAM2")
        traj.plot(droidslam[10], droidslam[2][1:], color="blue", lw=2, label="DROID-SLAM")
        #traj.plot(time, optimized[2], color="magenta", lw=4, label="Optimized")
        #traj.set_aspect('equal')
        traj.legend(fancybox=False, shadow=False, edgecolor='black')
        traj.set_ylabel("Depth direction [m]")
        traj.set_xlabel("Lateral direction [m]")
        traj.set_title("Z")
        plt.rcParams["font.family"] = "Times New Roman"
        plt.grid(True)
        plt.savefig('output/opted/z.png')
        #plt.show()
    
    def showRoll(self, groundtruth, opensfm, orbslam, droidslam, optimized, equalizedORB, equalizedDROID):
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, roll = plt.subplots(figsize=(40, 8))
        time = CalcTraj().Nx
        #time2x = N2x
        #print(opensfm[4][0], "roll_opensfm")
        roll.plot(time, opensfm[2]-np.median(opensfm[2]), color="red", lw=2, label="OpenSfM")
        #roll.plot(time, droidslam[3]-np.median(droidslam[3]), color="blue", lw=2, label="DROID-SLAM")
        #roll.plot(time, orbslam[3]-np.median(orbslam[3]), color="green", lw=2, label="ORB-SLAM2")
        roll.plot(time, equalizedORB[3]-np.median(equalizedORB[3]), color="lightgreen", lw=2, label="equalized ORB-SLAM2")
        roll.plot(time, equalizedDROID[3]-np.median(equalizedDROID[3]), color="cyan", lw=2, label="equalized DROID-SLAM")
        roll.plot(time, groundtruth[4]-np.median(groundtruth[4]), color="black", lw=2, label="Ground Truth")
        roll.plot(time, optimized[3]-np.median(optimized[3]), color="magenta", lw=4, label="Optimized")
        roll.legend(fancybox=False, shadow=False, edgecolor='black',fontsize=20)
        roll.set_xlabel("Time [s]", fontsize=20)
        roll.set_ylabel("Roll angle [deg]", fontsize=20)
        roll.set_title("Roll angle", fontsize=20)
        plt.rcParams["font.family"] = "Times New Roman"
        plt.grid(True)
        plt.savefig('output/opted/roll.png')
        #plt.show()
    
    def showPitch(self, groundtruth, opensfm, orbslam, droidslam, optimized, equalizedORB, equalizedDROID):
        plt.rcParams['font.family'] = 'Times New Roman'
        fig, pitch = plt.subplots(figsize=(40, 8))
        time = CalcTraj().Nx
        #time2x = N2x
        #print(opensfm[3][0], "pitch_opensfm")
        pitch.plot(time, opensfm[3]-np.median(opensfm[3]), color="red", lw=2, label="OpenSfM")
        #pitch.plot(time, droidslam[4]-np.median(droidslam[4]), color="blue", lw=2, label="DROID-SLAM")
        #pitch.plot(time, orbslam[4]-np.median(orbslam[4]), color="green", lw=2, label="ORB-SLAM2")
        pitch.plot(time, equalizedORB[4]-np.median(equalizedORB[4]), color="lightgreen", lw=2, label="equalized ORB-SLAM2")
        pitch.plot(time, equalizedDROID[4]-np.median(equalizedDROID[4]), color="cyan", lw=2, label="equalized DROID-SLAM")
        pitch.plot(time, groundtruth[5]-np.median(groundtruth[5]), color="black", lw=2, label="Ground Truth")
        pitch.plot(time, optimized[4]-np.median(optimized[4]), color="magenta", lw=4, label="Optimized")
        pitch.legend(fancybox=False, shadow=False, edgecolor='black', fontsize=20)
        pitch.set_xlabel("Time [s]", fontsize=20)
        pitch.set_ylabel("Pitch angle [deg]", fontsize=20)
        pitch.set_title("Pitch angle", fontsize=20)
        plt.rcParams["font.family"] = "Times New Roman"
        plt.grid(True)
        plt.savefig('output/opted/pitch.png')
        #plt.show()

    def showYaw(self, groundtruth, opensfm, orbslam, droidslam, optimized, equalizedORB, equalizedDROID):
        plt.rcParams['font.family'] = 'Times New Roman'
        fig,yaw = plt.subplots(figsize=(40, 8))
        time = CalcTraj().Nx
        #time2x = N2x
        #print(opensfm[2][0], "yaw_opensfm")
        yaw.plot(time, opensfm[4]-np.median(opensfm[4]), color="red", lw=2, label="OpenSfM")
        #yaw.plot(time, droidslam[5]-np.median(droidslam[5]), color="blue", lw=2, label="DROID-SLAM")
        #yaw.plot(time, orbslam[5]-np.median(orbslam[5]), color="green", lw=2, label="ORB-SLAM2")
        yaw.plot(time, equalizedORB[5]-np.median(equalizedORB[5]), color="lightgreen", lw=2, label="equalized ORB-SLAM2")
        yaw.plot(time, equalizedDROID[5]-np.median(equalizedDROID[5]), color="cyan", lw=2, label="equalized DROID-SLAM")
        yaw.plot(time, groundtruth[6]-np.median(groundtruth[6]), color="black", lw=2, label="Ground Truth")
        yaw.plot(time, optimized[5]-np.median(optimized[5]), color="magenta", lw=4, label="Optimized")
        yaw.legend(fancybox=False, shadow=False, edgecolor='black', fontsize=20)
        yaw.set_xlabel("Time [s]", fontsize=20)
        yaw.set_ylabel("Yaw angle [deg]", fontsize=20)
        yaw.set_title("Yaw angle", fontsize=20)
        plt.rcParams["font.family"] = "Times New Roman"
        plt.grid(True)
        plt.savefig('output/opted/yaw.png')
        #plt.show()