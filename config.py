import os
import sys
from dataclasses import dataclass
os.system("")

TOKEN = 'CfDJ8J3HFu-R0HlNvutoAYRa68EjeSliPuQR8Ogt7niNVzgha2wJQ1jDNyCmxzGv95aKF911acVDx12U1BFi0z-JcR2taHJKjY6X0qWq2H5MD65oEZJYGUkzop-l7rOa8eJJKs1V9BjJZDjLPmdOsXmquBU'
COOKIE = '.AspNetCore.Antiforgery.pcAz0O62JyE=CfDJ8J3HFu-R0HlNvutoAYRa68FIgcbDEr06bq4cJyWCC5Pl6SyEHKMWynbvPsY7pf8KYwtuZLNZMHoMv8uhJxOUyWYpCA-yrH3NW8uH0pMACoc_u8afV2xtezmcOmG53Qe9uq8U7Hv-84UWvRRraNvbsQI'
SITE = 'https://tools.axinom.com/decoders/LicenseRequest'

# Separated by space and can set e.g [status]
# Must match from keys name from check.py @ line 96
FILE_NAME_FORMAT = 'manufacturer modelName systemId securityLevel [status]'
FILE_NAME_SEPARATOR = '-'


@dataclass(init=False)
class fg:
    RED: str = '\033[31m'
    GREEN: str = '\033[32m'
    YELLOW: str = '\033[33m'
    CYAN: str = '\033[36m'
    RESET: str = '\033[0m'


@dataclass(init=False)
class style:
    BRIGHT: str = '\033[1m'
    DIM: str = '\033[2m'
    NORMAL: str = '\033[22m'


# simple logger
def info(msg: str):
    print(f'{fg.GREEN}{style.DIM}[I]: {fg.RESET}{msg}')


def warn(msg: str):
    print(f'{fg.YELLOW}{style.DIM}[W]: {fg.RESET}{msg}')


def error(msg: str, auto_exit: bool = True):
    print(f'{fg.RED}{style.DIM}[E]: {fg.RESET}{msg}')
    if auto_exit:
        sys.exit()
