#
# code to look for obstacles
#
from r2d2_defines import *
#from ir_sensors import *
from softservo import Soft_servo
from distance import *

class Look:
    def __init__(self):
        # servo defines
        sweep_servo_pin = 17    # pin connected to servo (BCM #)

        self.MIN_DISTANCE = 30 # robot stops when object is nearer (in cm)
        self.CLEAR_DISTANCE = 70 # distance in cm considered attractive to move
        self.MAX_DISTANCE = 300 # the maximum range in cm of the distance sensor

        # servo angles: left, right, center
        self.servo_angles = [150, 30, 90]

        self.ping_pin = 27 # ping connected to ping signal pin (BCM #)

        self.s = Soft_servo(sweep_servo_pin) # attaches the servo pin to the servo object

    # !!! IR SENSORS DISABLED
    #def look_begin():
    #    ir_sensor_begin()           # initializes sensors !!! IR SENSORS DISABLED
    def look_for_obstacle(self, obstacle):
    #     "returns true if the given obstacle is detected"
    #     if obstacle == OBST_FRONT_EDGE:
    #         return ir_edge_detect(DIR_LEFT) and ir_edge_detect(DIR_RIGHT)
    #     elif obstacle == OBST_LEFT_EDGE:
    #         return ir_edge_detect(DIR_LEFT)
    #     elif obstacle == OBST_RIGHT_EDGE:
    #         return ir_edge_detect(DIR_RIGHT)
        if obstacle == OBST_FRONT:
            return look_at(self.servo_angles[DIR_CENTER]) <= self.MIN_DISTANCE
        else:
            return False


    def look_at(self, angle):
        "returns the distance in cm of objects at the given angle"
        print("Looking at:", angle, ": ")
        self.s.soft_servo_write(angle) # wait for servo to get into position
        distance = samples = cumulative = 0
        print("Pinging: ", end='')
        for i in range(0,4):
#            print(i, end=': ')
            distance = ping_get_distance(self.ping_pin)
#            print(distance)
            if distance > 0:
                samples += 1
                cumulative += distance

#        print("# samples: ", samples, "cumul: ", cumulative)

        if samples > 0:
            distance = cumulative / samples
        else:
            distance = 0

        print("look_at: distance: ", distance)

        if angle != self.servo_angles[DIR_CENTER]:
            print("looking at dir ", angle, " distance= ", distance, " cm")
            self.s.soft_servo_write(self.servo_angles[DIR_CENTER])
        return distance

# End file
