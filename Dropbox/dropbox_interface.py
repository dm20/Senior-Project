from picamera import PiCamera
from time import sleep
import RPi.GPIO as GPIO
import dropbox

class Uploader():
  # LED drive
  GPIO.setwarnings(False);
  GPIO.setmode(GPIO.BCM);
  pin = 13;
  GPIO.setup(pin,GPIO.OUT);
  GPIO.output(pin,0)

  # class variables
  numHours = 2
  secondsPerHour = 5
  running = 1          # running = button input signal indicates system on
  count = 0
  path = 'testing_path_'

  def db_upload(self,image, num):
    upload_name = '/' + self.path + str(num) + '.jpg' # edit the file path
    file1 = open(image).read()
    db = dropbox.Dropbox('') # initialize dropbox folder access (access key removed)
    db.files_upload(file1,upload_name) # upload the file

  # periodically capture pictures and upload to dropbox
  def run(self):
    if (self.running):
      camera = PiCamera() # open the camera
      current_path = self.path + '.jpg' 
      self.count+=1   # increment the photo ID count
      GPIO.output(self.pin,1) # turn on the LED
      sleep(0.2)
      camera.capture(current_path)     # capture photo while the light is on
      sleep(0.2)
      GPIO.output(self.pin,0) # turn off the LED      # turn off the light
      self.db_upload(current_path, self.count)
      sleep(self.numHours*self.secondsPerHour - 0.5)  # delay between captures (accounting for half second wait between runs for stop button)
      camera.close()                                  # close the camera between captures in case the function exits
      
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
