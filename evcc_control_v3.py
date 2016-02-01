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
# Lookup table: Mode-3-Status
mode3 = { '0000' : 'A',
          '0004' : 'B2',
          '0005' : 'C',
          '0006' : 'D',
          '0009' : 'B\'',
          '0013' : 'B1',
          '0003' : 'B1',
          '0017' : 'A\'',
          '0033' : 'Error CS',
          '0035' : 'Error EV',
          '0037' : 'Error locker',
          '0039' : 'Error ventilation',
          '0255' : 'MANUAL'
          }
# Lookup table: Set PWM for Max charge current
pwm   = { '6'  : '0000',
          '10' : '0001',
          '13' : '0002',
          '16' : '0003'
          }
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
read_status()
print 'The status is: ' + mode3[status]
# Main loop
while loop:
# User request for the next action
    next = raw_input('What do you want to do? \n [F]-check firmware\n [Q]-quit program\n \
[C]-start charging\n [S]-stop charging\n [M]-set max charge current\n [R]-read status\n')
# IF condition
    # Stop programm
    if next == 'Q':
        loop = False
    # Read Status
    elif next == 'R':
        read_status()
        print 'The status is: ' + status
    # Check firmware version
    elif next == 'F':
        write=ser.write('!0 01\r\n')
        time.sleep(0.2)
        byte=ser.inWaiting()
        fw=ser.read(byte)[6:]
        print 'The Firmware Version is: ' + fw
    # Start Charging
    elif next == 'C':
        read_status()
        if status == '0005':
            print 'EV is already charging (C)\n'
        elif status == '0000':
            print 'No EV connected (A)\n'
        elif status == '0009':
            print 'EV stopped charging (B\')\n'
        elif status == '0004':
            print 'EV not ready to charge (B2)\n'
        elif status == '0013' or '0003':
            # Clear bBreakCharge
            write=ser.write('!0 28\r\n')
            time.sleep(0.2)
            #byte=ser.inWaiting()
            #print ser.read(byte)[6:]
            read_status()
            print 'The new status is: C ' + status
        else:
            read_status()
            print 'The status is unknown. The status is: ' + status
    # Stop Charging
    elif next == 'S':
        read_status()
        if status == '0013':
            print 'EV is already stopped (B1)\n'
        elif status == '0000':
            print 'No EV connected (A)\n'
        elif status == '0009':
            print 'EV stopped charging (B\')\n'
        elif status == '0004':
            print 'EV not ready to charge (B2)\n'
        elif status == '0005':
            # Set bBreakCharge
            write=ser.write('!0 27\r\n')
            time.sleep(0.2)
            #byte=ser.inWaiting()
            # Stop charging
            write=ser.write('!0 25\r\n')
            time.sleep(0.2)
            #byte=ser.inWaiting()
            read_status()
            print 'The new status is: {0} (B1)\n'.format(status)
        else:
            read_status()
            print 'The status is unknown. The status is: ' + status
    # Set max charge current
    elif next == 'M':
            current = raw_input('Enter current value [6;10;13;16]:')
            x='!0 12 {0}\r\n'.format(pwm[current])
            write=ser.write(x)
            #write1=ser.write('!0 12 0000\r\n')
            time.sleep(0.2)
            byte=ser.inWaiting()
            ans = ser.read(byte)            
            write2=ser.write('!0 11\r\n')
            time.sleep(0.2)
            byte=ser.inWaiting()
            ans = ser.read(byte)[6:10]
            #print write1
            #print write2
            print ans
            #print x
    else:
        pass


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
