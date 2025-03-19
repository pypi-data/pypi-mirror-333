import numpy as np
import os

def generate_random_bits(n):
    return np.random.randint(2, size=n)

def generate_random_bases(n):
    return np.random.randint(2, size=n)

def encode_qubits(bits, bases):
    return [(bit, base) for bit, base in zip(bits, bases)]

def measure_qubits(qubits, measurement_bases):
    measured_bits = []
    for (bit, base), measure_base in zip(qubits, measurement_bases):
        if base == measure_base:
            measured_bits.append(bit)
        else:
            measured_bits.append(np.random.randint(2))
    return measured_bits

def sift_key(alice_bases, bob_bases, alice_bits, bob_bits):
    return [alice_bits[i] for i in range(len(alice_bits)) if alice_bases[i] == bob_bases[i]]

def bb84_protocol(n=100):
    alice_bits = generate_random_bits(n)
    alice_bases = generate_random_bases(n)

    qubits = encode_qubits(alice_bits, alice_bases)

    bob_bases = generate_random_bases(n)
    bob_bits = measure_qubits(qubits, bob_bases)

    return sift_key(alice_bases, bob_bases, alice_bits, bob_bits)

def binary_to_text(binary_str):
    chars = [chr(int(binary_str[i:i+8], 2)) for i in range(0, len(binary_str), 8)]
    return ''.join(chars)

def text_to_binary(text):
    return ''.join(format(ord(c), '08b') for c in text)

def encrypt_message(message, key):
    message_bits = text_to_binary(message)

    if len(key) < len(message_bits):
        key.extend(generate_random_bits(len(message_bits) - len(key)))

    key_bits = ''.join(map(str, key[:len(message_bits)]))
    encrypted_bits = ''.join(str(int(m) ^ int(k)) for m, k in zip(message_bits, key_bits))
    return encrypted_bits

def decrypt_message(encrypted_bits, key):
    key_bits = ''.join(map(str, key[:len(encrypted_bits)]))
    decrypted_bits = ''.join(str(int(e) ^ int(k)) for e, k in zip(encrypted_bits, key_bits))
    return binary_to_text(decrypted_bits)
