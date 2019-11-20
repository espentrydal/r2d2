#
# Main robot logic
#
#from adafruit_motorkit import MotorKit
#from time import sleep
from move import Move
from RPi.GPIO import cleanup
import traceback

if __name__ == 'r2d2':
    m = Move()
    m.move_set_speed(m.MIN_SPEED)
    print("Ready!")

if __name__ == '__main__':
    m = Move()
    m.move_set_speed(m.MIN_SPEED)
    print("Ready!")

    try:
        while True:
            m.move_forward()
            print("move_speed:", m.move_speed)
            m.roam()

    except KeyboardInterrupt:   # Reset by pressing CTRL + C
        print("Error:", traceback.format_exc())
        print("Stopping motors...:")
        m.move_stop()
        cleanup()

    except Exception:
        print("Error:", traceback.format_exc())
        print("Stopping motors...:")
        m.move_stop()
        cleanup()
        
# End of file
