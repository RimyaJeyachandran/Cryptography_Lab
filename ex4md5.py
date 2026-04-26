import math

def calculate_md5(message):
    # Initial state (The magic numbers)
    a0 = 0x67452301
    b0 = 0xefcdab89
    c0 = 0x98badcfe
    d0 = 0x10325476

    # Generate constants K[0..63] using sine
    K = [int(abs(math.sin(i + 1)) * (2**32)) & 0xFFFFFFFF for i in range(64)]
    
    # Rotation amounts for each round
    S = [7, 12, 17, 22] * 4 + [5, 9, 14, 20] * 4 + [4, 11, 16, 23] * 4 + [6, 10, 15, 21] * 4

    # --- Padding ---
    msg = bytearray(message, 'utf-8')
    orig_len_bits = (len(msg) * 8) & 0xFFFFFFFFFFFFFFFF
    
    msg.append(0x80)
    while (len(msg) * 8) % 512 != 448:
        msg.append(0x00)
    
    # MD5 is little-endian, including the length suffix
    msg += orig_len_bits.to_bytes(8, 'little')

    # --- Main Loop ---
    for offset in range(0, len(msg), 64):
        chunk = msg[offset : offset+64]
        M = [int.from_bytes(chunk[i:i+4], 'little') for i in range(0, 64, 4)]
        
        a, b, c, d = a0, b0, c0, d0
        
        for i in range(64):
            if i < 16:
                f = (b & c) | ((~b) & d)
                g = i
            elif i < 32:
                f = (d & b) | ((~d) & c)
                g = (5 * i + 1) % 16
            elif i < 48:
                f = b ^ c ^ d
                g = (3 * i + 5) % 16
            else:
                f = c ^ (b | (~d))
                g = (7 * i) % 16
            
            # Rotation and update
            rotate_val = (a + f + K[i] + M[g]) & 0xFFFFFFFF
            new_b = (b + ((rotate_val << S[i]) | (rotate_val >> (32 - S[i])))) & 0xFFFFFFFF
            
            # Shift variables for next round
            a, d, c, b = d, c, b, new_b
            
        # Add round results to running total
        a0 = (a0 + a) & 0xFFFFFFFF
        b0 = (b0 + b) & 0xFFFFFFFF
        c0 = (c0 + c) & 0xFFFFFFFF
        d0 = (d0 + d) & 0xFFFFFFFF

    # Format result back to little-endian hex string
    return "".join(f"{x:02x}" for x in struct.pack('<IIII', a0, b0, c0, d0))

if __name__ == "__main__":
    user_input = "good"
    print(f"MD5 Hash: {calculate_md5(user_input)}")