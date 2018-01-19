from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os.path
#import smbus
import time

###################################################
# This class controls                             #
# the operation of the camera and light fixture   #
###################################################  
class Uploader():
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
  
  # class variables
  photosPerHour = 1    # 1 photo/hour
  secondsPerHour = 3600
  captureInterval = secondsPerHour/photosPerHour
  numberOfDays = 7
  hoursPerDay = 24
  hoursPerTrial = numberOfDays*hoursPerDay   # 168 hours in a week
  numberOfPhotos = hoursPerTrial*photosPerHour
  running = 1   # running = button input signal indicates system on
  count = 0
  path = 'slime_capture' # the  path is in the format: "sample_capture_[count]_[month]_[day]_[year]_[hour]:[min]:[sec]"
  save_path = r'/home/pi/Desktop/Slime Growth Captures/'


  ##################################  
  # periodically capture pictures  #
  ##################################
  def run(self):
    if (self.running & self.count < self.numberOfPhotos):
      camera = PiCamera() # open the camera
      camera.resolution = (3268,2464)
      self.count+=1   # increment the photo ID count

      # turn on light
      GPIO.output(self.pin6,1);
      GPIO.output(self.pin13,1);
      GPIO.output(self.pin19,1);
      GPIO.output(self.pin26,1);

      # Let camera adjust to light
      sleep(4)

      upload_filename = self.path + str(self.count) + '.jpg'#'_' + time.strftime("%B_%d_%Y_%X") + '.jpg'
      completeName = os.path.join(self.save_path, upload_filename)
      camera.capture(completeName)
      file = open(completeName)
      sleep(2)#testing purposes to avoid hourly delay

      # turn off light
      GPIO.output(self.pin6,0);
      GPIO.output(self.pin13,0);
      GPIO.output(self.pin19,0);
      GPIO.output(self.pin26,0);


      #sleep(self.captureInterval - 4.1)  # delay between captures (subtract GUI and capture delay)
      camera.close()   # close the camera between captures in case it is needed elsewhere

  #############################  
  # Discontinue Photo Capture #
  #############################
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
