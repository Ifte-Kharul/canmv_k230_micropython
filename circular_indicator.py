from media.display import *
from media.media import *
import lvgl as lv
import time, gc, os
import gui_wifi_scan

# Display configuration
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480

def display_init():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
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

def lvgl_init():
    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)

    global disp_img1, disp_img2
    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)
    gc.collect()
    print("Free memory after lvgl init:", gc.mem_free())

def lvgl_deinit():
    global disp_img1, disp_img2
    lv.deinit()
    del disp_img1
    del disp_img2

def create_progress_indicator(scr):
    arc = lv.arc(scr)
    arc.center()
    arc.set_size(150, 150)
    arc.set_range(0, 100)
    arc.set_bg_angles(0, 360)
    arc.set_rotation(270)
    arc.set_value(0)
    arc.set_mode(lv.arc.MODE.NORMAL)
    return arc

def main():
    display_init()
    lvgl_init()
    scr = lv.scr_act()
    progress_arc = create_progress_indicator(scr)

    for i in range(101):
        progress_arc.set_value(i)
        lv.task_handler()
        time.sleep(0.05)

    lvgl_deinit()
    display_deinit()
    print("Progress completed! Launching WiFi scan...")
    gui_wifi_scan.main()

if __name__ == "__main__":
    main()
