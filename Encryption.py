import random
import math
import json

def str2ascii(st):
    return [ord(c) for c in st]

def is_prime(n):
    if n <= 1: return False
    if n <= 3: return True
    if n % 2 == 0 or n % 3 == 0: return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0: return False
        i += 6
    return True

def generate_prime(bits):
    while True:
        candidate = random.getrandbits(bits)
        candidate |= (1 << bits - 1) | 1  # Ensure it's of proper length and odd
        if is_prime(candidate): return candidate

def generate_keys(bits):
    p = generate_prime(bits)
    q = generate_prime(bits)
    while p == q:
        q = generate_prime(bits)
    n = p * q
    phi = (p - 1) * (q - 1)
    e = random.randrange(3, phi, 2)
    while math.gcd(e, phi) != 1:
        e = random.randrange(3, phi, 2)
    d = pow(e, -1, phi)
    return p, q, e, d, n

def encrypt(ascii_list, e, n):
    return [pow(m, e, n) for m in ascii_list]

# --- MAIN LOGIC ---
bit_length = int(input(" Enter bit length for primes (e.g., 16, 32, 64): "))
message = input("  Enter message to encrypt: ")
ascii_msg = str2ascii(message)

p, q, e, d, n = generate_keys(bit_length)
cipher = encrypt(ascii_msg, e, n)

# Save to file
with open("rsa_encrypted_data.json", "w") as f:
    json.dump({
        "ciphertext": cipher,
        "public_key": {"e": e, "n": n},
        "private_key": {"d": d, "n": n},
        "primes": {"p": p, "q": q},
        "original_ascii": ascii_msg
    }, f, indent=2)

# --- Display Info ---
print("\n Keys Generated:")
print(f"  p = {p}")
print(f"  q = {q}")
print(f"  n = {n}")
print(f"  e (public exponent) = {e}")
print(f"  d (private exponent) = {d}")

print(f"\n Public Key: (e={e}, n={n})")
print(f" Private Key: (d={d}, n={n})")

print(f"\n Original Message: '{message}'")
print(f" ASCII Encoding: {ascii_msg}")
print(f" Encrypted Ciphertext: {cipher}")
print(f"\n Data saved to 'rsa_encrypted_data.json'")

