import matplotlib.pyplot as plt
import numpy as np

#add taylor series sine wave 
       
class WINDOW:
    def __init__(self, N):
        self.N = N
        self.n = np.arange(N)
        
    def rectangular(self):
        return np.ones(self.N)
    
    def hanning(self):
        # Formula: 0.5 - 0.5 * cos(2*pi*n / (N-1))
        return 0.5 - 0.5 * np.cos((2 * np.pi * self.n) / (self.N - 1))

    def hamming(self):
        # Formula: 0.54 - 0.46 * cos(2*pi*n / (N-1))
        return 0.54 - 0.46 * np.cos((2 * np.pi * self.n) / (self.N - 1))

    def blackman(self):
        # Formula: 0.42 - 0.5*cos(...) + 0.08*cos(...)
        term1 = 0.5 * np.cos((2 * np.pi * self.n) / (self.N - 1))
        term2 = 0.08 * np.cos((4 * np.pi * self.n) / (self.N - 1))
        return 0.42 - term1 + term2
    
    def bartlett(self):
        # Triangle window
        # Math: 1 - | (n - (N-1)/2) / ((N-1)/2) |
        return 1.0 - np.abs((self.n - (self.N - 1) / 2.0) / ((self.N - 1) / 2.0))

def time_domain_convolution(signal, kernel):

    N = len(signal)
    M = len(kernel)

    output_length = N + M - 1

    output = [0] * output_length

    for n in range(output_length):
        accumulator = 0

        # formula: y[n] = sum(signal[n-k] * kernel[k])
        for k in range(M):
            if (n-k) >= 0 and (n-k) < N:
                accumulator += signal[n-k] * kernel[k]

            output[n] = accumulator
    
    return output

def frequency_domain_convolution(signal, kernel):

    N = len(signal)
    M = len(kernel)

    fft_length = N + M - 1

    signal_f = np.fft.fft(signal, fft_length)
    kernel_f = np.fft.fft(kernel, fft_length)

    output_frequency_domain = signal_f * kernel_f # in frequency domain multiplication

    output_time_domain = np.fft.ifft(output_frequency_domain) # return time domain

    return np.real(output_time_domain) # only real part

def discrete_fourier_transform(x):

    N = len(x)
    X = []

    for k in range(N):
        re = 0
        im = 0

        for n in range(N):
            euler = -2 * np.pi * k * n / N

            re += x[n] * np.cos(euler)
            im += x[n] * np.sin(euler)
        
        X.append(complex(re, im))
    
    return X

