import cv2
from  Stepper_Movement import send_position

# Load the cascade
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# To capture video from webcam. 
cap = cv2.VideoCapture(0)
while True:
    # Read the frame
    _, img = cap.read()
    img = cv2.rotate(img, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #img = cv2.resize(img, (800,480))
    img = img[0:400, 0:400]
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Detect the faces
    faces = face_cascade.detectMultiScale(gray, 2, 3)
    # Get x,y positions for the arduino
    screen_x,screen_y = img.shape[1],img.shape[0]
    # Center screen circle
    cv2.circle(img,(int(screen_x/2),int(screen_y/2)), 3, (0,0,255), -1)
    position = (screen_x/2,screen_y/2)
    # Draw the rectangle around each face
    for (x, y, w, h) in faces:
        position = (int((x+.5*w)),int((y+.5*h)))
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)
    try:
        # Send the object position to function to move the arduino
        faces = faces[:1]
        send_position(position, screen_x, screen_y)
    except:
        pass

    # Display
    cv2.imshow('img', img)
    # Stop if escape key is pressed
    k = cv2.waitKey(30) & 0xff
    if k==27:
        break
    
# Release the VideoCapture object
cap.release()