import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',
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
    usr = raw_input('Enter anything: ')
    cmd = usr + '\r\n'
    if usr == 'Q':
        loop = False
    else:
        byte=ser.inWaiting()
        fw=ser.read(byte)
        print 'The received data is: ' + fw

ser.close()
