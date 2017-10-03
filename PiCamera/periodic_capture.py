# Periodic photo capture script
# Rev #2
# TODO: image object, I/O, remote storage

from picamera import PiCamera
from time import sleep

camera = PiCamera()     # initialize camera
numHours = 2
secondsPerHour = 3600
# running = button input signal indicates system on
running = true
while running
  # image = take still shot 
  camera.start_preview()  # display camera preview on monitor
  sleep(numHours*secondsPerHour)               
  camera.stop_preview() # end preview
  # add image to storage, ensure wifi connection, if unavail. then store on Pi
  
