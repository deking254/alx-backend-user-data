#!/usr/bin/env python3
"""filtering logs of personal data"""
import re
import logging
import os
import mysql.connector
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
    logger.name = "user_data"
    logger.setLevel(logging.INFO)
    logger.propagate = False
    streemHandler = logging.StreamHandler().setFormatter(RedactingFormatter(PII_FIELDS))
    logger.addHandler(streemHandler)
    return logger

def get_db() -> mysql.connector.connection.MySQLConnection:
    """returns a connector to the database"""
    user = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    database = os.getenv('PERSONAL_DATA_DB_NAME')
    kwargs = {'user': user, 'password': password, 'host': host, 'database': database, 'port': 3306}
    return  mysql.connector.connection.MySQLConnection(**kwargs)
