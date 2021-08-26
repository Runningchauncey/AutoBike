#!/usr/bin/python3

import numpy as np
import matplotlib.pyplot as plt
from cali_acc import accel_fit
#import get_data_accel as gdata


def import_data(filename):
    f = open(filename, "r")
    data = np.loadtxt(f, dtype="float")
    return data
    f.close()

if __name__ == "__main__":
    # data = import_data("imu/calib_coeffs_accel.txt")
    # print(data)
    accel_labels = ["a_x","a_y","a_z"]
    
    # calib_size = 1000
    # calib_rate = 100
    #test_data = np.array(gdata.get_data(calib_size, calib_rate))
    test_data = import_data("imu/test_data.txt")
    g = 9.81

    coeffs = import_data("imu/calib_coeffs_accel.txt")

    plt.style.use('ggplot')
    fig,axs = plt.subplots(2,1,figsize=(12,9))
    for i in range(0,3):
        axs[0].plot(test_data[:,i]/g, label='${}$, Uncalibrated'.format(accel_labels[i]))
        axs[1].plot(accel_fit(test_data[:,i],*coeffs[i]), label='${}$, Calibrated'.format(accel_labels[i]))
    axs[0].legend(fontsize=14);axs[1].legend(fontsize=14)
    axs[0].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
    axs[1].set_ylabel('$a_{x,y,z}$ [g]',fontsize=18)
    axs[1].set_xlabel('Sample',fontsize=18)
    axs[0].set_ylim([-2,2])
    axs[1].set_ylim([-2,2])
    axs[0].set_title('Accelerometer Calibration Calibration Correction',fontsize=18)
    fig.savefig('imu/accel_calibration_output.png',dpi=300,
                    bbox_inches='tight',facecolor='#FCFCFC')
    fig.show()
