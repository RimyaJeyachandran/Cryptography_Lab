# Simplified AES-128 structure for readability
SBOX = [ ... ] # 256-value lookup table

def sub_bytes(state):
    """Replace each byte in the state with its corresponding S-Box value."""
    for i in range(16):
        state[i] = SBOX[state[i]]
    return state

def shift_rows(s):
    """Perform a cyclic shift on the rows of the state matrix."""
    return [s[0], s[5], s[10], s[15],  # Row 0: No shift
            s[4], s[9], s[14], s[3],   # Row 1: Shift 1
            s[8], s[13], s[2], s[7],   # Row 2: Shift 2
            s[12], s[1], s[6], s[11]]  # Row 3: Shift 3

def mix_columns(s):
    """Mix the data within each column to provide diffusion."""
    # (Simplified representation of the Galois Field multiplication logic)
    for i in range(0, 16, 4):
        a, b, c, d = s[i:i+4]
        s[i]   = (xtime(a) ^ (xtime(b) ^ b) ^ c ^ d) & 0xFF
        s[i+1] = (a ^ xtime(b) ^ (xtime(c) ^ c) ^ d) & 0xFF
        s[i+2] = (a ^ b ^ xtime(c) ^ (xtime(d) ^ d)) & 0xFF
        s[i+3] = ((xtime(a) ^ a) ^ b ^ c ^ xtime(d)) & 0xFF
    return s

def encrypt_block(plaintext, master_key):
    """Main AES encryption loop."""
    round_keys = expand_key(master_key) # Generate 11 keys (16 bytes each)
    
    # Initial Round
    state = xor_blocks(plaintext, round_keys[0])
    
    # Middle 9 Rounds
    for r in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = xor_blocks(state, round_keys[r])
        
    # Final Round (No MixColumns)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = xor_blocks(state, round_keys[10])
    
    return state