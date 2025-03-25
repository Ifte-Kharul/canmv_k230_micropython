import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
networks = wlan.scan()


print("Scanning manually:")


for net in networks:
    ssid = net.ssid  # Access the SSID using attribute notation
    print(f"SSID is {ssid}")

