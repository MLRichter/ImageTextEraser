import numpy as np
import cv2

from typing import List

from imagetexteraser.domain import BoundingBox


def blackfill(orig: np.ndarray, resized: np.ndarray, boxes: List[BoundingBox]) -> np.ndarray:
    # loop over the bounding boxes
    (H, W) = orig.shape[:2]
    (width, height) = resized.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 0, 0), -1)
    return orig


def bbox(orig: np.ndarray, resized: np.ndarray, boxes: List[BoundingBox]) -> np.ndarray:
    # loop over the bounding boxes
    (H, W) = orig.shape[:2]
    (width, height) = resized.shape[:2]

    # set the new width and height and then determine the ratio in change
    # for both the width and height
    (newW, newH) = (width, height)
    rW = W / float(newW)
    rH = H / float(newH)

    for (startX, startY, endX, endY) in boxes:
        # scale the bounding box coordinates based on the respective
        # ratios
        startX = int(startX * rW)
        startY = int(startY * rH)
        endX = int(endX * rW)
        endY = int(endY * rH)

        # draw the bounding box on the image
        cv2.rectangle(orig, (startX, startY), (endX, endY), (0, 255, 0), 2)
    return orig