import struct

# AES S-Box and helper tables (Simplified for readability)
SBOX = [...] # Keep your SBOX here

def aes_encrypt(block, round_keys):
    """Basic AES-128 encryption for a single 16-byte block."""
    state = list(block)
    
    # Initial Round
    for i in range(16): state[i] ^= round_keys[i]
    
    # 9 Rounds of substitution, shifting, mixing, and keys
    for r in range(1, 10):
        # Substitute bytes
        state = [SBOX[b] for b in state]
        # Shift rows (Manual index mapping)
        state = [state[0], state[5], state[10], state[15], state[4], state[9], state[14], state[3],
                 state[8], state[13], state[2], state[7], state[12], state[1], state[6], state[11]]
        # Mix Columns + Add Round Key (Abbreviated logic for space)
        # ... [Keep your existing MixColumns logic here] ...
    
    # Final Round (No MixColumns)
    # ... [Keep your existing Final Round logic here] ...
    return bytes(state)

def generate_subkeys(key_bytes):
    """Derives K1 and K2 for CMAC."""
    # Step 1: Encrypt a block of all zeros
    L = aes_encrypt(bytes(16), aes_key_expansion(key_bytes))
    
    def derive(val):
        msb = (val[0] >> 7) & 1
        # Shift left by 1 bit
        shifted = bytearray(16)
        overflow = 0
        for i in range(15, -1, -1):
            new_ov = (val[i] >> 7) & 1
            shifted[i] = ((val[i] << 1) | overflow) & 0xFF
            overflow = new_ov
        
        # If MSB was 1, XOR with the constant 0x87 (Rb)
        if msb:
            shifted[15] ^= 0x87
        return bytes(shifted)

    k1 = derive(L)
    k2 = derive(k1)
    return k1, k2

def compute_cmac(key, message):
    """Main CMAC calculation logic."""
    r_keys = aes_key_expansion(key)
    k1, k2 = generate_subkeys(key)
    
    # Determine padding needs
    block_size = 16
    n_blocks = (len(message) + block_size - 1) // block_size
    if n_blocks == 0: n_blocks = 1 # Handle empty message case
    
    is_complete = (len(message) > 0 and len(message) % block_size == 0)
    
    # CBC-MAC Chaining
    prev_block = bytes(16)
    for i in range(n_blocks - 1):
        chunk = message[i*block_size : (i+1)*block_size]
        mixed = bytes(x ^ y for x, y in zip(prev_block, chunk))
        prev_block = aes_encrypt(mixed, r_keys)

    # Final Block processing
    last_chunk = message[(n_blocks-1)*block_size:]
    if is_complete:
        # XOR with K1 if block is full
        final_input = bytes(x ^ y ^ z for x, y, z in zip(prev_block, last_chunk, k1))
    else:
        # Pad with 0x80... and XOR with K2
        padded = last_chunk + b'\x80' + b'\x00' * (block_size - len(last_chunk) - 1)
        final_input = bytes(x ^ y ^ z for x, y, z in zip(prev_block, padded, k2))
    
    return aes_encrypt(final_input, r_keys)

# Usage example
master_key = bytes.fromhex("2b7e151628aed2a6abf7158809cf4f3c")
msg = input("Enter message: ").encode()
print(f"Resulting Tag: {compute_cmac(master_key, msg).hex()}")