from math import sqrt, cbrt, modf, floor

def char_to_bin_ascii(msg: str) -> str:
    """
    Converts each character of a string to it's ASCII value and 8-bit binary representation.
    """
    print("\n--------Character Conversion To Binary--------\n")
    concatenated_bin = ""

    for char in msg:
        ascii_value = ord(char)
        binary_value = bin(ascii_value)[2:].zfill(8)
        concatenated_bin += binary_value

        print(f"Character: '{char}'")
        print(f"ASCII value: {ascii_value}")
        print(f"Binary representation: {binary_value}\n")

    print(f"Concatenated Binary Value for '{msg}': {concatenated_bin}")
    return concatenated_bin


def padding(bin_msg: str) -> str:
    """
    Pads Binary message to form 512-bit block.
    """
    print("\n--------Padding Process--------\n")
    initial_length = len(bin_msg)

    # Append a '1' bit
    pad_msg = bin_msg + '1'

    remainder = len(pad_msg) % 512

    if remainder == 448:
        zeros_to_add = 0    # No need to add zero
    elif remainder < 448:
        zeros_to_add = 448 - remainder    # Add zero upto 448 bit position 
    else :
        zeros_to_add = 512 - remainder + 448    # Add zero upto 448 bit position  of next block (Not used in our case.)

    # Append '0' bits
    pad_msg += '0' * zeros_to_add

    # Append 64 bit binary representation of original msg
    initial_length_bin = bin(initial_length)[2:].zfill(64)
    pad_msg += initial_length_bin

    print(f"Original length: {initial_length}")
    print(f"After adding '1': {len(bin_msg + '1')}")
    print(f"Zeros to add: {zeros_to_add}")
    print(f"Final padded length: {len(pad_msg)}")
    print(f"\nPadded Message: {pad_msg}")

    return pad_msg


def rotate_right(val, shift, bit_size=32):
    """
    Perform 32 bit Circular Left Shift
    """
    shift %= bit_size
    return ((val >> shift) | (val << (bit_size - shift))) & ((1 << bit_size) - 1)


def shift_right(val, shift, bit_size=32):
    """
    Perform 32 bit Logical Right Shift
    """
    return val >> shift

def sigma_zero(n):
    return rotate_right(n, 7) ^ rotate_right(n, 18) ^ shift_right(n, 3)

def sigma_one(n):
    return rotate_right(n, 17) ^ rotate_right(n, 19) ^ shift_right(n, 10)

def compute_words(msg: str) -> list:
    """
    Expand padded message to sixty-four 32-bit words"
    """
    print("\n--------Word Expansion Process--------\n")
    
    words = []
    for i in range(16):
        ith_word = int(msg[i * 32: (i + 1) * 32], 2)
        words.append(ith_word)
        print(f"w{i}: {hex(words[i])}")

    for i in range(16, 64):
        sigma_zero_val = sigma_zero(words[i-15])
        sigma_one_val = sigma_one(words[i-2])

        ith_word = (sigma_one_val + words[i-7] + sigma_zero_val + words[i-16]) & 0xFFFFFFFF
        
        words.append(ith_word)
        print(f"w{i}: {hex(words[i])}")

    return words


def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True


def first_n_prime(n):
    primes = []
    num = 2

    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1

    return primes


def compute_initial_hashs():
    """
    Computes initial SHA-256 hash values.
    """
    print("\n--------Computing Initial Hashes--------\n")

    prime_nums = first_n_prime(8)
    initial_hash_values = []

    for index, num in enumerate(prime_nums):
        root = sqrt(num)
        frac_part = modf(root)[0]
        scaled = floor(frac_part * (2 ** 32))
        initial_hash_values.append(scaled)
        print(f"H{index}: {hex(initial_hash_values[index])}")

    return initial_hash_values

def compute_constants():
    """
    Computes 64 constants of 32-bit words.
    """
    print("\n--------Computing Constants Values--------\n")

    prime_nums = first_n_prime(64)
    const_values = []
    
    for index, num in enumerate(prime_nums):
        cube_root = cbrt(num)
        frac_part = modf(cube_root)[0]
        scaled = floor(frac_part * (2 ** 32))
        const_values.append(scaled)
        print(f"K{index}: {hex(const_values[index])}")

    return const_values

def calculate_t1(h, e, f, g, k, w):
    sigma_one = rotate_right(e, 6) ^ rotate_right(e, 11) ^ rotate_right(e, 25)
    return (h + sigma_one + ch(e, f, g) + k + w) & 0xFFFFFFFF

def calculate_t2(a, b, c):
    sigma_zero = rotate_right(a, 2) ^ rotate_right(a, 13) ^ rotate_right(a, 22)
    return (sigma_zero + maj(a, b, c)) & 0xFFFFFFFF
    
def ch(e, f, g):
    """Choice function: (e AND f) XOR (NOT e AND g)"""
    return (e & f) ^ (~e & g)

def maj(a, b, c):
    """Majority function: (a AND b) XOR (a AND c) XOR (b AND c)"""
    return (a & b) ^ (a & c) ^ (b & c)

def sha(msg: str) -> str:
    "Computes sha-256 hash of given input"

    bin_msg = char_to_bin_ascii(msg)
    pad_msg = padding(bin_msg)
    words = compute_words(pad_msg)

    initial_hash = compute_initial_hashs()
    constants_val = compute_constants()

    a, b, c, d, e, f, g, h = initial_hash

    # Main Loop
    print("\n--------Round Loop Execution--------\n")

    for i in range(64):
        t1 = calculate_t1(h, e, f, g, constants_val[i], words[i])
        t2 = calculate_t2(a, b, c)
        h = g
        g = f
        f = e
        e = (d + t1) & 0xFFFFFFFF
        d = c
        c = b
        b = a
        a = (t1 + t2) & 0xFFFFFFFF

        print("\n","-" * 8)
        print(f"Round {i: 2d}")
        print("-" * 8, "\n")
        
        print(f"a = {hex(a)}")
        print(f"b = {hex(b)}")
        print(f"c = {hex(c)}")
        print(f"d = {hex(d)}")
        print(f"e = {hex(e)}")
        print(f"f = {hex(f)}")
        print(f"g = {hex(g)}")
        print(f"h = {hex(h)}")
    
    H0 = (initial_hash[0] + a) & 0xFFFFFFFF
    H1 = (initial_hash[1] + b) & 0xFFFFFFFF
    H2 = (initial_hash[2] + c) & 0xFFFFFFFF
    H3 = (initial_hash[3] + d) & 0xFFFFFFFF
    H4 = (initial_hash[4] + e) & 0xFFFFFFFF
    H5 = (initial_hash[5] + f) & 0xFFFFFFFF
    H6 = (initial_hash[6] + g) & 0xFFFFFFFF
    H7 = (initial_hash[7] + h) & 0xFFFFFFFF

    final_hash = [H0, H1, H2, H3, H4, H5, H6, H7]

    print("\n--------Final Hash Values--------\n")
    hash_hex = ""
    for i, hash_val in enumerate(final_hash):
        hex_val = format(hash_val, '08x')
        hash_hex += hex_val
        print(f"H{i}: {hex_val}")
    
    print(f"\nSHA-256 Hash of '{msg}': {hash_hex}")
    return hash_hex

def main():
    message = input("Enter a string: ")
    result = sha(message)

if __name__ == "__main__":
    main()