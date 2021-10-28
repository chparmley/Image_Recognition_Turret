# Importing Libraries
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)

def send_position(position,screen_width,screen_height):
  move_string = []
  for move in range(abs(int((position[0] - screen_width/2)/5))):
    # Checks if the target is within the margin of error
    if abs(position[0] - screen_width/2) > 1:
       # If target right of center
       if position[0] - screen_width/2 > 0:
          move_string.append('r')
       # If target left of center
       if position[0] - screen_width/2 < 0:
          move_string.append('l')
  for move in range(abs(int((position[1] - screen_height/2)/5))):
    # If not withing our margin of error
    if abs(position[1] - screen_height/2) > 1:
       # If target below center
       if position[1] - screen_height/2 > 0:
          move_string.append('d')
       # If target above center
       if position[1] - screen_height/2 < 0:
          move_string.append('u')

  if abs(position[0] - screen_width/2) < 35 and abs(position[1] - screen_height/2) < 35:
    print('Locked..', position)
  write_moves(move_string)

def write_moves(move_string):
    while len(move_string)!=0:
#        print(move_string[0])
        arduino.write(bytes(move_string.pop(), 'utf-8'))