

class Mixer:
    def __init__(self):
        nothingYet = 3.0

    def mix_samples(self, a, b):
        if len(a) < len(b):
            c = b.copy()
            c[:len(a)] += a
        else:
            c = a.copy()
            c[:len(b)] += b
        return c * 0.5