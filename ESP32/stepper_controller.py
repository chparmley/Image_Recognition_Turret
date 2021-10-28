# Importing Libraries
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)

def send_position(position,screen_width,screen_height):
   move_string = []
   axis = position.copy()
   # for the distance from center of target to center of camera on x axis
   for move in range(abs(int(axis[0] - screen_width/2))):
      if move > 64:
         step_setting = '4'
      elif move > 32:
         step_setting = '4'
      elif move > 16:
         step_setting = '4'
      elif move > 8:
         step_setting = '4'
      elif move > 4:
         step_setting = '4'
      elif move > 2:
         step_setting = '8'
      move_string.append(step_setting)
      axis[0] -= int(step_setting)
      print(move_string)
   
      # Check if the target is within the margin of error
      if abs(axis[0] - screen_width/2) > 1:
         # If target right of center
         if position[0] - screen_width/2 > 0:
            move_string.append('r')
         # If target left of center
         if position[0] - screen_width/2 < 0:
            move_string.append('l')


   # for the distance from center of target to center of camera on y axis
   for move in range(abs(int(position[1] - screen_height/2))):
      if move > 64:
         step_setting = '4'
      elif move > 32:
         step_setting = '4'
      elif move > 16:
         step_setting = '4'
      elif move > 8:
         step_setting = '4'
      elif move > 4:
         step_setting = '4'
      elif move > 2:
         step_setting = '8'
      move_string.append(step_setting)
      position[1] -= int(step_setting)

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