from picamera2 import Picamera2, Preview
from sense_hat import SenseHat
import time
import numpy as np 

sense=SenseHat()

picam2 = Picamera2()

img_id = 0

blue= (0,0,255)
yellow= (255,255,0)

pixel_location = np.array([3, 5])
sense.set_pixel(pixel_location[0],pixel_location[1], blue)
movements = {
    'right': np.array([1, 0]),
    'left': np.array([-1, 0]),
    'up': np.array([0, -1]),
    'down': np.array([0, 1])

}


while True:
    
    for event in sense.stick.get_events():
        if event.direction == 'middle' and event.action == 'pressed':
            sense.set_pixel(pixel_location[0],pixel_location[1], (0, 0, 0))
            exit()
        else:
        
            if event.direction in movements:
                sense.set_pixel(pixel_location[0],pixel_location[1], (0, 0, 0))
                pixel_location += movements[event.direction]
                pixel_location = pixel_location % 8
                sense.set_pixel(pixel_location[0],pixel_location[1], blue)
                time.sleep(0.2)


    

    
        
        