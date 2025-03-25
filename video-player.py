# Play MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can load local files to play. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.player import *  # Import player module for playing mp4 files
from media.display import *
import os
import time

start_play = False  # Playback end flag

def player_event(event, data):
    global start_play
    if event == K_PLAYER_EVENT_EOF:  # Playback end marker
        start_play = False  # Set playback end marker

def play_mp4_test(filename):
    global start_play
    # player = Player()  # Create player object
    # Use IDE as output display, can set any resolution
    # player = Player(Display.VIRT)
    # Use ST7701 LCD screen as output display, max resolution 800*480
    player = Player(Display.ST7701, fps=30) # Explicitly set resolution, matching DISPLAY_WIDTH and DISPLAY_HEIGHT
    # Use HDMI as output display
    # player = Player(Display.LT9611)
    player.load(filename)  # Load mp4 file
    player.set_event_callback(player_event)  # Set player event callback
    player.start()  # Start playback
    start_play = True

    # Wait for playback to end
    try:
        while start_play:
            time.sleep(0.1)
            os.exitpoint()
    except KeyboardInterrupt as e:
        print("user stop: ", e)
    except BaseException as e:
        import sys
        sys.print_exception(e)

    player.stop()  # Stop playback
    print("play over")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    play_mp4_test("/sdcard/examples/test.mp4")  # Play mp4 file
