#!/usr/bin/env python3
"""filtering logs of personal data"""
import re
import logging
from typing import List


def filter_datum(fields: List[str],
                 redaction: str, message: str, separator: str) -> str:
    """returns the log message obfuscated"""
    for field in fields:
        regex = '(?<={}=)[^{}]*'.format(field, separator)
        message = re.sub(regex, redaction, message)
    return message


class RedactingFormatter(logging.Formatter):
    """ Redacting Formatter class
        """

    REDACTION = "***"
    FORMAT = "[HOLBERTON] %(name)s %(levelname)s %(asctime)-15s: %(message)s"
    SEPARATOR = ";"

    def __init__(self, fields: List[str]):
        """this functions is called first when the class is init"""
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """formats the personal data into a format"""
        NotImplementedError
