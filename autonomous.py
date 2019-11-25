#
# Main robot logic
#
#from adafruit_motorkit import MotorKit
#from time import sleep
from move import Move
from RPi.GPIO import cleanup
import traceback
from bluedot import BlueDot
from signal import pause

class R2D2:
    button_pressed = 0
    
    @classmethod
    def toggle_press(cls, value):
        cls.button_pressed = value

    def __init__(self):
        self.m = Move()
        self.bd = BlueDot()

        self.m.move_set_speed(self.m.MIN_SPEED)

    def start(self):
        try:
            self.m.move_forward()
            print("move_speed:", self.m.move_speed)
            self.m.roam()

        except KeyboardInterrupt:   # Reset by pressing CTRL + C
            print("Error:", traceback.format_exc())
            print("Stopping motors...:")
            self.m.move_stop()
            cleanup()

        except Exception:
            print("Error:", traceback.format_exc())
            print("Stopping motors...:")
            self.m.move_stop()
            cleanup()

    def stop(self):
        print("Bluedot stopping motors...:")
        self.m.move_stop()
        cleanup()

if __name__ == '__main__':
    r = R2D2()
    print("Ready!")
    
    r.bd.when_pressed = r.start
    r.bd.when_moved = r.start
    r.bd.when_released = r.stop
    pause()

# End of file
