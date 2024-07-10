from argparse import ArgumentParser
from cli import CLI

def parse_args():
    parser = ArgumentParser()
    subs = parser.add_subparsers()

    # scrape subcommand
    scrape = subs.add_parser("scrape")
    scrape.set_defaults(func=CLI.scrape)
    scrape.add_argument("-c", "--condition", type=str, action="append", default=[])

    # list subcommand
    _list = subs.add_parser("list")
    _list.set_defaults(func=CLI._list)
    _list.add_argument("-m", "--mode", required=True, choices=["brands", "tools"])
    _list.add_argument("-b", "--brand", type=str, default=None)

    # add subcommand
    add = subs.add_parser("add")
    add.set_defaults(func=CLI.add)
    add.add_argument("-n", "--name", required=True, type=str)
    add.add_argument("-m", "--model", required=True, type=str)
    add.add_argument("-b", "--brand", required=True, type=str)

    args = parser.parse_args()

    return args