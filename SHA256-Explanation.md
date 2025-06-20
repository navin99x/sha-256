# In-Depth Explanation of the SHA-256 Process

This document provides a detailed, step-by-step explanation of the SHA-256 cryptographic hash function, as implemented in `sha256.py`. Each stage of the process is described, with relevant code snippets included for clarity.

---

## 1. Message Preprocessing

### 1.1. Converting Characters to Binary
Each character in the input message is converted to its ASCII value, then to an 8-bit binary string. The binary strings are concatenated to form the binary representation of the message.

```python
def char_to_bin_ascii(msg: str) -> str:
    # ...existing code...
```

---

### 1.2. Padding the Message
The binary message is padded to ensure its length is congruent to 448 modulo 512. Padding consists of:
- Appending a single '1' bit
- Appending enough '0' bits to reach 448 bits (mod 512)
- Appending the original message length as a 64-bit big-endian integer

```python
def padding(bin_msg: str) -> str:
    # ...existing code...
```

---

## 2. Parsing and Expanding the Message

### 2.1. Parsing into 32-bit Words
The padded message is split into sixteen 32-bit words.

### 2.2. Message Schedule Expansion
The 16 words are expanded into 64 words using bitwise operations (σ0, σ1) and modular addition.

```python
def compute_words(msg: str) -> list:
    # ...existing code...
```

---

## 3. Setting Initial Hash Values and Constants

### 3.1. Initial Hash Values
SHA-256 uses eight 32-bit initial hash values, derived from the fractional parts of the square roots of the first eight prime numbers.

```python
def compute_initial_hashs():
    # ...existing code...
```

### 3.2. Round Constants
Sixty-four 32-bit constants are derived from the fractional parts of the cube roots of the first 64 prime numbers.

```python
def compute_constants():
    # ...existing code...
```

---

## 4. The Compression Function (Main Loop)

SHA-256 processes the message in 64 rounds, updating eight working variables (a–h) using logical functions and modular arithmetic.

### 4.1. Logical Functions
- **Ch**: Choice function
- **Maj**: Majority function
- **Σ0, Σ1**: Bitwise rotation and shift functions

```python
def ch(e, f, g):
    # ...existing code...

def maj(a, b, c):
    # ...existing code...
```

### 4.2. Round Operations
Each round computes two temporary values, T1 and T2, and updates the working variables.

```python
def calculate_t1(h, e, f, g, k, w):
    # ...existing code...

def calculate_t2(a, b, c):
    # ...existing code...
```

---

## 5. Producing the Final Hash Value

After all rounds, the working variables are added to the initial hash values to produce the final 256-bit hash (as eight 32-bit words).

```python
def sha(msg: str) -> str:
    # ...existing code...
```

---

## 6. Limitations of This Implementation

- Only supports single-block messages (up to 55 ASCII characters)
- For educational purposes; not suitable for production use

---

## References
- [FIPS PUB 180-2: Secure Hash Standard (SHA)](https://cr.yp.to/bib/2002/-sha.pdf)
- [Wikipedia: SHA-2](https://en.wikipedia.org/wiki/SHA-2)
- [Youtube - RebBlockBlue](https://youtu.be/orIgy2MjqrA?feature=shared)
