import cv2
import imutils
import numpy as np
from skimage.segmentation import clear_border


class WordDetector:
    def __init__(self, image) -> None:
        self.image = image

    def get_grayscale(self):
        return cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

    def get_morphological(self, image, operation=cv2.MORPH_BLACKHAT):
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (242, 10))
        black_hat = cv2.morphologyEx(image, operation, rect_kern)
        return black_hat

    def get_light(
        self,
        image,
        thresh: int = 0,
        operation=cv2.MORPH_CLOSE,
    ):
        square_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (thresh, 1))
        light = cv2.morphologyEx(image, operation, square_kern)
        light = cv2.threshold(
            light, 0, 200, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )[1]
        return light

    def get_grad(self, image):
        gradX = cv2.Sobel(image, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
        gradX = np.absolute(gradX)
        (minVal, maxVal) = (np.min(gradX), np.max(gradX))
        gradX = 255 * ((gradX - minVal) / (maxVal - minVal))
        gradX = gradX.astype("uint8")
        return gradX

    def get_thresh(self, image):
        rect_kern = cv2.getStructuringElement(cv2.MORPH_RECT, (35, 20))
        gradX = cv2.GaussianBlur(image, (1, 1), 0)
        gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rect_kern)
        thresh = cv2.threshold(
            gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU
        )[1]
        return thresh

    def get_ero_dil(self, image):
        thresh = cv2.erode(image, None, iterations=2)
        thresh = cv2.dilate(thresh, None, iterations=2)
        return thresh

    def get_final(self, image, light):
        thresh = cv2.bitwise_and(image, image, mask=light)
        thresh = cv2.dilate(thresh, None, iterations=2)
        thresh = cv2.erode(thresh, None, iterations=1)
        return thresh

    def get_contours(self, raw, image, keep=5):
        cnts = cv2.findContours(
            image.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)[:keep]
        result = cv2.drawContours(np.copy(raw), cnts, -1, (0, 255, 0), 3)
        return cnts, result

    def locate_cadivi_text(
        self, gray, candidates, clearBorder=False, operation=cv2.MORPH_TOPHAT
    ):
        image_cnt = None
        rois = []
        result_images = []

        for c in candidates:
            (x, y, w, h) = cv2.boundingRect(c)
            ar = w / float(h)
            if ar <= 10:
                image_cnt = c
                result_image = gray[y : y + h, x : x + w]
                roi = self.get_morphological(result_image, operation)

                if clearBorder:
                    roi = clear_border(roi)
                rois.append(roi)
                result_images.append(result_image)
        return result_images, rois, image_cnt
