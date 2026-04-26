def shift_cipher(text, shift, mode='encrypt'):
    result = ""
    # Adjust shift for decryption
    if mode == 'decrypt':
        shift = -shift
    
    for char in text:
        if char.isalpha():
            # Stay within the bounds of A-Z or a-z
            start = ord('A') if char.isupper() else ord('a')
            # The modulo 26 ensures we wrap around the alphabet
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result += new_char
        else:
            # Keep spaces and punctuation as they are
            result += char
    return result

# Example Usage
message = "Hello World"
encrypted = shift_cipher(message, 3, 'encrypt')
print(f"Shift Encrypted: {encrypted}")