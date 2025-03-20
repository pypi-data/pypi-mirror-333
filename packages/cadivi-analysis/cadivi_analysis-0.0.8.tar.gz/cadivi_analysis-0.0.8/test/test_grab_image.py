import pypylon.pylon as py

from cadivi_analysis.settings import (
    camera99_consumer,
    camera27_consumer,
    camera55_consumer,
    # logging
)
from cadivi_analysis.utils.camera_utils import CameraUtils


def test_grab_image():
    tlf = py.TlFactory.GetInstance()
    devices = tlf.EnumerateDevices()

    camera_99 = CameraUtils(
        devices[0], offset_x=0, offset_y=342, exporsure_time=500
    )
    camera_27 = CameraUtils(
        devices[1], offset_x=0, offset_y=502, exporsure_time=500
    )
    camera_55 = CameraUtils(
        devices[2], offset_x=0, offset_y=292, exporsure_time=500
    )

    # Start Grabbing
    camera_99.start_grabbing(save=True, is_count_100=True)
    camera_27.start_grabbing(save=True)
    camera_55.start_grabbing(save=True)

    count = 0
    while True:
        if count > 150:
            break

        message_99 = camera99_consumer.poll()
        if not len(message_99.items()) == 0:
            for _, records in message_99.items():
                for rec in records:
                    print(rec.value)

        message_27 = camera27_consumer.poll()
        if not len(message_27.items()) == 0:
            for _, records in message_27.items():
                for rec in records:
                    print(rec.value)

        message_55 = camera55_consumer.poll()
        if not len(message_55.items()) == 0:
            count += 1
            for _, records in message_55.items():
                for rec in records:
                    print(rec.value)

    # Stop Grabbing
    camera_99.stop_grabbing()
    camera_27.stop_grabbing()
    camera_55.stop_grabbing()

    camera_99.delete_output_image_path()


def test_tesseract():
    pass


if __name__ == "__main__":
    test_grab_image()
