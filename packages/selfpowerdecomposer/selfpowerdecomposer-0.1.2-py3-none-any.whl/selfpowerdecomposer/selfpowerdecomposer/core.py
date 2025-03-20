import sys
import math
import struct
import os
import time
from itertools import groupby
import gmpy2
import random

try:
    # Set Python to allow large integers without limit (only in Python 3.11+)
    sys.set_int_max_str_digits(0)
except:
    pass

# -----------------------------
# 1) Self-Power Calculations
# -----------------------------
def compute_self_powers_and_sum(k):
    """
    Use gmpy2 mpz for i^i and sum.
    This typically gives a huge speed boost for large i.
    
    Args:
        k (int): Upper limit for calculating self powers
        
    Returns:
        tuple: (list of self powers, cumulative sum)
    """
    powers = []
    cum_sum = gmpy2.mpz(0)
    for i in range(1, k + 1):
        val = gmpy2.mpz(i) ** i  # uses GMP under the hood
        powers.append(val)
        cum_sum += val
    return powers, cum_sum

# -----------------------------
# 2) find_largest_k_binary
# -----------------------------
def find_largest_k_binary(N):
    """Finds the largest k such that k^k <= N using binary search."""
    if N < 1:
        return 0
    if N == 1:
        return 1

    ln_N = gmpy2.log(N)  # Use gmpy2.log for large numbers

    # Find an upper bound
    upper = 1
    while upper * gmpy2.log(upper) <= ln_N:  # Use gmpy2.log
        upper *= 2

    # Binary search
    lower, best = 1, 1
    while lower <= upper:
        mid = (lower + upper) // 2
        if mid == 0:
            mid_val = float('inf')
        else:
            mid_val = mid * gmpy2.log(mid)  # Use gmpy2.log

        if mid_val <= ln_N:
            best = mid
            lower = mid + 1
        else:
            upper = mid - 1

    # Adjust up or down for floating-point errors
    while (best + 1) ** (best + 1) <= N:
        best += 1
    while best > 1 and best ** best > N:
        best -= 1

    return best

