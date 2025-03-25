
#import network
#import time
#from machine import Pin
#import lvgl as lv

#def scan_networks():
#    wlan = network.WLAN(network.STA_IF)
#    wlan.active(True)
#    return "none"

#def connect_to_wifi(ssid, password):
#    wlan = network.WLAN(network.STA_IF)
#    wlan.active(True)
#    wlan.connect(ssid, password)
#    time.sleep(10)
#    return wlan.isconnected(), wlan.ifconfig()

#def create_ui():
#    lv.init()
#    scr = lv.scr_act()

#    label = lv.label(scr)
#    label.set_text("Available Networks:")
#    label.set_pos(10, 10)

#    list1 = lv.list(scr)
#    list1.set_size(200, 200)
#    list1.set_pos(10, 40)

#    networks = scan_networks()
#    for net in networks:
#        ssid = net[0].decode()
#        btn = list1.add_btn(None, ssid)
#        btn.set_event_cb(lambda e, s=ssid: on_select_network(s))

##    global password_input
##    password_input = lv.textarea(scr)
##    password_input.set_one_line(True)
##    password_input.set_placeholder_text("Enter Password")
##    password_input.set_pos(10, 250)
##    password_input.set_size(200, 30)

##    connect_btn = lv.btn(scr)
##    connect_btn.set_pos(10, 290)
##    lbl = lv.label(connect_btn)
##    lbl.set_text("Connect")
##    connect_btn.set_event_cb(on_connect)

##def on_select_network(ssid):
##    global selected_ssid
##    selected_ssid = ssid

##def on_connect(event):
##    global selected_ssid, password_input
##    if selected_ssid:
##        password = password_input.get_text()
##        success, info = connect_to_wifi(selected_ssid, password)
##        if success:
##            lv.label(lv.scr_act()).set_text(f"Connected! IP: {info[0]}")
##        else:
##            lv.label(lv.scr_act()).set_text("Connection Failed")

#selected_ssid = None
#create_ui()
#while True:
#    print("UI CREATED")
#    time.sleep_ms(lv.task_handler())
