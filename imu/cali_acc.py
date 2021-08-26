#!/usr/bin/python3

import time
import numpy as np
from numpy.core.fromnumeric import _mean_dispatcher
from numpy.lib.function_base import cov
from scipy.optimize.minpack import curve_fit
import matplotlib.pyplot as plt

t0 = time.time()
start_bool = False  # if accelerometer fails, stop calibration

while time.time() - t0 < 5:
    try:
        import board
        import busio
        import adafruit_adxl34x
        start_bool = True
        break
    except:
        continue

# read data from I2C connected to accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)


direction = ["x-", "y+", "z+"]


def accel_fit(x_input, m_x, b):
    return (x_input * m_x) + b


def get_data(size, rate):
    data = []
    while len(data) < size:
        try:
            time.sleep(1/rate)
            ax, ay, az = acc.acceleration
            data.append([ax, ay, az])
        except:
            continue
    return data


def cal_cov(data):
    data_arr = np.array(data)
    mean = np.mean(data_arr, axis=0)
    var = np.var(data_arr, axis=0)
    cov = np.zeros((3, 3))
    cov[0, 0] = var[0]
    cov[1, 1] = var[1]
    cov[2, 2] = var[2]
    return cov


def output(filename, term, measure):
    sdata = measure
    f = open(filename, "a")
    np.savetxt(f, sdata, fmt='%.5e')
    f.write("\n")
    f.close()


def measure_acc(m_axis):
    print("put imu along " + m_axis + " axis")
    input("Press Enter to continue..")
    data = get_data(calib_size, calib_rate)
    cov = cal_cov(data)
    # print(measure)
    return cov


def calib_acc():
    acc_coeffs = [[], [], []]
    calib_axes = ["x", "y", "z"]
    direction = [["downwards", "horizontally"], ["upwards", "horizontally"], ["upwards", "horizontally"]]  # calibration direction for x,y,z axes due to direction limitation
    denote_direc = [[-1.0, 0.0], [1.0, 0.0], [1.0, 0.0]]
    for axis_index, axis in enumerate(calib_axes):
        measure_axis = [[], []]
        for direc_index, direc in enumerate(direction[axis_index]):
            input("Please press Enter after put and hold the accelerometer steady along " + axis + "-axis " + direc)
            measure_arr = get_data(calib_size, calib_rate)
            measure_axis[direc_index] = np.array(measure_arr)[:, axis_index]

        popts, _ = curve_fit(accel_fit,
                             np.append(measure_axis[0], measure_axis[1]),
                             np.append(denote_direc[axis_index][0]*np.ones(np.shape(
                                 measure_axis[0])), denote_direc[axis_index][1]*np.zeros(np.shape(measure_axis[1]))),
                             maxfev=10000
                             )
        acc_coeffs[axis_index] = popts
    print("Accelerometer calibration completed.")
    return acc_coeffs


if __name__ == '__main__':
    if not start_bool:
        print("No, accelerometer detected, please check thee I2C and wirings")
    else:
        calib_size = 1000
        calib_rate = 100
        # do measurements and cal covariance matrix
        cov = np.zeros((3,3))
        for i, axis_direc in enumerate(["x-", "y", "z"]):
            cov = cov + measure_acc(axis_direc)
        cov = cov / 3.0
        print("covariance matrix:")
        print(cov)
        filename = "cov_accel.txt"
        output(filename, "cov", cov)

        accel_labels = ['a_x', 'a_y', 'a_z']  # labels for plots
        coeffs = calib_acc()
        print(coeffs)
        print(type(coeffs))
        filename = "calib_coeffs_accel.txt"
        output(filename, "coeff", np.array(coeffs))

        
