#!/bin/python3
# -*- coding: utf-8 -*-

import sys


def is_unicode_supported() -> bool:
    """Check for Unicode characters support.

    Returns:
        bool: True or False
    """
    try:
        # Check if sys.stdout.encoding is set and supports Unicode
        return sys.stdout.encoding.lower() in ["utf-8", "utf-16", "utf-32", "utf-8-sig"]
    except AttributeError:
        # sys.stdout.encoding might not be available in some environments
        return False


def is_ascii_compatible_terminal() -> bool:
    """Check for ascii terminal compatible.

    Returns:
        bool: True or False
    """
    try:
        # Attempt to encode an ASCII character and check for errors
        print('\x07', end='', flush=True)
        return True
    except UnicodeEncodeError:
        return False
