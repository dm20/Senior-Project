from tkinter import *
from picamera import PiCamera
from time import sleep
import os
import sys
from dropbox_interface import Uploader

# GUI init
root = Tk()
root.wm_title("Slime Mold Growth Tracking System")
width = 500
height = 200
root.minsize(width,height)

# photo capture status indicator
system_state = 0

# instantiate an uploader class
uploader = Uploader()

# callback function for camera preview
def preview():
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
    global uploader
    if (uploader.running == 0): # if the stop button was hit, reset the uploader for next time the run button is it
        uploader.running = 1
        return
    uploader.run()      # capture and upload a picture to dropbox
    root.after(500,run) # wait half a second between uploads for the user to stop the program if needed (whenever the stop button is hit the request is processed anyways)
        
# callback function for ending photo capture
def kill():
    global uploader
    uploader.stop()     # turn off the uploader
    return
        
# preview button init
b = Button(root, text="Camera Preview", command=preview)
b.place(relx=0.1,rely=0.1)

# run capture button init
b1 = Button(root, text="Begin Photo Capture", command=run)
b1.place(relx=0.5,rely=0.1)

# run capture button init
b2 = Button(root, text="End Photo Capture", command=kill)
b2.place(relx=0.51,rely=0.3)

#run gui
root.mainloop()


