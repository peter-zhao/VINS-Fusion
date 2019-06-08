# This script is to run all the experiments in one program

import os
import subprocess
import time
import signal

# SeqNameList = ['V2_02_medium'];
# SeqNameList = ['MH_01_easy', 'V2_02_medium', 'MH_05_difficult'];
SeqNameList = ['MH_01_easy', 'MH_02_easy', 'MH_03_medium', 'MH_04_difficult', 'MH_05_difficult', 'V1_01_easy', 'V1_02_medium', 'V1_03_difficult', 'V2_01_easy', 'V2_02_medium', 'V2_03_difficult'];

Result_root = '/mnt/DATA/tmp/EuRoC/vins_Stereo_IMU_Speedx'

Playback_Rate_List = [1.0] # [1.0, 2.0, 4.0];

# Number_GF_List = [70, 150, 200, 400, 600, 800]; 
Number_GF_List = [150] # [70, 150, 200, 400]; 

Num_Repeating = 10 # 20 #  5 # 
SleepTime = 5

config_prefix = '/home/yipuzhao/catkin_ws/src/VINS-Fusion/config/euroc/euroc_stereo_imu_config'

#----------------------------------------------------------------------------------------------------------------------
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    ALERT = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

subprocess.call('rosparam set use_sim_time true', shell=True)

for pi, rate in enumerate(Playback_Rate_List):
    for ri, num_gf in enumerate(Number_GF_List):
        
        Experiment_prefix = 'ObsNumber_' + str(int(num_gf))

        for iteration in range(0, Num_Repeating):

            Experiment_dir = Result_root + str(rate) + '/' \
             + Experiment_prefix + '_Round' + str(iteration + 1)
            cmd_mkdir = 'mkdir -p ' + Experiment_dir
            subprocess.call(cmd_mkdir, shell=True)

            for sn, sname in enumerate(SeqNameList):
                
                print bcolors.ALERT + "====================================================================" + bcolors.ENDC

                SeqName = SeqNameList[sn] #+ '_blur_9'
                print bcolors.ALERT + "Round: " + str(iteration + 1) + "; Seq: " + SeqName

                File_rosbag  = '/mnt/DATA/Datasets/EuRoC_dataset/BagFiles/' + SeqName + '.bag'
                Config_Yaml = config_prefix + '_lmk' + str(num_gf) + '.yaml'

                cmd_vinsrun   = str('rosrun vins vins_node ' + Config_Yaml)
                cmd_looprun   = str('rosrun loop_fusion loop_fusion_node ' + Config_Yaml)
                cmd_rosbag = 'rosbag play ' + File_rosbag + ' --clock -r ' + str(rate)
                cmd_timelog = str('cp /mnt/DATA/vins_tmpLog.txt ' + Experiment_dir + '/' + SeqName + '_Log.txt')
                cmd_vinslog = str('cp /mnt/DATA/vio.csv ' + Experiment_dir + '/' + SeqName + '_AllFrameTrajectory.txt')
                cmd_looplog = str('cp /mnt/DATA/vio_loop.csv ' + Experiment_dir + '/' + SeqName + '_KeyFrameTrajectory.txt')

                print bcolors.WARNING + "cmd_vinsrun: \n"   + cmd_vinsrun   + bcolors.ENDC
                print bcolors.WARNING + "cmd_looprun: \n"   + cmd_looprun   + bcolors.ENDC
                print bcolors.WARNING + "cmd_rosbag: \n" + cmd_rosbag + bcolors.ENDC
                print bcolors.WARNING + "cmd_timelog: \n" + cmd_timelog + bcolors.ENDC
                print bcolors.WARNING + "cmd_vinslog: \n" + cmd_vinslog + bcolors.ENDC
                print bcolors.WARNING + "cmd_looplog: \n" + cmd_looplog + bcolors.ENDC

                print bcolors.OKGREEN + "Launching SLAM" + bcolors.ENDC
                proc_vins = subprocess.Popen(cmd_vinsrun, shell=True)
                proc_loop = subprocess.Popen(cmd_looprun, shell=True)
                # proc_slam = subprocess.Popen("exec " + cmd_slam, stdout=subprocess.PIPE, shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to wait for vins_estimator init" + bcolors.ENDC
                time.sleep(SleepTime)

                print bcolors.OKGREEN + "Launching rosbag" + bcolors.ENDC
                proc_bag = subprocess.call(cmd_rosbag, shell=True)

                print bcolors.OKGREEN + "Finished rosbag playback, kill the process" + bcolors.ENDC
                subprocess.call('rosnode kill /loop_fusion', shell=True)
                subprocess.call('rosnode kill /vins_estimator', shell=True)
                # subprocess.call('pkill roslaunch', shell=True)
                # subprocess.call('pkill svo_node', shell=True)

                print bcolors.OKGREEN + "Sleeping for a few secs to wait for vins_estimator to quit" + bcolors.ENDC
                time.sleep(SleepTime)
                print bcolors.OKGREEN + "Copy the time log to result folder" + bcolors.ENDC
                subprocess.call(cmd_timelog, shell=True)
                print bcolors.OKGREEN + "Copy the local optim. track to result folder" + bcolors.ENDC
                subprocess.call(cmd_vinslog, shell=True)
                print bcolors.OKGREEN + "Copy the global optim. track to result folder" + bcolors.ENDC
                subprocess.call(cmd_looplog, shell=True)
                # proc_rec.terminate()
                # outs, errs = proc_rec.communicate()
                # proc_slam.kill()
