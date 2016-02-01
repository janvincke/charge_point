import serial
import time

ser = serial.Serial(
    port='/dev/ttyAMA0',
    baudrate=38400,
    timeout=1,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS
)

seconds = int(raw_input('Enter amount of seconds: '))

for i in range(0, seconds):
    write=ser.write('!0 02\r\n')
    time.sleep(1)
    byte=ser.inWaiting()
    status=ser.read(byte)[6:10]
    if status == '0000':        # A: No EV connected
        time.sleep(1)
        print status
    elif status == '0005':      # C: EV is charging
        write=ser.write('!0 27\r\n')
        time.sleep(1)
        write=ser.write('!0 25\r\n')
        time.sleep(1)
        byte=ser.inWaiting()
        ans=ser.read(byte)
        print status
    elif status == '0003':      # B-: Charging stopped by EVSE
        write=ser.write('!0 28\r\n')
        time.sleep(1)
        byte=ser.inWaiting()
        ans=ser.read(byte)
        print status
    else:
        time.sleep(1)
        print status

ser.close()