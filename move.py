#
# Movement functions
#
from adafruit_motorkit import MotorKit
import sleep from time

# Low-level definitions
MIN_SPEED = 40
SPEED_TABLE_INTERVAL = 10
NBR_SPEEDS = 1 + (100 - MIN_SPEED)/SPEED_TABLE_INTERVAL

speed_table = [40, 50, 60, 70, 80, 90, 100] # speeds
rotation_time = [5500, 3300, 2400, 2000, 1750, 1550, 1150] # time


# Mid-level definitions
kit = MotorKit()
move_state = MOV_STOP           # what robot is doing

move_speed = 0                  # move speed stored here (0-100%)
speed_increment = 10            # percent to increase or decrease speed

#def move_begin():
# Not necessary?

def move_left():
    change_move_state(MOV_LEFT)
    kit.motor1.throttle = 0
    kit.motor2.throttle = move_speed

def move_right():
    change_move_state(MOV_RIGHT)
    kit.motor1.throttle = move_speed
    kit.motor2.throttle = 0

def move_forward():
    change_move_state(MOV_FORWARD)
    kit.motor1.throttle = move_speed
    kit.motor2.throttle = move_speed

def move_backward():
    change_move_state(MOV_BACK)
    kit.motor1.throttle = -move_speed
    kit.motor2.throttle = -move_speed

def move_rotate():              # Needs more work
    change_move_state(MOV_ROTATE)
    print("Rotating ") # Add angle
    #if angle < 0
    #elif angle > 0

def move_stop():
    change_move_state(MOV_STOP)
    kit.motor1.throttle = 0
    kit.motor2.throttle = 0

# Add? Not finished.
def move_Brake():

def move_set_speed(speed):

def move_slower(decrement):

def move_faster(increment):

def move_get_state():
    return move_state

#
# Functions to rotate the robot
#

# return the time in milliseconds to turn the given angle at the given speed
def rotation_angle_to_time(angle, speed):
    full_rotation_time = 0

    if speed < MIN_SPEED:
        return 0

    angle = abs(angle)

    if speed >= 100:
        full_rotation_time = rotation_time[NBR_SPEEDS-1]
    else:
        i = (speed - MIN_SPEED) / SPEED_TABLE_INTERVAL
        t0 = rotation_time[i]
        t1 = rotation_time[i+1]
        full_rotation_time = map_range(speed, speed_table[i], speed_table[i+1], t0, t1)
        result = map_range(angle, 0, 360, 0, full_rotation_time)
        return result

def map_range(x, in_min, in_max, out_min, out_max):
    return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min

# rotate the robot from MIN_SPEED to 100% increasing by SPEED_TABLE_INTERVAL
def calibrate_rotation_rate(direction, angle):
    print(location_string[direction], " calibration")

    for speed in range(MIN_SPEED, 100, SPEED_TABLE_INTERVAL):
        sleep(1)
        if direction == DIR_LEFT: # rotate left
            kit.motor1.throttle = -speed
            kit.motor2.throttle = speed

        elif direction == DIR_RIGHT: # rotate right
            kit.motor1.throttle = speed
            kit.motor2.throttle = -speed

        else:
            print("Invalid direction")

        time = rotation_angle_to_time(angle, speed)

        print(location_string[direction], ": rotate", angle, " degrees at speed ",
              speed, " for ", time, " ms")
        sleep(time)
        kit.motor1.throttle = 0
        kit.motor2.throttle = 0
        sleep(2)                # two second delay between speeds

# low level movement state.
# it will differ from the command state when the robot is avoiding obstacles
def change_move_state(new_state):
    


