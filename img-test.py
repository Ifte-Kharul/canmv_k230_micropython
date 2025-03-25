from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv
from machine import TOUCH
import image
import uctypes
import xxhello
import tamim

DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

def display_init():
    Display.init(Display.ST7701, width=800, height=480, to_ide=True)
    MediaManager.init()

def display_deinit():
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(50)
    Display.deinit()
    MediaManager.deinit()

def disp_drv_flush_cb(disp_drv, area, color):
    global disp_img1, disp_img2

    if disp_drv.flush_is_last() == True:
        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
            Display.show_image(disp_img1)
        else:
            Display.show_image(disp_img2)
        time.sleep(0.01)

    disp_drv.flush_ready()

#class touch_screen():
#    def __init__(self):
#        self.state = lv.INDEV_STATE.RELEASED
#        self.indev_drv = lv.indev_create()
#        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
#        self.indev_drv.set_read_cb(self.callback)
##        self.touch = TOUCH(0)

#    def callback(self, driver, data):
#        x, y, state = 0, 0, lv.INDEV_STATE.RELEASED
#        tp = self.touch.read(1)
#        if len(tp):
#            x, y, event = tp[0].x, tp[0].y, tp[0].event
#            if event == 2 or event == 3:
#                state = lv.INDEV_STATE.PRESSED
#        data.point = lv.point_t({'x': x, 'y': y})
#        data.state = state

def lvgl_init():
    global disp_img1, disp_img2

    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)

    # Use RGB565 to reduce memory usage
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)

    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)
#    tp = touch_screen()
    gc.collect()
    print("Free memory after lvgl init:", gc.mem_free())

def lvgl_deinit():
    global disp_img1, disp_img2

    lv.deinit()
    del disp_img1
    del disp_img2




def show_text_lvgl(text, x, y, color=lv.color_white(),font_size=24):
    res_path = "/sdcard/examples/15-LVGL/data/"
    font_montserrat_16 = lv.font_load("A:" + res_path + "font/montserrat-16.fnt")
#    print("""Displays text using LVGL.""")
    label = lv.label(lv.scr_act())
    label.set_text(text)


    label.set_style_text_font(font_montserrat_16, 0)
    label.set_style_text_color(color, 0)
    label.set_width(650)
    label.set_pos(x, y)
#    print("""Displays text using LVGL -CCC.""")


def star_pyramid(rows):
    for i in range(1, rows + 1):
        show_text_lvgl(" " * (rows - i) + "#" * (2 * i - 1),300,i*10+200,color=lv.color_make(0, 0, 0))

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    ls = xxhello.fibonacci_sequence(20)
    try:
        display_init()
        lvgl_init()
        label = lv.label(lv.scr_act())
        show_text_lvgl("Helo Dear, The Multiplication of 10000 and 45000 is : "+str(xxhello.add_ints(10000,45000)), 100, 200,color=lv.color_make(0, 0, 0),font_size=32)

#        show_text_lvgl("Another line!", 300, 250, color=lv.color_make(255, 0, 0)) #example of different color and location
#        show_text_lvgl(str(ls), 100, 300,color=lv.color_make(0, 0, 0),font_size=32)
#        star_pyramid(5)
        while True:
            time.sleep_ms(lv.task_handler())
    except BaseException as e:
        import sys
        sys.print_exception(e)
    lvgl_deinit()
    display_deinit()
    gc.collect()

#def main():
#    os.exitpoint(os.EXITPOINT_ENABLE)
#    try:
#        display_init()
#        lvgl_init()
#        label = lv.label(lv.scr_act())
#        label.set_text("Test")
#        while True:
#            time.sleep_ms(lv.task_handler())
#    except BaseException as e:
#        import sys
#        sys.print_exception(e)
#    lvgl_deinit()
#    display_deinit()
#    gc.collect()

if __name__ == "__main__":
    main()

