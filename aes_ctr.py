import os
from Crypto.Cipher import AES

# Generate a random 128-bit AES key
def keygen():
    return os.urandom(16)

# Convert integer to AES block of given length
def int_to_block(x, length):
   return x.to_bytes(length, byteorder="big")

# XOR two byte sequences (used for CTR mode keystream)
def xor_bytes(data, keystream) -> bytes:
    if isinstance(data, str): data = data.encode("utf-8")
    if isinstance(keystream, str): keystream = keystream.encode("utf-8")
    return bytes(d ^ k for d, k in zip(data, keystream[:len(data)]))

# Encrypt plaintext using AES-CTR mode
def encrypt(message_plaintext, key):
    blocksize = 16
    nonce = os.urandom(blocksize)
    aes_ecb = AES.new(key, AES.MODE_ECB)
    total_length = len(message_plaintext)
    cyphertext = bytearray()
    number_of_blocks = (total_length + blocksize - 1) // blocksize 
    for block_index in range(number_of_blocks):
        counter_bytes = int_to_block(block_index, blocksize)
        counter_block = nonce[:8] + counter_bytes[8:]
        keystream = aes_ecb.encrypt(counter_block)
        start_byte = block_index * blocksize
        end_byte = min(start_byte + blocksize, total_length)
        plaintext_block = message_plaintext[start_byte:end_byte]
        cyphertext_block = xor_bytes(plaintext_block, keystream[:len(plaintext_block)])
        cyphertext.extend(cyphertext_block)
    return nonce + bytes(cyphertext)

# Decrypt ciphertext using AES-CTR mode
def decrypt(ciphertext, key):
    blocksize = 16
    nonce = ciphertext[:blocksize]
    ciphertext_body = ciphertext[blocksize:]
    aes_ecb = AES.new(key, AES.MODE_ECB)
    total_length = len(ciphertext_body)
    plaintext = bytearray()
    number_of_blocks = (total_length + blocksize - 1) // blocksize 
    for block_index in range(number_of_blocks):
        counter_bytes = int_to_block(block_index, blocksize)
        counter_block = nonce[:8] + counter_bytes[8:]
        keystream = aes_ecb.encrypt(counter_block)
        start_byte = block_index * blocksize
        end_byte = min(start_byte + blocksize, total_length)
        ciphertext_block = ciphertext_body[start_byte:end_byte]
        plaintext_block = xor_bytes(ciphertext_block, keystream[:len(ciphertext_block)])
        plaintext.extend(plaintext_block)
    return bytes(plaintext)

if __name__ == "__main__":
    # Example usage and test
    raw_message = "comment=hello;userdata=abc;admin=0;end"
    print(f"Raw message: {raw_message}")
    key = keygen()
    encrypted_message = encrypt(raw_message, key)
    print(f"Encrypted message: {encrypted_message}")
    decrypted_message = decrypt(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")
    print("Key used: ", key)
    decoded_message_as_string = decrypted_message.decode("utf-8")
    print("Decryption: success" if decoded_message_as_string == raw_message else f"Decryption: fail \n  Raw message: {raw_message} \n  Decrypted message: {str(decrypted_message)}")