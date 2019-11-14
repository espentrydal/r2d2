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
        self.NBR_SPEEDS = 1 + (100 - self.MIN_SPEED)/self.SPEED_TABLE_INTERVAL

        self.speed_table = [40, 50, 60, 70, 80, 90, 100] # speeds
        self.rotation_time = [5500, 3300, 2400, 2000, 1750, 1550, 1150] # time

        # left and right motor speeds stored here (0-100%), to be used instead
        # of move_speed if differential speed needs to be taken into account.
        self.motor_speed = [0, 0]

        # Mid-level definitions
        self.kit = MotorKit()
        self.move_state = MOV_STOP           # what robot is doing

        self.move_speed = 0                  # move speed stored here (0-100%)
        self.speed_increment = 10            # percent to increase or decrease speed
    def move_begin(self):
        self.move_stop()

    def move_left(self):
        self.change_move_state(MOV_LEFT)
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = self.move_speed/100

    def move_right(self):
        self.change_move_state(MOV_RIGHT)
        self.kit.motor1.throttle = self.move_speed/100
        self.kit.motor2.throttle = 0

    def move_forward(self):
        self.change_move_state(MOV_FORWARD)
        self.kit.motor1.throttle = self.move_speed/100
        self.kit.motor2.throttle = self.move_speed/100

    def move_backward(self):
        self.change_move_state(MOV_BACK)
        self.kit.motor1.throttle = -self.move_speed/100
        self.kit.motor2.throttle = -self.move_speed/100

    def move_rotate(self, angle):
        self.change_move_state(MOV_ROTATE)
        print("Rotating ", angle)
        if angle < 0:
            print(" (left)")
            self.kit.motor1.throttle = -self.move_speed/100
            self.kit.motor2.throttle = self.move_speed/100
            angle = - angle
        elif angle > 0:
            print(" (right)")
            self.kit.motor1.throttle = self.move_speed/100
            self.kit.motor2.throttle = -self.move_speed/100
            ms = self.rotation_angle_to_time(angle, self.move_speed)
            self.moving_delay(ms)
            self.move_brake()

    def move_stop(self):
        self.change_move_state(MOV_STOP)
        self.kit.motor1.throttle = 0
        self.kit.motor2.throttle = 0

    def move_brake(self):
        self.move_stop()

    def move_set_speed(self, speed):
        """move_speed sets both motors to same speed. motor_speed[motor] (set
        by calling motor_set_speed) takes in to account the differential
        constant set above in definitions for motors that responds
        unequally to the MotorKit throttle function.

        """
        self.motor_set_speed(MOTOR_LEFT, speed)
        self.motor_set_speed(MOTOR_RIGHT, speed)
        self.move_speed = speed

    def motor_set_speed(self, motor, speed):
        if (motor == MOTOR_LEFT) and (speed > self.differential):
            speed -= self.differential
            self.motor_speed[motor] = speed    

    def move_slower(self, decrement):
        print(" Slower: ", end='')
        if self.move_speed >= self.speed_increment + self.MIN_SPEED:
            self.move_speed -= self.speed_increment
        else:
            self.move_speed = self.MIN_SPEED

    def move_faster(self, increment):
        print(" Faster: ")
        move_speed += speed_increment
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
            i = (speed - self.MIN_SPEED) / self.SPEED_TABLE_INTERVAL
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
                self.kit.motor1.throttle = -speed/100
                self.kit.motor2.throttle = speed/100

            elif direction == DIR_RIGHT: # rotate right
                self.kit.motor1.throttle = speed/100
                self.kit.motor2.throttle = -speed/100

            else:
                print("Invalid direction")

            time = self.rotation_angle_to_time(angle, speed)

            print(location_string[direction], ": rotate", angle, " degrees at speed ",
                  speed, " for ", time, " ms")
            sleep(time)
            self.kit.motor1.throttle = 0
            self.kit.motor2.throttle = 0
            sleep(2)                # two second delay between speeds

    def change_move_state(self, new_state):
        """low level movement state. it will differ from the command state
         when the robot is avoiding obstacles"""

        if new_state != self.move_state:
            print("Changing move state from ", states[self.move_state],
                  " to ", states[new_state])
            self.move_state = new_state

    #
    # high level movement functions
    #

    def timed_move(self, direction, duration):
        """# moves in the given direction at the curent speed for the given
        duration in milliseconds"""
        print("Timed move ", end='')
        if direction == MOV_FORWARD:
            print("forward")
        elif direction == MOV_BACK:
            print("back")
        else:
            print("?")

        self.moving_delay(duration)
        self.move_stop()

    def moving_delay(self, duration):
        """check for obstacles while delaying the given duration in ms"""
        l = Look()
        start_time = monotonic()*1e-3
        while monotonic()*0.001 - start_time < duration:
            # function in =look= module checks for obstacle in direction of movement
            if l.check_movement() == False:
                if self.move_state != MOV_ROTATE: # rotate is only valid movement
                    print("Stopping in moving_delay()")
                    self.move_brake()

    # End of move.py
