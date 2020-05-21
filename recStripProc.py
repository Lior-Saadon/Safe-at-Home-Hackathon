from scipy.io.wavfile import read
import matplotlib.pyplot as plt
from scipy.signal import hann
from scipy.fftpack import rfft
import numpy as np


class RecordStrip(object):

    def __init__(self, recording_inputs_path):
        super(RecordStrip, self).__init__()
        self.audio_in = []
        self.phisio_in = []
        self.loc = []
        self.sensors = []
        self.sensors_weight ={} # dictionary, maps between sensor type and weight
        self.tot_score = 0
        self.alert = False
        self.audio_path = recording_inputs_path
        self.init_signals()
        self.init_sensors()

    def init_signals(self):
        self.audio_in = read(self.audio_path)

    def init_sensors(self):
        new_pitch_sensor = PitchSensor()
        new_pitch_sensor.extract_signal(self.audio_in)
        self.sensors.append(new_pitch_sensor)

    def proc_sensors(self):
        for sensor in self.sensors:
            sensor.proc_sensor()

    def get_tot_score(self):
        tot_score = 0
        sensors_num = len(self.sensors)
        if sensors_num>0 :
            for sensor in self.sensors:
                tot_score += sensor.score       # multiply by weight (TBD)
            self.tot_score = tot_score/sensors_num


class Sensor(object):

    def __init__(self):
        super(Sensor, self).__init__()
        self.type = None  # PITCH / SPEECH_RATE / NUM_PARTICIPANTS / STRESS / NLP
        self.signal = []
        self.F_sample = 0
        self.signal_len = 0
        self.detection = 0
        self.thresh = 0
        self.score = 0

    def extract_signal(self, input_data):
        self.signal = input_data[1]
        self.F_sample = input_data[0]  # samples per sec
        self.signal_len = self.signal.size  # let M be the length of the time series
        len_sec = self.signal_len / self.F_sample
        print(self.signal_len, self.F_sample, len_sec)

    def proc_sensor(self):
        self.detection = self.analyze_signal()
        self.score = np.abs(self.detection - self.thresh)/self.thresh

    def analyze_signal(self):
        detection = 0
        return detection


class PitchSensor(Sensor):

    def __init__(self):
        super(PitchSensor, self).__init__()
        self.type = "PITCH"
        self.thresh = 97    # arbitrary TBD
        self.low_cutoff = 80
        self.high_cutoff = 3000
        self.window_size = 400000
        self.window_margin = int(self.window_size/2)

    def analyze_signal(self):
        wind_Indexes = np.arange(self.window_margin, self.signal_len - self.window_margin, self.window_size)
        len(wind_Indexes)

        pitchVector = []
        # magVector = []
        windowLen = []
        for window_index in wind_Indexes:  # Run a window of appropriate length across the audio file
            window = self.signal[window_index - self.window_margin:window_index + self.window_margin]
            # magVector.append(maxMagnitude(window, F_sample))
            pitchVector.append(self.maxFrequency(window, self.F_sample))
            windowLen.append(len(window))

        detection = np.max(pitchVector) # OR avg Or other.. TBD
        return detection

    def maxFrequency(self, X, F_sample):
        """ Searching presence of frequencies on a real signal using FFT
        Inputs
        =======
        X: 1-D numpy array, the real time domain audio signal (single channel time series)
        Low_cutoff: float, frequency components below this frequency will not pass the filter (physical frequency in unit of Hz)
        High_cutoff: float, frequency components above this frequency will not pass the filter (physical frequency in unit of Hz)
        F_sample: float, the sampling frequency of the signal (physical frequency in unit of Hz)
        """
        Low_cutoff = self.low_cutoff
        High_cutoff = self.high_cutoff
        M = X.size  # let M be the length of the time series
        Spectrum = rfft(X, n=M)
        [Low_cutoff, High_cutoff, F_sample] = map(float, [Low_cutoff, High_cutoff, F_sample])

        # Convert cutoff frequencies into points on spectrum
        [Low_point, High_point] = map(lambda F: F / F_sample * M, [Low_cutoff, High_cutoff])

        [Low_point, High_point] = map(int, [Low_point, High_point])

        maximumFrequencyIndx = np.where(
            Spectrum == np.max(Spectrum[Low_point: High_point]))  # Calculating which frequency has max power.

        return Spectrum[maximumFrequencyIndx]


