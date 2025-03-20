from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="selfpowerdecomposer",
    version="0.1.0",
    author="SelfPower Team",
    author_email="lordrichado@gmail.com",
    description="Large integer compression and secure encoding using self-power decomposition",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/joirichi/selfpowerdecomposer",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
        "Topic :: System :: Archiving :: Compression",
        "Topic :: Security :: Cryptography",
    ],
    python_requires=">=3.6",
    install_requires=[
        "gmpy2>=2.0.8",  # Required for efficient large integer operations
        "numpy>=1.19.0",  # For numerical operations
        "matplotlib>=3.3.0",  # For visualization (optional)
    ],
)
