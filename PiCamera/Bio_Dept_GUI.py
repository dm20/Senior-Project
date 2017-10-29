#!/usr/bin/python
from tkinter import *
from picamera import PiCamera
from time import sleep
import os
import sys

# initialize the GUI
root = Tk()

# photo capture status indicator (initially off)
system_state = 0
	
# title of GUI
label = Label(root,text="Slime Mold GUI")
label.pack()

# callback function for camera preview
def prev():
    global system_state
    if (system_state == 0):
        camera = PiCamera()     # initialize camera
        camera.resolution = (768,768)
        camera.start_preview()  # display camera preview on monitor
        sleep(5)
        camera.stop_preview() # end preview
        camera.close()

# callback function for photo capture
def run():
    global system_state
    if (system_state == 0):
        system_state = 1
        os.system('python /home/pi/periodic_capture.py') # run the dropbox upload script

# callback function for ending photo capture
def kill():
    global system_state
    if (system_state == 1):
        system_state = 0
        quit()            # kill the GUI and update system state (needs to be modified)

# preview button init
b = Button(root, text="Camera Preview", command=prev)
b.pack()

# run capture button init
b1 = Button(root, text="Begin Photo Capture", command=run)
b1.pack()

# run capture button init
b2 = Button(root, text="End Photo Capture", command=kill)
b2.pack()

#run gui
root.mainloop()
