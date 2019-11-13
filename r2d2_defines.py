# Global defines

# Defines for directions
DIR_LEFT = 0
DIR_RIGHT = 1
DIR_CENTER =2

location_string = ["Left", "Right", "Center"]

# Obstacles constants
OBST_NONE = 0
OBST_LEFT_EDGE = 1
OBST_RIGHT_EDGE = 2
OBST_FRONT_EDGE = 3
OBST_FRONT = 4
OBST_REAR = 5

MOTOR_LEFT = 0; MOTOR_RIGHT = 1

MOV_LEFT = 0; MOV_RIGHT = 1; MOV_FORWARD = 2; MOV_BACK = 3;
MOV_ROTATE = 4; MOV_STOP = 5
states = ["Left", "Right", "Forward", "Back", "Rotate", "Stop"]

def map_range(x, in_min, in_max, out_min, out_max):
    "Corresponds to map() function on Arduino."
    return (x - in_min)*(out_max - out_min)/(in_max - in_min) + out_min


# End of global defines
