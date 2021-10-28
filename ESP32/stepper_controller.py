# Importing Libraries
import serial
arduino = serial.Serial(port='/dev/ttyUSB0', baudrate=19200, timeout=1)

def send_position(position,screen_width,screen_height):
   move_string = []
   error_margin = 5
   buffer = 5
   # There are 200 steps in a revolution of the stepper motor
   # This variable attempts to each pixel to a step
   pixel_per_step_scaler = .8

   # for the distance from center of target to center of camera on x axis
   distance_x = abs(int(position[0] - screen_width/2))*pixel_per_step_scaler
   while distance_x > error_margin *pixel_per_step_scaler:
      if distance_x > 96 *pixel_per_step_scaler:
         step_setting = '1'
      elif distance_x > 64 *pixel_per_step_scaler:
         step_setting = '2'
      elif distance_x > 32 *pixel_per_step_scaler:
         step_setting = '4'
      elif distance_x > 24 *pixel_per_step_scaler:
         step_setting = '8'
      elif distance_x > 8 *pixel_per_step_scaler:
         step_setting = '16'
      else:
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

   distance_y = abs(int(position[1] - screen_height/2))*pixel_per_step_scaler
   # for the distance from center of target to center of camera on y axis
   while distance_y > error_margin *pixel_per_step_scaler:
      if distance_y > 32 *pixel_per_step_scaler:
         step_setting = '1'
      elif distance_y > 16 *pixel_per_step_scaler:
         step_setting = '2'
      elif distance_y > 8 *pixel_per_step_scaler:
         step_setting = '4'
      elif distance_y > 4 *pixel_per_step_scaler:
         step_setting = '8'
      elif distance_y > 2 *pixel_per_step_scaler:
         step_setting = '16'
      else:
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


   if distance_x < error_margin and distance_y < error_margin:
      print('Locked..', position)
   write_moves(move_string)

# Send moves to center target in camera to arduino
def write_moves(move_string):
    while len(move_string)!=0:
#        print(move_string[0])
        arduino.write(bytes(move_string.pop(), 'utf-8'))