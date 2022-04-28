from pathlib import Path
from tkinter import Tk
from tkinter.ttk import Progressbar, Label
from typing import Protocol, Tuple, Callable, List
import numpy as np


class Backend(Protocol):

        stop_flag: bool

        def process_image(self, img: Path, tgt_folder: Path, confidence: float):
                ...

        def process_images(self, src_folder: Path, tgt_folder: Path,
                           confidence: float, pb: Progressbar, value_label: Label,
                           labelupdater: Callable, window: Tk):
                ...


class Model(Protocol):
        ...


Confidence = float
BoundingBox = Tuple[int, int, int, int]
InferenceFunction = Callable[[Model, np.ndarray, int, int, float], Tuple[List[BoundingBox], List[Confidence]]]
ModFunc = Callable[[np.ndarray, np.ndarray, List[BoundingBox]], np.ndarray]
