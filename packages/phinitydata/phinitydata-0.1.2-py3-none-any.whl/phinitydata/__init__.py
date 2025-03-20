"""
Phinity Data - A package for generating synthetic data for LLMs
"""

__version__ = "0.1.2"

from .client import Client
from .testset.sft_generator import SFTGenerator
from .testset.rag_generator import TestsetGenerator

__all__ = ["Client", "SFTGenerator", "TestsetGenerator"]
