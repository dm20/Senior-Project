# LMU Senior-Project 2017

# Purpose: 
Provide LMU Biology Department with camera system for monitoring the growth of slime mold, 
a simple yet fascinating amoeba. 

# Overview: 
This repository contains the code for Pi camera and user interface. 
The program will periodically take pictures of the slime as it grows and then store the pictures 
to a separate storage location that can be accessed by the Bio department. 

# Additional Info:
Currently we are using the Dropbox Python API for developers in order to upload photos
taken by the Pi in real time. One of our next steps is to develop a user interface for the 
system using either a command line tool (bash script wrapper) or a python GUI using PyQt.
We are also considering the option of running the camera system immediately once the Pi
is supplied with power.

