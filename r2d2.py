#
# Main robot logic
#
#from adafruit_motorkit import MotorKit
#from time import sleep
from move import Move
from look import Look
from RPi.GPIO import cleanup

m = Move()
m.move_set_speed(m.MIN_SPEED + 10)
l = Look()
print("Ready!")

if __name__ == '__main__':
    try:
        while True:
            m.move_forward()
            l.roam()

    except KeyboardInterrupt:   # Reset by pressing CTRL + C
        print("Stopping motors...:")
        m.move_stop()
        cleanup()
        
# End of file
