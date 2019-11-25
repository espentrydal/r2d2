import smbus
import time
from serial import Serial
import io

bus = smbus.SMBus(1)
address = 0x52

bus.write_byte_data(address, 0x40, 0x00)
bus.write_byte_data(address, 0xF0, 0x55)
bus.write_byte_data(address, 0xFB, 0x00)

ser = Serial('/dev/rfcomm0', timeout=1)
ser.reset_output_buffer()
sio = io.TextIOWrapper(io.BufferedRWPair(ser, ser)) # to transmit unicode strings
sio.flush()

time.sleep(2)

try:
    while True:
        bus.write_byte(address, 0x00)
        time.sleep(1)
        data0 = bus.read_byte(address)
        data1 = bus.read_byte(address)
        data2 = bus.read_byte(address)
        data3 = bus.read_byte(address)
        data4 = bus.read_byte(address)
        data5 = bus.read_byte(address)
        data = [data0, data1, data2, data3, data4, data5]
        joy_x = data[0]
        joy_y = data[1]

        message = '\n' + str(data[0]) + "," + str(data[1]) + '\n'
        ser.reset_output_buffer()
        sio.write(message)
        print(message)
        sio.flush()
#        ser.reset_output_buffer()
 
except IOError as e:
    print(e)
    sio.flush()
    ser.reset_output_buffer
    ser.close()
