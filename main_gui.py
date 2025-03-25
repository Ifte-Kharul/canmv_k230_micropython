from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv
from machine import TOUCH
import image
#import uctypes
#import xxhello
#import wifi
#import uctypes
from machine import Pin
from machine import FPIOA
import gui_wifi_scan
import page_manager
import scroll_button
# Display resolution
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

# Initialize display
def display_init():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

# Deinitialize display
def display_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(50)
    Display.deinit()
    MediaManager.deinit()

# LVGL display buffer management
def disp_drv_flush_cb(disp_drv, area, color):
    global disp_img1, disp_img2
    if disp_drv.flush_is_last():
        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
            Display.show_image(disp_img1)
        else:
            Display.show_image(disp_img2)
        time.sleep(0.01)
    disp_drv.flush_ready()

# Initialize LVGL
def lvgl_init():
    global disp_img1, disp_img2
    lv.init()

    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)

    # Using BGRA8888 for display buffers
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)

    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)

    gc.collect()
    print("Free memory after lvgl init:", gc.mem_free())

# Deinitialize LVGL
def lvgl_deinit():
    global disp_img1, disp_img2
    lv.deinit()
    del disp_img1
    del disp_img2
    gc.collect()


# Initialize system
display_init()
lvgl_init()


page_manager.init(scroll_button.start())


lvgl_deinit()
display_deinit()
