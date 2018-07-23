##!/usr/bin/env python

from scale.scale import Scale
from labelwriter.labelwriter import Labelwriter

import time
import keyboard
import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from decimal import *

HUGE_FONT = ("Verdana", 24)
LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

g_dweight = ''


def printlabel(labelwriter):
    print('printing label')
    data = {'friendlyname':'Common Periwinkle', 'scientificname':'LITTORINA LITTOREA',
    'productinthirdlanguage':'Produit', 'gtin':'7072773000030', 'processingmethod':'Climbed',
    'batchno':'000001', 'grade':'Super Jumbo', 'catchdate':'2018-05-10', 'weight':g_dweight, 'pcskg':'100-141 #/kg'}
    print(data)
    labelwriter.print_label(data)

class ProcesshallApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._tweight = tk.StringVar()
        self._dweight = tk.StringVar()
        self._status = tk.StringVar()

        self._labelwriteronline = 0
        self._scaleonline = 0

        s = ttk.Style(self)
        s.theme_use('clam')

        self.configure(background='#dde1e3')
        self.tk_setPalette(background='#dde1e3', foreground='black', activeBackground='black', activeForeground='red')

        self.container = tk.Frame(self)
        self.container.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        # labelframes
        self.lfLabelEntry = tk.LabelFrame(self.container, text='Label Entry')
        self.lfLabelEntry.grid(row=0,column=0,sticky=tk.EW)

        self.lfScale = tk.LabelFrame(self.container, text='Scale')
        self.lfScale.grid(row=1,column=0,sticky=tk.EW)

        self.lfLabelWriterOnline = tk.LabelFrame(self.container, text='Label Writer Online?')
        self.lfLabelWriterOnline.grid(row=0,column=1,sticky=tk.EW)

        self.lfScaleOnline = tk.LabelFrame(self.container, text='Scale Online?')
        self.lfScaleOnline.grid(row=1,column=1,sticky=tk.EW)

        # self.lfLabelWriterOnline
        self.lblLabelWriterOnline = tk.Label(self.lfLabelWriterOnline, text="NA", font=HUGE_FONT, padx=10,pady=10)
        self.lblLabelWriterOnline.grid(row=0, column=0, sticky=tk.W)

        # self.lfScaleOnline
        self.lblScaleOnline = tk.Label(self.lfScaleOnline, text="NA", font=HUGE_FONT, padx=10,pady=10)
        self.lblScaleOnline.grid(row=0, column=0, sticky=tk.W)

        # self.lfLabelEntry
        label = tk.Label(self.lfLabelEntry, text="Product:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=0, column=0, sticky=tk.W)

        products = [("Common Periwinkle - Ungraded", "7072773000009"),
        ("Common Periwinkle - Large", "7072773000016"),
        ("Common Periwinkle - Jumbo", "7072773000023"),
        ("Common Periwinkle - Super Jumbo", "7072773000030"),
        ("Common Periwinkle - Statsnail", "7072773000047")
        ]
        selectedProduct = tk.StringVar()
        selectedProduct.set("Common Periwinkle - Ungraded")

        productMenu = tk.OptionMenu(self.lfLabelEntry, selectedProduct, *products)
        productMenu.grid(row=0, column=1, sticky=tk.W)

        label = tk.Label(self.lfLabelEntry, text="Batch no:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=1, column=0, sticky=tk.W)

        eBatchNo = tk.Entry(self.lfLabelEntry, background = "snow")
        eBatchNo.grid(row=1, column=1, sticky=tk.W)
        eBatchNo.insert(0, "000001")

        label = tk.Label(self.lfLabelEntry, text="Catch date:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=2, column=0, sticky=tk.W)

        cal = Calendar(self.lfLabelEntry, width=5, background='black', foreground='white', borderwidth=2)
        cal.grid(row=2, column=1, sticky=tk.W)

        label = tk.Label(self.lfLabelEntry, text="Customer:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=5, column=0, sticky=tk.W)

        txtCustomer = tk.Entry(self.lfLabelEntry, background = "snow")
        txtCustomer.grid(row=5, column=1, sticky=tk.W)

        btnPrintlabel = ttk.Button(self.lfLabelWriterOnline, text="Print label",
                            command=lambda: print('hello'))
        btnPrintlabel.grid(row=1, column=0, sticky=tk.EW)

        # self.lfScale
        label = tk.Label(self.lfScale, text="Weight:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=0, column=3, sticky=tk.W)

        lblDWeight = tk.Label(self.lfScale, textvariable=self._dweight, font=HUGE_FONT, width=5, padx=10,pady=10)
        lblDWeight.grid(row=0, column=4, sticky=tk.W)

        label = tk.Label(self.lfScale, text="Tare weight:", font=SMALL_FONT)
        label.grid(row=0, column=6, sticky=tk.E)

        lblTWeight = tk.Label(self.lfScale, textvariable=self._tweight, font=SMALL_FONT, width=5)
        lblTWeight.grid(row=0, column=7, sticky=tk.W)

        label = tk.Label(self.lfScale, text="kg", font=SMALL_FONT)
        label.grid(row=0, column=8, sticky=tk.W)

        label = tk.Label(self.lfScale, text="Status:", font=HUGE_FONT, padx=10,pady=10)
        label.grid(row=1, column=3, sticky=tk.W)

        self.lblStatus = tk.Label(self.lfScale, textvariable=self._status, font=HUGE_FONT, padx=10,pady=10)
        self.lblStatus.grid(row=1, column=4, sticky=tk.W)
        

        label = tk.Label(self.lfScale, text="kg", font=HUGE_FONT)
        label.grid(row=0, column=5, sticky=tk.W)
        
        self.update_colors_and_status()
        #seperator1 = ttk.Separator(container, orient=tk.HORIZONTAL)
        #seperator1.grid(row=6,column=2,sticky=tk.EW)

    def update_colors_and_status(self):
        if 'ST' in self._status.get():
            self.lblStatus.configure(background= 'green')
        elif 'US' in self._status.get():
            self.lblStatus.configure(background= 'red')
        else:
            self.lblStatus.configure(background= 'yellow')

        if self._scaleonline:
            self.lfScaleOnline.configure(background= 'green')
            self.lblScaleOnline.configure(background= 'green')
            self.lblScaleOnline['text'] = 'ON'
        else:
            self.lfScaleOnline.configure(background= 'red')
            self.lblScaleOnline.configure(background= 'red')
            self.lblScaleOnline['text'] = 'OFF'

        if self._labelwriteronline:
            self.lfLabelWriterOnline.configure(background= 'green')
            self.lblLabelWriterOnline.configure(background= 'green')
            self.lblLabelWriterOnline['text'] = 'ON'
        else:
            self.lfLabelWriterOnline.configure(background= 'red')
            self.lblLabelWriterOnline.configure(background= 'red')
            self.lblLabelWriterOnline['text'] = 'OFF'
        tk.Tk.after(self, 100, lambda: self.update_colors_and_status())

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
    global g_dweight
    print("running processhall application")
    myscale = Scale('192.168.1.4','4001')

    mylabelwriter = Labelwriter('192.168.1.3', 9100)
    mylabelwriter.beep()

    app = ProcesshallApp()
    app.geometry("800x600")
    app.resizable(0, 0)

    app._labelwriteronline = 1
    app._scaleonline = 1
    
    keyboard.add_hotkey('space', lambda: printlabel(mylabelwriter))
    
    LOOP_ACTIVE = True
    while LOOP_ACTIVE:
        app.update()
        scaledata = myscale.lastdata()
        app.status = scaledata[1]
        app.dweight = scaledata[2]
        g_dweight = scaledata[2]

    app.quit()

if __name__ == '__main__':
    main()