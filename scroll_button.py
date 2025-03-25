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
## Display resolution
#DISPLAY_WIDTH = 800
#DISPLAY_HEIGHT = 480

## Initialize display
#def display_init():
#    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
#    MediaManager.init()

## Deinitialize display
#def display_deinit():
#    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
#    time.sleep_ms(50)
#    Display.deinit()
#    MediaManager.deinit()

## LVGL display buffer management
#def disp_drv_flush_cb(disp_drv, area, color):
#    global disp_img1, disp_img2
#    if disp_drv.flush_is_last():
#        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
#            Display.show_image(disp_img1)
#        else:
#            Display.show_image(disp_img2)
#        time.sleep(0.01)
#    disp_drv.flush_ready()

## Initialize LVGL
#def lvgl_init():
#    global disp_img1, disp_img2
#    lv.init()

#    disp_drv = lv.disp_create(DISPLAY_WIDTH, DISPLAY_HEIGHT)
#    disp_drv.set_flush_cb(disp_drv_flush_cb)

#    # Using BGRA8888 for display buffers
#    disp_img1 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)
#    disp_img2 = image.Image(DISPLAY_WIDTH, DISPLAY_HEIGHT, image.BGRA8888)

#    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)

#    gc.collect()
#    print("Free memory after lvgl init:", gc.mem_free())

## Deinitialize LVGL
#def lvgl_deinit():
#    global disp_img1, disp_img2
#    lv.deinit()
#    del disp_img1
#    del disp_img2
#    gc.collect()

# Input keys
KEY1 = Pin(21, Pin.IN, Pin.PULL_UP)  # Scroll
KEY2 = Pin(19, Pin.IN, Pin.PULL_UP)  # Enter

# Create menu UI
def create_menu():
    global current_index, labels, menu_items, scr

    scr = lv.obj()
    menu_items = ["WiFi Settings", "Start Face Recognition", "Scan the wifi networks", "Option 4"]
    current_index = 0
    labels = []
    res_path = "/sdcard/examples/15-LVGL/data/"

    font_montserrat_22 = lv.font_load("A:" + res_path + "font/montserrat-22.fnt")
    for i, item in enumerate(menu_items):
        label = lv.label(scr)
        label.set_text(item)
        label.set_style_text_font(font_montserrat_22,0)
        label.align(lv.ALIGN.TOP_MID, 0, 50 * i)
        labels.append(label)

    update_menu()
    lv.scr_load(scr)
#    return scr


def update_menu():
    """Highlight the selected menu item"""
    for i, label in enumerate(labels):
        if i == current_index:
            label.set_style_text_color(lv.color_hex(0xFF0000), 0)  # Red for highlight
            label.set_style_bg_color(lv.color_hex(0xb5e2ff), 0)
        else:
            label.set_style_text_color(lv.color_hex(0x000000), 0)  # White for normal

def read_buttons():
    """Check button states and handle scrolling and selection"""
    global current_index
    last_key1_state = KEY1.value()
    last_key2_state = KEY2.value()

    while True:
        lv.timer_handler()  # Update LVGL UI

        key1_state = KEY1.value()
        key2_state = KEY2.value()

        # Scroll when KEY1 is pressed (active-low)
        if key1_state == 0 and last_key1_state == 1:
            current_index = (current_index + 1) % len(menu_items)
            update_menu()
            time.sleep(0.2)  # Debounce delay

        # Select option when KEY2 is pressed
        if key2_state == 0 and last_key2_state == 1:
            print("Selected:", menu_items[current_index])
            if menu_items[current_index] == "WiFi Settings":
                open_wifi_gui()

            time.sleep(0.2)  # Debounce delay

        last_key1_state = key1_state
        last_key2_state = key2_state

        time.sleep(0.05)  # Reduce CPU usage

def open_wifi_gui():
    """Open the WiFi settings page"""
#    lv.scr_act().delete()
    gc.collect()
     # Deinitialize LVGL to free memory
    print("gui wifi scan start",gc.mem_free())

#    page_m = page_manager.PageManager()
#    page_m.init(create_menu())
    page_manager.load_page(gui_wifi_scan.main())
      # Call the WiFi GUI main function
    print("gui wifi scan end")
#    lvgl_init()  # Reinitialize LVGL after exiting WiFi GUI
#    print("Returned from WiFi GUI, reinitializing menu...")
#    display_init()  # Reinitialize display
#    lvgl_init()  # Reinitialize LVGL
#    create_menu()
#    create_menu()  # Reload menu after returning

# Initialize system

def start():
    create_menu()

    try:
        read_buttons()
    except KeyboardInterrupt:
        print("Exiting...")
        lvgl_deinit()
        display_deinit()
