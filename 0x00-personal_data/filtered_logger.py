#!/usr/bin/env python3
'''Regex-ing'''
import re
from typing import List


def filter_datum(fields: List[str], redaction: str,
                 message: str, separator: str) -> str:
    '''Regex-ing'''
    return re.sub(fr'({separator.join(fields)})[^{separator}]*(\
            ?:{separator}|$)', redaction, message)
