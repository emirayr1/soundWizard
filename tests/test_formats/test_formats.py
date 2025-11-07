import os
from sound_wizard.formats.wav_read import *
import soundfile as sf
import numpy as np

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "test.wav")

# x, fs = sf.read(file_path)
data = read_wav(file_path)
samples = data['samples']
sample_rate = data['sample_rate']
num_channels = data['channels']
bits_per_sample = data['bits_per_sample']
# writed_wave = write_wav("a", samples, sample_rate, 2, 24)
# print(np.array_equal(x, samples)) # TRUE
# print(np.array_equal(writed_wave, denormalize_samples1(samples, 24, 2)))

write_wav("write_test.wav", samples, sample_rate, num_channels, bits_per_sample)

print(get_megabyte(file_path))

# sf.write("denemeOwnTranspose.wav", samples, sample_rate)