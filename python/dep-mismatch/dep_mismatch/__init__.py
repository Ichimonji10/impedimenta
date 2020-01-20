#!/usr/bin/env python3
# coding=utf-8
"""Print info about an ISO-8601 string."""
from dateutil.parser import isoparse


def main():
    """Print info about an ISO-8601 string."""
    input_ = '2020-01-21T11:35-05'
    output = isoparse(input_)
    print(f'The string "{input_}" was parsed as {output}')
