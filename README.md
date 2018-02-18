# **Slime Mold Monitoring and Imaging System**
## **LMU EE/CS Department Senior Project**
<img src="images/oie_124645G3I2Cvl3-1.jpg" width="300" hspace="5">

*Physarum Polycephalum Plasmodium (Slime Mold)*
## Purpose:
### Phase 1)
Provide LMU Biology Department with a camera system for monitoring the growth of slime mold, 
a simple yet fascinating amoeba. 

<a href= "https://www.youtube.com/watch?v=GwKuFREOgmo" >This video demonstrates slime mold's impressive intelligence.</a>

### Phase 2)
Build an test an <a href= "https://en.wikipedia.org/wiki/Optical_coherence_tomography" >Optical Coherence Tomography (OCT)</a> system that generates images of biological samples, like slime mold. The baseline task of the team is to create an OCT system that can measure the height of a sample at a single point. This process can be then used to generate 3D models of the sample by scanning a 2D area and plotting the heights in 3D.

## Overview: 
This repository contains the code for Raspbeery Pi camera and growth tracking system user interface. 
The system periodically takes pictures of the slime as it grows and then stores the pictures 
locally. Biology department students and staff can access the photos remotely by connecting to the 
Pi with RealVNC viewer or directly from the Pi via keyboard, monitor, and mouse. Also contained in this repository
are the programs used to analyze the spectral data produced by the OCT system.

## Status:
Currently we are working on simplifying the camera system's hardware. We are also calibrating the OCT system; so far we are using spectral data simulated in MATLAB to calculate the height of a sample at a single point.

<img src="images/lmuseaver.jpg" width="110" hspace="5">    <img src="images/1024px-Python-logo-notext.svg.png" width="40" hspace="5">    <img src="images/Raspberry_Pi_Logo.svg.png" width="30" hspace="5">
<img src="images/realvnc.jpg" width="40" hspace="3">
