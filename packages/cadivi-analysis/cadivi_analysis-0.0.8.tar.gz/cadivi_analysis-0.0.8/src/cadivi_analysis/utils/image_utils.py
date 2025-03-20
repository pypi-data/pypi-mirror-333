import os
import json
import hashlib
from typing import Tuple, Dict, List, Any

import cv2
import numpy as np
import requests


# Function to decode base64 frame
def decode_base64_frame(encoded_frame):
    np_data = np.frombuffer(encoded_frame, np.uint8)
    return cv2.imdecode(np_data, cv2.IMREAD_COLOR)


# Function to encode frame to base64
def encode_frame_base64(frame):
    _, buffer = cv2.imencode(".jpg", frame)
    return buffer.tobytes()


def write_frame(img, image_file):
    cv2.imwrite(
        f"{image_file}",
        img,
    )


def write_temp_file(obd, mime_type, file_path) -> Tuple[str, str]:
    h = hashlib.sha1()
    h.update(obd)
    os.makedirs(file_path, exist_ok=True)

    if mime_type in ["jpg", "jpeg"]:
        image_name = f"{h.hexdigest()}.jpg"
    elif mime_type == "png":
        image_name = f"{h.hexdigest()}.png"
    else:
        raise ValueError(f"Unsupported mime_type: {mime_type}")

    # file_path = config_util.get_property(
    #     section=ConfigConst.TESSERACT, key=ConfigConst.TMP_PATH
    # )
    file_name = file_path + f"/{image_name}"

    with open(file_name, "wb") as handle:
        handle.write(obd)
    return file_name, image_name


def request_bentoml(
    model_id: str, images: List[str], bentoml_url: str, conf_minimum: float
) -> List[Dict[Any, Any]]:
    payload = {"model_id": model_id}

    files = [
        (
            "images",
            ("file", open(f"{image}", "rb"), "application/octet-stream"),
        )
        for i, image in enumerate(images)
    ]

    headers = {"accept": "application/json"}

    response = requests.request(
        "POST", bentoml_url, headers=headers, data=payload, files=files
    )

    if response.status_code != 200:
        raise Exception(f"Failed {response.status_code}: {response.text}")

    data = json.loads(response.text)

    filtered_data = [
        {
            "label": "".join(
                char
                for char, conf in zip(item["labels"], map(float, item["conf"]))
                if conf > conf_minimum
            ),
            "conf": [
                conf for conf in map(float, item["conf"]) if conf > conf_minimum
            ],
        }
        for item in data
    ]
    return filtered_data
