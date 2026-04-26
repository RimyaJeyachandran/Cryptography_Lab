def vigenere_cipher(text, key, mode='encrypt'):
    result = []
    key = key.upper()
    key_index = 0
    
    for char in text:
        if char.isalpha():
            # Determine shift based on the current key character
            shift = ord(key[key_index % len(key)]) - ord('A')
            if mode == 'decrypt':
                shift = -shift
                
            start = ord('A') if char.isupper() else ord('a')
            new_char = chr((ord(char) - start + shift) % 26 + start)
            result.append(new_char)
            
            # Only move to the next key letter if we actually processed a character
            key_index += 1
        else:
            result.append(char)
            
    return "".join(result)

# Example Usage
key = "LUCID"
message = "Python is fun"
encrypted = vigenere_cipher(message, key, 'encrypt')
print(f"Vigenere Encrypted: {encrypted}")