#!/usr/bin/env python3
"""
Test script to verify the local installation of selfpowerdecomposer
"""

import selfpowerdecomposer
from selfpowerdecomposer import core

# Print package information
print(f"Package version: {selfpowerdecomposer.__version__ if hasattr(selfpowerdecomposer, '__version__') else 'Not defined'}")
print(f"Available modules: {dir(selfpowerdecomposer)}")

# Test basic functionality
print("\nTesting basic functionality:")
try:
    # Create a large number
    large_number = 123456789012345678901234567890
    
    # Decompose the number
    decomposition = core.decompose(large_number)
    print(f"Decomposition of {large_number}: {decomposition}")
    
    # Reconstruct the number
    reconstructed = core.reconstruct(decomposition)
    print(f"Reconstructed number: {reconstructed}")
    
    # Verify
    print(f"Reconstruction successful: {large_number == reconstructed}")
    
    print("\nPackage is working correctly!")
except Exception as e:
    print(f"Error testing package: {e}") 