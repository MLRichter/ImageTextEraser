from imutils.object_detection import non_max_suppression
import numpy as np
import argparse
import time
import cv2
from pathlib import Path

from imagetexteraser.domain import Model, InferenceFunction, BoundingBox, Confidence, ModFunc
from imagetexteraser.model_factories import east_model
from typing import Callable, Tuple, List, Optional

from imagetexteraser.modification import blackfill
from imagetexteraser.utils import save_image_to_folder


def blob_from_image(image: np.ndarray,
                    height: int,
                    width: int,
                    color_means: Tuple[float, float, float] = (123.68, 116.78, 103.94),
                    swapRB: bool = True,
                    crop: bool = False,
                    ) -> bytes:
    blob = cv2.dnn.blobFromImage(
        image, 1.0, (width, height), color_means, swapRB=swapRB, crop=crop)
    return blob


def process_image(conduct_inference: InferenceFunction,
                  net: Model,
                  src_path: Path,
                  height: int = 320,
                  width: int = 320,
                  min_conf: float = 0.5,
                  modify_func: ModFunc = blackfill
                  ) -> Optional[Tuple[List[BoundingBox], List[Confidence]]]:
    # load the input image and grab the image dimensions
    image = cv2.imread(str(src_path))
    if image is None:
        return image
    orig = image.copy()

    # resize the image and grab the new image dimensions
    image = cv2.resize(image, (width, height))
    (H, W) = image.shape[:2]
    rects, confidences = conduct_inference(net, image, H, W, min_conf)

    # apply non-maxima suppression to suppress weak, overlapping bounding
    # boxes
    boxes = non_max_suppression(np.array(rects), probs=confidences)
    modified_img = modify_func(orig, image, boxes)
    return modified_img


if __name__ == '__main__':
    from imagetexteraser.model_factories import east_model
    from imagetexteraser.modification import bbox
    src_path: Path = Path("../test_images/im1.png")
    tgt_path: Path = Path("result")
    net, inference = east_model("../frozen_east_text_detection.pb")
    img = process_image(conduct_inference=inference, net=net, src_path=src_path, modify_func=bbox)
    # show the output image
    save_image_to_folder(img, src_path=src_path, tgt_folder=tgt_path)
    cv2.imshow("Text Detection", img)
    cv2.waitKey(0)