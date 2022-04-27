import glob
from pathlib import Path
from attr import attrs

from domain import Backend, Model, InferenceFunction, ModFunc
from image_processing import process_image
from imagetexteraser.modification import blackfill
from imagetexteraser.utils import save_image_to_folder
from tkinter.ttk import Progressbar
from tkinter import Tk, Label


@attrs(auto_attribs=True, frozen=True, slots=True)
class SimpleEastBackend(Backend):

    net: Model
    inference: InferenceFunction
    height: int = 320
    width: int = 320
    modifier: ModFunc = blackfill

    def process_image(self, img: Path, tgt_folder: Path, confidence: float):
        r_img = process_image(
            self.inference, self.net, src_path=img,
            height=self.height, width=self.width, min_conf=confidence,
            modify_func=self.modifier)
        save_image_to_folder(r_img, img, tgt_folder)

    def process_images(self, src_folder: Path, tgt_folder: Path, confidence: float, pb: Progressbar, value_label: Label, window: Tk):
        files = [i for i in src_folder.rglob("*") if i.is_file()]
        for i, file in enumerate(files):
            pb['value'] = round(self.progressbar['value'] + 0.1, 2)
            value_label['text'] = self.labelupdater()
            window.update_idletasks()
            self.process_image(file, tgt_folder, confidence)
        return
