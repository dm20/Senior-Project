import visa
import numpy as np
from Tkinter import *
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

###########################
#     VISA GPIB INIT      #
###########################
inst = None;
def initialize():
	global inst
	# http://www.pythonforbeginners.com/error-handling/python-try-and-except
	rm = visa.ResourceManager()
	inst = rm.open_resource('GPIB0::1::INSTR')
	inst.timeout = 30000;
	return

initialize()

#########################
# 		GUI SETUP       #
#########################
root = Tk()
root.wm_title("OCT GUI")
width = 1000
height = 700
root.minsize(width,height)
root.configure(background='lightgray')

fig = plt.figure(1,figsize=(7.1, 7))
canvas = FigureCanvasTkAgg(fig, master=root)
plot_widget = canvas.get_tk_widget()
plt.subplot(211)
plt.title('Power vs. Wavelength')
plt.subplot(212)
plt.title('IFFT(Power vs. Wavelength)')
plot_widget.place(relx = 0.05, rely = 0.05)

t1 = 0.0
t2 = 0.0
peak1 = 0.0
peak2 = 0.0
peaks = [];
time = [];

# Sweep the spectrum once on the OSA
def sweepSingle():
	global inst
	### update plots ???
	inst.write(':INITIATE')
	print("Plot Data");
	return

# Continuously sweep the spectrum on the OSA
def sweepContinuous():
	global inst
	### update plots based on frequency of OSA sweep using same method as bio_dept_gui checker ???
	inst.write(':INITIATE:SMODE 2')
	inst.write(':INITIATE')
	print("Plot Continously");
	return

# set the start wavelength on the OSA and plotting windows in the GUI
def setStartWavelength():
	global inst
	startWL = e1.get()
	inst.write('SENSE:WAVELENGTH:START ' + startWL +'NM')
	inst.write(':INITIATE')
	print("Set Start WL");
	return

# set the stop wavelength on the OSA and plotting windows in the GUI
def setStopWavelength():
	global inst
	stopWL = e2.get()
	inst.write('SENSE:WAVELENGTH:STOP ' + stopWL + 'NM')
	inst.write(':INITIATE')
	print("Set Stop WL");
	return

# set the reference level of the OSA and plotting windows in the GUI
def setRefLevel():
	global inst
	refLevel = e3.get()
	inst.write(':DISPlAY:TRACE:Y1:SPACING LINEAR')
	inst.write(':DISPLAY:TRACE:Y1:RLEVEL ' + refLevel + 'NW')
	inst.write(':INITIATE')
	print("Set Ref Level");
	return

# set the reference level scale on the OSA
def setLogScale():
	global inst	
	inst.write(':DISPlAY:TRACE:Y1:PDIVISION 0.5DB')
	inst.write(':INITIATE')
	print("Set Log Scale");
	return 

def setLinearScale():
	global inst	
	inst.write(':DISPlAY:TRACE:Y1:SPACING LINEAR')
	inst.write(':INITIATE')
	print("Set Lin Scale");
	return

# Clear the plotting windows in the GUI
def clearPlotWindow():
	### matplotlib clear window function ???
	print("Clear Plot Window");
	return
 
# Plot the spectrum data in the GUI immediately  
def plotSpectrumData():
	# write Trace A to memory as "plot.CSV" in the slime mold folder
	inst.write(':MMEMory:CDIRectory "SlimeMold"')
	cmd = ':MMEMory:STORe:TRACE TRA, CSV,"plot",INT'  
	inst.write(cmd)

	# pull raw spectrum from memory
	values = (inst.query(':MMEMory:DATA? "plot.CSV"'))
	s = "[TRACE DATA]";
	i = values.index(s) + len(s) + 4
	y = values[i:len(values)]
	y = y.split('\r\n')
	z = zip(y[0::2], y[1::2])
	mags = [] # magnitudes along the wavelength axis
	for i in range(len(z)-1):
		elm = z[i]
		mags = mags + [float(elm[0].split(",",1)[1])]
		mags = mags + [float(elm[1].split(",",1)[1])]
	zeros = [0] * (len(mags)/2);
	# zero pad the raw data from the OSA
	mags = zeros + mags + zeros

	fig = plt.figure(1,figsize=(7.1, 7))
	canvas = FigureCanvasTkAgg(fig, master=root)
	plot_widget = canvas.get_tk_widget()

	# plot raw spectrum
	plt.subplot(211)
	wavelengths = np.linspace(755.63,805.63,len(mags)) # need to make this dynamic, can be pulled from spectrometer directly or through the same process that is used to get the magnitude values
	plt.plot(wavelengths,mags)
	plt.axis([np.amin(wavelengths), np.amax(wavelengths), np.amin(mags), np.amax(mags)*1.1])

	plt.subplot(212)
	# apply IFFT to raw spectrum to get peaks
	global peaks
	peaks = np.unwrap(np.fft.fftshift(np.abs(np.fft.ifft(mags))))
	
	# below is translated from oct_Script.m
	f = []
	w = []
	# divide by 1 nm
	for i in range(len(mags)):
		w[i] = mags[i]*(1e-9)
	# convert to frequency
	for i in range(len(mags)):
		f[i] = 3e8 / w[i]
	# calculate time axis
	DeltaT = np.abs(1/(f[2]-f[1]))
	global time
	time = np.linspace(-DeltaT/2,DeltaT/2,len(f))
	
	# plot IFFT of spectrum (peaks)
	plt.plot(time,peaks,color='red')
	plt.axis([np.amin(time), np.amax(time), np.amin(peaks), np.amax(peaks)*1.1])
				   
	plt.hold(True)
	computeWidth()
	findPeaks()
	plot_widget.place(relx = 0.05, rely = 0.05)
	return

