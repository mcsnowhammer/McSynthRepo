import pyaudio
import numpy as np
from scipy import signal
from numpy import pi
from numpy import sin
from numpy import mod
import matplotlib.pyplot as plt

from Tkinter import *








#volume = 0.5     # range [0.0, 1.0]
#fs = 44100       # sampling rate, Hz, must be integer
#duration = 1.0   # in seconds, may be float
#f = 440.0        # sine frequency, Hz, may be float

# generate samples, note conversion to float32 array
#samples = (np.sin(2*np.pi*np.arange(fs*duration)*f/fs)).astype(np.float32)


p = pyaudio.PyAudio()


SAMPLE_RATE = 48000

def get_sine_wave(freq, duration, freqOsc=0):
    samples = np.arange(SAMPLE_RATE * duration)
    #print samples.dtype
    #print freq

    #samples.fill(1)
    #plt.plot(freqOsc + freq)
    #samples1 = np.sin(2 * np.pi * freq / SAMPLE_RATE)
    #plt.plot(samples)
    frequency = freqOsc + freq
    #plt.plot(np.sin(2 * np.pi * samples * (freqOsc + freq) / SAMPLE_RATE))
    #plt.show()
    #2 * t - cos(t)
    phase_correction = np.add.accumulate(
        samples * np.concatenate((np.zeros(1), 2 * np.pi * (frequency[:-1] - frequency[1:])))) / SAMPLE_RATE
    #plt.plot(phase_correction)
    #plt.show()
    return  np.sin(2 * np.pi * samples * frequency / SAMPLE_RATE + phase_correction)
    #samples = np.arange(SAMPLE_RATE * duration)
    #return  np.sin(2 * np.pi * freq / SAMPLE_RATE * samples).astype(np.float32)


#dt = 1./defaults['framerate']
#time = np.arange(0., 6., dt)
#frequency = 440. - 10*np.sin(2*math.pi*time*1.)  # a 1Hz oscillation
#phase_correction = np.add.accumulate(time*np.concatenate((np.zeros(1), 2*np.pi*(frequency[:-1]-frequency[1:]))))
#waveform = np.sin(2*math.pi*time*frequency + phase_correction)


def get_saw_wave(freq, duration, risingWidth=1):
    samples = np.linspace(0, duration, SAMPLE_RATE * duration)
    return signal.sawtooth(2 * np.pi * freq * samples, risingWidth).astype(np.float32)


def get_saw_pwm_wave(freq, duration, modFreq, modAmp):
    samples = np.linspace(0, duration, SAMPLE_RATE * duration)
    modulationWave = np.sin(2 * np.pi * modFreq * samples) * modAmp
    modDuty = (modulationWave + 1.0) / 2.0
    return signal.sawtooth(2 * np.pi * freq * samples, width=modDuty).astype(np.float32)


def get_square_wave(freq, duration, duty=0.5):
    samples = np.linspace(0, duration, SAMPLE_RATE * duration, endpoint=False)
    return signal.square(2 * np.pi * freq * samples, duty).astype(np.float32)


def get_pwm_wave(freq, duration, modFreq, modAmp):
    samples = np.linspace(0, duration, SAMPLE_RATE * duration)
    modulationWave = np.sin(2 * np.pi * modFreq * samples) * modAmp
    modDuty = (modulationWave + 1.0) / 2.0
    return signal.square(2 * np.pi * freq * samples, duty=modDuty).astype(np.float32)


def get_sweep_poly_wave(freq, duration):

    #0p = np.poly1d([0.5, -0.75, 2.5, 5.0])
    p = np.poly1d([50000, -50000, 100, 100.0])
    samples = np.linspace(0, duration, SAMPLE_RATE * duration)
    #t = np.linspace(0, 10, 5001)
    w = signal.sweep_poly(samples, p)

    return w

def get_chirp_wave(freq, duration):
    #t = np.linspace(0, 10, 5001)
    samples = np.linspace(0, duration, SAMPLE_RATE * duration, endpoint=False)
    w = signal.chirp(samples, f0=freq, t1=0.15, f1=100, method='hyperbolic', phi=0)
    return w

def add_lowpass_filter(samples):
    b, a = signal.butter(3, 0.5)
    print a
    print b
    zi = signal.lfilter_zi(b, a)
    z, _ = signal.lfilter(b, a, samples, zi=zi * samples[0])
    z2, _ = signal.lfilter(b, a, z, zi=zi * z[0])
    y = signal.filtfilt(b, a, samples)
    #plt.plot(y)
    #plt.show()
    return y

