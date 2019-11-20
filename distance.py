#
# distance sensor code
#
import RPi.GPIO as gpio
from time import sleep, time

#
# code for ping distance sensor
#

def ping_get_distance(ping_pin):
    """Returns the distance in cm. Returns 0 if no ping sensor is connected."""
    #GPIO Mode (BOARD / BCM)
    gpio.setmode(gpio.BCM)
 
    ### SENDING
    gpio.setup(ping_pin, gpio.OUT)
    # set Trigger to HIGH
    gpio.output(ping_pin, True)
 
    # set Trigger after 0.01ms to LOW
    sleep(0.00001)
    gpio.output(ping_pin, False)
 
    ### RECEIVING 
    gpio.setup(ping_pin, gpio.IN)

    # save start time
    start_time = time()
    stop_time = time()
    while gpio.input(ping_pin) == 0:
        if time()-start_time > 20e-3:
            # if a pulse does not arrive within 20 ms the ping sensor is
            # not connected
            print("Ping sensor not connected")
            return 0
 
    # save time of arrival
    while gpio.input(ping_pin) == 1:
        stop_time = time()
 
    # time difference between start and arrival
    time_elapsed = stop_time - start_time
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (time_elapsed * 34300) / 2
 
    return distance # in cm

# End of file
    
    
