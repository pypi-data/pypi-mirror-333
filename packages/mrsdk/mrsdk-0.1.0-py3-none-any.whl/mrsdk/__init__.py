"""
MindRoot API SDK - A simple Python client for the MindRoot API.

This SDK provides an easy way to interact with MindRoot AI agents programmatically.
"""

from .client import MindRootClient
from .exceptions import MindRootError

__version__ = '0.1.0'
__all__ = ['MindRootClient', 'MindRootError']
