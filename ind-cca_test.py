import aes_ctr as aes_ctr

def perform_attack(ciphertext, original_byte, desired_flipped_value, plaintext):
  
    ciphertext = bytearray(ciphertext)  # make mutable
    original_ord = ord(original_byte)
    desired_ord = ord(desired_flipped_value)

    # Iterate over all bytes in plaintext
    for i, p_byte in enumerate(plaintext.encode()):  # convert plaintext to bytes
        if p_byte == original_ord:
            # compute mask and flip ciphertext byte
            d_mask = original_ord ^ desired_ord
            ciphertext[i] ^= d_mask

    return bytes(ciphertext)


if __name__ == "__main__":
    # Message
    print("We will be using a string that in reality could carry important information and tampering/bit flipping would have serious consequences.")
    
    raw_message = "userid=123;username=test;admin=0"
    print(f"Raw message: {raw_message}")
    print("---------------------------------------------------------------------------------------")

    # AES-CTR encryption
    key = aes_ctr.keygen()
    encrypted_message = aes_ctr.encrypt(raw_message, key)
    
    #Attack
    print("Our goal is to bit flip the admin=0 -> admin=1, thus to alleviate authorization.")
    print("For this we will locate the bit 0 and try to change it to 1 using XOR mask.")
    print("---------------------------------------------------------------------------------------")
    
    altered_message = perform_attack(encrypted_message,"0","1",raw_message)

    # Decrypt the altered message
    print("Checking decrypted altered message")
    encrypted_message = aes_ctr.encrypt(raw_message, key)
    decrypted_altered_message = aes_ctr.decrypt(altered_message, key)
    print(decrypted_altered_message)