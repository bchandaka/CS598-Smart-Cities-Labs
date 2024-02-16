from picamera2 import Picamera2, Preview
from sense_hat import SenseHat
import time

sense=SenseHat()

picam2 = Picamera2()

img_id = 0

camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
time.sleep(2)

blue= (0,0,255)
yellow= (255,255,0)

while True:
    
    
    
    for event in sense.stick.get_events():
        if event.direction == 'middle' and event.action == 'pressed':
            
            picam2.capture_file(f"test{img_id}.jpg")
            sense.show_message(f"test{img_id}.jpg", text_colour=blue, back_colour=yellow, scroll_speed=0.05)
            img_id += 1