def findPeaks():
	plt.subplot(212)
	plt.plot(t1,peak1,marker='o',color='lightgreen')
	plt.plot(t2,peak2,marker='o',color='lightgreen')
	plot_widget.place(relx = 0.05, rely = 0.05)
	return

def computeWidth():
	z = zip(peaks,time) #pair the magnitude values at each time with their corresponding time in the format: (raw data value, time instance)
	z.sort() #sort all the magnitude-time pairs 
	global peak1
	peak1 = z[len(z) - 1] # one of the peaks is the absolute max of all magnitude-time pairs
	global t1
	t1 = peak1[1]
	global peak2
	peak2 = z[len(z) - 2]
	i = 2
	# the other peak needs to be some minimum time away from the other peak, 
	# not necessarily the second greatest value in the list. If we simply choose the second greatest
	# value in the list we'll probably just get the point that is immediately to the 
	# left/right of the highest peak. This time threshold is a minimum that would
	# indicate a height of 1 micrometer (1 micrometer = (c/1.00029) * t) -> t = 3.33652e-15 s
	# so far the below threshold is the sweet spot
	minimumTimeDelta = 3.336524349566377e-12
	while (abs(peak2[1] - t1) <= minimumTimeDelta): 
		peak2 = z[len(z) - i] # go through the list of ordered pairs until the other peak is found
		i+=1
	t2 = peak2[1]
	peak2 = peak2[0]
	peak1 = peak1[0]
	T = abs(t2-t1)
	c = 3e8 / 1.00029 #refraction index of air = 1.00029
	global height
	height = c * T
	updateHeightMeasurement(height)
	return

####################################
#  SPECTRUM DATA PLOTTING BUTTONS  #
####################################
x_shift = 0.1;
y_shift = 0.1;
plotting_div = Label(root, background='gray', height=20,width=30)
plotting_div.place(relx=0.75 - x_shift,rely=0.15 - y_shift)
plotting_div_text = Label(root, text='DATA AQUISITION', background='gray',foreground='black',borderwidth=2, relief="groove")
plotting_div_text.place(relx=0.75 - x_shift,rely=0.15 - y_shift)

b1 = Button(root, text="Single Sweep", command=sweepSingle)
b1.place(relx=0.80 - x_shift,rely=0.2 - y_shift)

# run capture button init
b2 = Button(root, text="Continuous Sweep", command=sweepContinuous)
b2.place(relx=0.80 - x_shift,rely=0.3 - y_shift)

# run capture button init
b3 = Button(root, text="Clear Plot Windows", command=clearPlotWindow)
b3.place(relx=0.80 - x_shift,rely=0.4 - y_shift)

b4 = Button(root, text="Plot Spectrum Data", command=plotSpectrumData)
b4.place(relx=0.3,rely=0.924)

def updateHeightMeasurement(height):
	msg = Label(root, text='Sample Height: ' + str(round(height,6)*1000) + ' mm', background='yellow',foreground='blue')
	msg.place(relx=0.46,rely=0.93)
	return

#############################################
#  OSA SETTINGS BUTTONS AND TEXTFIELDS      #
#############################################
y_shift = 0.15;
settings_div = Label(root, background='lightblue', height=20,width=30)
settings_div.place(relx=0.75 - x_shift,rely=0.55 - y_shift)
settings_div_text = Label(root, text='OSA DISPLAY SETTINGS', background='lightblue',foreground='black',borderwidth=2, relief="groove")
settings_div_text.place(relx=0.75 - x_shift,rely=0.55 - y_shift)

# preview button init
b6 = Button(root, text="Set Start Wavelength", command=setStartWavelength)
b6.place(relx=0.80 - x_shift,rely=0.6 - y_shift)
e1 = Entry(root)
e1.place(relx=0.80 - x_shift,rely=0.65 - y_shift)

# run capture button init
b7 = Button(root, text="Set Stop Wavelength", command=setStopWavelength)
b7.place(relx=0.80 - x_shift,rely=0.7 - y_shift)
e2 = Entry(root)
e2.place(relx=0.80 - x_shift,rely=0.75 - y_shift)

# run capture button init
b8 = Button(root, text="Set Reference Level", command=setRefLevel)
b8.place(relx=0.80 - x_shift,rely=0.8 - y_shift)
e3 = Entry(root)
e3.place(relx=0.80 - x_shift,rely=0.85 - y_shift)

# run capture button init
b9 = Button(root, text="LINEAR SCALE", command=setLinearScale)
b9.place(relx=0.80 - x_shift,rely=0.90 - y_shift)

# run capture button init
b10 = Button(root, text="LOGARITHMIC SCALE", command=setLogScale)
b10.place(relx=0.80 - x_shift,rely=0.95 - y_shift)

##########################
#      RUN THE GUI       #
##########################
root.mainloop()


