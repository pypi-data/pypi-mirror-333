"""
Phinity: Synthetic data generation for AI systems
"""

__version__ = "0.1.0"

from .client import Client
from .testset.rag_generator import TestsetGenerator
from .testset.sft_generator import SFTGenerator

__all__ = ["Client", "TestsetGenerator", "SFTGenerator"]
