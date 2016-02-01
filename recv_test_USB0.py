import serial
import time

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=38400,
    timeout=2,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)
# Set loop variable TRUE
loop = True
# Main loop
while loop:
    usr = raw_input('Enter command: ')
    cmd = usr + '\r\n'
    if usr == 'Q':
        loop = False
    else:
        byte=ser.inWaiting()
        fw=ser.read(byte)
        print 'The answer is: ' + fw

ser.close()
