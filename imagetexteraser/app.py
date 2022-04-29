import os
import tkinter as tk
from pathlib import Path
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *
from backend_registry import east_model, standard_east_backend, face_and_text_backend

from imagetexteraser.frontend.browser import FilepathFiller, StartProcess, ProgessBarLabelUpdate


# pyinstaller .\imagetexteraser\app.py -p imagetexteraser --add-data "imagetexteraser\\weights\\frozen_east_text_detection.pb;weights" -w --name Textterminator


def main():
    window = tk.Tk()
    window.title("Dr. Richter's Texterminator")
    window.geometry("600x250")
    window.resizable(0, 0)

    # configure the grid
    window.columnconfigure(0, weight=3)
    window.columnconfigure(1, weight=1)

    # creating file selectors
    ent1 = tk.Entry(window)
    ent1.grid(ipadx=130, row=0, column=0)
    browsefunc1 = FilepathFiller(ent1)

    b1 = tk.Button(window, text="Bildordner", command=browsefunc1)
    b1.grid(row=0, column=1)
    ent2 = tk.Entry(window)
    ent2.grid(ipadx=130, row=1, column=0)
    browsefunc2 = FilepathFiller(ent2)

    b2 = tk.Button(window, text="Zielordner", command=browsefunc2)
    b2.grid(row=1, column=1)

    detect_face = BooleanVar()
    detect_text = BooleanVar()
    Checkbutton(window, text="Erase Text\t", variable=detect_text).grid(row=0, column=2, sticky=E)
    Checkbutton(window, text="Erase Faces\t", variable=detect_face).grid(row=1, column=2, sticky=E)
    detect_text.set(True)
    detect_face.set(True)

    # progressbar
    pb = ttk.Progressbar(
        window,
        orient='horizontal',
        mode='determinate',
        length=200
    )
    # place the progressbar
    pb.grid(columnspan=3, row=2, sticky=EW, padx=10, pady=10)
    # label
    update_progress_label = ProgessBarLabelUpdate(pb)
    value_label = ttk.Label(window, text=update_progress_label())
    value_label.grid(columnspan=3, row=3)
    backend = face_and_text_backend("weights/frozen_east_text_detection.pb")
    progress = StartProcess(window=window, progressbar=pb,
                            labelupdater=update_progress_label,
                            value_label=value_label, backend=backend,
                            src_entry=ent1, tgt_entry=ent2, erase_text=detect_text, erase_face=detect_face)

    # start button
    start_button = ttk.Button(
        window,
        text='Start Cleaning',
        command=progress
    )
    start_button.grid(columnspan=3, row=4)
    w2 = Scale(window, from_=0, to=100, tickinterval=0.01, orient=HORIZONTAL, length=1000,
               command=lambda x: setattr(StartProcess, "confidence", 1.0-(int(x)/100)))
    w2.set(70)
    w2.grid(row=6, columnspan=3, padx=100)
    length_label = Label(window, text="Sensitivität der Detektoren\nHöher bedeutet mehr Erkennung aber auch mehr Falsch-Positive").grid(row=7, columnspan=3)







    window.eval('tk::PlaceWindow . center')
    window.mainloop()


if __name__ == '__main__':
    main()