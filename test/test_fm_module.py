from __future__ import absolute_import
import unittest
import config
import audio
import synth
import fm_module
import numpy as np


class TestFmModule(unittest.TestCase):
    def setUp(self):
        super(TestFmModule, self).setUp()
        self._synth = synth.Synth()
        self._audio = audio.Audio()

    def testFmModule(self):
        fmModule1 = fm_module.FmModule()