import os

import cv2

from cadivi_analysis.common.config_util import ConfigUtil
from cadivi_analysis.common import config_const as ConfigConst
from cadivi_analysis.utils.image_utils import write_frame
from cadivi_analysis.error_detector.error_detector import ErrorDetector


def main():
    config_util = ConfigUtil()
    error_detector = ErrorDetector()

    input_image_path = config_util.get_property(
        section=ConfigConst.YOLOV8, key=ConfigConst.IMAGE_DEMO
    )
    output_image_path = config_util.get_property(
        section=ConfigConst.YOLOV8, key=ConfigConst.OUTPUT_IMAGE_PATH
    )
    bentoml_url = config_util.get_property(
        section=ConfigConst.YOLOV8, key=ConfigConst.BENTOML_URL
    )
    # conf_minimum = config_util.get_float(
    #     section=ConfigConst.YOLOV8,
    #     key=ConfigConst.CONF_MINIMUM,
    #     default_val=ConfigConst.DEFAULT_CONF,
    # )

    # Read Image
    images = []
    image = cv2.imread(input_image_path)
    images.append(image)

    # Save Image
    image_paths = []
    os.makedirs(output_image_path, exist_ok=True)
    write_frame(image, f"{output_image_path}/output_image.png")
    image_paths.append(f"{output_image_path}/output_image.png")

    # Call bentoml yolo
    try:
        data = error_detector.request_yolo_bentoml(image_paths, bentoml_url)
        print(data)
    except Exception as e:
        print(e)

    # Draw Output
    output_images = error_detector.draw_bboxes(images, data)
    for img in output_images:
        write_frame(img, f"{output_image_path}/output_image.png")
