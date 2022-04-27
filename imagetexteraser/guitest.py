import tkinter as tk
from tkinter import filedialog as fd
from tkinter import ttk
from tkinter.messagebox import showinfo
from tkinter import *

from imagetexteraser.frontend.browser import FilepathFiller, StartProcess, ProgessBarLabelUpdate


def main():
    window = tk.Tk()
    window.title("Dr. Richter's Texterminator")
    window.geometry("500x150")
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


    # progressbar
    pb = ttk.Progressbar(
        window,
        orient='horizontal',
        mode='determinate',
        length=200
    )
    # place the progressbar
    pb.grid(columnspan=2, row=2, sticky=EW, padx=10, pady=10)
    # label
    update_progress_label = ProgessBarLabelUpdate(pb)
    value_label = ttk.Label(window, text=update_progress_label())
    value_label.grid(columnspan=2, row=3)

    progress = StartProcess(window=window, progressbar=pb, labelupdater=update_progress_label, value_label=value_label)

    # start button
    start_button = ttk.Button(
        window,
        text='Start Cleaning',
        command=progress
    )
    start_button.grid(columnspan=2, row=4)
    window.eval('tk::PlaceWindow . center')
    window.mainloop()


if __name__ == '__main__':
    main()