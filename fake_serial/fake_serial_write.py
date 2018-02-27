import serial
import time
import random

port = "COM10"
ser = serial.Serial(port, 9600)

with open('frame.txt') as f:
    lines = f.readlines()
    
while True:
    frame = random.choice(lines)
    ser.write(frame.encode())
    print('Writing to {} port'.format(port))
    print(frame)
    time.sleep(2)
