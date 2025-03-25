from machine import WDT #Import WDT module
import time

#Construct watchdog object.
wdt = WDT(1,3) #Watchdog number 1, timeout period 3 seconds.


#Feed the dog every 1 second, and do this 3 times.
for i in range(3):

    time.sleep(1)
    print(i)

    wdt.feed() #Feed dog

#Stop feeding the dog, the system will restart.
while True:

    time.sleep(0.01) #Prevent CPU from running full.
