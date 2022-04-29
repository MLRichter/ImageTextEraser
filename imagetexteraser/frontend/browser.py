import os
from pathlib import Path
from threading import Thread
from tkinter.messagebox import showinfo
from typing import Optional

from attr import attrs, attrib
from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import messagebox

from imagetexteraser.domain import Backend


@attrs(auto_attribs=True, frozen=True, slots=True)
class FilepathFiller:
    entry: tk.Entry

    def __call__(self):
        filename = fd.askdirectory()
        self.entry.insert(tk.END, filename)  # add this


@attrs(auto_attribs=True, frozen=True, slots=True)
class ProgessBarLabelUpdate:
    progressbar: ttk.Progressbar

    def __call__(self):
        return f"Current Progress: {self.progressbar['value']}%"


@attrs(auto_attribs=True, slots=True)
class StartProcess:

    window: tk.Tk
    progressbar: ttk.Progressbar
    labelupdater: ProgessBarLabelUpdate
    value_label: tk.Label
    backend: Backend
    src_entry: tk.Entry
    tgt_entry: tk.Entry
    erase_face: tk.BooleanVar
    erase_text: tk.BooleanVar
    confidence: float = 0.5
    _thread: Optional[Thread] = None

    def __call__(self):

        print(self.confidence)

        if hasattr(self.backend, "face_recognition"):
            self.backend.face_recognition = self.erase_face.get()
        if hasattr(self.backend, "text_recognition"):
            self.backend.text_recognition = self.erase_text.get()

        if Path(self.src_entry.get()) == Path(self.tgt_entry.get()):
            showinfo(message="Source and target folder may not be the same")
            return

        if self._thread is not None:
            response = messagebox.askyesno(message='Process is already running!\n Do you want to abort?')
            if response:
                self.backend.stop_flag = True
            return

        if os.listdir(self.tgt_entry.get()) != []:
            response = messagebox.askyesno(message=f'{self.tgt_entry.get()} is not empty! Files may be overwritten by this action!\nProceed anyway?')
            if not response:
                return

        def func():
            self.backend.process_images(
                src_folder=Path(self.src_entry.get()),
                tgt_folder=Path(self.tgt_entry.get()),
                confidence=self.confidence,
                pb=self.progressbar,
                value_label=self.value_label,
                labelupdater=self.labelupdater,
                window=self.window
            )
            if not self.backend.stop_flag:
                showinfo(message='Copying is complete, you can close the application now')
            else:
                self.progressbar['value'] = 0
                self.value_label['text'] = "Aborted"
                self.backend.stop_flag = False
            self._thread = None

        self._thread = Thread(target=func)
        self._thread.start()
