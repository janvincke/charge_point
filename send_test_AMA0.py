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
# Definition of the ReadStatus function
def read_status():
    global status
    time.sleep(0.5)
    byte=ser.inWaiting()
    trash=ser.read(byte)
    ser.write('!0 02\r\n')
    time.sleep(0.5)
    byte=ser.inWaiting()
    status=ser.read(byte)[6:10]
# Check the status of the EVCC
#read_status()
#print 'The status is: ' + status
# Main loop
while loop:
# User request for the next action
    usr = raw_input('Enter message: ')
    cmd = usr + '\r\n'
    if usr == 'Q':
        loop = False
    else:
        write=ser.write(cmd)
        time.sleep(0.2)
        byte=ser.inWaiting()
        fw=ser.read(byte)
        print 'The sent data is: ' + cmd
        print 'The received data is: ' , fw

ser.close()
