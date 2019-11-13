#
# software servo control
#
# these functions block until complete
import RPi.GPIO as gpio
from time import sleep
from r2d2_defines import map_range

class Soft_servo:
    servo_pin = 0
    freq = 50                   # Frequency in Hz (50Hz = 20 ms)
#    servo = gpio.PWM(servo_pin, 0)

    def soft_servo_attach(self, pin):
        self.servo_pin = pin
        gpio.setmode(gpio.BCM)
        gpio.setup(pin, gpio.OUT)
        
        self.servo = gpio.PWM(pin, self.freq)
        self.servo.start(6.2)   # dutycycle (6.2% = width 1240 microseconds)

    def soft_servo_write(self, angle, servo_delay):
        "Writes given angle to servo for given delay in milliseconds."
        pulsewidth = map_range(angle, 0, 180, 380, 2100) # width in microseconds
    
        while True:
            self.servo.ChangeDutyCycle(pulsewidth*self.freq*100)
            servo_delay -= 20
            if servo_delay < 0:
                break

# End of file