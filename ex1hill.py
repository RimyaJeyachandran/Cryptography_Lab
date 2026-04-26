import numpy as np

def hill_cipher_2x2(text, key_matrix, mode='encrypt'):
    # Prepare text: uppercase and remove non-alpha
    text = "".join(filter(str.isalpha, text.upper()))
    
    # Padding if the text length is odd
    if len(text) % 2 != 0:
        text += 'X'
    
    # If decrypting, we need the modular multiplicative inverse of the matrix
    if mode == 'decrypt':
        # Calculate determinant
        det = int(np.round(np.linalg.det(key_matrix)))
        # Find modular inverse of determinant (det * inv % 26 == 1)
        det_inv = pow(det % 26, -1, 26)
        
        # Adjugate matrix for 2x2: [[d, -b], [-c, a]]
        adjugate = np.array([
            [key_matrix[1,1], -key_matrix[0,1]],
            [-key_matrix[1,0], key_matrix[0,0]]
        ])
        # Inverse matrix mod 26
        key_matrix = (det_inv * adjugate) % 26

    result = ""
    # Process text in chunks of 2
    for i in range(0, len(text), 2):
        # Convert chars to numbers (0-25)
        vector = [ord(text[i]) - ord('A'), ord(text[i+1]) - ord('A')]
        # Matrix multiplication
        transformed = np.dot(key_matrix, vector) % 26
        # Convert back to chars
        result += chr(int(transformed[0]) + ord('A'))
        result += chr(int(transformed[1]) + ord('A'))
        
    return result

# Example Usage (Key matrix must be invertible mod 26)
# Key: [[3, 3], [2, 5]]
key = np.array([[3, 3], [2, 5]])
message = "HELP"
encrypted = hill_cipher_2x2(message, key, 'encrypt')
decrypted = hill_cipher_2x2(encrypted, key, 'decrypt')

print(f"Hill Encrypted: {encrypted}")
print(f"Hill Decrypted: {decrypted}")