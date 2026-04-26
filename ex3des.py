# Initial and Final Permutations
IP = [58, 50, 42, 34, 26, 18, 10, 2, ...] 
FP = [40, 8, 48, 16, 56, 24, 64, 32, ...]

def feistel_function(right_half, subkey):
    """The core 'F' function of DES."""
    # 1. Expansion (32-bit to 48-bit)
    expanded = expand(right_half)
    
    # 2. Key Mixing
    mixed = xor(expanded, subkey)
    
    # 3. Substitution (Using 8 S-Boxes)
    substituted = sbox_lookup(mixed)
    
    # 4. Permutation (P-Box)
    return p_box_permutation(substituted)

def des_encrypt(block, key):
    """Standard DES encryption flow."""
    # Step 1: Initial Permutation
    block = permute(block, IP)
    left, right = block[:32], block[32:]
    
    # Step 2: 16 Rounds of Feistel Network
    subkeys = generate_16_subkeys(key)
    for i in range(16):
        temp = right
        # New Right = Old Left XOR F(Old Right, Round Key)
        right = xor(left, feistel_function(right, subkeys[i]))
        left = temp
        
    # Step 3: Final Swap and Permutation
    combined = right + left # Note the final swap
    return permute(combined, FP)