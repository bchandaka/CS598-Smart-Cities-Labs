import os
import socket
import fcntl
import struct
from sense_hat import SenseHat
from time import sleep
import netifaces as ni

def get_ip_address(ifname):
    return ni.ifaddresses(ifname)[2][0]['addr']

sense=SenseHat()
blue= (0,0,255)
yellow= (255,255,0)
print("Wifi: ", get_ip_address('wlan0'))
for i in range(0,2):
    #sense.show_message("Welcome to CS 437")
    
    sense.show_message(f"Wifi:{get_ip_address('wlan0')}", text_colour=blue, back_colour=yellow, scroll_speed=0.08)
    #sense.show_letter("R", red)
    #sleep(1)

sense.clear()