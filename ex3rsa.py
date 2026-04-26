def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

# 1. Pick two primes
p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)

# 2. Choose public exponent e
e = 65537 # Common choice

# 3. Calculate private key d (modular inverse)
def extended_gcd(a, b):
    if a == 0: return b, 0, 1
    d, x1, y1 = extended_gcd(b % a, a)
    return d, y1 - (b // a) * x1, x1

_, d, _ = extended_gcd(e, phi)
d = d % phi # Ensure d is positive

# 4. Encryption/Decryption
msg = 42 # The "message" as a number
encrypted = pow(msg, e, n)
decrypted = pow(encrypted, d, n)

print(f"Original: {msg} | Encrypted: {encrypted} | Decrypted: {decrypted}")