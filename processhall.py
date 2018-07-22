##!/usr/bin/env python

from scale.scale import Scale
from labelwriter.labelwriter import Labelwriter

import time
import keyboard
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar

HUGE_FONT = ("Verdana", 24)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

class ProcesshallApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._dweight = tk.StringVar()
        self._status = tk.StringVar()

        s = ttk.Style(self)
        s.theme_use('clam')

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(200, weight=1)
        container.grid_columnconfigure(200, weight=1)

        menubar = tk.Menu(container)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Save settings", command=lambda: popupmsg("Not supported just yet"))
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=quit)
        menubar.add_cascade(label="File", menu=filemenu)
        tk.Tk.config(self, menu=menubar)

        label = tk.Label(container, text="Product:", font=HUGE_FONT)
        label.grid(row=0, column=0, sticky=tk.W)

        products = [("Common Periwinkle - Ungraded", "7072773000009"),
        ("Common Periwinkle - Large", "7072773000016"),
        ("Common Periwinkle - Jumbo", "7072773000023"),
        ("Common Periwinkle - Super Jumbo", "7072773000030"),
        ("Common Periwinkle - Statsnail", "7072773000047")
        ]
        selectedProduct = tk.StringVar()
        selectedProduct.set("Common Periwinkle - Ungraded")

        productMenu = tk.OptionMenu(container, selectedProduct, *products)
        productMenu.grid(row=0, column=1, sticky=tk.W)

        label = tk.Label(container, text="Batch no:", font=HUGE_FONT)
        label.grid(row=1, column=0, sticky=tk.W)
        txtBatchNo = ttk.Entry(container)
        txtBatchNo.grid(row=1, column=1, sticky=tk.W)

        label = tk.Label(container, text="Catch date:", font=HUGE_FONT)
        label.grid(row=2, column=0, sticky=tk.W)

        cal = Calendar(container, width=12, background='black', foreground='white', borderwidth=2)
        cal.grid(row=2, column=1, sticky=tk.W)

        label = tk.Label(container, text="Customer:", font=HUGE_FONT)
        label.grid(row=3, column=0, sticky=tk.W)

        txtCustomer = ttk.Entry(container)
        txtCustomer.grid(row=3, column=1, sticky=tk.W)

        frame = tk.Frame(container, width=100)
        frame.grid(row=0, column=2)

        label = tk.Label(container, text="Scale:", font=HUGE_FONT)
        label.grid(row=0, column=3, sticky=tk.W)

        lblWeight = tk.Label(container, textvariable=self._dweight, font=HUGE_FONT)
        lblWeight.grid(row=0, column=4, sticky=tk.E)

        label = tk.Label(container, text="Status:", font=HUGE_FONT)
        label.grid(row=1, column=3, sticky=tk.W)

        lblStatus = tk.Label(container, textvariable=self._status, font=HUGE_FONT)
        lblStatus.grid(row=1, column=4, sticky=tk.E)

        label = tk.Label(container, text="kg", font=HUGE_FONT)
        label.grid(row=0, column=5, sticky=tk.W)

        btnPrintlabel = ttk.Button(container, text="Print label",
                            command=lambda: print('hello'))
        btnPrintlabel.grid(row=5, column=0, sticky=tk.W)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()

    @property
    def dweight(self):
        return str(self._dweight.get())

    @dweight.setter
    def dweight(self, value):
        self._dweight.set(str(value))

    @property
    def status(self):
        return str(self._status.get())

    @status.setter
    def status(self, value):
        self._status.set(str(value))

def main():
    print("running processhall application")
    myscale = Scale('192.168.1.4','4001')

    app = ProcesshallApp()
    app.geometry("1280x720")
    app.resizable(0, 0)

    #keyboard.add_hotkey('space', printlabel)
    LOOP_ACTIVE = True
    while LOOP_ACTIVE:
        app.update()
        scaledata = myscale.lastdata()
        app.status = scaledata[1]
        app.dweight = scaledata[2]
    app.quit()

if __name__ == '__main__':
    main()