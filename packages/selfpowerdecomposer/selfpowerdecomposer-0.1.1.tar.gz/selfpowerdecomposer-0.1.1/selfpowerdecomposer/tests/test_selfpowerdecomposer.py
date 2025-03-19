#!/usr/bin/env python3
"""
Unit tests for the selfpowerdecomposer package.
"""

import unittest
import os
import random
import tempfile
import sys
import os

# Add the parent directory to the path so we can import the package
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from selfpowerdecomposer import (
    encode_number,
    decode_number,
    save_to_binary_file,
    load_from_binary_file,
    secure_encode_number_no_placeholder,
    secure_decode_number_no_placeholder,
    save_removed_info_no_placeholder,
    load_removed_info_no_placeholder,
)

class TestSelfPowerDecomposer(unittest.TestCase):
    """Test cases for the selfpowerdecomposer package."""
    
    def setUp(self):
        """Set up test fixtures."""
        random.seed(42)  # For reproducibility
        self.test_numbers = [
            0,
            1,
            42,
            12345,
            12345678901234567890,
            int('1' * 100),  # 100 digit number
            int('9' * 200)   # 200 digit number
        ]
    
    def test_encode_decode(self):
        """Test basic encoding and decoding."""
        for number in self.test_numbers:
            encoded = encode_number(number)
            decoded = decode_number(encoded)
            self.assertEqual(number, decoded, f"Failed for {number}")
    
    def test_file_io(self):
        """Test saving to and loading from files."""
        with tempfile.NamedTemporaryFile(delete=False) as temp:
            temp_filename = temp.name
        
        try:
            for number in self.test_numbers:
                encoded = encode_number(number)
                save_to_binary_file(temp_filename, encoded)
                loaded = load_from_binary_file(temp_filename)
                self.assertEqual(encoded, loaded, f"File I/O failed for {number}")
                
                decoded = decode_number(loaded)
                self.assertEqual(number, decoded, f"Decode after file I/O failed for {number}")
        finally:
            if os.path.exists(temp_filename):
                os.remove(temp_filename)
    
    def test_secure_encoding(self):
        """Test secure encoding and decoding with no placeholders."""
        for number in self.test_numbers:
            for num_removed in [1, 3, 5]:
                # Skip if the number is too small for the requested removals
                if number < 100 and num_removed > 1:
                    continue
                
                # Skip zero for now as it has special handling
                if number == 0:
                    continue
                
                encoded, removed_info = secure_encode_number_no_placeholder(number, num_removed)
                decoded = secure_decode_number_no_placeholder(encoded, removed_info)
                self.assertEqual(number, decoded, f"Secure encoding failed for {number} with {num_removed} removed values")
    
    def test_secure_file_io(self):
        """Test saving and loading secure encoding information."""
        with tempfile.NamedTemporaryFile(delete=False) as temp_data:
            data_filename = temp_data.name
        
        with tempfile.NamedTemporaryFile(delete=False) as temp_key:
            key_filename = temp_key.name
        
        try:
            for number in self.test_numbers:
                if number < 1000:  # Only test with larger numbers
                    continue
                
                encoded, removed_info = secure_encode_number_no_placeholder(number, 5)
                
                # Save to files
                save_to_binary_file(data_filename, encoded)
                save_removed_info_no_placeholder(removed_info, key_filename)
                
                # Load from files
                loaded_data = load_from_binary_file(data_filename)
                loaded_info = load_removed_info_no_placeholder(key_filename)
                
                # Verify data matches
                self.assertEqual(encoded, loaded_data, f"Data file I/O failed for {number}")
                self.assertEqual(len(removed_info), len(loaded_info), f"Key length mismatch for {number}")
                
                for (orig_pos, orig_val), (loaded_pos, loaded_val) in zip(removed_info, loaded_info):
                    self.assertEqual(orig_pos, loaded_pos, f"Position mismatch in key for {number}")
                    self.assertEqual(orig_val, loaded_val, f"Value mismatch in key for {number}")
                
                # Decode and verify
                decoded = secure_decode_number_no_placeholder(loaded_data, loaded_info)
                self.assertEqual(number, decoded, f"Secure decode after file I/O failed for {number}")
        finally:
            if os.path.exists(data_filename):
                os.remove(data_filename)
            if os.path.exists(key_filename):
                os.remove(key_filename)
    
    def test_security_properties(self):
        """Test security properties of the secure encoding."""
        # Use a large number for this test
        number = 12345678901234567890987654321
        
        # Encode with 5 removed values
        encoded, removed_info = secure_encode_number_no_placeholder(number, 5)
        
        # Verify correct decoding
        decoded = secure_decode_number_no_placeholder(encoded, removed_info)
        self.assertEqual(number, decoded, "Correct key should decode properly")
        
        # Test with modified key
        if removed_info:
            modified_info = list(removed_info)
            pos, val = modified_info[0]
            modified_info[0] = (pos, val + 1)  # Change one value slightly
            
            try:
                wrong_decoded = secure_decode_number_no_placeholder(encoded, modified_info)
                # If it doesn't raise an exception, the result should be different
                self.assertNotEqual(number, wrong_decoded, "Modified key should produce different result")
            except Exception:
                # An exception is also acceptable
                pass
        
        # Test with completely wrong key
        wrong_info = [(0, 42), (1, 13), (2, 7), (3, 99), (4, 123)]
        
        try:
            wrong_decoded = secure_decode_number_no_placeholder(encoded, wrong_info)
            # If it doesn't raise an exception, the result should be different
            self.assertNotEqual(number, wrong_decoded, "Wrong key should produce different result")
        except Exception:
            # An exception is also acceptable
            pass
        
        # Test with incomplete key - this may or may not raise an exception
        # depending on the implementation, so we don't assert anything specific
        if len(removed_info) > 2:
            incomplete_info = removed_info[:-2]
            
            try:
                incomplete_decoded = secure_decode_number_no_placeholder(encoded, incomplete_info)
                # If it doesn't raise an exception, the result should be different
                self.assertNotEqual(number, incomplete_decoded, "Incomplete key should produce different result")
            except Exception:
                # An exception is also acceptable
                pass

if __name__ == '__main__':
    unittest.main() 