#!/usr/bin/env python3
from interface import Uploader
from picamera import PiCamera
from time import sleep
from tkinter import *
import time
import sys
import os



# GUI init
root = Tk()
root.wm_title("Slime Mold Growth Tracking System")
width = 500
height = 200
root.minsize(width,height)

# photo capture status indicator
disablePreview = False

# instantiate an uploader class
uploader = Uploader()

# callback function for camera preview
def preview():
    global disablePreview
    if (not disablePreview):     # only allow the preview feature to run when the system is not capturing
        camera = PiCamera()     # initialize camera
        camera.resolution = (768,768)
        camera.start_preview()  # display camera preview on monitor
        sleep(5)
        camera.stop_preview() # end preview
        camera.close()

# callback function for photo capture
def run():
    global uploader
    global disablePreview
    disablePreview = True
    if (uploader.running == 0): # if the stop button was hit, reset the uploader for next time the run button is it
        uploader.running = 1
        disablePreview = False    # allow preview functionality while system is not capturing
        return
    uploader.run()      # capture and upload a picture to dropbox
    root.after(500,run) # wait half a second between uploads for the user to stop the program if needed
        
# callback function for ending photo capture
def kill():
    global uploader
    uploader.stop()     # turn off the uploader
    return
        
# preview button init
b = Button(root, text="Camera Preview", command=preview)
b.place(relx=0.1,rely=0.4)

# run capture button init
b1 = Button(root, text="Begin Photo Capture", command=run)
b1.place(relx=0.5,rely=0.25)

# run capture button init
b2 = Button(root, text="End Photo Capture", command=kill)
b2.place(relx=0.51,rely=0.55)

#run gui
root.mainloop()


