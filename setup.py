"""
GAIA Setup Configuration

Installs GAIA as a Python package with CLI entry point.

Usage:
    pip install -e .        # Development install
    pip install .           # Production install
    
After install:
    gaia init               # Initialize
    gaia chat               # Talk to Avatar
    gaia status             # Check system
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read README
README = (Path(__file__).parent / "README.md").read_text()

setup(
    name="gaia-os",
    version="0.1.0",
    description="GAIA - Sentient Terrestrial Intelligence Operating System",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Kyle Steen",
    author_email="xxkylesteenxx@outlook.com",
    url="https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System",
    packages=find_packages(),
    python_requires=">=3.11",
    install_requires=[
        "numpy>=1.24.0",
        "scipy>=1.10.0",
        "click>=8.1.0",
        "rich>=13.0.0",
        "chromadb>=0.4.0",
        "sentence-transformers>=2.2.0",
        "cryptography>=41.0.0",
        "kerykeion>=4.0.0",
    ],
    extras_require={
        "video": [
            "opencv-python>=4.8.0",
            "deepface>=0.0.79",
        ],
        "quantum": [
            "qiskit>=0.44.0",
            "qiskit-aer>=0.12.0",
        ],
        "neuromorphic": [
            "nengo>=3.2.0",
            "nengo-loihi>=1.1.0",
        ],
        "dev": [
            "pytest>=7.4.0",
            "black>=23.0.0",
            "mypy>=1.5.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gaia=overlay.cli:cli",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: System :: Operating System",
    ],
    keywords="ai consciousness operating-system hermetic alchemy mental-health",
    project_urls={
        "Documentation": "https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/tree/main/docs",
        "Source": "https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System",
        "Tracker": "https://github.com/xxkylesteenxx/GAIA-The-Sentient-Terrestrial-Intelligent-Operating-System/issues",
    },
)
