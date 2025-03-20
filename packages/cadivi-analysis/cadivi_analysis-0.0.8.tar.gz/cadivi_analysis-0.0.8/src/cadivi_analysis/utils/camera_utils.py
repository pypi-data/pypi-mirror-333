import os
import threading
import time

# import cv2
import numpy as np
import pypylon.pylon as py

from cadivi_analysis.settings import logging, camera_producer

from cadivi_analysis.utils.image_utils import write_frame
from cadivi_analysis.common.config_util import ConfigUtil
from cadivi_analysis.common import config_const as ConfigConst

SCANLINE_WIDTH = 1000
VIRTUAL_FRAME_WIDTH = 1000


class CameraUtils:
    def __init__(self, device, offset_x, offset_y, exporsure_time):
        self.cam = py.InstantCamera(
            py.TlFactory.GetInstance().CreateDevice(device)
        )

        self.offset_x = offset_x
        self.offset_y = offset_y
        self.exporsure_time = exporsure_time
        self.config_camera()
        self.name = self.cam.GetDeviceInfo().GetSerialNumber()

        config_util = ConfigUtil()
        output_image_path = config_util.get_property(
            section=ConfigConst.CAMERA, key=ConfigConst.CAMERA_DATA_PATH
        )
        self.output_image_path = output_image_path + f"/camera-{self.name}"

        os.makedirs(self.output_image_path, exist_ok=True)

    def delete_output_image_path(self):
        for item in os.listdir(self.output_image_path):
            if item.endswith(".png"):
                os.remove(os.path.join(self.output_image_path, item))

    def config_camera(self):
        self.cam.Open()

        self.cam.Width.SetValue(SCANLINE_WIDTH)
        self.cam.Height.SetValue(1000)
        self.cam.OffsetX.SetValue(self.offset_x)
        self.cam.OffsetY.SetValue(self.offset_y)

        self.cam.PixelFormat = "BGR8"
        self.cam.ExposureTime.SetValue(self.exporsure_time)
        self.cam.Gain.SetValue(0)

        # Frame Rate
        self.cam.BandwidthReserveMode.SetValue("Performance")

        logging.info(
            f"Resulting framerate: {self.cam.ResultingFrameRate.Value}"
        )

    def grab_frame(
        self,
        save: bool = False,
        is_count_100: bool = False,
        time_delay: float = 3.0,
    ) -> None:
        # Set camera to continuous acquisition mode
        self.cam.AcquisitionMode.SetValue("Continuous")
        self.cam.StartGrabbing(py.GrabStrategy_LatestImageOnly)

        img = np.ones(
            (self.cam.Height.Value, VIRTUAL_FRAME_WIDTH, 3), dtype=np.uint8
        )
        missing_column = (
            np.ones((self.cam.Height.Value, SCANLINE_WIDTH, 3), dtype=np.uint8)
            * 255
        )
        image_idx = 0
        while self.cam.IsGrabbing():
            if image_idx == 100 and is_count_100:
                image_idx = 0

            for idx in range(VIRTUAL_FRAME_WIDTH // SCANLINE_WIDTH):
                with self.cam.RetrieveResult(
                    2000, py.TimeoutHandling_ThrowException
                ) as result:
                    try:
                        if result.GrabSucceeded():
                            out_array = result.GetArray()
                            img[
                                :,
                                idx * SCANLINE_WIDTH : idx * SCANLINE_WIDTH
                                + SCANLINE_WIDTH,
                            ] = out_array
                        else:
                            img[
                                :,
                                idx * SCANLINE_WIDTH : idx * SCANLINE_WIDTH
                                + SCANLINE_WIDTH,
                            ] = missing_column
                            logging.info(f"Missing column at index {idx}")
                        time.sleep(time_delay)
                    except py.RuntimeException as e:
                        logging.error(e)
                        result.Release()

            # Save the resulting frame as an image
            if save:
                write_frame(
                    img,
                    f"{self.output_image_path}/{image_idx}.png",
                )

            # logging.info(f"{self.name")
            camera_producer.send(
                f"camera-{self.name}",
                f"{self.output_image_path}/{image_idx}.png",
            )

            camera_producer.send(
                f"camera-{self.name}-yolo",
                f"{self.output_image_path}/{image_idx}.png",
            )

            # Kafka
            # frame = encode_frame_base64(img)
            # camera_producer.send(
            #     f"camera-{self.name}", frame
            # )

            image_idx += 1

    def start_grabbing(
        self,
        save: bool = False,
        is_count_100: bool = False,
        time_delay: float = 1.0,
    ) -> None:
        self.thread = threading.Thread(
            target=self.grab_frame, args=(save, is_count_100, time_delay)
        )
        # self.thread = threading.Thread(target=self.grab_frame)
        self.thread.start()

    def stop_grabbing(self):
        self.cam.StopGrabbing()
        self.cam.Close()
        self.thread.join()
