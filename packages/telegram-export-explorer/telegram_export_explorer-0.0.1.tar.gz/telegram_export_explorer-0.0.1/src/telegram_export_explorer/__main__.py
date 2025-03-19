import sys

from .build_db import build_db

if __name__ == "__main__":
    # TODO Improve arg parsing
    build_db(*sys.argv[1:])
