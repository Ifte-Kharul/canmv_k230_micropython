from media.display import *
from media.media import *
import time, os, gc, lvgl as lv
import network
from machine import Pin, FPIOA
from machine import Pin
import page_manager
import scroll_button
#from main import create_menu
KEY1 = Pin(21, Pin.IN, Pin.PULL_UP)  # Scroll button (Back)
# Display configuration
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 480
SCAN_INTERVAL = 10  # seconds

# Global variables
net_list = None
scroll_container = None
last_scan_time = 0

def display_init():
    Display.init(Display.ST7701, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT, to_ide=True)
    MediaManager.init()

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

def create_wifi_list(parent):
    global scroll_container

    # Create scroll container
    scroll_container = lv.obj(parent)
    scroll_container.set_size(700, 350)
    scroll_container.set_pos(40, 100)
    scroll_container.set_flex_flow(lv.FLEX_FLOW.COLUMN)
    scroll_container.set_style_pad_row(5, 0)

    # Style the scroll container
#    scroll_container.add_style(lv.style()
#        .set_bg_color(lv.color_hex(0xFFFFFF))
#        .set_border_color(lv.color_hex(0xCCCCCC))
#        .set_radius(5), 0)

def update_wifi_list():
    global net_list, scroll_container, last_scan_time

    # Clear previous results
    scroll_container.clean()

    # Scan networks
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    networks = wlan.scan()
    last_scan_time = time.time()

    if not networks:
        label = lv.label(scroll_container)
        label.set_text("No networks found!")
        label.set_style_text_color(lv.color_hex(0xFF0000), 0)
        return

    for net in networks:
        try:
            # Create network container
            cont = lv.obj(scroll_container)
            cont.set_size(lv.pct(100), 130)
            cont.set_flex_flow(lv.FLEX_FLOW.ROW)

            # Signal strength indicator
            rssi_bar = lv.obj(cont)
            rssi_bar.set_size(80, 30)
            rssi_bar.set_style_bg_color(get_signal_color(net.rssi), 0)
            rssi_bar.set_style_radius(5, 0)

            # Network info
            info_cont = lv.obj(cont)
            info_cont.set_size(lv.pct(70), lv.pct(100))
            info_cont.set_flex_flow(lv.FLEX_FLOW.COLUMN)

            # SSID
            ssid_label = lv.label(info_cont)
            ssid_label.set_text(net.ssid)
            ssid_label.set_style_bg_color(lv.color_hex(0xff0000), 0)
#            ssid_label.set_style_text_color(lv.color_hex(0x000000), 0)
            ssid_label.set_style_text_font(lv.font_montserrat_16, 0)

            # Details
            details_label = lv.label(info_cont)
            details = (f"RSSI: {net.rssi}dBm | Channel: {net.channel} | Security: {str(net.security).rsplit('_', 1)[-1] if net.security else 'Unknown'}")

            details_label.set_text(details)
            details_label.set_style_text_color(lv.color_hex(0x0000ff), 0)

        except Exception as e:
            print("Error displaying network:", e)

def get_signal_color(rssi):
    if rssi >= -50:
        return lv.color_hex(0x00FF00)  # Green
    elif rssi >= -70:
        return lv.color_hex(0xFFA500)  # Orange
    else:
        return lv.color_hex(0xFF0000)  # Red

def create_header(parent):
    # Header container
    header = lv.obj(parent)
    header.set_size(lv.pct(100), 60)
    header.set_style_bg_color(lv.color_hex(0x2C3E50), 0)

    # Title
    title = lv.label(header)
    title.set_text("Available WiFi Networks")
    title.set_style_text_color(lv.color_white(), 0)
#    title.set_style_text_font(lv.font_montserrat_22, 0)
    title.center()

    # Last scan time
    time_label = lv.label(header)
    time_label.set_text("Last scan: --:--")
    time_label.set_pos(600, 20)
    time_label.set_style_text_color(lv.color_hex(0xCCCCCC), 0)
    return time_label

def create_refresh_button(parent):
    btn = lv.btn(parent)
    btn.set_size(120, 50)
    btn.set_pos(320, 400)
    btn_label = lv.label(btn)
    btn_label.set_text("Refresh")
#    btn.add_event_cb(lambda e: update_wifi_list(), lv.EVENT.CLICKED, None)
    return btn

def main():
    global last_scan_time

    # Initialize hardware
#    display_init()
#    lvgl_init()

    # Create UI elements
#    scr = lv.scr_act()
    scr = lv.obj()
    lv.scr_load(scr)
    time_label = create_header(scr)
    create_wifi_list(scr)
    create_refresh_button(scr)

    # Initial scan
    update_wifi_list()
    print("WiFi GUI started. Press KEY1 to go back.")
    # Main loop

    last_key1_state = KEY1.value()
    while True:
        lv.task_handler()

        key1_state = KEY1.value()
#        print(key1_state)
        if key1_state == 0 and last_key1_state == 1:  # If KEY1 is pressed (active-low)
            print("Going back to menu...")
            go_back()
            time.sleep(0.2)
            break  # Exit WiFi GUI loop

        last_key1_state = key1_state
        time.sleep_ms(50)

def go_back():
    """Return to main menu"""
    print("go back is called")

    page_manager.go_back()
#    page_manager.load_page(scroll_button.start())

#    lv.scr_act().delete()  # Clear the current UI
    gc.collect()
     # Reload main menu
