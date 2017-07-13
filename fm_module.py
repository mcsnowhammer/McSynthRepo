import config
import numpy as np
import synth

class FmModule:
    def __init__(self):
        self._generator = None
        self._modulator = None
        self._synth = synth.Synth()

    def get_osc_fm_wave(self, frequency, modFrequency, modAmp, duration):
        modulatorDecay = np.linspace(1.0 * modAmp, 0.0, config.SAMPLE_RATE * duration)

        generatorWave = self._synth.get_sine_wave(frequency, duration)
        modulatorWave = self._synth.get_sine_wave(modFrequency, duration)

        resultingWave = generatorWave + modulatorWave * modulatorDecay
        return resultingWave

