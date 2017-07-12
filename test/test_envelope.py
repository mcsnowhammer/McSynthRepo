from __future__ import absolute_import
import unittest
import config
import audio
import synth
import envelope


class TestFilter(unittest.TestCase):
    def setUp(self):
        super(TestFilter, self).setUp()
        self._synth = synth.Synth()
        self._envelope = envelope.Envelope()

    def test_envelope(self):
        sound = self._synth.get_saw_wave(220, 1.5)
        adsrSound = self._envelope.ADSR(sound, 0.5, 0.1, 0.2, 0.5, 0.3)

        self.assertEqual(sound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(adsrSound)

    def _playSound(self, sound):
        myAudio = audio.Audio()
        myAudio.play(sound)
        myAudio.close()
