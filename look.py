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
        self.servo_delay = 500  # time in ms for servo to move

        self.MIN_DISTANCE = 8 # robot stops when object is nearer (in inches)
        self.CLEAR_DISTANCE = 50 # distance in cm considered attractive to move
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
        self.s.soft_servo_write(angle, self.servo_delay) # wait for servo to get into position
        distance = samples = cumulative = 0
        print("Pinging: ", end='')
        for i in range(0,4):
            print(i, end=': ')
            distance = ping_get_distance(self.ping_pin)
            print(distance)
            if distance > 0:
                samples += 1
                cumulative += distance

        print("# samples: ", samples, "cumul: ", cumulative)

        if samples > 0:
            distance = cumulative / samples
        else:
            distance = 0

        print("look_at: distance: ", distance)

        if angle != self.servo_angles[DIR_CENTER]:
            print("looking at dir ", angle, " distance= ", distance, " cm")
            self.s.soft_servo_write(self.servo_angles[DIR_CENTER],
                                    self.servo_delay/2)

        return distance

    # def check_movement(self):
    #     """Function to check if robot can continue moving in current direction.
    #     Returns true if robot is not blocked moving in current direction.
    #     This version only tests for obstacles in front."""
    #     is_clear = True             # default return value if no obstacles
    #     # !!! IR_SENSORS DISABLED
    #     if m.move_state == MOV_FORWARD:
    #          if self.look_for_obstacle(OBST_FRONT) == True:
    #              is_clear = False
    #     return is_clear

    # def roam(self):
    #     "Look for and avoid obstacles using servo to scan."
    #     m = Move()
    #     print("Roaming: ")
    #     distance = self.look_at(self.servo_angles[DIR_CENTER])
    #     print("roam: distance: ", distance)
    #     if distance == 0:
    #         m.move_stop()
    #         print("No front sensor")
    #         return                  # no sensor
    #     elif distance <= self.MIN_DISTANCE:
    #         m.move_stop()
    #         print("Scanning:")
    #         left_distance = self.look_at(self.servo_angles[DIR_LEFT])
    #         if left_distance > self.CLEAR_DISTANCE:
    #             print(" moving left: ")
    #             m.move_rotate(-90)
    #         else:
    #             sleep(0.5)
    #             right_distance = self.look_at(self.servo_angles[DIR_RIGHT])
    #             if right_distance > self.CLEAR_DISTANCE:
    #                 # print(" moving right: ")
    #                 m.move_rotate(90)
    #             else:
    #                 # print(" no clearance : ")
    #                 distance = max(left_distance, right_distance)
    #                 if distance < self.CLEAR_DISTANCE/2:
    #                     m.timed_move(MOV_BACK, 1000) # back up for one second
    #                     m.move_rotate(-180)
    #                 else:
    #                     if left_distance > right_distance:
    #                         m.move_rotate(-90)
    #                     else:
    #                         m.move_rotate(90)
# End file
