#
# code to look for obstacles
#

# servo defines
sweep_servo_pin = 9             # pin connected to servo
servo_delay = 500               # time in ms for servo to move

MIN_DISTANCE = 8                # robot stops when object is nearer (in inches)
CLEAR_DISTANCE = 24             # distance in inches considered attractive to move
MAX_DISTANCE = 150              # the maximum range of the distance sensor

# servo angles: left, right, center
servo_angles = [150, 30, 90]

ping_pin = 10                   # digital pin 10

def look_begin():
    ir_sensor_begin()           # initializes sensors
    soft_servo_attach(sweep_servo_pin) # attaches the servo pin to the servo object

# returns true if the given obstacle is detected
def look_for_obstacle(obstacle):
    return {
        OBST_FRONT_EDGE : ir_edge_detect(DIR_LEFT) && ir_edge_detect(DIR_RIGHT)
        OBST_LEFT_EDGE  : ir_edge_detect(DIR_LEFT)
        OBST_RIGHT_EDGE : ir_edge_detect(DIR_RIGHT)
        OBST_FRONT      : look_at(servo_angles[DIR_CENTER]) <= MIN_DISTANCE
        }.get(obstacle, false)  # return false if obstacle not found

# returns the distance of objects at the given anle
def look_at(angle):
    soft_servo_write(angle, servo_delay) # wait for servo to get into position

    distance = samples = cume = 0
    for i in range(0,4):
        distance = ping_get_distance(ping_pin)
        if distance > 0:
            samples++
            cume += distance

    if samples > 0:
        distance = cume / samples
    else:
        distance = 0

    if angle != servo_angles[DIR_CENTER]:
        print("looking at dir ", angle, " distance= ", distance)
        soft_servo_write(servo_angles[DIR_CENTER], servo_delay/2)

    return distance

# function to check if robot can continue moving in current direction
# returns true if robot is not blocket moving in current direction
# this version only tests for obstacles in front
def check_movement():
    is_clear = True             # default return value if no obstacles
    if move_get_state() == MOV_FORWARD:
        if look_for_obstacle(OBST_FRONT) == True:
            is_clear = False
    return is_clear

