csv_path = 'datapoints.csv';
data = csvread(csv_path, 1, 0);

blax = data(:,1);
blay = data(:,2);
blaz = data(:,3);
trax = data(:,4);
tray = data(:,5);
traz = data(:,6);
ms = data(:,7);
ms = ms - min(ms);
time = ms / 1000;
samplingFrequency = 1 / mean(diff(time));

bl_acceleration = blaz;
tr_acceleration = traz
%time = linspace(0, 10, 1000); % Time vector from 0 to 10 seconds
%acceleration = sin(20 * pi * 2 * time) + 1 * randn(size(time)); % Example acceleration signal

% Set parameters for the spectrogram
windowSize = 256; % Size of the window for computing the FFT
overlap = 200; % Overlap between consecutive windows
%samplingFrequency = 1 / (time(2) - time(1)); % Calculate the sampling frequency

% Create a figure with two subplots
figure;

% Subplot 1: Original signal
%subplot(2, 1, 1);
plot(time, bl_acceleration);
hold;
plot(time, tr_acceleration);
title('Original Acceleration Signal');
xlabel('Time (seconds)');
ylabel('Acceleration (m/s^2)');
legend();

% % Subplot 2: Spectrogram
% subplot(2, 1, 2);
% 
% % Using the spectrogram function
% spectrogram(bl_acceleration, windowSize, overlap, [], samplingFrequency, 'yaxis');
% 
% % Add labels and title
% title('Spectrogram of Acceleration Signal');
% xlabel('Time (seconds)');
% ylabel('Frequency (Hz)');
% 
% % You can customize the color map if needed
% colormap('jet');
% 
% % Show colorbar
% colorbar;

