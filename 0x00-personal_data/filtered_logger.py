#!/usr/bin/env python3
"""filtering logs"""
from re


def filter_datum(fields: List,
                 redaction: str, message: str, separator: str) - > str:
    """returns the log message obfuscated"""
    for field in fields:
        regex = '(?<={}=)[^{}]*'.format(field, separator)
        message = re.sub(regex, redaction, message)
    return message
