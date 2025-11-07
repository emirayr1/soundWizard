import struct
import os

def read_wav(file):
    if not os.path.exists(file):
        raise FileNotFoundError(f"File not found: {file}")
    
    with open(file, 'rb') as f:
        # Parse RIFF header (12 bytes)
        riff_header = f.read(12)
        if len(riff_header) < 12:
            raise ValueError("File too small to be a valid WAV file")
        
        chunk_id = riff_header[0:4]
        file_size = struct.unpack('<I', riff_header[4:8])[0] # unpack returns a tuple (1000, ) -> we need [0]th
        format_type = riff_header[8:12]
        
        # Validate RIFF header
        if chunk_id != b'RIFF':
            raise ValueError(f"Not a RIFF file. Expected 'RIFF', got {chunk_id}")
        if format_type != b'WAVE':
            raise ValueError(f"Not a WAVE file. Expected 'WAVE', got {format_type}")
        
        # Initialize variables
        fmt_data = None
        audio_data = None
        
        # Read chunks until we find fmt and data
        while f.tell() < file_size + 8:  # +8 because file_size doesn't include first 8 bytes
            chunk_header = f.read(8)
            if len(chunk_header) < 8:
                break
                
            chunk_id = chunk_header[0:4]
            chunk_size = struct.unpack('<I', chunk_header[4:8])[0]
            
            # Parse fmt chunk
            if chunk_id == b'fmt ':
                fmt_data = f.read(chunk_size)
                if len(fmt_data) < 16:
                    raise ValueError("Invalid fmt chunk size")
                
                # Parse fmt chunk data
                audio_format = struct.unpack('<H', fmt_data[0:2])[0]
                num_channels = struct.unpack('<H', fmt_data[2:4])[0]
                sample_rate = struct.unpack('<I', fmt_data[4:8])[0]
                byte_rate = struct.unpack('<I', fmt_data[8:12])[0]
                block_align = struct.unpack('<H', fmt_data[12:14])[0]
                bits_per_sample = struct.unpack('<H', fmt_data[14:16])[0]
                
            # Parse data chunk
            elif chunk_id == b'data':
                audio_data = f.read(chunk_size)
                
            else:
                f.seek(chunk_size, 1)  # Skip unwanted chunks 

            if chunk_size % 2 != 0:
                f.read(1) # padding byte 
        
        if fmt_data is None:
            raise ValueError("No fmt chunk found in WAV file")
        if audio_data is None:
            raise ValueError("No data chunk found in WAV file")
        
        bytes_per_sample = bits_per_sample // 8
        num_frames = len(audio_data) // (num_channels * bytes_per_sample) # [L, R], [L, R]
        
        # raw samples
        all_samples = unpack(audio_data, bits_per_sample)

        # normalized samples
        normalized_samples = normalize_samples(all_samples, bits_per_sample)

        sample_array = []
        # if stereo
        if num_channels == 2:
            left = normalized_samples[0::2] # start from 0 and go to end by 2 steps 
            right = normalized_samples[1::2] # start from 1 and go to end by 2 steps
            sample_array = [left, right]
        elif num_channels == 1:
            sample_array = [normalized_samples]

        # normalized and transposed samples
        sample_array = transpose_array(sample_array, num_channels)

        # PROBLEM WAS!!!!!
        # samples = [
        #     [L0, L1, L2, L3, ...],  # Left channel
        #     [R0, R1, R2, R3, ...]   # Right channel
        # ]

        # # What soundfile wants:
        # samples = [ is this called interleaved?
        #     [L0, R0],  # Frame 0
        #     [L1, R1],  # Frame 1
        #     [L2, R2],  # Frame 2
        #     ...
        # ]

        return {
            'sample_rate': sample_rate,
            'channels': num_channels,
            'bits_per_sample': bits_per_sample,
            'audio_format': audio_format,
            'data': audio_data,
            'num_frames': num_frames,
            'duration': num_frames / sample_rate,
            'samples': sample_array
        }
    
def write_wav(file, data, sample_rate, num_channels, bits_per_sample):
    
    # 1- Denormalize the samples
    # 2- Calculate sizes
    # 3- Write RIFF header
    # 4- Write fmt chunk
    # 5- Write data chunk

    int_samples = denormalize_samples(data, bits_per_sample, num_channels)

    audio_bytes = pack(int_samples, bits_per_sample, num_channels)

    bytes_per_sample = bits_per_sample // 8
    block_align = num_channels * bytes_per_sample
    byte_rate = sample_rate * block_align
    data_size = len(audio_bytes)
    # data_size = len(int_samples)
    fmt_chunk_size = 16
    file_size = 36 + data_size


    with open(file, 'wb') as f:
        # RIFF HEADER (12 bytes)
        f.write(b'RIFF')
        f.write(struct.pack('<I', file_size))
        f.write(b'WAVE')

        # FMT CHUNK (24 bytes)
        f.write(b'fmt ')
        f.write(struct.pack('<I', 16)) # subchunk size
        f.write(struct.pack('<H', 1)) # PCM
        f.write(struct.pack('<H', num_channels))
        f.write(struct.pack('<I', sample_rate))
        f.write(struct.pack('<I', byte_rate))
        f.write(struct.pack('<H', block_align))
        f.write(struct.pack('<H', bits_per_sample))

        # Write Data Chunk
        f.write(b'data')
        f.write(struct.pack('<I', data_size))
        f.write(audio_bytes)
        # f.write(int_samples)

