from pathlib import Path

import cv2
from MTCNN import MTCNN
import numpy as np

from imagetexteraser.domain import Model, InferenceFunction, Confidence, BoundingBox
from imagetexteraser.utils import blob_from_image
from typing import List, Tuple


def _east_inference(net: Model, image: np.ndarray, height: int, width: int, min_confidence: float,
                      layer_names: List[str] = ("feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3")
                      ) -> Tuple[List[BoundingBox], List[Confidence]]:
    blob = blob_from_image(image, height, width)
    net.setInput(blob)
    (scores, geometry) = net.forward(list(layer_names))
    # grab the number of rows and columns from the scores volume, then
    # initialize our set of bounding box rectangles and corresponding
    # confidence scores
    (numRows, numCols) = scores.shape[2:4]
    rects = []
    confidences = []

    # loop over the number of rows
    for y in range(0, numRows):
        # extract the scores (probabilities), followed by the geometrical
        # data used to derive potential bounding box coordinates that
        # surround text
        scoresData = scores[0, 0, y]
        xData0 = geometry[0, 0, y]
        xData1 = geometry[0, 1, y]
        xData2 = geometry[0, 2, y]
        xData3 = geometry[0, 3, y]
        anglesData = geometry[0, 4, y]

        # loop over the number of columns
        for x in range(0, numCols):
            # if our score does not have sufficient probability, ignore it
            if scoresData[x] < min_confidence:
                continue

            # compute the offset factor as our resulting feature maps will
            # be 4x smaller than the input image
            (offsetX, offsetY) = (x * 4.0, y * 4.0)

            # extract the rotation angle for the prediction and then
            # compute the sin and cosine
            angle = anglesData[x]
            cos = np.cos(angle)
            sin = np.sin(angle)

            # use the geometry volume to derive the width and height of
            # the bounding box
            h = xData0[x] + xData2[x]
            w = xData1[x] + xData3[x]

            # compute both the starting and ending (x, y)-coordinates for
            # the text prediction bounding box
            endX = int(offsetX + (cos * xData1[x]) + (sin * xData2[x]))
            endY = int(offsetY - (sin * xData1[x]) + (cos * xData2[x]))
            startX = int(endX - w)
            startY = int(endY - h)

            # add the bounding box coordinates and probability score to
            # our respective lists
            rects.append((startX, startY, endX, endY))
            confidences.append(scoresData[x])

    return rects, confidences


def east_model(model_path: Path) -> Tuple[Model, InferenceFunction]:
    net = cv2.dnn.readNet(str(model_path))
    return net, _east_inference


def _mtcnn_inference(net: Model, image: np.ndarray, height: int, width: int, min_confidence: float,
                      layer_names: List[str] = ("feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3")
                      ) -> Tuple[List[BoundingBox], List[Confidence]]:
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    result = net.detect_faces(image)

    bounding_boxes = []
    confidences = []
    for prediction in result:
        bounding_box = result[0]["box"]
        processed_box = (bounding_box[0],
                         bounding_box[1],
                         bounding_box[0] + bounding_box[2],
                         bounding_box[1] + bounding_box[3])
        bounding_boxes.append(processed_box)
        confidences.append(prediction["confidence"])
    return bounding_boxes, confidences


def mtcnn_model(*args, **kwargs) -> Tuple[Model, InferenceFunction]:
    net = MTCNN()
    return net, _mtcnn_inference


def _mtcnn_composite_inference(net: Model, image: np.ndarray,
                               height: int, width: int, min_confidence: float,
                               layer_names: List[str] = ("feature_fusion/Conv_7/Sigmoid", "feature_fusion/concat_3"),
                               face_recognition: bool = True, text_recognition: bool = True
                      ) -> Tuple[List[BoundingBox], List[Confidence]]:
    use_mtcnn = face_recognition
    use_east = text_recognition
    if use_mtcnn:
        faces, face_confs = _mtcnn_inference(net=net[1], image=image, height=height, width=width,
                                             min_confidence=min_confidence, layer_names=layer_names)
    else:
        faces, face_confs = [], []
    if use_east:
        text, text_confs = _east_inference(net=net[0], image=image, height=height, width=width,
                                           min_confidence=min_confidence, layer_names=layer_names)
    else:
        text, text_confs = [], []
    return faces + text, face_confs + text_confs


def composit_model(*args, **kwargs) -> Tuple[Model, InferenceFunction]:
    mtcnn, mtcnn_inf = mtcnn_model(*args, **kwargs)
    east, east_inf = east_model(*args, **kwargs)
    return (east, mtcnn), _mtcnn_composite_inference
