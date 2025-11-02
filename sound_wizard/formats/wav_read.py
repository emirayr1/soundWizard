import struct
import os

def read_wav(filename):
    """
    Read and parse a WAV audio file.
    
    Args:
        filename: Path to the WAV file
        
    Returns:
        dict:
            - sample_rate: Sample rate in Hz (e.g., 44100)
            - channels: Number of audio channels (1=mono, 2=stereo)
            - bits_per_sample: Bit depth (e.g., 16, 24, 32)
            - audio_format: Audio format (1=PCM)
            - data: Raw audio data as bytes
            - num_frames: Number of audio frames
            
    Raises:
        ValueError: If file is not a valid WAV file
        FileNotFoundError: If file doesn't exist
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"File not found: {filename}")
    
    with open(filename, 'rb') as f:
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
        
        return {
            'sample_rate': sample_rate,
            'channels': num_channels,
            'bits_per_sample': bits_per_sample,
            'audio_format': audio_format,
            'data': audio_data,
            'num_frames': num_frames,
            'duration': num_frames / sample_rate # seconds
        }
