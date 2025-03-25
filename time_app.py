from media.display import *
from media.media import *
import time,os,sys,gc
import lvgl as lv
import machine # Import machine module to use RTC


DISPLAY_WIDTH = ALIGN_UP(800,16)
DISPLAY_HEIGHT = 480

def display_init():
    print("display_init: starting")
    Display.init(Display.ST7701,width=DISPLAY_WIDTH,height=DISPLAY_HEIGHT,to_ide=True)
    MediaManager.init()
    print("display_init: finished")


def display_deinit():
    print("display_deinit: starting")
    os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
    time.sleep_ms(50)
    Display.deinit()
    MediaManager.deinit()
    print("display_deinit: finished")


def disp_drv_flush_cb(disp_drv,area,color):
    global disp_img1, disp_img2
    print("disp_drv_flush_cb: flushing display")

    if disp_drv.flush_is_last()==True:
        if disp_img1.virtaddr() == uctypes.addressof(color.__dereference__()):
            Display.show_image(disp_img1)
        else:
            Display.show_image(disp_img2)

    disp_drv.flush_ready()
    print("disp_drv_flush_cb: flush ready")


def lvgl_init():
    global disp_img1, disp_img2, ttf_font
    print("lvgl_init: starting")
    lv.init()
    disp_drv = lv.disp_create(DISPLAY_WIDTH,DISPLAY_HEIGHT)
    disp_drv.set_flush_cb(disp_drv_flush_cb)
    disp_img1 = image.Image(DISPLAY_WIDTH,DISPLAY_HEIGHT,image.BGRA8888)
    disp_img2 = image.Image(DISPLAY_WIDTH,DISPLAY_HEIGHT,image.BGRA8888)
    disp_drv.set_draw_buffers(disp_img1.bytearray(), disp_img2.bytearray(), disp_img1.size(), lv.DISP_RENDER_MODE.DIRECT)

    # --- Load TTF Font ---
    try:
        font_path = "S:/SourceHanSansSC-Normal-Min.ttf" # Assuming font file is in the root of SD card "S:/"
        font_size = 48 # Adjust font size as needed
        ttf_font = lv.font_load(font_path, font_size) # Load TTF font
        if ttf_font:
            print(f"lvgl_init: TTF font loaded successfully from {font_path}, size {font_size}")
        else:
            print(f"lvgl_init: Failed to load TTF font from {font_path}")
            ttf_font = lv.font_default # Fallback to default font
    except Exception as e:
        print(f"lvgl_init: Error loading TTF font: {e}")
        ttf_font = lv.font_default # Fallback to default font
    print("lvgl_init: finished")


def lvgl_deinit():
    global disp_img1, disp_img2, ttf_font
    print("lvgl_deinit: starting")

    lv.deinit()
    del disp_img1
    del disp_img2
    print("lvgl_deinit: finished")

def user_gui_init():
    global time_label, ttf_font
    print("user_gui_init: starting")
    # --- Set screen background color to light gray ---
    lv.scr_act().set_style_bg_color(lv.color_hex(0xdddddd), 0) # Light gray background for screen
    print("user_gui_init: screen background color set")


    time_label = lv.label(lv.scr_act())
    print("user_gui_init: time_label created")
    time_label.align(lv.ALIGN.CENTER,0,0)

    # --- Style for White Text Color and Label Background ---
    time_label_style = lv.style_t()
    time_label_style.init()
    time_label_style.set_text_color(lv.color_white()) # Set text color to white
    time_label_style.set_bg_color(lv.color_hex(0x333333)) # Set label background to dark gray
    time_label_style.set_bg_opa(lv.OPA.COVER) # Make label background opaque
    # --- Set the TTF font ---
    if ttf_font:
        time_label_style.set_text_font(ttf_font) # Use the loaded TTF font
        print("user_gui_init: TTF font style applied")
    else:
        print("user_gui_init: No TTF font loaded, using default font")
        time_label_style.set_text_font(lv.font_default) # Fallback to default font
    time_label.add_style(time_label_style, 0) # Apply the style to the label
    print("user_gui_init: style applied")
    print("user_gui_init: finished")


def set_time_manually():
    """
    Sets the device's time manually to: Tuesday, March 11, 2025 1:24:40 PM Dhaka time (+06).
    Time will reset when the device restarts.
    """
    # Set the time as a tuple: (year, month, day, hour, minute, second, weekday, yearday)
    # Tuesday, March 11, 2025 1:24:40 PM Dhaka time (+06)
    current_time_tuple = (2025, 3, 11, 13, 24, 40, 1, 70) # Year, Month, Day, Hour (13=1PM), Minute, Second, Weekday (Tuesday=1), Yearday (approx)

    try:
        rtc = machine.RTC() # Get the RTC instance
        rtc.datetime(current_time_tuple) # Set RTC datetime
        print("Time set manually to:", "{:02d}:{:02d}:{:02d}".format(current_time_tuple[3], current_time_tuple[4], current_time_tuple[5]))
    except Exception as e:
        print(f"Error setting time manually: {e}")
        print("Check if 'machine.RTC' is the correct method for your device and RTC is enabled.")



def update_time():
    current_time= time.localtime() # Get current time from the device's RTC
    time_str = "{:02d}:{:02d}:{:02d}".format(current_time[3], current_time[4], current_time[5]) # Format HH:MM:SS
    print(f"update_time: time_str = {time_str}")
    time_label.set_text(time_str)
    # lv.obj_invalidate(lv.scr_act()) # Force screen redraw - try adding this
    print("update_time: text set")


def main():
    os.exitpoint(os.EXITPOINT_ENABLE)
    try:
        display_init()
        lvgl_init()
        user_gui_init()
        set_time_manually() # Set time manually at startup

        while True:
            update_time()
            time.sleep_ms(lv.task_handler())

    except BaseException as e:
        import sys
        sys.print_exception(e)

    lvgl_deinit()
    display_deinit()
    gc.collect()


#if __name__ == "main":
#    main()
main()
