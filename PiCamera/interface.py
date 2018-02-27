from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import os.path
import time

###################################################
# This class controls                             #
# the operation of the camera and light fixture   #
###################################################  
class Uploader():
  # initialize LED drive pins
  GPIO.setwarnings(False);
  GPIO.setmode(GPIO.BCM);
  pin26 = 26;
  GPIO.setup(pin26,GPIO.OUT);
  GPIO.output(pin26,0);
  
  # class variables
  photosPerHour = 1    # 1 photo/hour
  secondsPerHour = 3600
  captureInterval = secondsPerHour/photosPerHour
  numberOfDays = 1
  hoursPerDay = 24
  hoursPerTrial = numberOfDays*hoursPerDay   
  numberOfPhotos = hoursPerTrial*photosPerHour
  running = 1   # running = button input signal indicates system on
  count = 0
  path = 'slime_capture' # the  path is in the format: "sample_capture_[count]_[month]_[day]_[year]_[hour]:[min]:[sec]"
  currentPath = ''

  save_path = r'/home/pi/Desktop/Slime_Captures_' + time.strftime("%h_%d_%Y_%X")
  if not os.path.exists(save_path):
    os.makedirs(save_path)

  ##################################  
  # periodically capture pictures  #
  ##################################
  def run(self):
    if (self.running & self.count < self.numberOfPhotos):
      camera = PiCamera() # open the camera
      camera.resolution = (3268,2464)
      self.count += 1   # increment the photo ID count

      # turn on light
      GPIO.output(self.pin26,1);

      # Let camera adjust to light
      #sleep(2)

      upload_filename = self.path + str(self.count) + '_' + time.strftime("%B_%d_%Y_%X") + '.jpg'
      self.currentPath = os.path.join(self.save_path, upload_filename)
      camera.capture(self.currentPath)
      file = open(self.currentPath)

      # turn off light
      GPIO.output(self.pin26,0);

      camera.close()   # close the camera between captures in case it is needed elsewhere
    return
  #############################  
  # Discontinue Photo Capture #
  #############################
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
      self.count = 0
      self.save_path = self.generateFolder()

  #####################################
  # Get the path of the current image #
  #####################################
  def getCurrentImagePath(self):
    return self.currentPath

  ############################################################################
  # Make a new directory and update the location of where to save files path #
  ############################################################################
  def generateFolder(self):
    newpath = r'/home/pi/Desktop/Slime_Captures_' + time.strftime("%h_%d_%Y_%X")
    if not os.path.exists(newpath):
      os.makedirs(newpath)
    return newpath
  
  #############################  
  # Discontinue Photo Capture #
  #############################
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
      self.count = 0
      self.save_path = self.generateFolder()
