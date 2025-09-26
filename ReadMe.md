AES-CTR IND-CCA Assignment
--------------------------------------------
- Compilation and Installation
  - Prerequisites
      - Python 3.8+
      - pycryptodome library for AES block cipher operations

      - Install prerequisites with:

        sudo apt update
        sudo apt install python3 python3-pip
        pip3 install pycryptodome

- Files
  - aes_ctr.py: Implements AES-CTR encryption, decryption, and key generation.
  - ind-cca_test.py: Contains tests for correctness and IND-CCA attack.

- Running the Tests
    To run the correctness and IND-CCA attack tests, execute:
    python3 ind-cca_test.py

  - Expected output:
    The script prints the original message, ciphertext, modified ciphertext, and decrypted outputs.
    For both test cases, the IND-CCA attack should succeed, demonstrating that CTR mode is not IND-CCA secure.

    The output should end with:
    "IND-CCA attack on CTR succeeded for both test messages."

---------------------------------------------------------------------------------------------
- General Approach
  - Key Generation: Uses os.urandom to generate a random 128-bit AES key.
  - Nonce Generation: For each encryption, a random 128-bit nonce is generated using os.urandom. The nonce is prepended to the ciphertext and used as part of the counter block for AES-CTR.
  - Encryption (CTR mode): Splits the plaintext into 16-byte blocks. For each block, a counter is combined with part of the key to form the input to AES-CTR, producing a keystream block. The plaintext block is XORed with the keystream block to produce ciphertext. 
  - Decryption: Identical to encryption (CTR mode is symmetric).
  - Testing: The IND-CCA test script creates two messages, encrypts them, modifies the ciphertext, and demonstrates that the attack can distinguish which message was encrypted.

- IND-CCA Attack Description
  CTR mode is malleable: flipping a bit in the ciphertext flips the same bit in the decrypted plaintext. The test script demonstrates this by modifying the ciphertext and using the decryption oracle to distinguish which message was encrypted, showing that AES-CTR is not IND-CCA secure.

