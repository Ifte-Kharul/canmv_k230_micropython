from mpp.mp4_format import *
from mpp.mp4_format_struct import *
from media.vencoder import *
from media.sensor import *
from media.media import *
import uctypes
import time
import os
class Record:
    def __init__(file_name, fmp4_flag):
        mp4_cfg = k_mp4_config_s()
        mp4_cfg.config_type = K_MP4_CONFIG_MUXER
        mp4_cfg.muxer_config.file_name[:] = bytes(file_name, 'utf-8')
        mp4_cfg.muxer_config.fmp4_flag = fmp4_flag

        handle = k_u64_ptr()
        ret = kd_mp4_create(handle, mp4_cfg)
        if ret:
            raise OSError("kd_mp4_create failed.")
        return handle.value

    def mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type):
        video_track_info = k_mp4_track_info_s()
        video_track_info.track_type = K_MP4_STREAM_VIDEO
        video_track_info.time_scale = 1000
        video_track_info.video_info.width = width
        video_track_info.video_info.height = height
        video_track_info.video_info.codec_id = video_payload_type
        video_track_handle = k_u64_ptr()
        ret = kd_mp4_create_track(mp4_handle, video_track_handle, video_track_info)
        if ret:
            raise OSError("kd_mp4_create_track failed.")
        return video_track_handle.value

    #def mp4_muxer_create_audio_track(mp4_handle, channel, sample_rate, bit_per_sample, audio_payload_type):
    #    audio_track_info = k_mp4_track_info_s()
    #    audio_track_info.track_type = K_MP4_STREAM_AUDIO
    #    audio_track_info.time_scale = 1000
    #    audio_track_info.audio_info.channels = channel
    #    audio_track_info.audio_info.codec_id = audio_payload_type
    #    audio_track_info.audio_info.sample_rate = sample_rate
    #    audio_track_info.audio_info.bit_per_sample = bit_per_sample
    #    audio_track_handle = k_u64_ptr()
    #    ret = kd_mp4_create_track(mp4_handle, audio_track_handle, audio_track_info)
    #    if ret:
    #        raise OSError("kd_mp4_create_track failed.")
    #    return audio_track_handle.value


    def start_recording(duration=30, width=1280, height=720, venc_payload_type=K_PT_H264, custom_name=None, sensor=None):
        if custom_name:
            file_name = f"/sdcard/examples/{custom_name}.mp4"
        else:
            current_time = time.localtime()
            file_name = "/data/examples/{:04d}-{:02d}-{:02d}_{:02d}-{:02d}-{:02d}.mp4".format(
                current_time[0], current_time[1], current_time[2],
                current_time[3], current_time[4], current_time[5]
            )
        print(f"Saving stream to file: {file_name}")

        venc_chn = VENC_CHN_ID_0
        width = ALIGN_UP(width, 16)

        frame_data = k_mp4_frame_data_s()
        save_idr = bytearray(width * height * 3 // 4)
        idr_index = 0

        # mp4 muxer init
        mp4_handle = mp4_muxer_init(file_name, True)

        # create video track
        if venc_payload_type == K_PT_H264:
            video_payload_type = K_MP4_CODEC_ID_H264
        elif venc_payload_type == K_PT_H265:
            video_payload_type = K_MP4_CODEC_ID_H265
        mp4_video_track_handle = mp4_muxer_create_video_track(mp4_handle, width, height, video_payload_type)

        # Use existing sensor if provided
        if sensor is None:
            sensor = Sensor()
            sensor.reset()
            sensor.set_framesize(width=width, height=height, alignment=12)
            sensor.set_pixformat(Sensor.YUV420SP)
            start_sensor = True
        else:
            start_sensor = False

        # Instantiate video encoder
        encoder = Encoder()
        encoder.SetOutBufs(venc_chn, 8, width, height)

        # Bind camera and venc
        link = MediaManager.link(sensor.bind_info()['src'], (VIDEO_ENCODE_MOD_ID, VENC_DEV_ID, venc_chn))

        # Configure and initialize MediaManager
    #    MediaManager._config()  # Add this line
    #    MediaManager.init()

        if venc_payload_type == K_PT_H264:
            chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H264, encoder.H264_PROFILE_MAIN, width, height)
        elif venc_payload_type == K_PT_H265:
            chnAttr = ChnAttrStr(encoder.PAYLOAD_TYPE_H265, encoder.H265_PROFILE_MAIN, width, height)

        streamData = StreamData()

        # Create encoder
        encoder.Create(venc_chn, chnAttr)

        # Start encoding
        encoder.Start(venc_chn)
        # Start camera if it was initialized here
        if start_sensor:
            sensor.run()

        video_start_timestamp = 0
        get_first_I_frame = False
        start_time = time.time()

        try:
            while True:
                os.exitpoint()
                encoder.GetStream(venc_chn, streamData)
                stream_type = streamData.stream_type[0]

                if not get_first_I_frame:
                    if stream_type == encoder.STREAM_TYPE_I:
                        get_first_I_frame = True
                        video_start_timestamp = streamData.pts[0]
                        save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                        idr_index += streamData.data_size[0]

                        frame_data.codec_id = video_payload_type
                        frame_data.data = uctypes.addressof(save_idr)
                        frame_data.data_length = idr_index
                        frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

                        ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                        if ret:
                            raise OSError("kd_mp4_write_frame failed.")
                        encoder.ReleaseStream(venc_chn, streamData)
                        continue

                    elif stream_type == encoder.STREAM_TYPE_HEADER:
                        save_idr[idr_index:idr_index+streamData.data_size[0]] = uctypes.bytearray_at(streamData.data[0], streamData.data_size[0])
                        idr_index += streamData.data_size[0]
                        encoder.ReleaseStream(venc_chn, streamData)
                        continue
                    else:
                        encoder.ReleaseStream(venc_chn, streamData)
                        continue

                # Write video frame
                frame_data.codec_id = video_payload_type
                frame_data.data = streamData.data[0]
                frame_data.data_length = streamData.data_size[0]
                frame_data.time_stamp = streamData.pts[0] - video_start_timestamp

                print(f"Video size: {streamData.data_size[0]}, Type: {stream_type}, Timestamp: {frame_data.time_stamp}")
                ret = kd_mp4_write_frame(mp4_handle, mp4_video_track_handle, frame_data)
                if ret:
                    raise OSError("kd_mp4_write_frame failed.")

                encoder.ReleaseStream(venc_chn, streamData)

                # Check duration
                if time.time() - start_time >= duration:
                    break

        except KeyboardInterrupt as e:
            print("User stopped recording:", e)
        except Exception as e:
            import sys
            sys.print_exception(e)
        finally:
            # Cleanup
            if start_sensor:
                sensor.stop()
            del link
            encoder.Stop(venc_chn)
            encoder.Destroy(venc_chn)
            MediaManager.deinit()
            kd_mp4_destroy_tracks(mp4_handle)
            kd_mp4_destroy(mp4_handle)
            print("Recording stopped")

#if __name__ == "__main__":
#    os.exitpoint(os.EXITPOINT_ENABLE)
#    start_recording()  # Starts 30-second recording with auto-generated filename
