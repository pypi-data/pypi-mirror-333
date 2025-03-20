#!/usr/bin/env python3
"""
Basic Usage Example

This example demonstrates the basic functionality of the selfpowerdecomposer package
for compressing large integers using self-power decomposition.
"""

from selfpowerdecomposer import (
    encode_number, 
    decode_number, 
    save_to_binary_file, 
    load_from_binary_file,
    self_power_decomposition
)
import time

def print_separator(title):
    """Print a section separator with title"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def demonstrate_basic_usage():
    """Demonstrate the basic encoding/decoding functionality"""
    # Create some test numbers of different sizes
    test_numbers = [
        ("SMALL", 12345),
        ("MEDIUM", 12345678901234567890),
        ("LARGE", 12345678901234567890123456789012345678901234567890)
    ]
    
    for name, number in test_numbers:
        print_separator(name + " NUMBER")
        
        # Print information about the number
        print(f"Original: {number}")
        print(f"Number of digits: {len(str(number))}")
        print(f"Binary length: {number.bit_length()} bits")
        
        # Encode the number
        print("\nEncoding...")
        start_time = time.time()
        encoded_data = encode_number(number)
        encoding_time = time.time() - start_time
        
        print(f"Encoding time: {encoding_time:.6f} seconds")
        print(f"Encoded data size: {len(encoded_data)} bytes")
        
        # Calculate compression ratio (bits)
        original_bits = number.bit_length()
        encoded_bits = len(encoded_data) * 8
        compression_ratio = encoded_bits / original_bits
        print(f"Compression ratio: {compression_ratio:.2f}x")
        
        # Save to a file
        filename = f"{name.lower()}_encoded.bin"
        save_to_binary_file(filename, encoded_data)
        print(f"Saved to {filename}")
        
        # Load from the file
        loaded_data = load_from_binary_file(filename)
        
        # Decode the number
        print("\nDecoding...")
        start_time = time.time()
        decoded_number = decode_number(loaded_data)
        decoding_time = time.time() - start_time
        
        print(f"Decoding time: {decoding_time:.6f} seconds")
        print(f"Decoded: {decoded_number}")
        print(f"Match: {number == decoded_number}")
        
        # Show the self-power decomposition
        print("\nSelf-Power Decomposition:")
        coeffs, self_powers, _ = self_power_decomposition(number)
        
        # Print the first few terms and the last few terms
        max_terms = 5
        if len(coeffs) <= max_terms * 2:
            # If there are few terms, print them all
            for i, (coeff, power) in enumerate(zip(coeffs, self_powers)):
                if coeff > 0:
                    print(f"  {coeff} × {i+1}^{i+1} = {coeff} × {power}")
        else:
            # Print first few terms
            for i in range(min(max_terms, len(coeffs))):
                if coeffs[i] > 0:
                    print(f"  {coeffs[i]} × {i+1}^{i+1} = {coeffs[i]} × {self_powers[i]}")
            
            print("  ...")
            
            # Print last few terms
            for i in range(len(coeffs) - max_terms, len(coeffs)):
                if coeffs[i] > 0:
                    print(f"  {coeffs[i]} × {i+1}^{i+1} = {coeffs[i]} × {self_powers[i]}")

if __name__ == "__main__":
    print_separator("BASIC USAGE EXAMPLE")
    demonstrate_basic_usage() 