# SHA-256 Python Implementation

> A simple, educational implementation of the SHA-256 cryptographic hash function in Python.

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python 3](https://img.shields.io/badge/python-3-blue.svg)

---

## Demo

**Example:**

```
Input:  Never Gonna Give ...
Output:  8f4df3c656d619e4877b4fc3d20e0f830c1c11514686068f6e1a083896abcdfa
```

---

## Features
- Converts input strings to their SHA-256 hash values
- Step-by-step breakdown of the hashing process with detailed print statements
- No external dependencies required (uses only Python standard library)

## Usage
1. Run the script:
   ```bash
   python sha256.py
   ```
2. Enter a string when prompted. The script will display the SHA-256 hash and intermediate steps.

## File Structure
- `sha256.py` — Main Python script containing the SHA-256 implementation
- `sha.pdf` — Documentation on SHA family.

## In-Depth Explanation

For a detailed, step-by-step breakdown of the SHA-256 process, see [`SHA256-Explanation.md`](./SHA256-Explanation.md).

## Requirements
- Python 3.x (no external libraries required)

---

## License

This project is licensed under the [MIT License](./LICENSE).

## Notes
- This implementation is for educational purposes and demonstrates the internal workings of SHA-256.
- This program only handles a single 512-bit block of the SHA-256 operation, so it cannot process large inputs (i.e., messages longer than 55 ASCII characters).
- For production use, prefer Python's built-in `hashlib` library for cryptographic operations.
