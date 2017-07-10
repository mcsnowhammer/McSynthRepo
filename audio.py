import pyaudio
import config
import numpy as np


class Audio:
    def __init__(self):
        self.controller = pyaudio.PyAudio()
        self.stream = self.controller.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=config.SAMPLE_RATE,
            output=True)

    def play(self, waveSamples):
        self.stream.write(waveSamples.astype(np.float32), waveSamples.size)
        self.stream.stop_stream()

    def close(self):
        self.stream.close()
        self.controller.terminate()



#stream = p.open(format=pyaudio.paFloat32,
#                channels=1,
#                rate=SAMPLE_RATE,
#                output=True)
#stream.write(waveToPlay.astype(np.float32), waveToPlay.size)
#stream.stop_stream()
#stream.close()
#p.terminate()