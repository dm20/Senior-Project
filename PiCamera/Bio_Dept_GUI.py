#####!/usr/bin/env python3
from interface import Uploader
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import PIL.Image
from PIL import ImageTk
from tkinter import *
import time

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
height = 300
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

        # turn on the light
        GPIO.output(6,1);
        GPIO.output(13,1);
        GPIO.output(19,1);
        GPIO.output(26,1);
        
        camera.start_preview()  # display camera preview on monitor
        sleep(5)
        camera.stop_preview() # end preview

        GPIO.output(6,0);
        GPIO.output(13,0);
        GPIO.output(19,0);
        GPIO.output(26,0);

        camera.close()
    return

# callback function for photo capture
def run():
    global uploader
    global disablePreview
    disablePreview = True
    if (uploader.running == 0): # if the stop button was hit, reset the uploader for next time the run button is it
        uploader.running = 1
        disablePreview = False    # allow preview functionality while system is not capturing
        refreshImageIcon(0)
        return
    uploader.run()      # capture and save an image
    refreshImageIcon(1)
    root.after(500,run) # wait half a second between uploads for the user to stop the program if needed
    return

# callback function for ending photo capture
def kill():
    global uploader
    uploader.stop()     # turn off the uploader
    return
        
# preview button init
b = Button(root, text="Camera Preview", command=preview)
b.place(relx=0.58,rely=0.2)

# run capture button init
b1 = Button(root, text="Begin Photo Capture", command=run)
b1.place(relx=0.55,rely=0.4)

# run capture button init
b2 = Button(root, text="End Photo Capture", command=kill)
b2.place(relx=0.56,rely=0.6)

# text for before the preview is displayed
msg = Label(root, text='No Slime Capture\nTo Preview Yet', foreground='red')
msg.place(relx=0.1,rely=0.4)

# text for after an image is captured
textIsUpdated = 0 # boolean for whether or not the text has been updated already (only want it to be done once)
def updateText():
    newText = Label(root, text='Most Recent Capture', foreground='blue')
    newText.place(relx=0.12,rely=0.17)
    return
    
# display preview of most recent capture
def refreshImageIcon(enable):
    global textIsUpdated
    imagePath = uploader.getCurrentImagePath()
    if (imagePath != '' and enable == 1):
        imgFile = PIL.Image.open(imagePath)
        size = 200,125 # phi
        imgFile.thumbnail(size, PIL.Image.ANTIALIAS)
        img = ImageTk.PhotoImage(imgFile)
        icon = Label(root, image=img)
        icon.place(relx=0.09,rely=0.25)
        icon.image = img
    if (not textIsUpdated):
        textIsUpdated = 1
        updateText()
    return
   
#run gui
root.mainloop()
