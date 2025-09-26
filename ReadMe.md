AES-CTR IND-CCA Assignment
--------------------------------------------

## Compilation and Installation

### Prerequisites
- Python 3.8+
- `pycryptodome` library for AES block cipher operations

Install prerequisites with:
```sh
sudo apt update
sudo apt install python3 python3-pip
pip3 install pycryptodome
```

## Files
- `aes_ctr.py`: Implements AES-CTR encryption, decryption, and key generation.
- `ind-cca_test.py`: Contains tests for correctness and IND-CCA attack.

## Running the Tests

To run the correctness and IND-CCA attack tests, execute:
```sh
python3 ind-cca_test.py
```
Expected output:
- The script prints the original message, ciphertext, modified ciphertext, and decrypted outputs.
- For both test cases, the IND-CCA attack should succeed, demonstrating that CTR mode is not IND-CCA secure.

The output should end with:
```
IND-CCA attack on CTR succeeded for both test messages.
```

---------------------------------------------------------------------------------------------

## General Approach

### Key Generation

A random 128-bit AES key is generated using `os.urandom`:
```python
import os
def keygen():
    return os.urandom(16)
```

### Nonce Generation

For each encryption, a random 128-bit nonce is generated and prepended to the ciphertext:
```python
nonce = os.urandom(16)
```

### Encryption (CTR mode)

The plaintext is split into 16-byte blocks. For each block, a counter is combined with the nonce to form the input to AES-CTR, producing a keystream block. The plaintext block is XORed with the keystream block to produce ciphertext.

```python
def encrypt(message_plaintext, key):
    ...
```

### Decryption

Decryption is identical to encryption (CTR mode is symmetric):

```python
def decrypt(ciphertext, key):
    ...
```

### Testing

The IND-CCA test script creates two messages, encrypts them, modifies the ciphertext, and demonstrates that the attack can distinguish which message was encrypted.

---------------------------------------------------------------------------------------------

## IND-CCA Attack Description

CTR mode is malleable: flipping a bit in the ciphertext flips the same bit in the decrypted plaintext. The test script demonstrates this by modifying the ciphertext and using the decryption oracle to distinguish which message was encrypted, showing that AES-CTR is not IND-CCA secure.

## How it works 

1. Challenge Phase: The attacker chooses two messages (`m0`, `m1`) of the same length that differ in a known way (e.g., one byte is different).
2. Encryption Oracle: The challenger randomly selects one of the messages and encrypts it, returning the ciphertext (`c*`) to the attacker.
3. Ciphertext Modification: The attacker modifies `c*` by flipping a bit in the ciphertext (e.g., flipping the least significant bit of the first byte).
4. Decryption Oracle: The attacker submits the modified ciphertext (`c'`) to the decryption oracle, which returns the decrypted plaintext (`m'`).
5. Distinguishing Because CTR mode is malleable, the attacker can observe which bit was flipped in the decrypted message and thus determine which original message was encrypted.

### Implementation in `ind-cca_test.py`

- The test script creates two messages:
  ```python
  m0 = bytes([0]*16)  # all zeros
  m1 = bytes([1] + [0]*15)  # first byte is 1, rest are zeros
  ```
- It encrypts one of them and gets the ciphertext.
- It flips the least significant bit of the first byte of the ciphertext (after the nonce).
  
  ```python
  c_prime = flip_byte_in_ciphertext(c_star, idx=16)
  ```
- It decrypts the modified ciphertext and checks the first byte to see which message was encrypted.

  ```python
  m_prime = dec(c_prime, key)
  guessed_b = 0 if (m_prime[0] & 1) else 1
  ```
- If the guess matches the actual message, the attack succeeds.

This demonstrates that AES-CTR is not IND-CCA secure because the attacker can reliably distinguish which message was encrypted by exploiting the malleability of CTR mode.

