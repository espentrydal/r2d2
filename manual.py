from move import Move
from RPi.GPIO import cleanup
import traceback
from serial import Serial
from time import sleep
import io

def main():
    "Main robot logic for manual control
    "
    # Setting up serial over bluetooth
    ser = Serial('/dev/rfcomm0', timeout=1)
    ser.reset_input_buffer()
    # Setting up io stream to read unicode string
    sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser))
    sio.flush()

    m = Move()
    m.move_set_speed(m.MIN_SPEED)
    print("Ready!")
    
    try:
        while True:
            ser.reset_input_buffer()
            sio.flush()
            input = sio.readline().strip()
            if input:           # if not a blank line
                input = input.split(',')
                joy_x = input[0]
                joy_y = input[1]
                joy_x = int(joy_x)
                joy_y = int(joy_y)
                print("x: ", joy_x)
                print("y: ", joy_y)

                # Joystick left
                if joy_x < 50:
                    m.move_rotate(-90)
                    sleep(1)
                # Joystick right
                if joy_x > 200:
                    m.move_rotate(90)
                    sleep(1)
                # Joystick not forward
                if joy_y < 200:
                    # Joystick backward
                    if joy_y < 50:
                        m.move_backward()
                        sleep(1)
                    # Joystick neutral
                    else:
                        m.move_stop()
                        sleep(1)
                # Joystick forward
                if joy_y > 200:
                    m.move_forward()
                    sleep(1)
                    
                ser.reset_input_buffer()
                ser.reset_output_buffer()

            else:
                ser.reset_input_buffer()
                ser.reset_output_buffer()

    except KeyboardInterrupt:   # Reset by pressing CTRL + C
        print("Error:", traceback.format_exc())
        print("Stopping motors...:")
        m.move_stop()
        cleanup()
        sio.flush()
        ser.close()


    except Exception:
        print("Error:", traceback.format_exc())
        print("Stopping motors...:")
        m.move_stop()
        cleanup()
        sio.flush()
        ser.close()

if __name__ == '__main__':
    main()
