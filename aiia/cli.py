#!/usr/bin/env python
import sys
import argparse
import json

from . import parse

eprint = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)


def parse_command(file_path, input_format='markdown', output_format='json'):
    if file_path == "-":
        eprint("> Parsing chat logs from stdin")
        data = sys.stdin.read()
    else:
        eprint(f"> Parsing chat logs from file: {file_path}")
        with open(file_path, "r") as file:
            data = file.read()

    if input_format == 'markdown':
        eprint("> Parsing chat logs from markdown")
        data = parse.parse_chat_markdown(data)
    elif input_format == 'json':
        eprint("> Parsing chat logs from json")
        data = json.loads(data)

    if output_format == 'json':
        eprint("> Converting chat logs to json")
        print(json.dumps(data, indent=4))
    elif output_format == 'markdown':
        eprint("> Converting chat logs to markdown")
        print(parse.to_chat_markdown(data))


def respond_command():
    print("Given a chat log with a trailing user message, get GPT to respond")


def create_parser():
    parser = argparse.ArgumentParser(
        prog="aiia",
        description="The Army of AI Interns will help you accomplish anything you want",
    )

    subparsers = parser.add_subparsers(title="Commands", dest="command")

    parse_parser = subparsers.add_parser(
        "parse",
        help="parse a chatlog to and from `.json` and `.chat.md` formats",
    )
    parse_parser.add_argument(
        "file_path",
        nargs="?",
        default="-",
        help="file path to parse, reads from stdin if not provided",
    )

    parse_parser.add_argument(
        "-of", "--output-format", choices=["json", "markdown"], default="json"
    )

    parse_parser.add_argument(
        "-if", "--input-format", choices=["json", "markdown"], default="markdown"
    )

    respond_parser = subparsers.add_parser(
        "respond",
        help="given a chatlog with a trailing user message, get GPT to respond",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "parse":
        parse_command(args.file_path, input_format=args.input_format, output_format=args.output_format)
    elif args.command == "respond":
        respond_command()
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
