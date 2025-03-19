# SelfPowerDecomposer

A Python package for large integer compression and secure encoding using self-power decomposition.

## Description

SelfPowerDecomposer provides tools for compressing large integers using a novel approach based on self-power decomposition. It offers both standard compression and secure encoding options.

## Features

- Efficient compression of large integers
- Secure encoding with key-based protection
- Binary file I/O utilities
- Various encoding/decoding utilities (delta, RLE, zigzag, varint)

## Installation

```bash
pip install selfpowerdecomposer
```

## Usage

### Basic Compression

```python
import selfpowerdecomposer

# Compress a large number
large_number = 123456789012345678901234567890
encoded_data = selfpowerdecomposer.encode_number(large_number)

# Decompress back to the original number
decoded_number = selfpowerdecomposer.decode_number(encoded_data)

print(f"Original: {large_number}")
print(f"Encoded size: {len(encoded_data)} bytes")
print(f"Decoded: {decoded_number}")
print(f"Match: {large_number == decoded_number}")
```

### Secure Encoding

```python
import selfpowerdecomposer
import random

# Generate a large number
large_number = 123456789012345678901234567890

# Securely encode with removed values (no placeholders)
encoded_data, removed_info = selfpowerdecomposer.secure_encode_number_no_placeholder(
    large_number, 
    removal_count=5
)

# Save the removed info (this would be your "key")
selfpowerdecomposer.save_removed_info_no_placeholder(removed_info, "key.bin")

# Later, to decode:
removed_info = selfpowerdecomposer.load_removed_info_no_placeholder("key.bin")
decoded_number = selfpowerdecomposer.secure_decode_number_no_placeholder(encoded_data, removed_info)

print(f"Original: {large_number}")
print(f"Decoded: {decoded_number}")
print(f"Match: {large_number == decoded_number}")
```

## Requirements

- Python 3.6+
- gmpy2
- numpy
- matplotlib (optional, for visualization)

## License

MIT License 