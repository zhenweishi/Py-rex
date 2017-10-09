# -*- coding: utf-8 -*-
"""
Created on Tue Jul 25 19:36:45 2017

@author: zhenwei.shi
"""

#from Tkinter import *
import Tkinter as tk
import Run_script

   

def ExecutePyrex():
    Run_script.Run(e1.get(),e2.get(),e3.get(),e4.get())
master = tk.Tk()

tk.Label(master, text="Path of DICOM File").grid(row=0)
tk.Label(master, text="Path of RTSTURCT").grid(row=1)
tk.Label(master, text="Output Directory").grid(row=2)
tk.Label(master, text="ROI").grid(row=3)

e1 = tk.Entry(master)
e2 = tk.Entry(master)
e3 = tk.Entry(master)
e4 = tk.Entry(master)

e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)
e4.grid(row=3, column=1)

#Window setting
master.title( "Py-rex" )
master.geometry("400x400")
tk.Button(master, text='Quit', command=master.destroy).grid(row=6, column=0, padx=5, pady=8)
tk.Button(master, text='Execute', command=ExecutePyrex).grid(row=6, column=1, padx=5, pady=8)
tk.mainloop( )