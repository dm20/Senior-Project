# Periodic photo capture script
# Rev #2
# TODO: time stamping, button for on/off

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import dropbox

# LED drive
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin = 13;
GPIO.setup(pin,GPIO.OUT);
GPIO.output(pin,0)

# camera and timing elements
camera = PiCamera()     # initialize camera
numHours = 2
secondsPerHour = 20
running = 1          # running = button input signal indicates system on
count = 0;
img = 'image_'

# display brief preview
camera.start_preview()  # display camera preview on monitor
sleep(5)
camera.stop_preview()

def db_upload(image):
  upload_name = "/" + image;
  file1 = open(image).read()
  db = dropbox.Dropbox('ippz4jAbhKAAAAAAAAAACSgGqnfO0L2JvjAb-YJ6l7KWZqo3uGLsjSU6d6afDKse')
  db.files_upload(file1,upload_name)

# periodically capture pictures and upload to dropbox
while running:
  current_img = img + str(count)
  count+=1
  current_img = current_img + '.jpg'
  GPIO.output(pin,1) # turn on the LED
  sleep(0.2)
  camera.capture(current_img)
  sleep(0.2)
  GPIO.output(pin,0) # turn off the LED
  db_upload(current_img)
  sleep(numHours*secondsPerHour)               

