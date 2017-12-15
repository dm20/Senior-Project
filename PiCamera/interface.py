from picamera import PiCamera
from time import sleep
import os.path
import smbus
import time

###################################################
# This class controls                             #
# the operation of the camera and light fixture   #
###################################################  
class Uploader():
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
  address = 0x70 # light fixture address
  mode = 0x00 # light fixture mode (all LEDs on)
  on = 0xFF # light on
  off = 0x00 # light off
  bus = smbus.SMBus(1) # interface to bus
  save_path = r'/home/pi/Desktop/Slime Growth Captures/'


  ##################################  
  # periodically capture pictures  #
  ##################################
  def run(self):
    if (self.running & self.count < self.numberOfPhotos):
      camera = PiCamera() # open the camera
      camera.resolution = (3268,2464)
      self.count+=1   # increment the photo ID count
      self.bus.write_byte_data(self.address, self.mode, self.on) # turn on light
      sleep(2)
      upload_filename = self.path + str(self.count) + '_' + time.strftime("%B_%d_%Y_%X") + '.jpg'
      completeName = os.path.join(self.save_path, upload_filename)
      #print(self.save_path)
      #print(completeName)
      camera.capture(completeName)
      #print('here:(')
      file = open(completeName)
      sleep(2)
      self.bus.write_byte_data(self.address, self.mode, self.off) # turn off light
      sleep(self.captureInterval - 4.5)  # delay between captures (subtract GUI and capture delay)
      camera.close()   # close the camera between captures in case it is needed elsewhere

  #############################  
  # Discontinue Photo Capture #
  #############################
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
