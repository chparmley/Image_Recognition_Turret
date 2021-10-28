# Importing Libraries
import serial
import time
import pyautogui
arduino = serial.Serial(port='/dev/cu.usbmodem13201', baudrate=19200, timeout=.1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def write(x):
    arduino.write(bytes(x, 'utf-8'))

# takes in a tuple coordinate pair x,y and sends it to the arduino
# min (0,0) max (180,180)
def send_position(coordinate_pair):
    xaxis,yaxis = coordinate_pair
    write(str(xaxis)+'x')
    write(str(yaxis)+'y')
    time.sleep(.004)

# gets current position of mouse
def mouse_position():
    x, y = pyautogui.position()
    return x,y

current_pos = (90,90)
send_position(current_pos)
time.sleep(.5)
while True:
    mousex,mousey = mouse_position()
    print(mousex,mousey)
    if mousex >= 0 and mousex <= 1280 and mousey >=0 and mousey <= 799:
        new_position = (int(180-mousex/7),int(mousey/4))
        send_position(new_position)




