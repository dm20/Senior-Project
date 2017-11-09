
from time import sleep
import RPi.GPIO as GPIO

GPIO.setwarnings(False);
GPIO.setmode(GPIO.BCM);
pin5 = 5;
pin6 = 6;
pin13 = 13;
pin19 = 19;
pin26 = 26;
GPIO.setup(pin5,GPIO.OUT);
GPIO.setup(pin6,GPIO.OUT);
GPIO.setup(pin13,GPIO.OUT);
GPIO.setup(pin19,GPIO.OUT);
GPIO.setup(pin26,GPIO.OUT);

GPIO.output(pin5,0);
GPIO.output(pin6,0);
GPIO.output(pin13,0);
GPIO.output(pin19,0);
GPIO.output(pin26,0);

sleep(2)
for i in range(30):
    GPIO.output(pin5,1);
    GPIO.output(pin6,1);
    GPIO.output(pin13,1);
    GPIO.output(pin19,1);
    GPIO.output(pin26,1);
    sleep(1)

    GPIO.output(pin5,0);
    GPIO.output(pin6,0);
    GPIO.output(pin13,0);
    GPIO.output(pin19,0);
    GPIO.output(pin26,0);
    
    sleep(1)
 

