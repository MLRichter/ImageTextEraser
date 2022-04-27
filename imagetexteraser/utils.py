from pathlib import Path

import numpy as np
from typing import Tuple
import cv2


def blob_from_image(image: np.ndarray,
                    height: int,
                    width: int,
                    color_means: Tuple[float, float, float] = (123.68, 116.78, 103.94),
                    swapRB: bool = True,
                    crop: bool = False,
                    ) -> np.ndarray:
    blob = cv2.dnn.blobFromImage(
        image, 1.0, (width, height), color_means, swapRB=swapRB, crop=crop)
    return blob


def save_image_to_folder(img: np.ndarray, src_path: Path, tgt_folder: Path) -> None:
    tgt_folder.mkdir(exist_ok=True)
    cv2.imwrite(str(tgt_folder / src_path.name), img)