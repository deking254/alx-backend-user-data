#!/usr/bin/env python3
"""filtering logs"""
import re


def filter_datum(fields, redaction, message, separator):
    """returns the log message obfuscated"""
    for field in fields:
        regex = '(?<={}=)[^{}]*'.format(field, separator)
        message = re.sub(regex, redaction, message)
    return message
