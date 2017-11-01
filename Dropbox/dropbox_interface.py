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
  photosPerHour = 1    # 1 photo/hour
  secondsPerHour = 3600
  captureInterval = secondsPerHour/photosPerHour
  hoursPerWeek = 168   # 168 hours in a week
  numberOfPhotos = hoursPerWeek*photosPerHour
  running = 1          # running = button input signal indicates system on
  count = 0
  path = 'sample_capture_'

  def db_upload(self,image, num):
    upload_filename = '/' + self.path + str(num) + '_' + time.strftime("%B_%d_%Y_%X") + '.jpg' # filename with date and photo number
    fileToUpload = open(image).read()
    db = dropbox.Dropbox('') # initialize dropbox folder access (access key removed)
    db.files_upload(fileToUpload,upload_filename) # upload the file

  # periodically capture pictures and upload to dropbox
  def run(self):
    if (self.running & count < numberOfPhotos):
      camera = PiCamera() # open the camera
      temp_path = self.path + '.jpg' 
      self.count+=1   # increment the photo ID count
      GPIO.output(self.pin,1) # turn on the LED
      camera.capture(temp_path)     # capture photo while the light is on
      GPIO.output(self.pin,0) # turn off the LED      # turn off the light
      self.db_upload(temp_path, self.count)
      sleep(self.captureInterval - 0.5)  # delay between captures (GUI waits 0.5s per call)
      camera.close()                                  # close the camera between captures in case it is needed elsewhere
      
  def stop(self):
      self.running = 0 # stop the run loop from capturing and uploading
