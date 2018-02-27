# Interpreteur de trame
# Projet Hydros NEOMYS
# Auteur:  AN NAHRI

import XBee_Threaded_series_2
import struct
from time import sleep

if __name__ == "__main__":
    xbee = XBee_Threaded_series_2.XBee("COM3")

    def bytes_to_int(bytes):
        result = 0

        for b in bytes:
            result = result * 256 + int(b)

        return result

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



