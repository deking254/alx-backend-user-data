#!/usr/bin/env python3
"""filtering logs"""
from re import sub


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for field in fields:
        regex = '(?<={}=)[^{}]*'.format(field, separator)
        message = sub(regex, redaction, message)
    return message
