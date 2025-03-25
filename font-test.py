def check_font_file(path):
    try:
        with open(path, 'rb') as f:
            header = f.read(4)
            print("Font header bytes:", header)

            # LVGL binary fonts should start with 0x28 0x42 0x30 0xAE
            if header == b'(\xB0\xAE':
                print("Valid LVGL v8.x font header")
            else:
                print("Invalid header - Likely wrong format")
    except Exception as e:
        print("File read error:", e)

check_font_file("/sdcard/examples/15-LVGL/data/font/times.bin")
