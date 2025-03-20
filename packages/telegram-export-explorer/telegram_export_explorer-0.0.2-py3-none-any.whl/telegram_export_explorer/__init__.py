import sys

from .build_db import build_db


def cli_build_db() -> None:
    # TODO Improve arg parsing
    build_db(*sys.argv[1:])
