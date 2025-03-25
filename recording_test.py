# Save MP4 file example
#
# Note: You will need an SD card to run this example.
#
# You can capture audio and video and save them as MP4. The current version only supports MP4 format, video supports 264/265, and audio supports g711a/g711u.

from media.mp4format import *
import os

def mp4_muxer_test():
    print("mp4_muxer_test start")
    width = 800
    height = 480
    # Instantiate mp4 container
    mp4_muxer = Mp4Container()
    mp4_cfg = Mp4CfgStr(mp4_muxer.MP4_CONFIG_TYPE_MUXER)
    if mp4_cfg.type == mp4_muxer.MP4_CONFIG_TYPE_MUXER:
#        file_name = "/sdcard/examples/test.mp4"
        current_time = time.localtime()
        file_name = "/data/{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}.mp4".format(
            current_time[0], current_time[1], current_time[2],
            current_time[3], current_time[4], current_time[5]
        )
        mp4_cfg.SetMuxerCfg(file_name, mp4_muxer.MP4_CODEC_ID_H265, width, height, mp4_muxer.MP4_CODEC_ID_G711U)
    # Create mp4 muxer
    mp4_muxer.Create(mp4_cfg)
    # Start mp4 muxer
    mp4_muxer.Start()

    frame_count = 0
    try:
        while True:
            os.exitpoint()
            # Process audio and video data, write to file in MP4 format
            mp4_muxer.Process()
            frame_count += 1
            print("frame_count = ", frame_count)
            if frame_count >= 2000:
                break
    except BaseException as e:
        print(e)
    # Stop mp4 muxer
    mp4_muxer.Stop()
    # Destroy mp4 muxer
    mp4_muxer.Destroy()
    print("mp4_muxer_test stop")

if __name__ == "__main__":
    os.exitpoint(os.EXITPOINT_ENABLE)
    mp4_muxer_test()
