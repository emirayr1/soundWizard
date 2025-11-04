import os
from sound_wizard.formats.wav_read import read_wav
import soundfile as sf
import numpy as np

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "test.wav")

x, fs = sf.read(file_path)
samples = read_wav(file_path)['samples']
sample_rate = read_wav(file_path)['sample_rate']

print(np.array_equal(x, samples)) # TRUE

sf.write("denemeOwnTranspose.wav", samples, sample_rate)