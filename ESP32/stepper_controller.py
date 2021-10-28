# Importing Libraries
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)

def send_position(position,screen_width,screen_height):
   move_string = []
   error_margin = 5
   buffer = 5
   # for the distance from center of target to center of camera on x axis
   distance_x = abs(int(position[0] - screen_width/2))
   for move in range(int(distance_x/5)):
      if distance_x > 96:
         step_setting = '1'
      elif distance_x > 64:
         step_setting = '2'
      elif distance_x > 32:
         step_setting = '4'
      if distance_x > 24:
         step_setting = '8'
      elif distance_x > 8:
         step_setting = '16'
      elif distance_x > 1:
         step_setting = '32'
      move_string.append(step_setting)

      # If target right of center
      if position[0] - screen_width/2 > 0:
         move_string.append('r')
         distance_x -= 32/int(step_setting)
      # If target left of center
      if position[0] - screen_width/2 < 0:
         move_string.append('l')
         distance_x -= 32/int(step_setting)

   distance_y = abs(int(position[1] - screen_height/2))
   # for the distance from center of target to center of camera on y axis
   for move in range(int(distance_y/5)):
      if distance_y > 32:
         step_setting = '1'
      elif distance_y > 16:
         step_setting = '2'
      elif distance_y > 8:
         step_setting = '4'
      if distance_y > 4:
         step_setting = '8'
      elif distance_y > 2:
         step_setting = '16'
      elif distance_y > 1:
         step_setting = '32'
      move_string.append(step_setting)

      # If target below center
      if position[1] - screen_height/2 > 0:
         move_string.append('d')
         distance_y -= 32/int(step_setting)
      # If target above center
      if position[1] - screen_height/2 < 0:
         move_string.append('u')
         distance_y -= 32/int(step_setting)


   if distance_x < 35 and distance_y < 35:
      print('Locked..', position)
   write_moves(move_string)

def write_moves(move_string):
    while len(move_string)!=0:
#        print(move_string[0])
        arduino.write(bytes(move_string.pop(), 'utf-8'))