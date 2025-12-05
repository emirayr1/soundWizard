import matplotlib.pyplot as plt
import numpy as np

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

