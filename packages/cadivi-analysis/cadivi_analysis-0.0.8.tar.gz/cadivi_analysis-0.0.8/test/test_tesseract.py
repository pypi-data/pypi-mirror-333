import os

import cv2

from cadivi_analysis.common.config_util import ConfigUtil
from cadivi_analysis.common import config_const as ConfigConst
from cadivi_analysis.utils.image_utils import write_frame, request_bentoml
from cadivi_analysis.word_detector.word_detector import WordDetector


def test_tesseract():
    config_util = ConfigUtil()
    input_image_path = config_util.get_property(
        section=ConfigConst.TESSERACT, key=ConfigConst.IMAGE_DEMO
    )
    bentoml_url = config_util.get_property(
        section=ConfigConst.TESSERACT, key=ConfigConst.BENTOML_URL
    )
    conf_minimum = config_util.get_float(
        section=ConfigConst.TESSERACT,
        key=ConfigConst.CONF_MINIMUM,
        default_val=ConfigConst.DEFAULT_CONF,
    )

    # Read Image
    image = cv2.imread(input_image_path)

    # Processing image to get words
    word_detector = WordDetector(image)
    gray = word_detector.get_grayscale()
    blackhat = word_detector.get_morphological(gray, operation=cv2.MORPH_TOPHAT)
    light = word_detector.get_light(
        blackhat, thresh=140, operation=cv2.MORPH_GRADIENT
    )
    cnts, result = word_detector.get_contours(image, light, keep=2)
    result_images, rois, _ = word_detector.locate_cadivi_text(
        gray, cnts, True, operation=cv2.MORPH_TOPHAT
    )

    # Save Image
    output_image_path = config_util.get_property(
        section=ConfigConst.TESSERACT, key=ConfigConst.OUTPUT_IMAGE_PATH
    )
    os.makedirs(output_image_path, exist_ok=True)

    images = []
    for i, roi in enumerate(result_images):
        write_frame(roi, f"{output_image_path}/output_image_{i}.png")
        images.append(f"{output_image_path}/output_image_{i}.png")

    # Word Detector by BentoML
    try:
        filtered_data = request_bentoml(
            "trba", images, bentoml_url, conf_minimum
        )
        print(filtered_data)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    test_tesseract()