# -----------------------------
# 3) Greedy Remainder Distribution
# -----------------------------
def greedy_remainder_distribution(R, self_powers):
    """
    Distribute remainder R greedily among self-powers.
    
    Args:
        R (mpz): Remainder to distribute
        self_powers (list): List of self-powers
        
    Returns:
        list: Coefficients for each self-power
    """
    coeffs = [0] * len(self_powers)
    
    for i in range(len(self_powers) - 1, -1, -1):
        power_i = self_powers[i]
        if power_i <= R:
            coeff = int(R // power_i)
            coeffs[i] = coeff
            R -= coeff * power_i
    
    return coeffs

# -----------------------------
# 4) Self-Power Decomposition
# -----------------------------
def self_power_decomposition(N):
    """
    Decompose N into sum of c_i * i^i terms.
    
    Args:
        N (int): Number to decompose
        
    Returns:
        tuple: (coefficients, self-powers, delta-encoded coefficients)
    """
    N = gmpy2.mpz(N)
    
    # Find largest k such that k^k <= N
    k = find_largest_k_binary(N)
    
    # Compute self-powers up to k
    self_powers, _ = compute_self_powers_and_sum(k)
    
    # Distribute remainder greedily
    coeffs = greedy_remainder_distribution(N, self_powers)
    
    # Delta encode the coefficients
    delta_encoded = delta_encode(coeffs)
    
    return coeffs, self_powers, delta_encoded

# -----------------------------
# 5) Delta Encoding/Decoding
# -----------------------------
def delta_encode(coeffs):
    """
    Delta encode a list of coefficients.
    
    Args:
        coeffs (list): List of coefficients
        
    Returns:
        list: Delta-encoded coefficients
    """
    if not coeffs:
        return []
    
    deltas = [coeffs[0]]
    for i in range(1, len(coeffs)):
        deltas.append(coeffs[i] - coeffs[i-1])
    
    return deltas

def delta_decode(deltas):
    """
    Decode delta-encoded coefficients.
    
    Args:
        deltas (list): Delta-encoded coefficients
        
    Returns:
        list: Original coefficients
    """
    if not deltas:
        return []
    
    coeffs = [deltas[0]]
    for i in range(1, len(deltas)):
        coeffs.append(coeffs[i-1] + deltas[i])
    
    return coeffs

# -----------------------------
# 6) Run-Length Encoding/Decoding
# -----------------------------
def rle_encode(data):
    """
    Run-length encode a list of values.
    
    Args:
        data (list): List of values
        
    Returns:
        list: Run-length encoded data as (value, count) pairs
    """
    return [(k, len(list(g))) for k, g in groupby(data)]

def rle_decode(encoded_data):
    """
    Decode run-length encoded data.
    
    Args:
        encoded_data (list): Run-length encoded data as (value, count) pairs
        
    Returns:
        list: Original data
    """
    result = []
    for value, count in encoded_data:
        result.extend([value] * count)
    return result

# -----------------------------
# 7) ZigZag Encoding/Decoding
# -----------------------------
def zigzag_encode(n):
    """
    ZigZag encode a signed integer to an unsigned integer.
    
    Args:
        n (int): Signed integer
        
    Returns:
        int: Unsigned integer
    """
    return (n << 1) ^ (n >> 63)

def zigzag_decode(n):
    """
    Decode a ZigZag encoded unsigned integer back to signed.
    
    Args:
        n (int): Unsigned integer
        
    Returns:
        int: Signed integer
    """
    return (n >> 1) ^ (-(n & 1))

# -----------------------------
# 8) Varint Encoding/Decoding
# -----------------------------
def encode_varint(n):
    """
    Encode an integer using variable-length encoding.
    
    Args:
        n (int): Integer to encode
        
    Returns:
        bytes: Encoded bytes
    """
    result = bytearray()
    while n >= 0x80:
        result.append((n & 0x7F) | 0x80)
        n >>= 7
    result.append(n & 0x7F)
    return bytes(result)

def decode_varint(bytestream, offset=0):
    """
    Decode a variable-length encoded integer.
    
    Args:
        bytestream (bytes): Encoded bytes
        offset (int): Starting offset in bytestream
        
    Returns:
        tuple: (decoded integer, new offset)
    """
    result = 0
    shift = 0
    
    while True:
        if offset >= len(bytestream):
            raise ValueError("Incomplete varint")
        
        b = bytestream[offset]
        offset += 1
        
        result |= ((b & 0x7F) << shift)
        if not (b & 0x80):
            break
        
        shift += 7
        if shift > 63:
            raise ValueError("Varint too long")
    
    return result, offset

# -----------------------------
# 9) RLE Decision
# -----------------------------
def should_apply_rle(delta_data):
    """
    Determine if RLE should be applied based on data characteristics.
    
    Args:
        delta_data (list): Delta-encoded data
        
    Returns:
        bool: True if RLE should be applied
    """
    # Count runs of same value
    runs = 1
    run_lengths = []
    
    for i in range(1, len(delta_data)):
        if delta_data[i] == delta_data[i-1]:
            runs += 1
        else:
            if runs > 1:
                run_lengths.append(runs)
            runs = 1
    
    if runs > 1:
        run_lengths.append(runs)
    
    # If we have runs of length > 3, RLE is likely beneficial
    if run_lengths and max(run_lengths) > 3:
        return True
    
    # If we have many runs, RLE is likely beneficial
    if len(run_lengths) > len(delta_data) // 10:
        return True
    
    # If we have many zeros, RLE is likely beneficial
    zero_count = delta_data.count(0)
    if zero_count > len(delta_data) // 5:
        return True
    
    return False

# -----------------------------
# 10) Main Encoding/Decoding
# -----------------------------
def encode_number(N):
    """
    Encode a large integer using self-power decomposition.
    
    Args:
        N (int): Number to encode
        
    Returns:
        bytes: Encoded data
    """
    # Special case zero
    if N == 0:
        return b'\x00'
    
    # Decompose N into self-powers
    _, _, delta_encoded = self_power_decomposition(N)
    
    # Decide whether to use RLE
    use_rle = should_apply_rle(delta_encoded)
    
    # Apply RLE if beneficial
    if use_rle:
        rle_data = rle_encode(delta_encoded)
        # Flatten RLE data and prepare for encoding
        flat_data = []
        for value, count in rle_data:
            flat_data.append(zigzag_encode(value))
            flat_data.append(count)
        
        # Encode as varints
        result = bytearray([1])  # Flag for RLE
        for n in flat_data:
            result.extend(encode_varint(n))
    else:
        # Encode delta values directly
        result = bytearray([0])  # Flag for no RLE
        for delta in delta_encoded:
            result.extend(encode_varint(zigzag_encode(delta)))
    
    return bytes(result)

def decode_number(encoded_data):
    """
    Decode data encoded with encode_number.
    
    Args:
        encoded_data (bytes): Encoded data
        
    Returns:
        int: Decoded number
    """
    if not encoded_data:
        raise ValueError("Empty encoded data")
    
    # Special case for zero
    if encoded_data == b'\x00':
        return 0
    
    # Check encoding flag
    flag = encoded_data[0]
    offset = 1
    
    if flag == 0:  # No RLE
        # Decode delta values
        delta_encoded = []
        while offset < len(encoded_data):
            value, offset = decode_varint(encoded_data, offset)
            delta_encoded.append(zigzag_decode(value))
    elif flag == 1:  # RLE
        # Decode RLE data
        rle_data = []
        while offset < len(encoded_data):
            value, offset = decode_varint(encoded_data, offset)
            count, offset = decode_varint(encoded_data, offset)
            rle_data.append((zigzag_decode(value), count))
        
        # Decode RLE
        delta_encoded = rle_decode(rle_data)
    else:
        raise ValueError(f"Unknown encoding flag: {flag}")
    
    # Decode deltas to coefficients
    coeffs = delta_decode(delta_encoded)
    
    # Compute self-powers
    k = len(coeffs)
    self_powers, _ = compute_self_powers_and_sum(k)
    
    # Reconstruct the number
    N = gmpy2.mpz(0)
    for i, coeff in enumerate(coeffs):
        if coeff != 0:
            N += coeff * self_powers[i]
    
    return int(N)

# -----------------------------
# 11) File I/O
# -----------------------------
def save_to_binary_file(filename, data):
    """Save binary data to a file."""
    with open(filename, 'wb') as f:
        f.write(data)

def load_from_binary_file(filename):
    """Load binary data from a file."""
    with open(filename, 'rb') as f:
        return f.read()

# -----------------------------
# 12) No-Placeholder Secure Encoding/Decoding
# -----------------------------
def secure_encode_number_no_placeholder(N, num_removed=5):
    """
    Encode a number, completely removing some delta values.
    The first delta value (position 0) is always removed for security.
    
    Args:
        N (int): Number to encode
        num_removed (int): Number of delta values to remove
        
    Returns:
        tuple: (encoded data, list of (position, value) pairs for removed deltas)
    """
    # Special case zero
    if N == 0:
        return b'\x01', [(0, 0)]
    
    # Decompose N into self-powers
    _, _, delta_encoded = self_power_decomposition(N)
    
    # Ensure we don't try to remove more values than we have
    num_removed = min(num_removed, len(delta_encoded))
    
    # Always include position 0 (first delta) in the removed positions for security
    removed_positions = [0]
    
    # Randomly select additional positions to remove
    if num_removed > 1:
        additional_positions = random.sample(range(1, len(delta_encoded)), num_removed - 1)
        removed_positions.extend(additional_positions)
    
    # Sort positions for consistency
    removed_positions.sort()
    
    # Extract values at removed positions
    removed_info = [(pos, delta_encoded[pos]) for pos in removed_positions]
    
    # Create partial delta array by skipping removed positions
    partial_delta = []
    for i in range(len(delta_encoded)):
        if i not in removed_positions:
            partial_delta.append(delta_encoded[i])
    
    # Encode the partial delta array
    result = bytearray([2])  # Flag for no-placeholder secure encoding
    for delta in partial_delta:
        result.extend(encode_varint(zigzag_encode(delta)))
    
    return bytes(result), removed_info

def secure_decode_number_no_placeholder(encoded_data, removed_info):
    """
    Decode data encoded with secure_encode_number_no_placeholder.
    
    Args:
        encoded_data (bytes): Encoded data
        removed_info (list): List of (position, value) pairs for removed deltas
        
    Returns:
        int: Decoded number
    """
    if not encoded_data:
        raise ValueError("Empty encoded data")
    
    # Check encoding flag
    flag = encoded_data[0]
    if flag != 2:
        raise ValueError(f"Expected no-placeholder secure encoding flag (2), got {flag}")
    
    # Sort removed_info by position
    removed_info = sorted(removed_info, key=lambda x: x[0])
    
    # Decode partial delta array
    offset = 1
    partial_delta = []
    while offset < len(encoded_data):
        value, offset = decode_varint(encoded_data, offset)
        partial_delta.append(zigzag_decode(value))
    
    # Reconstruct full delta array by inserting removed values
    delta_encoded = []
    partial_idx = 0
    
    for i in range(max(removed_info[-1][0] + 1, len(partial_delta) + len(removed_info))):
        # Check if this position was removed
        removed_pos = next((pos for pos, val in removed_info if pos == i), None)
        if removed_pos is not None:
            # Insert the removed value
            removed_val = next(val for pos, val in removed_info if pos == i)
            delta_encoded.append(removed_val)
        else:
            # Insert from partial delta if we haven't exhausted it
            if partial_idx < len(partial_delta):
                delta_encoded.append(partial_delta[partial_idx])
                partial_idx += 1
            else:
                # This shouldn't happen with valid data
                raise ValueError("Ran out of partial delta values during reconstruction")
    
    # Decode deltas to coefficients
    coeffs = delta_decode(delta_encoded)
    
    # Compute self-powers
    k = len(coeffs)
    self_powers, _ = compute_self_powers_and_sum(k)
    
    # Reconstruct the number
    N = gmpy2.mpz(0)
    for i, coeff in enumerate(coeffs):
        if coeff != 0:
            N += coeff * self_powers[i]
    
    return int(N)

def save_removed_info_no_placeholder(removed_info, filename):
    """
    Save removed delta information to a binary file.
    
    Args:
        removed_info (list): List of (position, value) pairs
        filename (str): Output filename
    """
    with open(filename, 'wb') as f:
        # Write number of entries
        f.write(struct.pack('<I', len(removed_info)))
        
        # Write each (position, value) pair
        for pos, val in removed_info:
            # Write position as varint
            f.write(encode_varint(pos))
            
            # Write value as zigzag varint
            f.write(encode_varint(zigzag_encode(val)))

def load_removed_info_no_placeholder(filename):
    """
    Load removed delta information from a binary file.
    
    Args:
        filename (str): Input filename
        
    Returns:
        list: List of (position, value) pairs
    """
    with open(filename, 'rb') as f:
        data = f.read()
    
    # Read number of entries
    if len(data) < 4:
        raise ValueError("Invalid file format")
    
    num_entries = struct.unpack('<I', data[:4])[0]
    offset = 4
    
    # Read each (position, value) pair
    removed_info = []
    for _ in range(num_entries):
        # Read position
        pos, offset = decode_varint(data, offset)
        
        # Read value
        val_encoded, offset = decode_varint(data, offset)
        val = zigzag_decode(val_encoded)
        
        removed_info.append((pos, val))
    
    return removed_info
