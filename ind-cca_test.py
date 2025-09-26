import aes_ctr

def try_api():
    if hasattr(aes_ctr, "encrypt") and hasattr(aes_ctr, "decrypt"):
        def enc(p,key):
                return aes_ctr.encrypt(p,key)
        def dec(c, key):
                return aes_ctr.decrypt(c, key)
        return enc, dec

def flip_byte_in_ciphertext(ct, idx=16):
    if idx >= len(ct):
        raise IndexError(f"Index {idx} out of range for ciphertext of length {len(ct)}")
    b = bytearray(ct)
    b[idx] ^= 1  # flip least significant bit of chosen byte
    return bytes(b)

def ind_cca_ctr_test():
    print("\n================ IND-CCA Attack Test on AES-CTR ================\n")
    enc, dec = try_api()

    # Choose two challenge messages of same length that differ in a predictable way.
    m0 = bytes([0]*16)  #all zeros
    m1 = bytes([0]*16) #all zeros
    m1 = bytearray(m1); m1[0] = 1 #first byte is 1
    m1 = bytes(m1)  #convert back to bytes

    for actual_b, m in [(0, m0), (1, m1)]:
        print("\n--- IND-CCA Test Case: b = {} ---".format(actual_b))
        print("Original message (m):", m.hex())

        key = aes_ctr.keygen()
        print("Generated key:", key.hex() if hasattr(key, 'hex') else key)

        c_star = enc(m, key) #challenge ciphertext
        print("Ciphertext (c_star):", c_star.hex())
        print("Challenge ciphertext length:", len(c_star))

        # Attacker now modifies c* to get c' (allowed under CCA since c' != c*)
        c_prime = flip_byte_in_ciphertext(c_star, idx=16)    #modified ciphertext
        print("Modified ciphertext (c_prime):", c_prime.hex())
        print("Difference at first byte (nonce excluded) : c_star[16]={}, c_prime[16]={}".format(c_star[16], c_prime[16]))

        if c_prime == c_star:
            raise RuntimeError("c' should differ from c* (unexpected).")

        m_prime = dec(c_prime, key)

        # m_prime = m XOR delta  where delta is the same bit flipped in ciphertext.
        # Because we flipped the first byte LSB, we can check byte 0 to distinguish.
        guessed_b = 0 if (m_prime[0] & 1) else 1
        print("Actual b:", actual_b, "Recovered guess:", guessed_b)

        assert guessed_b == actual_b, "Attack failed for case b = {}".format(actual_b)

        print("Original message (m):", m.hex())
        print("Decrypted original message (should match m):", dec(c_star, key).hex())

        # Now ask the decryption oracle to decrypt c' (allowed under CCA since c' != c*)
        print("Decrypted modified message (m_prime):", m_prime.hex())
        print("m_prime[0]:", m_prime[0])
        print("--- End of IND-CCA Test Case: b = {} ---\n".format(actual_b))

    print("================ End IND-CCA Attack Test on AES-CTR ================\n")

if __name__ == "__main__":
    ind_cca_ctr_test()