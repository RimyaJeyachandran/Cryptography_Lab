import math

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True # 2 and 3 are prime
    if n % 2 == 0 or n % 3 == 0:
        return False # Eliminate multiples of 2 and 3 early
    
    # Check from 5 to sqrt(n), skipping even numbers
    for i in range(5, int(math.sqrt(n)) + 1, 6):
        if n % i == 0 or n % (i + 2) == 0:
            return False
    return True