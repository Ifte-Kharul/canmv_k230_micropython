from machine import UART
import time

# Initialize UART2
u2 = UART(UART.UART2, baudrate=115200, bits=8, parity=UART.PARITY_NONE,stop=UART.STOPBITS_ONE) # Using UART(3) as per documentation

print("Serial listener started. Waiting for data...")

while True:
    received_data_byte = u2.read()  # Try to read 1 byte, non-blocking
    if received_data_byte is not None:  # Check if any byte was read (not None)
        try:
            decoded_data = received_data_byte.decode('utf-8', 'ignore').strip() # Decode, ignoring errors
            print('Received:', decoded_data)
        except UnicodeError:
            print('Received non-text data') # Handle non-text data

    time.sleep_ms(100) # Small delay
