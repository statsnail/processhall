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
LARGE_FONT = ("Verdana", 16)
NORM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)

class ProcesshallApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self._printlabelnext = False

        self._selectedProductLanguage = tk.StringVar()
        self._productlanguages = {"Norway":"",
        "France":"Produit",
        "Spain":"Producto"
        }
        self._selectedProductLanguage.set("Select a product language")

        self._selectedProduct = tk.StringVar()
        self._products = {"Common Periwinkle":"7072773000009",
        "Green Sea Urchin":"7072773000016"
        }
        self._selectedProduct.set("Select a product")

        self._selectedGrade = tk.StringVar()
        self._grades = {"Ungraded":"",
        "Large":"> 190 #/kg", "Jumbo":"140-190 #/kg", "Super Jumbo":"100-140 #/kg",
        "Statsnail":"< 100 #/kg","Normal":"50-100 g/#",
        "Big":"100-150 g/#","Huge":"> 150 g/#"
        }
        self._selectedGrade.set("Select a grade")

        self._selectedProcessing = tk.StringVar()
        self._processes = ('Climbed', 'Unprocessed')
        self._selectedProcessing.set("Climbed")

        self._tweight = tk.StringVar()
        self._dweight = tk.StringVar()
        self._status = tk.StringVar()
        self._labelwriteronline = False
        self._scaleonline = False


        self.myscale = Scale('192.168.1.4','4001')

        self.mylabelwriter = Labelwriter('192.168.1.3', 9100)
        self.mylabelwriter.beep()
        
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
        self.lblLabelWriterOnline = tk.Label(self.lfLabelWriterOnline, text="NA", font=LARGE_FONT, padx=10,pady=10)
        self.lblLabelWriterOnline.grid(row=0, column=0, sticky=tk.W)

        # self.lfScaleOnline
        self.lblScaleOnline = tk.Label(self.lfScaleOnline, text="NA", font=LARGE_FONT, padx=10,pady=10)
        self.lblScaleOnline.grid(row=0, column=0, sticky=tk.W)

        # self.lfLabelEntry
        self.label = tk.Label(self.lfLabelEntry, text="Product:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=0, column=0, sticky=tk.W)
        
        self.productMenu = tk.OptionMenu(self.lfLabelEntry, self._selectedProduct, *self._products.keys())
        self.productMenu.grid(row=0, column=1, sticky=tk.W)

        self.label = tk.Label(self.lfLabelEntry, text="Grade:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=1, column=0, sticky=tk.W)

        self.gradeMenu = tk.OptionMenu(self.lfLabelEntry, self._selectedGrade, *self._grades.keys())
        self.gradeMenu.grid(row=1, column=1, sticky=tk.W)


        self.label = tk.Label(self.lfLabelEntry, text="Product Language:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=2, column=0, sticky=tk.W)
        self.productlanguageMenu = tk.OptionMenu(self.lfLabelEntry, self._selectedProductLanguage, *self._productlanguages.keys())
        self.productlanguageMenu.grid(row=2, column=1, sticky=tk.W)


        self.label = tk.Label(self.lfLabelEntry, text="Processing:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=3, column=0, sticky=tk.W)
        self.processingmenu = tk.OptionMenu(self.lfLabelEntry, self._selectedProcessing, *self._processes)
        self.processingmenu.grid(row=3, column=1, sticky=tk.W)

        self.label = tk.Label(self.lfLabelEntry, text="Batch no:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=4, column=0, sticky=tk.W)

        self.eBatchNo = tk.Entry(self.lfLabelEntry, background = "snow")
        self.eBatchNo.grid(row=4, column=1, sticky=tk.W)
        self.eBatchNo.insert(0, "000001")

        self.label = tk.Label(self.lfLabelEntry, text="Catch date:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=5, column=0, sticky=tk.W)

        self.cal = Calendar(self.lfLabelEntry, width=5, background='black', foreground='white', borderwidth=2)
        self.cal.grid(row=5, column=1, sticky=tk.W)

        self.label = tk.Label(self.lfLabelEntry, text="Customer:", font=LARGE_FONT, padx=10,pady=10)
        self.label.grid(row=6, column=0, sticky=tk.W)

        self.txtCustomer = tk.Entry(self.lfLabelEntry, background = "snow")
        self.txtCustomer.grid(row=6, column=1, sticky=tk.W)

        self.btnPrintlabel = ttk.Button(self.lfLabelWriterOnline, text="Print label",
                            command=self.printlabel)
        self.btnPrintlabel.grid(row=1, column=0, sticky=tk.EW)

        # self.lfScale
        self.label = tk.Label(self.lfScale, text="Weight:", font=HUGE_FONT, padx=10,pady=10)
        self.label.grid(row=0, column=3, sticky=tk.W)

        self.lblDWeight = tk.Label(self.lfScale, textvariable=self._dweight, font=HUGE_FONT, width=5, padx=10,pady=10)
        self.lblDWeight.grid(row=0, column=4, sticky=tk.E)

        self.label = tk.Label(self.lfScale, text="Tare weight:", font=SMALL_FONT)
        self.label.grid(row=0, column=6, sticky=tk.E)

        self.lblTWeight = tk.Label(self.lfScale, textvariable=self._tweight, font=SMALL_FONT, width=5)
        self.lblTWeight.grid(row=0, column=7, sticky=tk.W)

        self.label = tk.Label(self.lfScale, text="kg", font=SMALL_FONT)
        self.label.grid(row=0, column=8, sticky=tk.W)

        self.label = tk.Label(self.lfScale, text="Status:", font=HUGE_FONT, padx=10,pady=10)
        self.label.grid(row=1, column=3, sticky=tk.W)

        self.lblStatus = tk.Label(self.lfScale, textvariable=self._status, font=HUGE_FONT, padx=50,pady=10)
        self.lblStatus.grid(row=1, column=4, sticky=tk.E)
        

        self.label = tk.Label(self.lfScale, text="kg", font=HUGE_FONT)
        self.label.grid(row=0, column=5, sticky=tk.W)
        
        self.update_colors_and_status()
        #seperator1 = ttk.Separator(container, orient=tk.HORIZONTAL)
        #seperator1.grid(row=6,column=2,sticky=tk.EW)

    def update_colors_and_status(self):
        # Naive, todo check status
        self._labelwriteronline = True
        self._scaleonline = True

        # Get data from scale
        scaledata = self.myscale.lastdata()
        self._status.set(scaledata[1])
        self._dweight.set(scaledata[2])
        self._tweight.set(scaledata[3])

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

        if self._printlabelnext:
            self.printlabel()

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

    def printlabel(self):
        print('printing label')
        labelwriter = self.mylabelwriter
        scientificnames = {"Common Periwinkle":"LITTORINA LITTOREA", "Green Sea Urchin":"STRONGYLOCENTROTUS DROEBACHIENSIS"}

        friendlyname = self._selectedProduct.get()
        gtin = self._products[self._selectedProduct.get()]
        scientificname = scientificnames[friendlyname]
        productlanguage = self._productlanguages[self._selectedProductLanguage.get()]
        batchno = self.eBatchNo.get()
        grade = self._selectedGrade.get()
        gradedetail = self._grades[self._selectedGrade.get()]
        catchdate = str(self.cal.selection_get())
        weight = self._dweight.get()
        processingmethod = self._selectedProcessing.get()
        customer = self.txtCustomer.get()

        data = {'friendlyname':friendlyname, 'scientificname':scientificname,
        'productinthirdlanguage':productlanguage, 'gtin':gtin, 'processingmethod':processingmethod,
        'batchno':'000001', 'grade':grade, 'catchdate':catchdate, 'weight':weight, 'pcskg':gradedetail, 'customer':customer}
        #print(data)
        labelwriter.print_label(data)
        self._printlabelnext = False

def printlabelnext(theapp):
    theapp._printlabelnext = True
    print('labelnext')

def main():
    print("running processhall application")


    app = ProcesshallApp()
    app.geometry("800x700")
    app.resizable(0, 0)
    


    keyboard.add_hotkey('space', lambda: printlabelnext(app))
    
    LOOP_ACTIVE = True
    while LOOP_ACTIVE:
        app.update()

    app.quit()




if __name__ == '__main__':
    main()