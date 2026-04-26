def get_gcd(a, b):
    while b != 0:
        # a becomes b, b becomes the remainder of a / b
        a, b = b, a % b
    return a

# Example
# get_gcd(48, 18)
# 48 % 18 = 12 -> (18, 12)
# 18 % 12 = 6  -> (12, 6)
# 12 % 6 = 0   -> (6, 0)
# Result: 6