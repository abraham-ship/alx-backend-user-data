#!/usr/bin/env python3
'''Regex-ing'''
import re


def filter_datum(fields, redaction, message, separator):
    '''Regex-ing'''
    return re.sub(fr'({separator.join(fields)})[^{separator}]*(\
            ?:{separator}|$)', redaction, message)
