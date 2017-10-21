# Periodic photo capture script
# Rev #2
# TODO: time stamping, button for on/off

from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import dropbox

access = ''

# LED drive
GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin = 13;
GPIO.setup(pin,GPIO.OUT);
GPIO.output(pin,0)

# camera and timing elements
camera = PiCamera()     # initialize camera
numHours = 2
secondsPerHour = 5
running = 1          # running = button input signal indicates system on
count = 0;
img = 'image_0'

# display brief preview
camera.start_preview()  # display camera preview on monitor
sleep(5)
camera.stop_preview()

def db_upload(image, num):
  upload_name = '/' + img + str(num) + '.jpg'
  file1 = open(image).read()
  db = dropbox.Dropbox(access)
  db.files_upload(file1,upload_name)

# periodically capture pictures and upload to dropbox
while running:
  current_img = img + '.jpg'
  count+=1
  GPIO.output(pin,1) # turn on the LED
  sleep(0.2)
  camera.capture(current_img)
  sleep(0.2)
  GPIO.output(pin,0) # turn off the LED
  db_upload(current_img, count)
  sleep(numHours*secondsPerHour)               