def unpack16(audio_data, bits_per_sample):
    bytes_per_sample = bits_per_sample // 8

    samples = []

    # wave data standart is little endian 
    # byte1 is low, byte2 is high
    # 1- shift byte2 << 8
    # 2- use or statment to combine byte1 & byte2
    # 3- convert combined_value to signed
    # 4- if value >= 2**(bits_per_sample - 1) then value = value - 2**bitsperSample
    
    for i in range(0, len(audio_data), bytes_per_sample):
        byte1 = audio_data[i] # 0, 2, 4, 6, 8
        byte2 = audio_data[i + 1] # 1, 3, 5, 7

        # combine (little-endian)
        value = byte1 | (byte2 << 8) # shift byte2 left by 8 bit

        # convert to signed
        if value >= 2 ** (bits_per_sample - 1): # negative when (bits_p_s - 1)th bits is 1 or active
            value = value - (2 ** bits_per_sample)

        samples.append(value)
    return samples

def unpack(audio_data, bits_per_sample):
    # wave data standart is little endian 
    # byte1 is low, byte2 is high
    # 1- shift byte2 << 8
    # 2- use or statment to combine byte1 & byte2
    # 3- convert combined_value to signed
    # 4- if value >= 2**(bits_per_sample - 1) then value = value - 2**bitsperSample

    bytes_per_sample = bits_per_sample // 8

    samples = []
    
    for i in range(0, len(audio_data), bytes_per_sample):
        value = 0

        for j in range(bytes_per_sample):
            byte = audio_data[i + j]
            value = value | (byte << (8 * j)) # first iteration value = byte[0]
        
        # handle 8 bits as unsigned
        if bits_per_sample == 8:
            value = value - 128
        else:
            # convert to signed
            if value >= 2 ** (bits_per_sample - 1):
                value = value - (2 ** bits_per_sample)

        samples.append(value)
    return samples

def pack(audio_data, bits_per_sample, num_channels):
    bytes_per_sample = bits_per_sample // 8
    samples = []

    for sample in range(0, len(audio_data), 1):
        for channel in range(num_channels):
            for j in range(0, bytes_per_sample, 1):
                if j == bytes_per_sample - 1: # MSB
                    if audio_data[sample][channel] < 0:
                        samples.append(((audio_data[sample][channel] >> (8 * j)) & 0XFF) | 0X80)
                    else:
                        samples.append((audio_data[sample][channel] >> (8 * j)) & 0XFF)
                else: # LSB
                    samples.append((audio_data[sample][channel] >> (8 * j)) & 0XFF)

    return bytes(samples)
        
def normalize_samples(samples, bits_per_sample):

    
    normalized = []

    for sample in samples:
        normalized.append(sample / (2 ** (bits_per_sample - 1)))

    return normalized

def transpose_array(samples, num_channels):
    if num_channels == 1:
        return samples[0]
    
    '''
    the main goal is transpose 
    samples = [[1,2,3,4], [5,6,7,8]] left and right channel data to

    |
    v

    samples = [[1,5], [2,6], [3,7], [4,8]] 

    '''

    num_frames = len(samples[0]) # samples 0 is [1, 2, 3, 4] = 4
    
    frames = []
    for i in range(num_frames):

        frame = []
        for channel in range(num_channels):
            frame.append(samples[channel][i]) # i=0: frame = [samples[0][0], samples[1][0]] -> [1, 5]
        frames.append(frame) # [[1,5], [2,6], [3,7]]
    return frames

def denormalize_samples(samples, bits_per_sample, num_channels) -> dict:
    if num_channels == 1:
        for i in range(len(samples)):
            samples[i] *= (2 ** (bits_per_sample - 1))
            samples[i] = int(samples[i])
    elif num_channels >= 2:
        for i in range(len(samples)):
            for j in range(2):
                samples[i][j] *= (2 ** (bits_per_sample - 1))
                samples[i][j] = int(samples[i][j])
    return samples

def get_megabyte(file):
    wav_data = read_wav(file)
    sample_rate = wav_data['sample_rate']
    bits_per_sample = wav_data['bits_per_sample']
    num_channels = wav_data['channels']
    duration = wav_data['duration']

    bits_per_second = bits_per_sample * sample_rate * num_channels
    bytes_per_second = bits_per_second / 8
    total_bytes = bytes_per_second * duration

    megabytes = total_bytes / (1024 * 1024)
    return megabytes