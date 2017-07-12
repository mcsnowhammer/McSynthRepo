from __future__ import absolute_import
import unittest
import config
import audio
import synth
import filter


class TestFilter(unittest.TestCase):
    def setUp(self):
        super(TestFilter, self).setUp()
        self._synth = synth.Synth()
        self._filter = filter.Filter()

    def test_lowpass_filter(self):
        sound = self._synth.get_saw_wave(70, 0.3)
        filterSound = self._filter.add_lowpass_filter(1.0, sound)
        self.assertEqual(sound.size, 0.3 * config.SAMPLE_RATE)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(1.0, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.2, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.1, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.05, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.025, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.01, sound)
        self._playSound(filterSound)
        filterSound = self._filter.add_lowpass_filter(0.005, sound)
        self._playSound(filterSound)

    def _playSound(self, sound):
        myAudio = audio.Audio()
        myAudio.play(sound)
        myAudio.close()