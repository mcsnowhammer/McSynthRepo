import pyaudio
import config
import numpy as np
import envelope


class Audio:
    def __init__(self):
        self._envelope = envelope.Envelope()
        self._controller = pyaudio.PyAudio()
        self._stream = self._controller.open(
            format=pyaudio.paFloat32,
            channels=1,
            rate=config.SAMPLE_RATE,
            output=True)

    def __del__(self):
        self.close()

    def play(self, waveSamples):
        wave = self._envelope.smoothEdges(waveSamples)
        self._stream.write(waveSamples.astype(np.float32), wave.size)

    def close(self):
        self._stream.stop_stream()
        self._stream.close()
        self._controller.terminate()
