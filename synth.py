import config
import numpy as np
from scipy import signal

class Synth:
    def __init__(self):
        nothingYet = 1.0

    def get_sine_wave(self, freq, duration):
        samples = np.arange(config.SAMPLE_RATE * duration)
        return np.sin(2 * np.pi * samples * freq / config.SAMPLE_RATE)

    def get_sine_wave_with_vibrato(self, freq, duration, freqOsc=0):
        samples = np.arange(config.SAMPLE_RATE * duration)
        frequency = freqOsc + freq
        phase_correction = np.add.accumulate(
            samples * np.concatenate((np.zeros(1), 2 * np.pi * (frequency[:-1] - frequency[1:])))) / config.SAMPLE_RATE
        return np.sin(2 * np.pi * samples * frequency / config.SAMPLE_RATE + phase_correction)

    def get_saw_wave(self, freq, duration, risingWidth=1):
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration)
        return signal.sawtooth(2 * np.pi * freq * samples, risingWidth).astype(np.float32)

    def get_saw_pwm_wave(self, freq, duration, modFreq, modAmp):
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration)
        modulationWave = np.sin(2 * np.pi * modFreq * samples) * modAmp
        modDuty = (modulationWave + 1.0) / 2.0
        return signal.sawtooth(2 * np.pi * freq * samples, width=modDuty).astype(np.float32)

    def get_square_wave(self, freq, duration, duty=0.5):
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration, endpoint=False)
        return signal.square(2 * np.pi * freq * samples, duty).astype(np.float32)

    def get_pwm_wave(self, freq, duration, modFreq, modAmp):
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration)
        modulationWave = np.sin(2 * np.pi * modFreq * samples) * modAmp
        modDuty = (modulationWave + 1.0) / 2.0
        return signal.square(2 * np.pi * freq * samples, duty=modDuty).astype(np.float32)

    def get_sweep_poly_wave(self, freq, duration):
        p = np.poly1d([50000, -50000, 100, 100.0])
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration)
        w = signal.sweep_poly(samples, p)
        return w

    def get_chirp_wave(self, freq, duration):
        samples = np.linspace(0, duration, config.SAMPLE_RATE * duration, endpoint=False)
        w = signal.chirp(samples, f0=freq, t1=0.15, f1=100, method='hyperbolic', phi=0)
        return w

    def add_lowpass_filter(self, samples):
        b, a = signal.butter(3, 0.5)
        print a
        print b
        zi = signal.lfilter_zi(b, a)
        z, _ = signal.lfilter(b, a, samples, zi=zi * samples[0])
        z2, _ = signal.lfilter(b, a, z, zi=zi * z[0])
        y = signal.filtfilt(b, a, samples)
        return y

    def get_fm_wave(self, f_carrier=220, f_mod=220, Ind_mod=1, length=1):
        sampleInc = 1.0 / config.SAMPLE_RATE
        x = np.arange(0, length, sampleInc)
        y = np.sin(2 * np.pi * f_carrier * x + Ind_mod * np.sin(2 * np.pi * f_mod * x))
        mx = 1.059 * (max(abs(y)))  # scale to max pk of -.5 dB
        y = y / mx
        wavData = np.asarray(y, dtype=np.float32)
        return wavData

    def mix_samples(self, a, b):
        if len(a) < len(b):
            c = b.copy()
            c[:len(a)] += a
        else:
            c = a.copy()
            c[:len(b)] += b
        return c * 0.5

    def ADSR(self, wave, attack, decay, sustainLevel, sustainTime, release):
        aGain = np.linspace(0, 1.0, config.SAMPLE_RATE * attack)
        dGain = np.linspace(1.0, sustainLevel, config.SAMPLE_RATE * decay)
        sGain = np.linspace(sustainLevel, sustainLevel, config.SAMPLE_RATE * sustainTime)
        rGain = np.linspace(sustainLevel, 0, config.SAMPLE_RATE * release)
        ADSRGain = np.append(aGain, dGain)
        ADSRGain = np.append(ADSRGain, sGain)
        ADSRGain = np.append(ADSRGain, rGain)
        endFillSize = wave.size - ADSRGain.size
        fillGain = np.linspace(0, 0, endFillSize)
        ADSRGain = np.append(ADSRGain, fillGain)
        waveToPlay = wave * ADSRGain
        return waveToPlay

    def get_noise_wave(self, min, max, duration):
        samples = np.random.uniform(min, max, duration * config.SAMPLE_RATE)
        return samples