#import camera, sleep, raspberry pi pinour, dropbox interface, and time libraries
from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import dropbox
import time

##############################################################################
# Class: SlimeUploader
#
# Description: this class is the packaged uploader script that takes photos
#     and uploads them to a specified dropbox account
#
# Attributes:
#   4 pins (GPIOs 6, 13, 29, and 26)
#   days: number of days the program will run
#   hours_per_day: number of hours per day
#   photos_per_hour: number of photos that will be taken and uploaded per hour
#   total_photos_taken: total number of photos to be taken
#   sleep_time: the time the pi will sleep between photos
#   numHours
#   secondsPerHour
#   running: variable to determine if the system is running
#   count: running count of number of photos taken thus far
#   path: root name of all photos taken
#   root_name: root name of all photos taken
#
# Functions:
#   __init__
#   db_upload
#   run
#   stop
#
##############################################################################
class SlimeUploader():
  # initialize LED drive pins
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


  # ensure initial state of the light system is off
  GPIO.output(pin6,0);
  GPIO.output(pin13,0);
  GPIO.output(pin19,0);
  GPIO.output(pin26,0);

  
  ###########################################################################
  # Function Name: init
  #
  # Description: This function creates a new instance of the SlimeUploader
  #   class defining default total number of photos to be taken
  #
  ###########################################################################
  def __init__(self, numDays=7, hrPd=24, phPhr=1, rn='Sample_Capture_'): 
    self.max_num_photos = numDays * hrPd * phPhr
    self.days_ = numDays
    self.hours_per_day = hrPd
    self.photos_per_hour = phPhr
    self.sleep_time = 3600 / self.photos_per_hour
    self.root_name = rn;
    self.pin6 = 6
    self.pin13= 13
    self.pin19 = 19
    self.pin26 = 26
    self.testpath = ''

  
  numHours = 2
  secondsPerHour = 5

  
  running = 1          # running = button input signal indicates system on
  count = 0
  path = 'sample_capture_'


  
  ###########################################################################
  # Function Name: db_upload
  #
  # Description: This function takes in an image and a count and subsiquently
  #   appends the current time to the path name with the count then uploads
  #   the image to dropbox 
  #
  ###########################################################################
  def db_upload(self,image, num):
    # create unique name for uploaded image
    upload_name = '/' + self.path + str(num) + '_' + time.strftime("%B_%d_%Y_%X") + '.jpg'
    print(upload_name)
    # read the image in
    file1 = open(image, mode='rb').read()
    # create a new instance of dropbox with an given acess key
    db = dropbox.Dropbox('ippz4jAbhKAAAAAAAAAACSgGqnfO0L2JvjAb-YJ6l7KWZqo3uGLsjSU6d6afDKse')
    # upload the image to dropbox
    db.files_upload(file1,upload_name)


  
  ###########################################################################
  # Function Name: run
  #
  # Description: This function periodically creates a camera instance, path
  #   then turns on a light, takes a photo, turns the light off, then calls
  #   db_upload.  
  #
  ###########################################################################
  def run(self):
    if (self.running):

      # instantiate new camera instance
      camera = PiCamera()

      # instantiate new path
      self.testpath = self.root_name + '.jpg'

      self.count+=1

      # turn on the light
      GPIO.output(self.pin6,1);
      GPIO.output(self.pin13,1);
      GPIO.output(self.pin19,1);
      GPIO.output(self.pin26,1);

      # give time for light to fill the space the camera to adjust
      sleep(3)

      # capture the image
      camera.capture(self.testpath)
      sleep(1)

      # turn the light off
      GPIO.output(self.pin6,0);
      GPIO.output(self.pin13,0);
      GPIO.output(self.pin19,0);
      GPIO.output(self.pin26,0);

      # upload the new image
      self.db_upload(self.testpath, self.count)

      # sleep between caputures
      sleep(4)
      #sleep(self.sleeptime - 4)
      #sleep(self.numHours*self.secondsPerHour - 4)

      # check if we have taken all the photos yet
      if (self.count >= self.max_num_photos):
        self.running = 0;
        #send an email notifying that the photo capture session is complete

      # gracefully end the camera instance
      camera.close()

  ###########################################################################
  # Function Name: stop
  #
  # Description: This function ends the running process by user request
  #
  ###########################################################################      
  def stop(self):
      self.running = 0
