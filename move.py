#
# Movement functions
#
from adafruit_motorkit import MotorKit
from time import sleep, monotonic
from r2d2_defines import *
from look import Look

class Move:
    def __init__(self):
        # Low-level definitions
        self.differential = 0
        self.MIN_SPEED = 40
        self.SPEED_TABLE_INTERVAL = 10
        self.NBR_SPEEDS = int(1 + (100 - self.MIN_SPEED)/self.SPEED_TABLE_INTERVAL)

        self.speed_table = [40, 50, 60, 70, 80, 90, 100] # speeds
        self.rotation_time = [2450, 1740, 1420, 1224, 1120, 1020, 920] # time

        # left and right motor speeds stored here (0-100%), to be used instead
        # of move_speed if differential speed needs to be taken into account.
        self.motor_speed = [0, 0]

        # Mid-level definitions
        self.kit = MotorKit()
        self.move_state = MOV_STOP # what robot is doing

        self.move_speed = 0       # move speed stored here (0-100%)
        self.speed_increment = 10 # percent to increase or decrease speed
        self.l = Look()

    def move_begin(self):
        self.move_stop()

    def move_left(self):
        self.change_move_state(MOV_LEFT)
        self.kit.motor3.throttle = 0
        self.kit.motor4.throttle = self.move_speed/100

    def move_right(self):
        self.change_move_state(MOV_RIGHT)
        self.kit.motor3.throttle = self.move_speed/100
        self.kit.motor4.throttle = 0

    def move_forward(self):
        self.change_move_state(MOV_FORWARD)
        self.kit.motor3.throttle = self.move_speed/100
        self.kit.motor4.throttle = self.move_speed/100

    def move_backward(self):
        self.change_move_state(MOV_BACK)
        self.kit.motor3.throttle = -self.move_speed/100
        self.kit.motor4.throttle = -self.move_speed/100

    def move_rotate(self, angle):
        self.change_move_state(MOV_ROTATE)
        print("Rotating ", angle)
        if angle < 0:
            print(" (left)")
            self.kit.motor3.throttle = -self.move_speed/100
            self.kit.motor4.throttle = self.move_speed/100
            angle = - angle
        elif angle > 0:
            print(" (right)")
            self.kit.motor3.throttle = self.move_speed/100
            self.kit.motor4.throttle = -self.move_speed/100
        ms = self.rotation_angle_to_time(angle, self.move_speed)
        self.moving_delay(ms)
        self.move_brake()

    def move_stop(self):
        self.change_move_state(MOV_STOP)
        self.kit.motor3.throttle = 0
        self.kit.motor4.throttle = 0

    def move_brake(self):
        self.move_stop()

    def move_set_speed(self, speed):
        """move_speed sets both motors to same speed. motor_speed[motor] (set
        by calling motor_set_speed) takes in to account the differential
        constant set above in definitions for motors that responds
        unequally to the MotorKit throttle function.

        """
        # self.motor_set_speed(MOTOR_LEFT, speed)
        # self.motor_set_speed(MOTOR_RIGHT, speed)
        self.move_speed = speed
        print("move_speed is now:", self.move_speed)

    def move_slower(self, decrement):
        print(" Slower: ", end='')
        if self.move_speed >= self.speed_increment + self.MIN_SPEED:
            self.move_speed -= self.speed_increment
        else:
            self.move_speed = self.MIN_SPEED

    def move_faster(self, increment):
        print(" Faster: ")
        self.move_speed += self.speed_increment
        if move_speed > 100:
            move_speed = 100
            self.move_set_speed(move_speed)

    def move_get_state(self):
        return self.move_state

    #
    # Functions to rotate the robot
    #

    def rotation_angle_to_time(self, angle, speed):
        """return the time in milliseconds to turn the given angle at the
        given speed"""
        full_rotation_time = 0

        if speed < self.MIN_SPEED:
            return 0

        angle = abs(angle)

        if speed >= 100:
            full_rotation_time = self.rotation_time[self.NBR_SPEEDS-1]
        else:
            i = int((speed - self.MIN_SPEED) / self.SPEED_TABLE_INTERVAL)
            t0 = self.rotation_time[i]
            t1 = self.rotation_time[i+1]
            full_rotation_time = map_range(speed, self.speed_table[i],
                                           self.speed_table[i+1], t0, t1)
        result = map_range(angle, 0, 360, 0, full_rotation_time)
        return result

    def calibrate_rotation_rate(self, direction, angle):
        """rotate the robot from MIN_SPEED to 100% increasing by
        SPEED_TABLE_INTERVAL"""
        print(location_string[direction], " calibration")

        for speed in range(self.MIN_SPEED, 100, self.SPEED_TABLE_INTERVAL):
            sleep(1)
            if direction == DIR_LEFT: # rotate left
                self.kit.motor3.throttle = -speed/100
                self.kit.motor4.throttle = speed/100

            elif direction == DIR_RIGHT: # rotate right
                self.kit.motor3.throttle = speed/100
                self.kit.motor4.throttle = -speed/100

            else:
                print("Invalid direction")

            time = self.rotation_angle_to_time(angle, speed)

            print(location_string[direction], ": rotate", angle, " degrees at speed ",
                  speed, " for ", time, " ms")
            sleep(time*1e-3)
            self.kit.motor3.throttle = 0
            self.kit.motor4.throttle = 0
            sleep(2)                # two second delay between speeds

    def change_move_state(self, new_state):
        """low level movement state. it will differ from the command state
         when the robot is avoiding obstacles"""

        if new_state != self.move_state:
            print("Changing move state from ", states[self.move_state],
                  " to ", states[new_state])
            self.move_state = new_state
            print("move_state is now", self.move_state)

    #
    # high level movement functions
    #

    def timed_move(self, direction, duration):
        """moves in the given direction at the curent speed for the given
        duration in milliseconds"""
        print("Timed move ", end='')
        if direction == MOV_FORWARD:
            print("forward")
        elif direction == MOV_BACK:
            print("back")
        else:
            print("?")
        print("Duration:", duration)

        self.moving_delay(duration)
        self.move_stop()

    def moving_delay(self, duration):
        """check for obstacles while delaying the given duration in ms"""
        start_time = monotonic()
        while (monotonic() - start_time)*1e3 < duration:
            if self.check_movement() == False:
                if self.move_state != MOV_ROTATE: # rotate is only valid movement
                    print("Stopping in moving_delay()")
                    self.move_brake()

    def check_movement(self):
        """Function to check if robot can continue moving in current direction.
        Returns true if robot is not blocked moving in current direction.
        This version only tests for obstacles in front."""
        is_clear = True             # default return value if no obstacles
        # !!! IR_SENSORS DISABLED
        if self.move_state == MOV_FORWARD:
             if self.l.look_for_obstacle(OBST_FRONT) == True:
                 is_clear = False
        return is_clear

    def roam(self):
        "Look for and avoid obstacles using servo to scan."
        print("Roaming: ")
        distance = self.l.look_at(self.l.servo_angles[DIR_CENTER])
        print("roam: distance: ", distance)
        if distance == 0:
            self.move_stop()
            print("No front sensor")
            return                  # no sensor
        elif distance <= self.l.MIN_DISTANCE:
            self.move_stop()
            print("Scanning:")
            left_distance = self.l.look_at(self.l.servo_angles[DIR_LEFT])
            if left_distance > self.l.CLEAR_DISTANCE:
                print(" moving left: ")
                self.move_rotate(-90)
            else:
                sleep(0.5)
                right_distance = self.l.look_at(self.l.servo_angles[DIR_RIGHT])
                if right_distance > self.l.CLEAR_DISTANCE:
                    # print(" moving right: ")
                    self.move_rotate(90)
                else:
                    # print(" no clearance : ")
                    distance = max(left_distance, right_distance)
                    if distance < self.l.CLEAR_DISTANCE/2:
                        self.timed_move(MOV_BACK, 1000) # back up for one second
                        self.move_rotate(-180)
                    else:
                        if left_distance > right_distance:
                            self.move_rotate(-90)
                        else:
                            self.move_rotate(90)
