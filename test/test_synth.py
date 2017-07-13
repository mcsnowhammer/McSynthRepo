from __future__ import absolute_import
import unittest
import config
import audio
import synth
import numpy as np
# import matplotlib.pyplot as plt


class TestSynth(unittest.TestCase):
    def setUp(self):
        super(TestSynth, self).setUp()
        self._synth = synth.Synth()
        self._audio = audio.Audio()

    def tearDown(self):
        super(TestSynth, self).tearDown()
        #self._audio.close()

    def test_pwm_wave(self):
        sound = self._synth.get_pwm_wave(110, 1.5, 0.5, 0.6)
        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_sin_wave(self):
        sound = self._synth.get_sine_wave(880, 0.9)
        self.assertEqual(sound.size, 0.9 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_sin_wave_with_vibrato(self):
        sinDuration = 1.5
        modFreq = 7.0
        modAmp = 3.0
        freqSamples = np.linspace(0, sinDuration, sinDuration * config.SAMPLE_RATE)
        freqOsc = np.sin(2.0 * np.pi * modFreq * freqSamples) * modAmp
        sound = self._synth.get_sine_wave_with_vibrato(880, sinDuration, freqOsc)
        self.assertEqual(sound.size, sinDuration * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_saw_wave(self):
        sound = self._synth.get_saw_wave(80, 1.5)
        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_saw_pwm_wave(self):
        sound = self._synth.get_saw_pwm_wave(100, 1.5, 2.0, 1.0)
        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_square_wave(self):
        sound = self._synth.get_square_wave(50, 1.6, 0.5)
        self.assertEqual(sound.size, 1.6 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_chirp_wave(self):
        sound = self._synth.get_chirp_wave(10000, 0.3)
        self.assertEqual(sound.size, 0.3 * config.SAMPLE_RATE)
        self._playSound(sound)
        sound = self._synth.get_chirp_wave(5000, 0.3)
        self._playSound(sound)
        sound = self._synth.get_chirp_wave(2000, 0.4)
        self._playSound(sound)
        sound = self._synth.get_chirp_wave(1000, 0.5)
        self._playSound(sound)
        sound = self._synth.get_chirp_wave(500, 0.6)
        self._playSound(sound)
        sound = self._synth.get_chirp_wave(200, 1.5)
        self._playSound(sound)

    def test_sweep_poly_wave(self):
        sound = self._synth.get_sweep_poly_wave(400, 3.0)
        self.assertEqual(sound.size, 3.0 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_noise_wave(self):
        sound = self._synth.get_noise_wave(-0.9, 0.2, 1.0)
        self.assertEqual(sound.size, 1.0 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_fm_wave(self):
        sound = self._synth.get_fm_wave(500,83,7, 1.5)
        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_osc_fm_wave(self):
        duration = 1.5
        sound = self._synth.get_osc_fm_wave(90, 30, 10, duration)
        self.assertEqual(sound.size, duration * config.SAMPLE_RATE)
        self._playSound(sound)

    def _playSound(self, sound):
        #myAudio = audio.Audio()
        self._audio.play(sound)
        #myAudio.close()


if __name__ == '__main__':
    unittest.main()


