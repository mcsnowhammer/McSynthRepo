from __future__ import absolute_import
import unittest
import config
import audio
import synth
# import matplotlib.pyplot as plt


class TestSynth(unittest.TestCase):
    def setUp(self):
        super(TestSynth, self).setUp()
        self._synth = synth.Synth()

    def test_pwm_wave(self):
        sound = self._synth.get_pwm_wave(110, 1.5, 0.5, 0.6)
        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(sound)

    def test_sin_wave(self):
        sound = self._synth.get_sine_wave(880, 0.9)
        self.assertEqual(sound.size, 0.9 * config.SAMPLE_RATE)
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

    def _playSound(self, sound):
        myAudio = audio.Audio()
        myAudio.play(sound)
        myAudio.close()



if __name__ == '__main__':
    unittest.main()


