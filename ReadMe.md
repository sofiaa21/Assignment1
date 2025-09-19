# AES-128 in CTR Mode

This project contains an implementation of the **AES-128** block cipher in **CTR (Counter) mode**.  
It provides a simple library with three main functions:

1. **Key Generation** → outputs a random 128-bit key  
2. **Encryption** → encrypts a message of length ℓ blocks (128-bit each)  
3. **Decryption** → decrypts a ciphertext back into the original plaintext  

---

## ⚙️ Compilation and Installation

### ✅ Prerequisites
- **Python 3.10+** (default on Ubuntu 24.04.2 LTS)  
- Required library:  
  - [`pycryptodome`](https://pypi.org/project/pycryptodome/) – provides AES functionality  

