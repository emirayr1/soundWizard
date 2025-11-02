import os
from sound_wizard.formats.wav_read import read_wav

# Get the directory where this script is located
script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, "test.wav")

print(read_wav(file_path)['audio_format'])