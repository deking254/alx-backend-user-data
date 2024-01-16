#!/usr/bin/env python3
"""filtering logs of personal data"""
import re
import logging
from typing import List
PII_FIELDS = ('name', 'email',  'phone', 'ssn', 'password')


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
        self.fields = fields
        super(RedactingFormatter, self).__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        """formats the personal data into a format"""
        if self.usesTime():
            record.asctime = self.formatTime(record)
        record.message = filter_datum(self.fields, self.REDACTION,
                                      record.getMessage(), self.SEPARATOR)
        return self.formatMessage(record)

def get_logger() -> logging.Logger:
    """returns a logging.Logger object."""
    logger = logging.Logger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    return logger
