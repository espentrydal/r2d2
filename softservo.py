#
# software servo control
#
# these functions block until complete
import RPi.GPIO as gpio
from time import sleep
from r2d2_defines import map_range

class Soft_servo:
    def __init__(self, pin):
        self.freq = 50                   # Frequency in Hz (50Hz = 20 ms)
        self.servo_pin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)
        self.servo = gpio.PWM(self.servo_pin, self.freq)
        self.servo.start(6.2)  # dutycycle (6.2% = width 1240 microseconds = 90 deg)
        self.servo.ChangeDutyCycle(6.2)
        self.servo_delay = 500
        sleep(self.servo_delay*1e-3)
        
    def soft_servo_write(self, angle):
        "Writes given angle to servo for given delay in milliseconds."
        pulsewidth = map_range(angle, 0, 180, 380, 2100) # width in microseconds

        self.servo.ChangeDutyCycle(pulsewidth*1e-6*self.freq*100)
        sleep(self.servo_delay*1e-3)
            

# End of file
