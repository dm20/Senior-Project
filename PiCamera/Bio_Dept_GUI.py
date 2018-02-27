#!/usr/bin/env python3
from interface import Uploader
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import PIL.Image
from PIL import *
from tkinter import *
from PIL import ImageTk
import time

# GPIO init
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin26 = 26;
GPIO.setup(pin26,GPIO.OUT);
GPIO.output(pin26,0);

# GUI init
root = Tk()
root.wm_title("Slime Mold Growth Tracking System")
width = 500
height = 300
root.minsize(width,height)

# photo capture status indicator
disablePreview = False
pauseSequence = False

# instantiate an uploader class
uploader = Uploader()

# callback function for camera preview
def preview():
    global disablePreview
    if (not disablePreview):     # only allow the preview feature to run when the system is not capturing
        camera = PiCamera()     # initialize camera
        camera.resolution = (768,768)

        # turn on the lights
        GPIO.output(26,1);
        
        camera.start_preview()  # display camera preview on monitor
        sleep(5)
        camera.stop_preview() # end preview

        # turn off the lights
        GPIO.output(26,0);

        camera.close()
    return

# callback function for photo capture
t = 0
def run():
    t1 = time.time()
    global t
    global uploader
    global disablePreview
    global pauseSequence
    disablePreview = True
    if (t == 0 or t % uploader.captureInterval <= 0.8 and not pauseSequence):
        uploader.run()      # capture and save an image
    if (uploader.running == 0): # if the stop button was hit, reset the uploader for next time the run button is it
        uploader.running = 1
        disablePreview = False    # allow preview functionality while system is not capturing
        refreshImageIcon(0)
        return
    refreshImageIcon(1)
    t2 = time.time()
    t += .05 + (t2 - t1)
    root.after(50,run) # wait 50 milisecond between uploads for the user to stop/drag window if needed
    return

# callback function for ending photo capture
def kill():
    global uploader
    uploader.stop()     # turn off the uploader
    return

# callback function for pausing photo capture
def pause():
    global pauseSequence
    pauseSequence = not pauseSequence
    updatePauseText(pauseSequence)
    return
        
# preview button init
b = Button(root, text="Camera Preview", command=preview, background='silver')
b.place(relx=0.57,rely=0.2)

# run capture button init
b1 = Button(root, text="Start Sequence", command=run, foreground='white',background='green')
b1.place(relx=0.57,rely=0.4)

# run capture button init
b2 = Button(root, text="Pause Sequence", command=pause, foreground='white',background='silver')
b2.place(relx=0.57,rely=0.6)

# run capture button init
b3 = Button(root, text="End Sequence", command=kill, foreground='white',background='red')
b3.place(relx=0.57,rely=0.8)

# text for before the preview is displayed
msg = Label(root, text='No Slime Capture\nTo Preview Yet', foreground='red')
msg.place(relx=0.1,rely=0.4)

# text for after an image is captured
textIsUpdated = 0 # boolean for whether or not the text has been updated already (only want it to be done once)
def updateText():
    newText = Label(root, text='Most Recent Photo Capture ',foreground='blue')
    newText.place(relx=0.1,rely=0.15)
    return

# text for after an image is captured
def updatePauseText(mode):
    s = ''
    if (mode):
        s = "Resume"
    else:
        s = " Pause"
    global b2
    b2.config(text=s + " Sequence")
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
        updateText()
    return
   
#run gui
root.mainloop()
