import os
from Crypto.Cipher import AES

#1. KeyGen()
def keygen():
    """Generate a random 128-bit AES key."""
    return os.urandom(16)

# Helper functions for encryption

# Turns numbers into AES-ready blocks
def int_to_block(x, length):
   return x.to_bytes(length, byteorder="big")

# The actual scrambling/descrambling step.
def xor_bytes(data, keystream) -> bytes:
    # https://www.reddit.com/r/learnpython/comments/zz76oc/how_would_i_xor_2_bytes_objects/

    if isinstance(data, str):
        data = data.encode("utf-8")
    if isinstance(keystream, str):
        keystream = keystream.encode("utf-8")

    return bytes(d ^ k for d, k in zip(data, keystream[:len(data)]))

# def xor_bytes_c(ciphertext_block,keystream):
#     n = min(len(ciphertext_block), n(keystream))
#     return bytes(x ^ y for x, y in zip(ciphertext_block[:n], keystream[:n]))


def increment_counter(counter):
   # moves the bits to the left
   shift = (1 << 128) - 1
   return(counter + 1) & shift


# 2. Encryption
    # Block size is 16 but im not sure if we should just use the int or a variable
def encrypt(message_plaintext, key):
    # Set block size to 16 --> 128 bits --> 16 bytes
    blocksize = 16

    # Generate number used only once
    # nonce = os.urandom(blocksize)

    # Encrypt using AES library
    aes_ecb = AES.new(key, AES.MODE_ECB)

    total_length = len(message_plaintext)

    # Initialize counter and future block of ciphertext
    counter = 0
    cyphertext = bytearray()

    number_of_blocks = (total_length + blocksize - 1) // blocksize 
    for block_index in range(number_of_blocks):

            # add the counter value an put it together with the nonce
            counter_bytes = int_to_block(counter + block_index, blocksize)
            index_split = (blocksize//2)
            counter_block = key[:index_split] + counter_bytes[index_split:]

            # encrypt the counter block with aes
            keystream = aes_ecb.encrypt(counter_block)

            # Get plaintext block to be encrypted
            start_byte = block_index * blocksize     #Get the full first byte
            end_byte = min(start_byte + blocksize, total_length)
            plaintext_block = message_plaintext[start_byte:end_byte]
            
            #XOR keystream with plaintet block
            cyphertext_block = xor_bytes(plaintext_block, keystream[:len(plaintext_block)])

            cyphertext.extend(cyphertext_block)

            #increment the counter
            counter = increment_counter(counter) 
    
    return bytes(cyphertext), key


# 3 Decrypt()
def decrypt(ciphertext,key):
    #since decrypt is symmetrical, the same method should work for this
    plaintext, nonce = encrypt(ciphertext, key)
    return plaintext, nonce



if __name__ == "__main__":
    
    #Testing 1
    # Message
    raw_message = "Toto je elektro ty obmedzeny kokotko"
    print("Raw message")
    
    #KeyGen()
    key = keygen()

    #encryption
    encrypted_message, nonce_used = encrypt(raw_message, key)
    
    print(f"Encrypted message (first 100 chars): {encrypted_message[:100]}")
    print(f"Encrypted message (first 100 chars) in hex vals: {encrypted_message[:100].hex()}")

    # decryption
    decrypted_message = decrypt(encrypted_message, key)
    print(f"Decrypted message: {decrypted_message}")