#!/usr/bin/python3

import numpy as np

import rospy
from sensor_msgs.msg import Imu

import time


import board
import busio
import adafruit_adxl34x


# read data from I2C connected to accelerometer
i2c = busio.I2C(board.SCL, board.SDA)
acc = adafruit_adxl34x.ADXL345(i2c)

calib = [[9.68749e-02,-2.43960e-02],
         [9.93610e-02,-2.42399e-02],
         [1.00340e-01,-6.17922e-02]]
lin_cov = [2.25344e-03,0.00000e+00,0.00000e+00,
0.00000e+00,2.31590e-03,0.00000e+00,
0.00000e+00,0.00000e+00,3.21196e-03]

def accel_fit(x_input, m_x, b):
    return (x_input * m_x) + b

def read_data():
    ax, ay, az = acc.acceleration
    ax = accel_fit(ax, calib[0][0], calib[0][1])
    ay = accel_fit(ay, calib[1][0], calib[1][1])
    az = accel_fit(az, calib[2][0], calib[2][1])
    return ax, ay, az

def arrange_msg(data):
    ax, ay, az = data
    imu_msg = Imu()
    #imu_msg.header.stamp = rospy.get_time()
    imu_msg.linear_acceleration.x = ax
    imu_msg.linear_acceleration.y = ay
    imu_msg.linear_acceleration.z = az
    imu_msg.linear_acceleration_covariance = lin_cov

    return imu_msg

def init_node():
    rospy.init_node('imu', anonymous=True)


def publisher():
    pub = rospy.Publisher("imu_raw", Imu)
    rate = rospy.Rate(10)
    while not rospy.is_shutdown():
        info_str = "Imu is working {}".format(rospy.get_time())
        rospy.loginfo(info_str)
        msg = arrange_msg(read_data())
        pub.publish(msg)
        rate.sleep()

if __name__ == '__main__':
    try:
        init_node()
        publisher()
    except rospy.ROSInterruptException:
        pass