import numpy as np

fade_in_seconds = 2.0
fade_out_seconds = 1.0
fade_type = "linear"
sample_rate = 48000

def fade(samples, num_channels, fade_in_seconds, fade_out_seconds, fade_type, sample_rate):
    samples = np.array(samples)
    fade_in_samples = fade_in_seconds * sample_rate
    print(samples[:fade_in_samples] * np.linspace(0, 1, fade_in_samples))
    # print(np.linspace(0, 1, fade_in_samples))
    
fade([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14], 1, 3, 1, "linear", 44100)