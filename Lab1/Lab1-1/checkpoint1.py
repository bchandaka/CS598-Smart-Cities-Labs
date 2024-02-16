from sense_hat import SenseHat
import time

sense=SenseHat()


sense.clear() ## to clear the LED matrix

pressure=sense.get_pressure()

first_temperature=sense.get_temperature()
first_temperature=round(first_temperature,1)  ## round temperature to 1 decimal place
epsilon = 1

humidity=sense.get_humidity()

blue= (0,0,255)
yellow= (255,255,0)
red=(255,0,0)
white=(255, 255, 255)
black=(0,0,0)
while True:
    pressure=sense.get_pressure()

    temperature=sense.get_temperature()
    temperature=round(temperature,1)  ## round temperature to 1 decimal place

    humidity=sense.get_humidity()
    sense.show_message("P:" + str(pressure), text_colour=blue, scroll_speed=0.05)
    sense.show_message("T:" + str(temperature), text_colour=red, scroll_speed=0.05)
    sense.show_message("H:" + str(humidity) , text_colour=yellow, scroll_speed=0.05)
    print("Diff", abs(first_temperature - temperature))
    if abs(first_temperature - temperature) > epsilon:
        for j in range(10):
            sense.set_pixel(3,3, red)
            time.sleep(0.5)
            sense.set_pixel(3,3, black)
            time.sleep(0.5)
    time.sleep(0.1)
    #sense.show_letter("R", red)
    #sleep(1)

sense.clear()

print()

print("The air temperature is", temperature, "celcius")

print("The humidity is", humidity, "%")


