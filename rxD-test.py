from machine import UART
import time
# Initialize UART3 with a baud rate of 115200, 8 data bits, no parity, and 1 stop bit
u3 = UART(UART.UART2, baudrate=115200, bits=UART.EIGHTBITS, parity=UART.PARITY_NONE, stop=UART.STOPBITS_ONE)

#Send data via UART3
while True:
    u3.write('Hello from CanMV K230!\r\n') # Send the message
    time.sleep(1) # Wait for 1 second

#Release UART resources
u3.deinit()


#01 studio

'''
Demo Name：UART
Author：01Studio
Platform：01Studio CanMV K230
Description：Realize serial communication through programming, and send and receive data with computer serial assistant
'''

#Import UART module
#from machine import UART
#from machine import FPIOA
#import time

#fpioa = FPIOA()

# UART1 Code
#fpioa.set_function(11,FPIOA.UART2_TXD)
#fpioa.set_function(12,FPIOA.UART2_RXD)

#uart=UART(UART.UART2,115200) #Set UART1 and baud rate

#'''

## UART2 Code
#fpioa.set_function(11,FPIOA.UART2_TXD)
#fpioa.set_function(12,FPIOA.UART2_RXD)

#uart=UART(UART.UART2,115200) #Set UART2 and baud rate
#'''

#uart.write('Hello 01Studio!')#Send data

#while True:

#    text=uart.read(128) #Receive 128 characters
#    if text != b'':
#        print(text) #Print the data received by UART3 through REPL

#    time.sleep(0.1) #100ms
