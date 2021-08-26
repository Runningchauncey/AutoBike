#!/usr/bin/python3

import time
import numpy as np

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



def get_data(size, rate):
    # read data from I2C connected to accelerometer
    i2c = busio.I2C(board.SCL, board.SDA)
    acc = adafruit_adxl34x.ADXL345(i2c)
    data = []
    while len(data) < size:
        try:
            time.sleep(1/rate)
            ax, ay, az = acc.acceleration
            data.append([ax, ay, az])
        except:
            continue
    return data

def save_data(filename, data):
    f = open(filename, "w")
    np.savetxt(f, data, fmt='%.5e')
    f.write("\n")
    f.close()

if __name__ == "__main__":
    calib_size = 10000
    calib_rate = 100
    save_data("imu/test_data.txt",np.array(get_data(calib_size, calib_rate)))