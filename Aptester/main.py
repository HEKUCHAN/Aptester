# -*- coding: utf-8 -*-
import textwrap
import argparse
from . import commands
from fabric.colors import red

def main():
    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description = textwrap.dedent(
            """\
            This is a tool for Competitive programming.
            You can use this tool to run many tests automatically.

            ©Copyright 2022 Hirose Heitor\
            """
        )
    )

    # Initial command
    sub_parser: argparse._SubParsersAction = parser.add_subparsers(
        dest="command", help="Normal Command."
    )

    # Run command
    parser_run: argparse.ArgumentParser = sub_parser.add_parser(
        "run", help="Command to run the tests. see `run -h`"
    )
    parser_run.set_defaults(handler=commands.run)

    # Config command
    parser_config: argparse.ArgumentParser = parser_config.add_parser(
        "config", help="You can change or check the config of tests. `config -h`"
    )
    parser_config.set_defaults(handler=commands.config)

    args: argparse.ArgumentParser = parser.parse_args()

    if hasattr(args, "handler"):
        args.handler(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
