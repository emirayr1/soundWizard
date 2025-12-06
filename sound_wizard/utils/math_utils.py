import numpy as np


def _len(array):
    count = 0
    for x in array:
        count += 1
    return count

def _sum(array):
    if _len(array) > 0 and isinstance(array[0], list):
        raise ValueError("Cannot calculate 2d or higher array") 
    sum = 0
    for x in array:
        sum += x
    return sum

def _sqrt(x):
    '''
    Calculate square root
    '''

    return x ** 0.5

def _mean(numbers):
    '''
    Calculate arithmetic mean (average) of numbers
    '''

    if _len(numbers) == 0:
        raise ValueError("Cannot calculate mean of empty numbers!")
    
    total = _sum(numbers)
    return total / _len(numbers)

def lerp(start, end, t):
    if t < 0: t=0
    if t > 1: t=1
    
    return start + (end - start) * t

def remap(value, old_min, old_max, new_min, new_max):
    percentage = (value - old_min) / (old_max - old_min)
    
    return new_min + (new_max - new_min) * percentage

def distance(point_a, point_b):
    dx = point_b[0] - point_a[0]
    dy = point_b[1] - point_a[1]
    
    return _sqrt(dx * dx + dy * dy)

def amp_to_db(amplitude):
    # Protect against zero (silence)
    if amplitude <= 0:
        return -100.0 # A "noise floor" lower limit
        
    return 20 * np.log10(amplitude)

def db_to_amp(db):
    # The inverse: Amplitude = 10^(dB/20)
    return 10 ** (db / 20)