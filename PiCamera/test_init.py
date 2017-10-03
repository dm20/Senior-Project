# Pi Camera initialization test

from picamera import PiCamera
from time import sleep

camera = PiCamera()     # initialize camera

camera.start_preview()  # display camera preview on monitor
sleep(10)               
camera.stop_preview() # end preview
