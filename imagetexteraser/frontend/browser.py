from threading import Thread
from tkinter.messagebox import showinfo
from typing import Optional

from attr import attrs, attrib
from tkinter import filedialog as fd
import tkinter as tk
from tkinter import ttk

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
    value_label: tk.Entry
    backend: Backend
    _thread: Optional[Thread] = None

    def __call__(self):
        import time
        #while self.progressbar['value'] != 100:
        #    self.progressbar['value'] = round(self.progressbar['value'] + 0.1, 2)
        #    self.value_label['text'] = self.labelupdater()
        #    self.window.update_idletasks()
        #    time.sleep(0.01)
        showinfo(message='Copying is complete, you can close the application now')
