#!/usr/bin/python
from tkinter import *
from picamera import PiCamera
from time import sleep

camera = PiCamera()     # initialize camera

root = Tk()

label = Label(root,text="Slime Mold GUI")

def prev():
	camera.start_preview()  # display camera preview on monitor
	sleep(10)               
	camera.stop_preview() # end preview
    

b = Button(master, text="Camera Preview", command=prev)
b.pack()
label.pack()
root.mainloop()
