from argparse import ArgumentParser
from cli import CLI

def parse_args():
    parser = ArgumentParser()
    subs = parser.add_subparsers()

    # scrape subcommand
    scrape = subs.add_parser("scrape")
    scrape.set_defaults(func=CLI.scrape)

    # list subcommand
    _list = subs.add_parser("list")
    _list.set_defaults(func=CLI._list)

    # add subcommand
    add = subs.add_parser("add")
    add.set_defaults(func=CLI.add)

    args = parser.parse_args()

    return args