import board
import time
import busio
import adafruit_adxl34x

i2c = busio.I2C(board.SCL, board.SDA)
accelerator = adafruit_adxl34x.ADXL345(i2c)

while True:
	print("ax=%f, ay=%f, az=%f"%accelerator.acceleration)
	time.sleep(1)
