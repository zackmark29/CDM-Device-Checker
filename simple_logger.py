import sys


def printf(tag: str, msg: str, sep='\t'):
    print(f'[{tag.upper()}]:{sep}', msg)


def info(msg: str):
    printf('INFO', msg)


def warn(msg: str):
    printf('WARN', msg)


def error(msg: str, auto_exit: bool = True):
    printf('ERROR', msg, "")
    if auto_exit:
        sys.exit()
