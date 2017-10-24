#!/usr/bin/python
from tkinter import *
from picamera import PiCamera
from time import sleep

camera = PiCamera()     # initialize camera

root = Tk()
	
# title of GUI
label = Label(root,text="Slime Mold GUI")

# callback function for camera preview
def prev():
    camera.start_preview()  # display camera preview on monitor
    sleep(10)               
    camera.stop_preview() # end preview

# button init
b = Button(root, text="Camera Preview", command=prev)
b.pack()

# label init
label.pack()

#run gui
root.mainloop()
