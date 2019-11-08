#
# Main robot logic
#
#from adafruit_motorkit import MotorKit
#from time import sleep
import move
import look

move_set_speed(MIN_SPEED + 10)
print("Ready")

while True:
    move_forward()
    roam()
    
    # Test code
    #
    # print("rotate cw, throttle 50%")
    # kit.motor1.throttle = 0.5
    # kit.motor2.throttle = -0.5
    # sleep(5)
    # print("rotate ccw, throttle 50%")
    # kit.motor1.throttle = -0.5
    # kit.motor2.throttle = 0.5
    # sleep(5)
    # print("stop")
    # kit.motor1.throttle = 0
    # kit.motor2.throttle = 0
    # sleep(5)
