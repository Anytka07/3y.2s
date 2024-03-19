import math
import string

# Define the English alphabet
alphabet = string.ascii_uppercase + ' '

# Define the substitution table
substitution_table = {
    'A': '00', 'B': '01', 'C': '02', 'D': '03', 'E': '04',
    'F': '05', 'G': '06', 'H': '07', 'I': '08', 'J': '09',
    'K': '10', 'L': '11', 'M': '12', 'N': '13', 'O': '14',
    'P': '15', 'Q': '16', 'R': '17', 'S': '18', 'T': '19',
    'U': '20', 'V': '21', 'W': '22', 'X': '23', 'Y': '24',
    'Z': '25', ' ': '26'
}

substitution_table_inv = {value: key for key, value in substitution_table.items()}

# Step 1: Choose two prime numbers
p = 3
q = 11

# Step 2: Compute n
n = p * q

# Step 3: Compute Euler's totient function
phi = (p - 1) * (q - 1)

# Step 4: Choose e
e = 7
while 1 < e < phi:
    if math.gcd(e, phi) == 1:
        break
    else:
        e += 1

# Step 5: Calculate d
d = 3

# Read plaintext from file
with open('message.txt', 'r') as file:
    plaintext = file.read().strip()

# Convert plaintext to uppercase
plaintext = plaintext.upper()

# Encrypt the plaintext using the substitution table
encrypted_message = ' '.join(substitution_table[char] for char in plaintext)
print(f'Original message: {plaintext}')
print(f'Encrypted message: {encrypted_message}')

# Convert encrypted message to integers
encrypted_numbers = [int(num) for num in encrypted_message.split()]

# Encryption
encrypted = [pow(num, e, n) for num in encrypted_numbers]
#print(f'Encrypted numbers: {encrypted}')

# Calculate the hash
hash_value = sum(map(int, encrypted_message.split())) % 33
print(f'Hash value: {hash_value}')

# Decryption
decrypted = [pow(num, d, n) for num in encrypted]
print(f'Decrypted numbers: {decrypted}')

# Map decrypted numbers back to original range (0-32)
decrypted = [num % 27 for num in decrypted]

# Convert decrypted numbers back to characters
decrypted_message = ''.join(substitution_table_inv[str(num).zfill(2)] for num in decrypted)
print(f'Decrypted message: {decrypted_message}')

# Calculate the hash of the decrypted message
decrypted_hash = sum(decrypted) % 33
print(f'Decrypted hash: {decrypted_hash}')

# Verify the integrity of the message
if hash_value == decrypted_hash:
    print("Integrity verified: Original message and decrypted message hashes match.")
else:
    print("Integrity verification failed: Hashes do not match. The message may have been tampered with.")