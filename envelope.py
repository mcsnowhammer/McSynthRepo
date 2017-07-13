import numpy as np
import config

class Envelope:
    def __init__(self):
        nothingYet = 1.0

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

    def smoothEdges(self, wave, nofStartSamples=100, nofEndSamples=200):
        smoothStart = np.linspace(0.0, 1.0, nofStartSamples)
        smoothEnd = np.linspace(1.0, 0.0, nofEndSamples)
        wave[:nofStartSamples] *= smoothStart
        wave[-nofEndSamples:] *= smoothEnd
        return wave