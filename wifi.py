import network,time,socket
from machine import Pin

def check_internet():
    try:
        addr = socket.getaddrinfo("google.com", 80)[0][-1]
        s = socket.socket()
        s.connect(addr)
        s.send(b"GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")
        response = s.recv(1024)
        s.close()
        print("Received response:", response[:50])  # Print the first 50 bytes
        return True
    except Exception as e:
        print("Internet check failed:", e)
        return False

def Wifi_Connect():
    WIFI_LED = Pin(52,Pin.OUT)
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)

    if not wlan.isconnected():
        print("connecting to network")
        wlan.connect('SOALIB2','bangladesh123')
        return "Connecting"

    if wlan.isconnected():
        WIFI_LED.value(1)
#        print("network Info : ",wlan.ifconfig())
        iplist = wlan.ifconfig()
        print_server_ip("jence.com")
        print(iplist[0])
        return iplist[0]

    else:
        for i in range(5):
            WIFI_LED.value(1)
            time.sleep_ms(300)
            WIFI_LED.value(0)
            time.sleep_ms(300)

        wlan.active(False)
        return "unable to connect"

    return "returnong"



def print_server_ip(hostname):
    """Prints the IP address of a given hostname."""
    try:
        addr_info = socket.getaddrinfo(hostname, 80) #80 is a dummy port, as we only want the IP.
        ip_address = addr_info[0][4][0]  # Extract the IP address
        print(f"IP address of {hostname}: {ip_address}")
        return ip_address
    except OSError as e:
        print(f"Error resolving hostname {hostname}: {e}")
        return "OS Error"
    except IndexError as e:
        print(f"Index Error resolving hostname {hostname}: {e}")
        return "Error resolving hostname"
    except Exception as e:
        print(f"General Error resolving hostname {hostname}: {e}")
        return "General Error"

#check_internet()
print(Wifi_Connect())
print_server_ip("jence.com")

