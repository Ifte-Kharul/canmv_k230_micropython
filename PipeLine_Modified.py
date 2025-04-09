import os
import ujson
from media.sensor import *
from media.display import *
from media.media import *
from libs.Utils import ScopedTiming
import nncase_runtime as nn
import ulab.numpy as np
import image
import gc
import sys
import time

class PipeLine:
    def __init__(
        self,
        rgb888p_size=[224, 224],
        display_mode="hdmi",
        display_size=None,
        osd_layer_num=1,
        debug_mode=0,
        num_cameras=1,  # Default: 1 camera, set to 3 for 3 cameras
    ):
        self.rgb888p_size = [ALIGN_UP(rgb888p_size[0], 16), rgb888p_size[1]]
        self.display_size = display_size if display_size else None
        self.display_mode = display_mode
        self.sensors = []  # List to hold multiple sensors
        self.osd_img = None
        self.cur_frame = None
        self.debug_mode = debug_mode
        self.osd_layer_num = osd_layer_num
        self.num_cameras = num_cameras  # Number of cameras (1, 2, or 3)

    def create(self, fps=30, hmirror=None, vflip=None):
        with ScopedTiming("init PipeLine", self.debug_mode > 0):
            nn.shrink_memory_pool()
            
            # Initialize Display
            Display.init(Display.LT9611, osd_num=self.num_cameras, to_ide=True)  # osd_num = num_cameras
            self.display_size = [Display.width(), Display.height()]
            camera_width = int(self.display_size[0] / self.num_cameras)  # Avoid rounding issues

            # Initialize OSD
            self.osd_img = image.Image(self.display_size[0], self.display_size[1], image.ARGB8888)
            
            for i in range(self.num_cameras):
                sensor = Sensor(id=i, fps=fps)
                sensor.reset()
                if hmirror is not None:
                    sensor.set_hmirror(hmirror)
                if vflip is not None:
                    sensor.set_vflip(vflip)

                # Configure display channel (YUV420)
                sensor.set_framesize(w=camera_width, h=self.display_size[1])
                sensor.set_pixformat(PIXEL_FORMAT_YUV_SEMIPLANAR_420)
                
                # Bind video layer
                bind_info = sensor.bind_info(x=i * camera_width, y=0, chn=CAM_CHN_ID_0)
                if Display.LAYER_VIDEO1 + i > Display.LAYER_VIDEO3:  # Safety check
                    raise ValueError(f"Too many cameras for available layers")
                Display.bind_layer(**bind_info, layer=Display.LAYER_VIDEO1 + i)

                # Configure AI channel (RGB888)
                ai_chn = CAM_CHN_ID_2 + i  # Unique channel per camera
                sensor.set_framesize(w=self.rgb888p_size[0], h=self.rgb888p_size[1], chn=ai_chn)
                sensor.set_pixformat(PIXEL_FORMAT_RGB_888_PLANAR, chn=ai_chn)

                self.sensors.append(sensor)  # ✅ Sensor added to list here

        MediaManager.init()
        for sensor in self.sensors:
            sensor.run()
   
   
    def get_frame(self, camera_id=0, chn=CAM_CHN_ID_2):
        """Get a frame from a specific camera and channel."""
        with ScopedTiming("get a frame", self.debug_mode > 0):
            if camera_id >= len(self.sensors):
                return None
            try:
                # Use camera-specific AI channel
                ai_chn = CAM_CHN_ID_2 + camera_id
                self.cur_frame = self.sensors[camera_id].snapshot(chn=ai_chn)
                return self.cur_frame.to_numpy_ref()
            except Exception as e:
                print(f"Error getting frame from camera {camera_id}: {e}")
                return None

    def show_image(self):
        """Display OSD overlay."""
        with ScopedTiming("show result", self.debug_mode > 0):
            Display.show_image(self.osd_img, 0, 0, Display.LAYER_OSD3)

    def get_display_size(self):
        return self.display_size

    def destroy(self):
        """Cleanup sensors and display."""
        with ScopedTiming("deinit PipeLine", self.debug_mode > 0):
            os.exitpoint(os.EXITPOINT_ENABLE_SLEEP)
            for sensor in self.sensors:
                sensor.stop()
            Display.deinit()
            time.sleep_ms(50)
            MediaManager.deinit()