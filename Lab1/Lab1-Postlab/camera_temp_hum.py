from sense_hat import SenseHat
import time
import datetime
import numpy as np

from picamera2 import Picamera2
from picamera2.encoders import H264Encoder
from picamera2.outputs import CircularOutput
from libcamera import controls


import cv2

sense=SenseHat()


sense.clear() ## to clear the LED matrix

pressure=sense.get_pressure()

first_temperature=sense.get_temperature()
first_temperature=round(first_temperature,1)  ## round temperature to 1 decimal place
epsilon = 1

first_humidity=sense.get_humidity()

blue= (0,0,255)
yellow= (255,255,0)
red=(255,0,0)
white=(255, 255, 255)
black=(0,0,0)
num_history_frames=5

picam2=Picamera2()  ## Create a camera object

back_sub= cv2.createBackgroundSubtractorMOG2(history=num_history_frames,varThreshold=25,detectShadows=False)
time.sleep(0.1)
max_foreground=127 # (0-255)

max_foreground=50 # (0-255)
## Create a kernel for morphological operation to remove noise from binary images.
## You can tweak the dimensions of the kernel ## e.g. instead of 20,20 you can try 30,30.
## This creates a square matrix of 20x20 filled with ones, suitable for closing operations.
## Closing operations smoothen out a binary image by removing small holes/gaps in detected objects
kernel= np.ones((20,20), np.uint8)


dispW=1280
dispH=720

picam2.preview_configuration.main.size = (dispW,dispH)  

picam2.preview_configuration.main.format= "RGB888"
picam2.preview_configuration.align() 
picam2.preview_configuration.controls.FrameRate=30

picam2.configure("preview")

faceCascade=cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

while True:
    pressure=sense.get_pressure()

    temperature=sense.get_temperature()
    temperature=round(temperature,1)  ## round temperature to 1 decimal place

    humidity=sense.get_humidity()
    
    print("Diff", abs(first_temperature - temperature), (abs(first_humidity - humidity)))
    if abs(first_temperature - temperature) > epsilon or (abs(first_humidity - humidity) > epsilon):

        picam2.start()
        while True:
            
            frame=picam2.capture_array() 
            
            frameGray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            faces=faceCascade.detectMultiScale(frameGray,1.3,5)

            # print(faces)
            for face in faces:
                x,y,w,h=face
                frame = cv2.rectangle(frame, (x,y), (x+w, y+h), (255,0,0),3) 

            ## Frame is a large 2D array of rows and cols
            fgmask = back_sub.apply(frame) ## obtains the foreground mask

            fgmask=cv2.medianBlur(fgmask,5)
            fgmask=cv2.morphologyEx(fgmask,	cv2.MORPH_CLOSE, kernel)

            _,fgmask=cv2.threshold(fgmask, max_foreground, 255, cv2.THRESH_BINARY)

            contours, hierarchy = cv2.findContours(fgmask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)[-2:]
            areas=[cv2.contourArea(c) for c in contours]

        # if there are no contours

            if len(areas) < 1: 
                cv2.imshow('Frame', frame)
                key = cv2.waitKey(1) & 0xFF ## wait for key press for 1 millisecond

                if key == ord("q"): ## stops for 1 ms to check if key Q is pressed
                    break

                # go to the top of the for loop

                continue

            else: # goes with "if len(areas)<1"

                    # find the largest moving object in the frame

                max_index= np.argmax(areas)

            ## Draw the bounding box
            cnt=contours[max_index]

            x,y,w,h= cv2.boundingRect(cnt)

            cv2.rectangle(frame, (x,y), (x+w, y+h), (0,255,0), 3) # Draw the circle in the center of the bounding box 
            
            x2= x + int(w/2)
            y2= y + int(h/2)

            cv2.circle(frame,(x2,y2), 4, (0,255,0), -1)

            ## Print the centroid coordinates (we'll use the center of the bounding ## box) on the image

            text= "x: " + str(x2) + ", y: " + str(y2)

            cv2.putText(frame, text, (x2-10, y2-10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

            ## Display the resulting frame 
            
            cv2.imshow("Frame", frame) 

            key=cv2.waitKey(1) & 0xFF
            
            if key == ord("q"): 
                cv2.destroyAllWindows()
                break
                            
            time.sleep(0.1)

sense.clear()

print()

print("The air temperature is", temperature, "celcius")

print("The humidity is", humidity, "%")


