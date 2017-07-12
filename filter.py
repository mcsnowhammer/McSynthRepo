from scipy import signal

class Filter:
    def __init__(self):
        nothingYet = 4.0

    def add_lowpass_filter(self, cutoff, samples):
        b, a = signal.butter(3, cutoff)
        zi = signal.lfilter_zi(b, a)
        z, _ = signal.lfilter(b, a, samples, zi=zi * samples[0])
        z2, _ = signal.lfilter(b, a, z, zi=zi * z[0])
        y = signal.filtfilt(b, a, samples)
        return y
