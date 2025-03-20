"""
A simple text wrapping tool
"""

# Supports only in Python 3.8+

from .txtwrap import (
    LOREM_IPSUM_W, LOREM_IPSUM_S, LOREM_IPSUM_P,
    mono, word, wrap, align, fillstr, printwrap,
    shorten
)

__version__ = '1.1.0'
__license__ = 'MIT'
__author__ = 'Azzam Muhyala'
__all__ = [
    'LOREM_IPSUM_W',
    'LOREM_IPSUM_S',
    'LOREM_IPSUM_P',
    'mono',
    'word',
    'wrap',
    'align',
    'fillstr',
    'printwrap',
    'shorten'
]