import argparse
import logging
import os

from . import __version__, api, constants
from .flight import flight

logger = logging.getLogger("arrakis")

##########


parser = argparse.ArgumentParser()
parser.add_argument("--version", "-v", action="version", version=__version__)
subparsers = parser.add_subparsers()


def add_subparser(cmd, **kwargs):
    sp = subparsers.add_parser(
        cmd.__name__,
        help=cmd.__doc__.splitlines()[0],
        description=cmd.__doc__,
        **kwargs,
    )
    sp.set_defaults(func=cmd)
    return sp


##########


def parse_pattern(pattern):
    if not pattern or pattern == "*":
        pattern = constants.DEFAULT_MATCH
    return pattern


def print_channel(chan):
    print(repr(chan))


##########


def count(args):
    """count channels matching pattern"""
    print(
        api.count(
            parse_pattern(args.pattern),
        )
    )


sparser = add_subparser(count)
sparser.add_argument("pattern", nargs="?", help="channel pattern")


def find(args):
    """find channels matching regexp pattern"""
    for chan in api.find(parse_pattern(args.pattern)):
        print_channel(chan)


sparser = add_subparser(find, aliases=["search", "list"])
sparser.add_argument("pattern", nargs="?", help="channel name regexp")


def describe(args):
    """describe channels"""
    for chan in api.describe(args.channels):
        print_channel(chan)


sparser = add_subparser(describe, aliases=["show"])
sparser.add_argument("channels", nargs="+", help="list of channels to describe")


def fetch(args):
    """fetch data for channels"""
    data = api.fetch(
        args.channels,
        start=args.start,
        end=args.end,
    )
    print(data)


sparser = add_subparser(fetch)
sparser.add_argument("channels", nargs="+", help="list of channels to fetch")
sparser.add_argument("--start", required=True, type=int, help="start time GPS")
sparser.add_argument("--end", required=True, type=int, help="end time GPS")


def stream(args):
    """stream data for channels"""
    for buf in api.stream(
        args.channels,
        start=args.start,
        end=args.end,
    ):
        print(buf)


sparser = add_subparser(stream)
sparser.add_argument("channels", nargs="+", help="list of channels to stream")
sparser.add_argument("--start", type=int, help="start time GPS")
sparser.add_argument("--end", type=int, help="end time GPS")

##########


def main():
    logger.setLevel(os.getenv("LOG_LEVEL", "DEBUG").upper())
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(message)s"))
    logger.addHandler(handler)

    args = parser.parse_args()

    if "func" not in args:
        parser.print_help()
        return

    func = args.func
    del args.func
    logger.debug(args)

    try:
        func(args)
    except flight.FlightError as e:
        msg = f"request error: {e}"
        raise SystemExit(msg) from e


if __name__ == "__main__":
    import signal

    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
