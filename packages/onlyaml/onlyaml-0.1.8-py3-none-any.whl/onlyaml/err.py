import sys


def perr_exit(value, exit_code=1):
    print(value, file=sys.stderr)
    exit(exit_code)
