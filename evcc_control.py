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
# Schleifen-Variable auf TRUE setzen
loop = True
# Check the status of the EVCC
write=ser.write('!0 02\r\n')
time.sleep(0.2)
byte=ser.inWaiting()
status=ser.read(byte)[6:10]
print 'The status is: ' + status

while loop:
# Eingabeaufforderung was als naechstes gemacht werden soll
    next = raw_input('What do you want to do? \n [F]-check firmware\n [Q]-quit program\n \
    [C]-start charging\n [S]-stop charging\n [M]-set max charge current\n')

# IF-Bedingung
    if next == 'Q':
        loop = False
    elif next == 'F':
        write=ser.write('!0 01\r\n')
        time.sleep(0.2)
        byte=ser.inWaiting()
        fw=ser.read(byte)[6:]
        print 'The Firmware Version is: ' + fw
# seconds = int(raw_input('Enter amount of seconds: '))

#for i in range(0, seconds):
#    write=ser.write('!0 02\r\n')
#    time.sleep(1)
#    byte=ser.inWaiting()
#    status=ser.read(byte)[6:10]
#    if status == '0000':        # A: No EV connected
#        time.sleep(1)
#        print status
#    elif status == '0005':      # C: EV is charging
#        write=ser.write('!0 27\r\n')
#        time.sleep(1)
#        write=ser.write('!0 25\r\n')
#        time.sleep(1)
#        byte=ser.inWaiting()
#        ans=ser.read(byte)
#        print status
#    elif status == '0003':      # B-: Charging stopped by EVSE
#        write=ser.write('!0 28\r\n')
#        time.sleep(1)
#        byte=ser.inWaiting()
#        ans=ser.read(byte)
#        print status
#    else:
#        time.sleep(1)
#        print status

ser.close()