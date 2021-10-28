# Importing Libraries
import serial
from time import sleep
arduino = serial.Serial(port='/dev/ttyACM1', baudrate=19200, timeout=1)

def send_position(position,screen_width,screen_height):
    move_string = []
    if abs(position[0] - screen_width/2) > 1:
       for move in range(abs(int((position[0] - screen_width/2)/10))):

          if position[0] - screen_width/2 > 0:
             move_string.append('r')

          if position[0] - screen_width/2 < 0:
             move_string.append('l')


    if abs(position[1] - screen_height/2) > 1:
       for _ in range(abs(int((position[1] - screen_width/2)/10))):

          if position[1] - screen_height/2 > 0:
             move_string.append('d')

          if position[1] - screen_height/2 < 0:
             move_string.append('u')

    write_moves(move_string)

def write_moves(move_string):
    while len(move_string)!=0:
        arduino.write(bytes(move_string.pop(), 'utf-8'))
    sleep()
