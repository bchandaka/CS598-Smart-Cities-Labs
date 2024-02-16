from sense_hat import SenseHat
import time
import matplotlib.pyplot as plt
import math
sense=SenseHat()


sense.clear() ## to clear the LED matrix
start = time.time()
t_array = []
times = []
while time.time() -start < 10:
    temp=sense.get_temperature()
    t_array.append(temp)
    times.append(time.time())
    time.sleep(0.1)
def avg(l):
    return sum(l)/len(l)
    
window = 10
smooth_t_array = [avg(t_array[i:i+window]) for i in range(len(t_array)-window)]

plt.plot(times, t_array, label="raw temp")
plt.plot( times[window:], smooth_t_array, label="smooth temp")
plt.legend()
plt.show()
