from adafruit_motorkit import MotorKit
from time import sleep, monotonic

kit = MotorKit()

speed = .4
kit.motor1.throttle = speed
kit.motor2.throttle = -speed
sleep(2.45)
kit.motor1.throttle = 0
kit.motor2.throttle = 0

