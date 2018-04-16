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
import subprocess
import gc
IPMSG = ' '

# GPIO init
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin19 = 19;
GPIO.setup(pin19,GPIO.OUT);
GPIO.output(pin19,0);
 

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

        # turn on the light
        GPIO.output(19,1);
        sleep(1)
        camera.start_preview()  # display camera preview on monitor
        sleep(5)
        camera.stop_preview() # end preview
        GPIO.output(19,0);
        camera.close()
    return

# callback function for photo capture
t = 0
first = True;
def run():
    t1 = time.time()
    global uploader
    if (uploader.running == 1):
        b1.config(state='disabled')
        b.config(state='disabled')
    global t
    global disablePreview
    global pauseSequence
    disablePreview = True
    if (uploader.running ==1 and (t == 0 or t % uploader.captureInterval <= 0.8) and not pauseSequence):
        uploader.run()      # capture and save an image
    if (uploader.running == 0): # if the stop button was hit, reset the uploader for next time the run button is it
        uploader.running = 1
        disablePreview = False    # allow preview functionality while system is not capturing
        refreshImageIcon(0)
        b1.config(state='normal')
        b.config(state='normal')
        return
    #refreshImageIcon(1)
    t2 = time.time()
    t += .05 + (t2 - t1)
    gc.collect()
    root.after(50,run) # wait 50 milisecond between uploads for the user to stop the program if needed
    return

# callback function for ending photo capture
def kill():
    global uploader
    global t
    uploader.stop()     # turn off the uploader
    t=0
    return

# callback function for pausing photo capture
def pause():
    global pauseSequence
    pauseSequence = not pauseSequence
    updatePauseText(pauseSequence)
    return

# callback function for pausing photo capture
def GetIP():
    #GetIP.py

    now = time.strftime("%Y%m%d%H%m")

    cmd1 = ['./ifconfig_to_txt.sh']
    p1 = subprocess.Popen(cmd1, stdout=subprocess.PIPE)
    p1.wait()

    # get relavent contents
    filename = now + '.txt'
    inetLines = []
    with open(filename) as inputfile:
        for line in inputfile:
            if "inet " in line:
                line = line.strip(' ')
                inetLines.append(line.split(' '))

    cmd2 = ['./garbage_collection.sh']
    p2 = subprocess.Popen(cmd2, stdout=subprocess.PIPE)
    p2.wait()


    inetLineLengths=[]      
    IPAddresses = []
    for i in range(len(inetLines)):
        inetLineLengths.append(len(inetLines[i]))

    ithLine = inetLineLengths.index(max(inetLineLengths))

    print(inetLines[ithLine][1])
    IPMSG = inetLines[ithLine][1]

    # text for before the preview is displayed
    ip_msg = Label(root, text=IPMSG, foreground='black')
    ip_msg.place(relx=0.77,rely=0.02)
        
# preview button init
b = Button(root, text="Camera Preview", command=preview, background='silver')
b.place(relx=0.57,rely=0.2)

# run capture button init
b1 = Button(root, text="Start Sequence", command=run, foreground='white',background='green')
b1.place(relx=0.57,rely=0.4)

# run capture button init
b2 = Button(root, text="Pause Sequence", command=pause, foreground='black',background='silver')
b2.place(relx=0.57,rely=0.6)

# run capture button init
b3 = Button(root, text="Reset", command=kill, foreground='white',background='red')
b3.place(relx=0.57,rely=0.8)

# Get IP address button init
b4 = Button(root, text="Real VNC IP", command=GetIP, foreground='white',background='blue')
b4.place(relx=0.57,rely=0.0)



# text for before the preview is displayed
msg = Label(root, text='No Slime Capture\nTo Preview Yet', foreground='red')
msg.place(relx=0.1,rely=0.4)

# text for after an image is captured
textIsUpdated = 0 # boolean for whether or not the text has been updated already (only want it to be done once)
def updateText():
    newText = Label(root, text='Most Recent Photo Capture ',foreground='blue')
    newText.place(relx=0.085,rely=0.15)
    del newText
    gc.collect()
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
    gc.collect()
    return
    
# display preview of most recent capture
def refreshImageIcon(enable):
    #global textIsUpdated
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
        del img
        del imgFile
        del size
        del icon
        gc.collect()
    del imagePath
    return
    
   
#run gui
root.mainloop()
