# Periodic photo capture script
# Rev #2
# TODO: image object, I/O, remote storage

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO

# LED drive
GPIO.setmode(GPIO.BCM);
pin = 15;
GPIO.setup(pin,GPIO.OUT);
GPIO.setwarnings(False);

# camera and timing elements
camera = PiCamera()     # initialize camera
numHours = 2
secondsPerHour = 3600
running = true          # running = button input signal indicates system on
count = 0;
img = 'image_'

# display brief preview
camera.start_preview()  # display camera preview on monitor
sleep(5)
camera.stop_preview()

# periodically capture pictures and upload to dropbox
while running:
  current_img = id + str(count)
  count += 1
  GPIO.output(pin,1) # turn on the LED
  sleep(0.2)
  camera.capture(current_img)
  sleep(0.2)
  GPIO.output(pin,0) # turn off the LED
  db_upload(current_img)
  sleep(numHours*secondsPerHour)               
  
def db_upload(image):
  upload_name = "/" + image;
  file1 = open(image).read()
  db = dropbox.Dropbox('ippz4jAbhKAAAAAAAAAACSgGqnfO0L2JvjAb-YJ6l7KWZqo3uGLsjSU6d6afDKse')
  db.files_upload(file1,upload_name)
