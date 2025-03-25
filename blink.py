# Untitled - By: tanzil - Sun Mar 2 2025
from machine import Pin
import time

# Define the GPIO pin connected to your LED.
# Replace 'your_pin_number' with the actual GPIO pin number.
LED_PIN = Pin(3, Pin.OUT)

# Example: If your LED is connected to GPIO pin 25, use:
# LED_PIN = Pin(25, Pin.OUT)
LED_PIN.value(2)

#try:
#    while True:
#        # Turn the LED on
#        LED_PIN.value(1)
#        time.sleep(0.5)    # Wait for 0.5 seconds

#        LED_PIN.value(0)  # Turn the LED off
#        time.sleep(0.5)    # Wait for 0.5 seconds

#except KeyboardInterrupt:
#    print("Blinking stopped.")
#    LED_PIN.value(0) # turn off LED when stopping the code.
