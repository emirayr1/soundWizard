
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
