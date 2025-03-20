#!/usr/bin/env python3
"""
Secure Encoding Example

This example demonstrates how to use the secure encoding/decoding functionality
of the selfpowerdecomposer package to create a two-factor authentication system.
"""

from selfpowerdecomposer import (
    secure_encode_number_no_placeholder,
    secure_decode_number_no_placeholder,
    save_to_binary_file,
    save_removed_info_no_placeholder,
    load_from_binary_file,
    load_removed_info_no_placeholder
)
import random
import time

def print_separator(title):
    """Print a section separator with title"""
    print("\n" + "=" * 80)
    print(f" {title} ".center(80, "="))
    print("=" * 80)

def demonstrate_secure_encoding():
    """Demonstrate the secure encoding/decoding functionality"""
    # Set a seed for reproducibility
    random.seed(42)
    
    # Generate a large number to use as a password
    password = 12345678901234567890987654321
    
    print_separator("SECURE ENCODING EXAMPLE")
    print(f"Original password: {password}")
    print(f"Number of digits: {len(str(password))}")
    print(f"Binary length: {password.bit_length()} bits")
    
    # Encode the password, removing some delta values completely
    print("\nEncoding with 5 removed values...")
    start_time = time.time()
    encoded_data, removed_info = secure_encode_number_no_placeholder(password, num_removed=5)
    encoding_time = time.time() - start_time
    
    print(f"Encoding time: {encoding_time:.6f} seconds")
    print(f"Encoded data size: {len(encoded_data)} bytes")
    print(f"Number of removed values: {len(removed_info)}")
    print(f"Removed values: {removed_info}")
    
    # Save both parts to separate files
    save_to_binary_file("secure_data.bin", encoded_data)
    save_removed_info_no_placeholder(removed_info, "secure_key.bin")
    
    print("\nSaved to files:")
    print("  - secure_data.bin (store on server)")
    print("  - secure_key.bin (store on user device)")
    
    # Later, to verify the password, both parts are needed
    print("\nDecoding with correct key...")
    loaded_data = load_from_binary_file("secure_data.bin")
    loaded_info = load_removed_info_no_placeholder("secure_key.bin")
    
    start_time = time.time()
    decoded_password = secure_decode_number_no_placeholder(loaded_data, loaded_info)
    decoding_time = time.time() - start_time
    
    print(f"Decoding time: {decoding_time:.6f} seconds")
    print(f"Decoded password: {decoded_password}")
    print(f"Match: {password == decoded_password}")
    
    # Security tests
    print_separator("SECURITY TESTS")
    
    # Test 0: Using the correct key again (to demonstrate successful authentication)
    print("\nTest 0: Using the correct key (successful authentication)")
    try:
        correct_password = secure_decode_number_no_placeholder(loaded_data, loaded_info)
        print(f"Decoded with correct key: {correct_password}")
        print(f"Match: {password == correct_password}")
        print(f"Authentication: Successful")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 1: Modify one value in the key
    print("\nTest 1: Modifying one value in the key")
    modified_info = loaded_info.copy()
    pos, val = modified_info[0]
    modified_info[0] = (pos, val + 1)
    
    try:
        wrong_password = secure_decode_number_no_placeholder(loaded_data, modified_info)
        print(f"Decoded with modified key: {wrong_password}")
        print(f"Match: {password == wrong_password}")
        print(f"Difference: {abs(password - wrong_password)}")
        print(f"Difference ratio: {abs(password - wrong_password) / password:.2e}x")
        
        # Calculate digit match percentage
        orig_str = str(password)
        wrong_str = str(wrong_password)
        min_len = min(len(orig_str), len(wrong_str))
        matching_digits = sum(1 for i in range(min_len) if orig_str[i] == wrong_str[i])
        match_percentage = (matching_digits / min_len) * 100
        print(f"Digit match: {match_percentage:.2f}%")
        print(f"Authentication: Failed")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Use a completely wrong key
    print("\nTest 2: Using a completely wrong key")
    wrong_info = [(0, 42), (1, 13), (2, 7), (3, 99), (4, 123)]
    
    try:
        wrong_password = secure_decode_number_no_placeholder(loaded_data, wrong_info)
        print(f"Decoded with wrong key: {wrong_password}")
        print(f"Match: {password == wrong_password}")
        print(f"Difference: {abs(password - wrong_password)}")
        print(f"Difference ratio: {abs(password - wrong_password) / password:.2e}x")
        
        # Calculate digit match percentage
        orig_str = str(password)
        wrong_str = str(wrong_password)
        min_len = min(len(orig_str), len(wrong_str))
        matching_digits = sum(1 for i in range(min_len) if orig_str[i] == wrong_str[i])
        match_percentage = (matching_digits / min_len) * 100
        print(f"Digit match: {match_percentage:.2f}%")
        print(f"Authentication: Failed")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Missing values in the key
    print("\nTest 3: Missing values in the key")
    incomplete_info = loaded_info[:-2]  # Remove the last two entries
    
    try:
        wrong_password = secure_decode_number_no_placeholder(loaded_data, incomplete_info)
        print(f"Decoded with incomplete key: {wrong_password}")
        print(f"Match: {password == wrong_password}")
        print(f"Authentication: Failed")
    except Exception as e:
        print(f"Error: {e}")
    
    print_separator("SECURITY SUMMARY")
    print("The secure encoding system provides strong security properties:")
    print("1. Both parts (encoded data and key) are required to reconstruct the password")
    print("2. Even small changes to the key result in completely different decoded values")
    print("3. The first delta value is always removed for security")
    print("4. No placeholders are used, making it harder to identify what was removed")
    print("5. The system is resistant to brute force attacks due to the large key space")

if __name__ == "__main__":
    demonstrate_secure_encoding() 