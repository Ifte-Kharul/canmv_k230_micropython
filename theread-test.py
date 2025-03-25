#import _thread
#import time
#import file1
#import file2
##def file1_task():
##    while True:
##        print("File 1 running")
##        time.sleep(1)

##def file2_task():
##    while True:
##        print("File 2 running")
##        time.sleep(2)

#_thread.start_new_thread(file1.hello_tamim, ())
#_thread.start_new_thread(file2hello_tamim, ())

# Main loop (optional)
#while True:
#    time.sleep(10) #Keep the main thread alive.


import os

def get_current_file_location():
    try:
        file_path = __file__
        absolute_path = os.stat(file_path)
        return absolute_path
    except NameError:
        return "Could not determine file location (interactive session or similar)."

current_location = get_current_file_location()
print(f"Current file location: {current_location}")
