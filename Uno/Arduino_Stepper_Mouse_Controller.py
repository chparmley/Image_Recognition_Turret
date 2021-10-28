# Importing Libraries
import serial
import time
import pyautogui

resolution = 32
speed = 60

arduino = serial.Serial(port='/dev/cu.usbmodem13201', baudrate=19200, timeout=1)
def write_read(x):
    arduino.write(bytes(x, 'utf-8'))
    time.sleep(0.05)
    data = arduino.readline()
    return data

def write(x):
    arduino.write(bytes(x, 'utf-8'))

def read():
    # get feedback from arduino on it's position
    msg = arduino.readline().decode('utf-8').strip()
    print(msg)

# takes in a tuple coordinate pair x,y and sends it to the arduino
# min (0,0) max (180,180)
def send_position(coordinate_pair,resolution):
    xaxis,yaxis = coordinate_pair
    write(str(xaxis)+'x')
    write(str(yaxis)+'y')
    write(str(resolution)+'r')
    write(str(speed)+'s')

# gets current position of mouse
def mouse_position():
    x, y = pyautogui.position()
    return x,y


def mouse_control():
    time.sleep(.5)
    height, width = pyautogui.size()  # current screen resolution width and height
    pyautogui.moveTo(height*.5,width*.5)
    while True:
        mousex,mousey = mouse_position()
        if mousex >= 0 and mousex <= height and mousey >=0 and mousey <= width:
            new_position = (mousex,mousey)
            send_position(new_position,resolution)
mouse_control()