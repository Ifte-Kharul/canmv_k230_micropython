from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv
from machine import TOUCH

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

class touch_screen():
    def __init__(self):
        self.state = lv.INDEV_STATE.RELEASED
        self.indev_drv = lv.indev_create()
        self.indev_drv.set_type(lv.INDEV_TYPE.POINTER)
        self.indev_drv.set_read_cb(self.callback)
        self.touch = TOUCH(0)

    def callback(self, driver, data):
        x, y, state = 0, 0, lv.INDEV_STATE.RELEASED
        tp = self.touch.read(1)
        if len(tp):
            x, y, event = tp[0].x, tp[0].y, tp[0].event
            if event == 2 or event == 3:
                state = lv.INDEV_STATE.PRESSED
        data.point = lv.point_t({'x': x, 'y': y})
        data.state = state

def lvgl_init():
    global disp_img1, disp_img2

    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)
    tp = touch_screen()

def lvgl_deinit():
    global disp_img1, disp_img2

    lv.deinit()
    del disp_img1
    del disp_img2

def btn_clicked_event(event):
    popup = lv.obj(lv.scr_act())
    popup.set_size(200, 100)
    popup.align(lv.ALIGN.CENTER, 0, 0)

    popup_label = lv.label(popup)
    popup_label.set_text("Welcome Jence!")
    popup_label.align(lv.ALIGN.CENTER, 0, 0)

    close_btn = lv.btn(popup)
    close_btn.align(lv.ALIGN.BOTTOM_MID, 0, 30)
    close_btn_label = lv.label(close_btn)
    close_btn_label.set_text("Close")

    def close_popup(event):
        popup.delete()

    close_btn.add_event(close_popup, lv.EVENT.CLICKED, None) #Corrected line.

def user_gui_init():
    btn = lv.btn(lv.scr_act())
    btn.align(lv.ALIGN.CENTER, 0, lv.pct(25))
    label = lv.label(btn)
    label.set_text('Show Popup')
    btn.add_event(btn_clicked_event, lv.EVENT.CLICKED, None) #Corrected line.

def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    try:
        display_init()
        lvgl_init()
        user_gui_init()
        while True:
            time.sleep_ms(lv.task_handler())
    except BaseException as e:
        import sys
        sys.print_exception(e)
    lvgl_deinit()
    display_deinit()
    gc.collect()

if __name__ == "__main__":
    main()