def get_fm_wave(f_carrier=220, f_mod=220, Ind_mod=1, length=1):
    sampleInc = 1.0 / SAMPLE_RATE
    x = np.arange(0, length, sampleInc)
    y = np.sin(2 * np.pi * f_carrier * x + Ind_mod * np.sin(2 * np.pi * f_mod * x))
    mx = 1.059 * (max(abs(y)))  # scale to max pk of -.5 dB
    y = y / mx
    wavData = np.asarray(y, dtype=np.float32)
    return wavData

def mix_samples(a, b):
    if len(a) < len(b):
        c = b.copy()
        c[:len(a)] += a
    else:
        c = a.copy()
        c[:len(b)] += b

    return c * 0.5

def ADSR(wave, attack, decay, sustainLevel, sustainTime, release):
    aGain = np.linspace(0, 1.0, SAMPLE_RATE * attack)
    dGain = np.linspace(1.0, sustainLevel, SAMPLE_RATE * decay)
    sGain = np.linspace(sustainLevel, sustainLevel, SAMPLE_RATE * sustainTime)
    rGain = np.linspace(sustainLevel, 0, SAMPLE_RATE * release)

    ADSRGain = np.append(aGain, dGain)
    ADSRGain = np.append(ADSRGain, sGain)
    ADSRGain = np.append(ADSRGain, rGain)

    endFillSize = wave.size - ADSRGain.size
    fillGain = np.linspace(0, 0, endFillSize)

    ADSRGain = np.append(ADSRGain, fillGain)

    #plt.plot(ADSRGain)
    #plt.show()
    waveToPlay = wave * ADSRGain
    return waveToPlay

def get_noise_wave(min, max, duration):
    samples = np.random.uniform(min, max, duration * SAMPLE_RATE)
    return samples



#samplesSine1 = get_sine_wave(100, 4.0)
#samplesSine2 = get_sine_wave(880, 1.0)
#samplesSaw1 = get_saw_wave(120, 1.0)
samplesSquare = get_square_wave(220, 0.5)
#samplesComb = np.append(samplesSine1, samplesSaw1)

#samplesSawPwm = get_saw_pwm_wave(220, 2.0, 1.0, 1.0)

sinDuration= 5.0
modFreq = 5.0
modAmp = 5.0
freqSamples = np.linspace(0, sinDuration, sinDuration * SAMPLE_RATE)
freqOsc = np.sin(2.0 * np.pi * modFreq * freqSamples) * modAmp
#freqOsc.fill(40.0)
freq = np.linspace(0, sinDuration, sinDuration * SAMPLE_RATE)
freq.fill(880.0)
#waveToPlay = get_sine_wave(freq, sinDuration, freqOsc)

#sweep = get_sweep_poly_wave(220.0, 5.0)
chirp = get_chirp_wave(1000, 1.0)

saw1 = get_saw_wave(219.5, 2.0)
saw2 = get_saw_wave(220.5, 2.0)
sinVib = get_sine_wave(freq, sinDuration, freqOsc)
waveToPlay = get_pwm_wave(110, 4.0, 2.0, 2.0)
#waveToPlay = add_lowpass_filter(0.05, saw1)

#waveToPlay = mix_samples(saw1, saw2)
#waveToPlay = mix_samples(pwm, waveToPlay)
#waveToPlay = add_lowpass_filter(0.02, waveToPlay)
#waveToPlay = mix_samples(sinVib, waveToPlay)

#waveToPlay = get_fm_wave(440,83,7, 4)

#waveToPlay = get_noise_wave(-0.9, 0.2, 1.0)
#waveToPlay = ADSR(waveToPlay, 0.0, 0.15, 0.1, 0.1, 0.05)

#plt.plot(waveToPlay)
#plt.show()



#samplesSaw1 = get_saw_wave(120, 1.0)
print waveToPlay.dtype
print waveToPlay.shape
print waveToPlay.size




stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=SAMPLE_RATE,
                output=True)

stream.write(waveToPlay.astype(np.float32), waveToPlay.size)


stream.stop_stream()
stream.close()



p.terminate()

window = Tk()
#window.title("Synth")
#close_button = Button(window, text="Close", command=window.quit)
#close_button.pack()

window.mainloop()




#TODOS
#*** Basic ADSR
# Test Sequencer
#*** Basic mixer
# Basic GUI
# Echo effect
# Save sounds
# Wave display in GUI
#*** Noise
