# Interpreteur de trame
# Projet Hydros NEOMYS
# Auteur:  AN NAHRI

import XBee_Threaded_series_2
import struct
import sys
import serial
from time import sleep
from serial import SerialException

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

def bytes_to_int(bytes):
    result = 0

    for b in bytes:
        result = result * 256 + int(b)

    return result

if __name__ == "__main__":
    print("Available ports: ")
    ports = serial_ports()
    for po in ports:
        print(po)
    port = input("Which port? ")
    try:
        xbee = XBee_Threaded_series_2.XBee(port)    
        while True:
            Msg = xbee.Receive(0)
            if Msg:
                content = Msg[14:-1]            
                data = content[6:]                        
                totemid = content[0:3].decode(encoding='ascii', errors='strict')
                ncf = bytes_to_int(content[3:4])

                if ncf == 0: cf = "Données capteurs"
                else: cf = "Image"

                offset = 0
                capteurs = []           
                for i in range(4):
                  getdata = struct.unpack('=f',data[offset:offset+4])              
                  capteurs.append(''.join(map(str, (getdata))))
                  offset+=4

                print("================================================")
                print("Totem Id: {}".format(totemid))
                print("Code fonction: {} ({})".format(ncf, cf))
                print("Données: ")
                print("\tNiveau: {} mm".format(capteurs[0]))
                print("\tTemperateur d'eau: {} °C".format(capteurs[1]))
                print("\tHumidité: {} %".format(capteurs[2]))
                print("\tTemperateur d'air: {} °C".format(capteurs[3]))
                print("================================================")
    except SerialException:
        print ("Error: port {} inexistant".format(port))
    except KeyboardInterrupt:
        print ("Program arrêté")


