from __future__ import absolute_import
import unittest
import config
import audio
import synth
import mixer


class TestMixer(unittest.TestCase):
    def setUp(self):
        super(TestMixer, self).setUp()
        self._synth = synth.Synth()
        self._mixer = mixer.Mixer()

    def test_mixer(self):
        saw1 = self._synth.get_saw_wave(439, 1.5)
        saw2 = self._synth.get_saw_wave(441, 1.5)
        pwmSound = self._synth.get_pwm_wave(110, 1.5, 0.5, 0.6)
        sinSound = self._synth.get_sine_wave(880, 1.5)
        mixedSound = self._mixer.mix(saw1, saw2)
        mixedSound = self._mixer.mix(mixedSound, pwmSound)
        mixedSound = self._mixer.mix(mixedSound, sinSound)
        self.assertEqual(mixedSound.size, 1.5 * config.SAMPLE_RATE)
        self._playSound(mixedSound)

    def _playSound(self, sound):
        myAudio = audio.Audio()
        myAudio.play(sound)
        myAudio.close()
