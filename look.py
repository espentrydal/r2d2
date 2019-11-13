#
# code to look for obstacles
#
from r2d2_defines import *
#from ir_sensors import *
from softservo import *
from distance import *

# servo defines
sweep_servo_pin = 17            # pin connected to servo (BCM #)
servo_delay = 500               # time in ms for servo to move

MIN_DISTANCE = 8                # robot stops when object is nearer (in inches)
CLEAR_DISTANCE = 50             # distance in cm considered attractive to move
MAX_DISTANCE = 300              # the maximum range in cm of the distance sensor

# servo angles: left, right, center
servo_angles = [150, 30, 90]

ping_pin = 27                   # ping connected to ping signal pin (BCM #)

s = Soft_servo(sweep_servo_pin) # attaches the servo pin to the servo object

# !!! IR SENSORS DISABLED
#def look_begin():
#    ir_sensor_begin()           # initializes sensors !!! IR SENSORS DISABLED
# def look_for_obstacle(obstacle):
#     "returns true if the given obstacle is detected"
#     if obstacle == OBST_FRONT_EDGE:
#         return ir_edge_detect(DIR_LEFT) and ir_edge_detect(DIR_RIGHT)
#     elif obstacle == OBST_LEFT_EDGE:
#         return ir_edge_detect(DIR_LEFT)
#     elif obstacle == OBST_RIGHT_EDGE:
#         return ir_edge_detect(DIR_RIGHT)
#     elif obstacle == OBST_FRONT:
#         return look_at(servo_angles[DIR_CENTER]) <= MIN_DISTANCE
#     else:
#         return False

def look_at(angle):
    "returns the distance in cm of objects at the given angle"
    s.soft_servo_write(angle, servo_delay) # wait for servo to get into position
    distance = samples = cumulative = 0
    for i in range(0,4):
        distance = ping_get_distance(ping_pin)
        if distance > 0:
            samples += 1
            cumulative += distance

    if samples > 0:
        distance = cumulative / samples
    else:
        distance = 0

    if angle != servo_angles[DIR_CENTER]:
        print("looking at dir ", angle, " distance= ", distance, " cm")
        s.soft_servo_write(servo_angles[DIR_CENTER], servo_delay/2)

    return distance

def check_movement():
    """Function to check if robot can continue moving in current direction.
    Returns true if robot is not blocked moving in current direction.
    This version only tests for obstacles in front."""
    is_clear = True             # default return value if no obstacles
    # !!! IR_SENSORS DISABLED
    # if move_get_state() == MOV_FORWARD:
    #     if look_for_obstacle(OBST_FRONT) == True:
    #         is_clear = False
    return is_clear

def roam():
    "Look for and avoid obstacles using servo to scan."
    distance = look_at(servo_angles[DIR_CENTER])
    if distance == 0:
        move_stop()
        print("No front sensor")
        return                  # no sensor
    elif distance <= MIN_DISTANCE:
        move_stop()
        # print("Scanning:")
        left_distance = look_at(servo_angles[DIR_LEFT])
        if left_distance > CLEAR_DISTANCE:
            # print(" moving left: ")
            move_rotate(-90)
        else:
            sleep(0.5)
            right_distance = look_at(servo_angles[DIR_RIGHT])
            if right_distance > CLEAR_DISTANCE:
                # print(" moving right: ")
                move_rotate(90)
            else:
                # print(" no clearance : ")
                distance = max(left_distance, right_distance)
                if distance < CLEAR_DISTANCE/2:
                    timed_move(MOV_BACK, 1000) # back up for one second
                    move_rotate(-180)
                else:
                    if left_distance > right_distance:
                        move_rotate(-90)
                    else:
                        move_rotate(90)

# End file
