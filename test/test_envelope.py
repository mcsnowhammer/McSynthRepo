from __future__ import absolute_import
import unittest
import config
import audio
import synth
import envelope
import matplotlib.pyplot as plt


class TestFilter(unittest.TestCase):
    def setUp(self):
        super(TestFilter, self).setUp()
        self._synth = synth.Synth()
        self._envelope = envelope.Envelope()
        self._audio = audio.Audio()

    def test_ADSR(self):
        sound = self._synth.get_saw_wave(220, 1.5)
        adsrSound = self._envelope.ADSR(sound, 0.5, 0.1, 0.2, 0.5, 0.3)
        self.assertEqual(adsrSound.size, 1.5 * config.SAMPLE_RATE)
        self._audio.play(adsrSound)

    def test_smoothEdges(self):
        sound = self._synth.get_saw_wave(440, 1.0)
        smoothSound = self._envelope.smoothEdges(sound)
        self.assertEqual(smoothSound.size, 1.0 * config.SAMPLE_RATE)
        self._audio.play(smoothSound)
        #plt.plot(smoothSound)
        #plt.show()
