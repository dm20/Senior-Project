#!/usr/bin/env python3
from tkinter import *
from picamera import PiCamera
import time
from time import sleep
import os
import sys
from Slime_db_interface_temp import SlimeUploader
import RPi.GPIO as GPIO

# GPIO init
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin6 = 6;
pin13 = 13; # our switch requires the current of at least 3 GPIO pins
pin19 = 19;
pin26 = 26;
GPIO.setup(pin6,GPIO.OUT);
GPIO.setup(pin13,GPIO.OUT); #Configure pins as outputs
GPIO.setup(pin19,GPIO.OUT);
GPIO.setup(pin26,GPIO.OUT);
GPIO.output(pin6,0);
GPIO.output(pin13,0);
GPIO.output(pin19,0);
GPIO.output(pin26,0);
  
# GUI init
root = Tk()
root.wm_title("Slime Mold Growth Tracking System")
width = 500
height = 200
root.minsize(width,height)

# photo capture status indicator
disablePreview = False

# instantiate an uploader class
uploader = SlimeUploader()

# callback function for camera preview
def preview():
    global disablePreview
    if (not disablePreview):     # only allow the preview feature to run when the system is not capturing
        camera = PiCamera()     # initialize camera
        camera.resolution = (768,768)
        # turn on the light
        GPIO.output(6,1);
        GPIO.output(13,1);
        GPIO.output(19,1);
        GPIO.output(26,1);
        camera.start_preview()  # display camera preview on monitor
        sleep(15)
        camera.stop_preview() # end preview
        GPIO.output(6,0);
        GPIO.output(13,0);
        GPIO.output(19,0);
        GPIO.output(26,0);
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

