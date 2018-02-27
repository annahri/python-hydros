# Get Frame
# Projet Hydros NEOMYS
# Auteur:  AN NAHRI

import XBee_Threaded_series_2
import sys
import glob
import serial
from time import sleep

if __name__ == "__main__":
    port = input(sys.argv)    
    xbee = XBee_Threaded_series_2.XBee(port)

    while True:
        Msg = xbee.Receive(0)
        if Msg:
            content = Msg[14:-1]            
            print('[ '+ xbee.format(content) + ' ]')



