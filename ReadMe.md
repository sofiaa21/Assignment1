
# AES-CTR IND-CCA Assignment

## Compilation and Installation

### Prerequisites
- Python 3.8+
- `pycryptodome` library for AES block cipher operations

# AES-CTR IND-CCA Assignment

## Setup & Installation
- Requires Python 3.8+ and `pycryptodome`.
- For Ubuntu 24.04, use Docker for easiest setup:
  ```sh
  docker build -t cryptography-assignment1 .
  docker run --rm cryptography-assignment1
  ```
This will automatically install all dependencies and run both the test for aes_ctr implementation and the IND-CCA test script.

## Running the tests and interpreting the Output
After building the docker the tests can be ran with the `docker run --rm cryptography-assignment1`  command. Afterwards, the following printouts should be available for intepretation.

#### AES - CTR Implementation
- The test prints message in all its forms: plaintext (raw), ciphertext (encrypted message) and the decryption. Additionaly it also prints the key and the final assert returns whether the string versions of the original plaintext and the decrypted message match.
- The output should look like this:
  ```
  Raw message: comment=hello;userdata=abc;admin=0;end
  Encrypted message: b'\x17|9E\xf3\xf3\xe6M<\xaf\x9c\n\r\x8dul\x15nA\xb1i\xf4\xbc\x7f\x1e\xbb4\x10Y\r\xc2\xff8y0\x90\xad\xe4\xfe\xe0t\xfb}\x1c\xb2\xccZ\xfb\xae\x1c\xc7\x11\x0b\x08'
  Decrypted message: b'comment=hello;userdata=abc;admin=0;end'
  Key used:  b'\x87\xd1zC~s\x06c<\xa5\xfa\xc7<gC4'
  Decryption: success
  ```

#### IND - CCA Attack
- The script prints the original message, ciphertext, modified ciphertext, and decrypted outputs for each test case.
- Example on what the output should look like for test case where the flipped bit is: 0:
  ```
  Original message (m): 00000000000000000000000000000000
  Generated key: 8808f9fcd2295a579e6f64da038a7ccf
  Ciphertext (c_star): 39e51b2927dbf735c408236b88e308cbc10db14e02a0b5ffb06db654d737d4fe
  Challenge ciphertext length: 32
  ```
- For both test cases, the attack should succeed, demonstrating that CTR mode is not IND-CCA secure.
We should also be able to observe the change in the modified message
  ```
    Modified ciphertext (c_prime): 39e51b2927dbf735c408236b88e308cbc00db14e02a0b5ffb06db654d737d4fe
  ```
  (Hint) Notice the difference after cbc -> flipped bit 
- The change in bits can also be observed in the output
  ```
    Difference at first byte (nonce excluded) : c_star[16]=193, c_prime[16]=192
    Actual b: 0 Recovered guess: 0
    Original message (m): 00000000000000000000000000000000
    Decrypted original message (should match m): 00000000000000000000000000000000
  ```
- Finally we should be able to observe the modified message + the flipped bit
  ```
    Decrypted modified message (m_prime): 01000000000000000000000000000000
    m_prime[0]: 1
  ```
