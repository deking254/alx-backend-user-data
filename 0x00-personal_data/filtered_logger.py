#!/usr/bin/env python3
"""filtering logs"""
from re
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        regex: str = '(?<={}=)[^{}]*'.format(field, separator)
        message: str = re.sub(regex, redaction, message)
    return message
