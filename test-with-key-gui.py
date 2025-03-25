from media.display import *
from media.media import *
import time, os, sys, gc
import lvgl as lv
from machine import TOUCH
import image
import uctypes
import xxhello
import wifi
import uctypes
from machine import Pin
from machine import FPIOA

#Global Variables:

ip_label = None
server_label = None
antenna_label = None
wifi_label = None


#Configure GPIO52、GPIO21 as a normal GPIO
fpioa = FPIOA()
fpioa.set_function(21,FPIOA.GPIO21)
KEY=Pin(21,Pin.IN,Pin.PULL_UP)

wifi.Wifi_Connect()

val = wifi.Wifi_Connect()
server_add = wifi.print_server_ip("1.1.1.1")



#server_add = wifi.print_server_ip("jence.com")
#print(val)
DISPLAY_WIDTH = ALIGN_UP(800, 16)
DISPLAY_HEIGHT = 480

def display_init():
    Display.init(Display.ST7701, width=800, height=480, to_ide=True)
#    Display.init(Display.LT9611, width=800, height=480, to_ide=True)
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

def refresh():
    global val, server_add, ip_label, server_label, antenna_label, wifi_label

    val = wifi.Wifi_Connect()
    server_add = wifi.print_server_ip("1.1.1.1")

    print("Refreshing...")

    # Update label text
    ip_label.set_text("IP address of this device: " + val)
    server_label.set_text("IP address of the server: " + str(server_add))
    antenna_label.set_text("Antenna is ON/OFF: ")
    wifi_label.set_text("WiFi: ")

    # Manually refresh LVGL UI
    lv.task_handler()


def show_text_lvgl(text, x, y, color=lv.color_white(),font_size=30):
    res_path = "/sdcard/examples/15-LVGL/data/"

    font_montserrat_22 = lv.font_load("A:" + res_path + "font/montserrat-22.fnt")

#    try:
#        os.stat(font_path)
#    except OSError as e:
#        print(f"Font error: {e}")
#        print("Check if font file exists at:", font_path)
#        return
#    c_font = lv.font_load(font_path)
#    if not c_font:
#        print("Font loaded but invalid format!")
#        return

#    print("""Displays text using LVGL.""")
    label = lv.label(lv.scr_act())
    label.set_text(text)
    label.set_style_text_font(font_montserrat_22,0)
#    label.set_style_text_size(font_size)
#    label.set_style_text_font(lv.style.LV_FONT_MONTSERRAT_30,0)
    label.set_style_text_color(color, 0)
    label.set_width(650)
    label.set_pos(x, y)
    print("Free mem:", gc.mem_free())
#    print("""Displays text using LVGL -CCC.""")
def createSquare(start,lbl_text=""):
    square_size = 50  # Size of each square
    spacing = 5       # Space between squares
    start_x = 550     # Starting X position (right side of 800px screen)
    start_y = start     # Same Y as text
    colors = [
        lv.color_make(255, 0, 0),  # Red
        lv.color_make(0, 255, 0),  # Green
        lv.color_make(0, 255, 197),
        lv.color_make(255, 255, 0) # Yellow
    ]
    # Create 4 square objects
    for i in range(4):
        square = lv.obj(lv.scr_act())
        square.set_size(square_size, square_size)
        square.set_pos(start_x - (4 - i) * (square_size + spacing), start_y)

        # Style the squares (black border, white background)
        square.set_style_bg_color(colors[i], lv.PART.MAIN)
        square.set_style_border_color(lv.color_black(), lv.PART.MAIN)
        square.set_style_border_width(2, lv.PART.MAIN)
        lbl = lv.label(square)
        if lbl_text == "":
            lbl.set_text(str(i+1))
        else:
            lbl.set_text(lbl_text)


        lbl.center()



#def anim_callback(obj, value):
#    obj.set_x(value)


#anim_cb = lv.anim_custom_exec_cb_t(anim_callback)

def create_marquee(text):
    res_path = "/sdcard/examples/15-LVGL/data/"
    font_montserrat_22 = lv.font_load("A:" + res_path + "font/montserrat-22.fnt")

    label = lv.label(lv.scr_act())
    label.set_text(text)
    label.set_style_text_font(font_montserrat_22, 0)
    label.set_style_text_color(lv.color_make(0, 0, 0), 0)  # Black text
    label_width = label.get_width()
    label.set_y(DISPLAY_HEIGHT - 50)  # Place at the bottom

    # Initial position (off-screen)
    label.set_x(DISPLAY_WIDTH)

    def update_position(timer):
        x = label.get_x() - 5  # Move left
        if x < -label_width:  # Reset when off-screen
            x = DISPLAY_WIDTH
        label.set_x(x)

    # ✅ Use an LVGL timer to update position every 50ms
    lv.timer_create(update_position, 50, None)




def main():
    global ip_label, server_label, antenna_label, wifi_label

    os.exitpoint(os.EXITPOINT_ENABLE)
    ls = xxhello.fibonacci_sequence(20)

    try:
        display_init()
        lvgl_init()

        ip_label = lv.label(lv.scr_act())
        ip_label.set_text("IP address of this device: " + val)
        ip_label.set_pos(100, 100)

        server_label = lv.label(lv.scr_act())
        server_label.set_text("IP address of the server: " + str(server_add))
        server_label.set_pos(100, 150)

        antenna_label = lv.label(lv.scr_act())
        antenna_label.set_text("Antenna is ON/OFF: ")
        antenna_label.set_pos(100, 220)
        antenna_label = lv.label(lv.scr_act())


        loss_label = lv.label(lv.scr_act())
        antenna_label.set_text("Return Loss:  ")
        antenna_label.set_pos(100, 290)

        wifi_label = lv.label(lv.scr_act())
        wifi_label.set_text("WiFi: ")
        wifi_label.set_pos(100, 360)

        createSquare(220)
        createSquare(285, "L")

        # Create a button to trigger refresh
        btn = lv.btn(lv.scr_act())
        btn.set_pos(200, 350)
        label = lv.label(btn)
        label.set_text("Scan")

        create_marquee("Hello From Jence.com")

        while True:
            if KEY.value() == 0:
                refresh()

            time.sleep_ms(lv.task_handler())

    except BaseException as e:
        import sys
        sys.print_exception(e)

    lvgl_deinit()
    display_deinit()
    gc.collect()



if __name__ == "__main__":
    main()
