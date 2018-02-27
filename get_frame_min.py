# Get Frame
# Projet Hydros NEOMYS
# Auteur:  AN NAHRI

import XBee_Threaded_series_2
import struct
import sys
import glob
import serial
from time import sleep

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

if __name__ == "__main__":
    print("Available ports: ")
    ports = serial_ports()
    for po in ports:
        print(po)
    port = input("Which port? ")    
    xbee = XBee_Threaded_series_2.XBee(port)

    Msg = xbee.Receive(0)
    if Msg:
        content = Msg[14:-1]            
        print('[ '+ xbee.format(content) + ' ]')

    xbee.shutdown()



