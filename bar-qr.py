# QRCode Example
#
# This example shows the power of the CanMV Cam to detect QR Codes.
import time, os, gc, sys

from media.sensor import *
from media.display import *
from media.media import *

DETECT_WIDTH = 800
DETECT_HEIGHT = 480

sensor = None

try:
    # construct a Sensor object with default configure
    sensor = Sensor(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # sensor reset
    sensor.reset()
    # set hmirror
    # sensor.set_hmirror(False)
    # sensor vflip
    # sensor.set_vflip(False)
    # set chn0 output size
    sensor.set_framesize(width = DETECT_WIDTH, height = DETECT_HEIGHT)
    # set chn0 output format
    sensor.set_pixformat(Sensor.GRAYSCALE)

    # use hdmi as display output, set to VGA
    # Display.init(Display.LT9611, width = 640, height = 480, to_ide = True)

    # use hdmi as display output, set to 1080P
    # Display.init(Display.LT9611, width = 1920, height = 1080, to_ide = True)

    # use lcd as display output
    Display.init(Display.ST7701, to_ide = True)

    # use IDE as output
#    Display.init(Display.VIRT, width = DETECT_WIDTH, height = DETECT_HEIGHT, fps = 100)

    # init media manager
    MediaManager.init()
    # sensor start run
    sensor.run()

    fps = time.clock()

    while True:
        fps.tick()

        # check if should exit.
        os.exitpoint()
        img = sensor.snapshot()

        for code in img.find_qrcodes():
            rect = code.rect()
            img.draw_rectangle([v for v in rect], color=(255, 0, 0), thickness = 5)
            img.draw_string_advanced(rect[0], rect[1], 32, code.payload())
            print(code)
        for code in img.find_barcodes():
            rect = code.rect()
            img.draw_rectangle([v for v in code.rect()], color=(255, 0, 0), thickness = 5)
            img.draw_string_advanced(rect[0], rect[1], 32, code.payload())
            print(code)


        # draw result to screen
        Display.show_image(img)
        gc.collect()

#        print(fps.fps())
        fps.fps()
except KeyboardInterrupt as e:
    print(f"user stop")
except BaseException as e:
    print(f"Exception '{e}'")
finally:
    # sensor stop run
    if isinstance(sensor, Sensor):
        sensor.stop()
    # deinit display
    Display.deinit()

    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(100)

    # release media buffer
    MediaManager.deinit()
