import random

# Common public parameters (p should be a large prime in practice)
p = 23  
g = 5   

# Alice's side
a_private = 6
a_public = (g ** a_private) % p  # Alice sends this to Bob

# Bob's side
b_private = 15
b_public = (g ** b_private) % p  # Bob sends this to Alice

# Calculating the Shared Secret
alice_shared_secret = (b_public ** a_private) % p
bob_shared_secret = (a_public ** b_private) % p

print(f"Alice's Secret: {alice_shared_secret}")
print(f"Bob's Secret: {bob_shared_secret}")