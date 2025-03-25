'''
Demo Name：KEY
Version：v1.0
Author：01Studio
Platform：01Studio CanMV K230
Description: Change the LED on/off status by pressing the key
'''

from machine import Pin
from machine import FPIOA
import time


#Configure GPIO52、GPIO21 as a normal GPIO
fpioa = FPIOA()
fpioa.set_function(52,FPIOA.GPIO52)
fpioa.set_function(21,FPIOA.GPIO21)
fpioa.set_function(19,FPIOA.GPIO19)

LED=Pin(52,Pin.OUT) #Build LED object and turn off LED
#KEY=Pin(21,Pin.IN,Pin.PULL_UP) #Construct KEY object
KEY=Pin(19,Pin.IN,Pin.PULL_UP)
state=0 #LED status

while True:

    if KEY.value()==0:   #Key pressed
        time.sleep_ms(10) #Eliminate jitter
        if KEY.value()==0: #Confirm key is pressed

            state=not state  #Use the not statement instead of the ~
            LED.value(state) #LED status flip
            print('KEY')

            while not KEY.value(): #Detect whether the button is released
                pass