def fft_core(x, dir):

    """ 
    *Recursive Cooley-Tukey FFT

    dir: -1 FFT, +1 IFFT e^(dir)2pi_j

    Twiddle Factor = time shift for odd part of the signal 

    evens = [A, B, C, D]
    odds = [x, y, z, w]

    len = 8,  angle = 360 / 8 = 45

    first half (adding)
    1 - A + (x -> 0dg)
    2 - B + (y -> 45dg)
    3 - C + (z -> 90dg)
    4 - D + (w -> 135dg)

    second half (sub)
    1 - A - (x -> 0dg)
    2 - B - (y -> 45dg)
    3 - C - (z -> 90dg)
    4 - D - (w -> 135dg)
    
    output[k] = evens[k] + turned_odds # adding
    output[k + len / 2] = evens[k] - turned_odds # sub

    """
    # add numpy vectorization later TODO TODO TODO TODO
    
    N = len(x)

    if N <= 1: # Recursion's Base Case
        return x # Here is the number
    
    evens = fft_core(x[0::2], dir) # A, solve this
    odds = fft_core(x[1::2], dir) # B, solve this

    # odds and evens are calculated on this part

    # combine
    # each odd index shifts according to their k / N angle
    T = [np.exp(dir * 2j * np.pi * k / N) * odds[k] for k in range(N // 2)] 

    left_part = [evens[k] + T[k] for k in range(N // 2)]
    right_part = [evens[k] - T[k] for k in range(N // 2)]

    return left_part + right_part # -> complex array output

def fft(x):
    return fft_core(x, dir=-1)

def ifft(x):
    raw_output = fft_core(x, dir=1)
    N = len(x)

    normalized_output = [value / N for value in raw_output]
    return normalized_output

def fft_freq(n, d=1.0):
    """
    Docstring for fft_freq
    
    :param n: Signal Length (Total number of samples)
    :param d: Time Difference (1/fs)
    """

    step_length = 1.0 / (n * d)

    # FFT OUTPUT IS: [0, 1, 2, ... | ... -3, -2, -1]
    # positive is 0 -> n//2 - 1
    # negative is - n//2 -> 0
    positive_indexes = list(range(0, (n+1) // 2)) 
    negative_indexes = list(range(-(n//2), 0))

    all_indexes = positive_indexes + negative_indexes

    result = [index * step_length for index in all_indexes]

    return result

def stft(signal, frame_size, hop_size, window_func):
    # study this later TODO TODO TODO TODO
    
    signal_len = len(signal)
    
    num_frames = 1 + (signal_len - frame_size) // hop_size
    
    stft_matrix = []
    
    # m=0: [10 20 30 40] m=1: [30 40 50 60] m=2: [50 60 70 80]
    for m in range(num_frames):
        start_index = m * hop_size
        end_index = start_index + frame_size
        
        chunk = signal[start_index:end_index]
        windowed_chunk = chunk * window_func
        
        fft_result = fft(windowed_chunk)
        fft_result = fft_result[:frame_size // 2]
        
        stft_matrix.append(fft_result)
        
        return np.array(stft_matrix).T

def auto_correlation(x):
    N = len(x)
    result = np.correlate(x, x, mode='full')
    return result[N-1:]

def cross_corelation(x, y):
    N = len(x)
    result = np.correlate(x, y, mode='full')
    return result[N-1:]

def plot_fft(_time, _original_signal, _freq_axis_half, _fft_mag_half):

    # --- ADIM 4: ÇİZİM (PLOTTING) ---
    plt.figure(figsize=(12, 8)) # Geniş bir tuval açalım

    # 1. GRAFİK: ZAMAN ALANI (Time Domain)
    plt.subplot(2, 1, 1) # 2 satır, 1 sütunluk yerin 1.si
    plt.plot(_time, _original_signal, color='blue')
    plt.title("Zaman Alanı Sinyali (Karışık 5Hz + 20Hz)")
    plt.xlabel("Zaman (saniye)")
    plt.ylabel("Genlik")
    plt.grid(True, linestyle='--', alpha=0.6)

    # 2. GRAFİK: FREKANS ALANI (Frequency Domain)
    plt.subplot(2, 1, 2) # 2 satır, 1 sütunluk yerin 2.si
    # Çubuk grafik (stem plot) frekansları daha net gösterir
    plt.stem(_freq_axis_half, _fft_mag_half, basefmt=" ", linefmt='red', markerfmt='ro')

    plt.title("Frekans Alanı (FFT Sonucu)")
    plt.xlabel("Frekans (Hz)")
    plt.ylabel("Büyüklük (Magnitude)")
    plt.grid(True, linestyle='--', alpha=0.6)

    # X eksenini sınırlayalım ki net görelim (0 ile 40 Hz arası yeterli)
    plt.xlim(0, 40)

    plt.tight_layout() # Grafikler birbirine girmesin
    plt.show()

# fs = 128
# t = np.arange(0, 1, 1/fs)
# N = fs
# signal = np.sin(2*np.pi*5*t) + 0.5 * np.sin(2*np.pi*20*t)

# fft_output = fft(signal)

# # magnitude = sqrt(a^2 + b^2)
# fft_magnitude = np.abs(fft_output) / (N / 2)

# freq_axis = fft_freq(N, 1/fs)

# fft_mag_half = fft_magnitude[:N // 2]
# freq_axis_half = freq_axis[:N // 2]


# plot_fft(t, signal, freq_axis_half, fft_mag_half)