import json
from typing import List, Any, Dict

import cv2
import requests


class ErrorDetector:
    def request_yolo_bentoml(
        self, images: List[str], bentoml_url: str
    ) -> List[Dict[Any, Any]]:
        files = [
            (
                "images",
                ("file", open(f"{image}", "rb"), "application/octet-stream"),
            )
            for image in images
        ]

        headers = {"accept": "application/json"}

        response = requests.request(
            "POST", bentoml_url, headers=headers, files=files
        )

        if response.status_code != 200:
            raise Exception(f"Failed {response.status_code}: {response.text}")

        data = json.loads(response.text)
        return data

    def draw_bboxes(self, images, error_detections):
        output_images = []
        for image, error_list in zip(images, error_detections):
            for error_dict in error_list:
                # Draw Bounding Boxes
                x1, y1, x2, y2 = (
                    error_dict["box"]["x1"],
                    error_dict["box"]["y1"],
                    error_dict["box"]["x2"],
                    error_dict["box"]["y2"],
                )
                cv2.putText(
                    image,
                    f"{error_dict['name']} {error_dict['confidence']:.2f}",
                    (int(x1), int(y1) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 0, 255),
                    2,
                )
                cv2.rectangle(
                    image,
                    (int(x1), int(y1)),
                    (int(x2), int(y2)),
                    (0, 0, 255),
                    2,
                )
            output_images.append(image)
        return output_images
