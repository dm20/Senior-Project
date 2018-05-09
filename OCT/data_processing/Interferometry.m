% OSA Fringe Data plotter in MATLAB
% Instruction: First you must define your arrays in the Command window by
% copy-pasting the data into an array like so:
% EDU>> PowerData01 = [ <PASTE DATA COLUMN HERE>
% ... ];
% EDU>> WaveLengths01 = [ <PASTE DATA COLUMN HERE>
% ... ];
close all;
%%%%%%%%%%%%%%%%%%%%%%%%%%% Resoltion %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plot Raw Data
figure(1);
hold on;
% Example plots with previously named data (see instructions):
plot(wavetrW0001,powertrW000,'b');
plot(wavetrW0001,powertrW001,'k');
plot(wavetrW0001,powertrW002,'r');
plot(wavetrW0001,powertrW003,'g');
grid on;
title('Optical Spectrum Analysis', 'fontsize', 18);
xlabel('Wavelength (nm)','fontsize', 18);
ylabel('Power (µW)', 'fontsize', 18);

% Convert the frequecy domain axis to time axis
lamdaMax = wavetrW0001(size(wavetrW0001,1),1);
lambdaMin = wavetrW0001(1,1);
f = 3e8./(wavetrW0001.*1e-9);
DeltaT = abs(1/(f(2)-f(1)));
t = linspace(-DeltaT/2,DeltaT/2,size(f,1));
interpT = linspace(min(t),max(t),3003);
d = t .* 3e8;
interpD = interpT.*3e8;
timepeaksW000 =unwrap(fftshift(abs(ifft(powertrW000))));
timepeaksW001 =unwrap(fftshift(abs(ifft(powertrW001))));
timepeaksW002 =unwrap(fftshift(abs(ifft(powertrW002))));
timepeaksW003 =unwrap(fftshift(abs(ifft(powertrW003))));

% do interpolation on the data
intPeaks0 = interp1(t,timepeaksW000,linspace(t(1),t(end),3*length(t)),'spline');
intPeaks1 = interp1(t,timepeaksW001,linspace(t(1),t(end),3*length(t)),'spline');
intPeaks2 = interp1(t,timepeaksW002,linspace(t(1),t(end),3*length(t)),'spline');
intPeaks3 = interp1(t,timepeaksW003,linspace(t(1),t(end),3*length(t)),'spline');

% Plot the Time Domain peaks
figure(2);
hold on;
plot(interpD,intPeaks0,'b');
plot(interpD,intPeaks1,'k');
plot(interpD,intPeaks2,'r');
plot(interpD,intPeaks3,'g');
title('Time Domain Peaks (Distance from Reference)', 'fontsize', 18);
xlabel('Distance (10µm)','fontsize', 18);
ylabel('Power (µW)', 'fontsize', 18);

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Range %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% Plot Raw Data
linearRangePow = 10.^(rangePow./10);
figure(3);
plot(rangeWav,linearRangePow,'k');
grid on;
title('Optical Spectrum Analysis', 'fontsize', 18);
xlabel('Wavelength (nm)','fontsize', 18);
ylabel('Power (µW)', 'fontsize', 18);

% Convert the frequecy domain axis to time axis
lamdaMaxR = rangeWav(size(rangeWav,1),1);
lambdaMinR = rangeWav(1,1);
fR = 3e8./(rangeWav.*1e-9);
DeltaTR = abs(1/(fR(2)-fR(1)));
tR = linspace(-DeltaTR/2,DeltaTR/2,size(fR,1));
interpTR = linspace(min(tR),max(tR),length(tR)*3);
dR = t .* 3e8;
interpDR = interpTR.*3e8;

% Conver fringes to time domain and do interpolation
rangeTime =unwrap(fftshift(abs(ifft(linearRangePow))));
newRangeTime = interp1(tR,rangeTime,linspace(tR(1),tR(end),3*length(tR)),'spline');

% Plot the Time Domain range peak
figure(4);
hold on;
plot(interpDR,newRangeTime,'k');
