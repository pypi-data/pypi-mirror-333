"""
SelfPowerDecomposer - A Python package for large integer compression using self-power decomposition

This package provides tools for compressing large integers using a novel approach
based on self-power decomposition. It requires gmpy2 for efficient large integer operations.

Main functions:
- encode_number: Compress a large integer
- decode_number: Decompress an encoded integer

Secure encoding/decoding (no placeholders):
- secure_encode_number_no_placeholder: Encode a number, completely removing some delta values
- secure_decode_number_no_placeholder: Decode a number with the removed delta values
- save_removed_info_no_placeholder: Save the removed delta values and positions to a file
- load_removed_info_no_placeholder: Load the removed delta values and positions from a file
"""

from .core import (
    # Main API functions
    encode_number,
    decode_number,
    save_to_binary_file,
    load_from_binary_file,
    
    # Core algorithm functions
    self_power_decomposition,
    compute_self_powers_and_sum,
    find_largest_k_binary,
    
    # Encoding/decoding utilities
    delta_encode,
    delta_decode,
    rle_encode,
    rle_decode,
    zigzag_encode,
    zigzag_decode,
    encode_varint,
    decode_varint,
    
    # Secure encoding/decoding (no placeholders)
    secure_encode_number_no_placeholder,
    secure_decode_number_no_placeholder,
    save_removed_info_no_placeholder,
    load_removed_info_no_placeholder,
)

__version__ = '0.1.0'
