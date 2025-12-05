from utils.math_utils import *

class GAIN:
    def __init__(self, samples, gain_factor = 1.0):
        self.samples = samples
        self.gain_factor = gain_factor

    def process(self):
        processed = []

        if len(self.samples) > 0 and isinstance(self.samples[0], list):

            for frame in self.samples:
                processed_samples = [sample * self.gain_factor for sample in frame]
                processed.append(processed_samples)
        else:
            processed_samples = [sample * self.gain_factor for sample in self.samples]
            processed.append(processed_samples)
        
        self.samples = processed

    def get_rms(self):
        processed = []
        if len(self.samples) > 0 and isinstance(self.samples[0], list):
            # [[L0, R0], [L1, R1]] -> [L0, R0, L1, R1]
            flat_samples = []
            for frame in samples:
                flat_samples.extend(frame)
            samples = flat_samples
        else:
            samples = self.samples

        sum_of_squares = 0
        for sample in samples:
            sum_of_squares += sample ** 2
        
        mean = sum_of_squares / len(samples)
        
        rms = mean ** 0.5
        
        return rms
    
    def is_stereo(self):
        return len(self.samples) > 0 and isinstance(self.samples[0], list)

    def get_samples(self):
        return self.samples

gain = GAIN([1,2,3,4], 2)
print(gain.get_rms())
# print(gain.get_samples())