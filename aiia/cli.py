#!/usr/bin/env python
import sys
import argparse
import json

from typing import Dict, Any

from . import parse
from . import gpt

eprint = lambda *args, **kwargs: print(*args, file=sys.stderr, **kwargs)


def parse_command(file_path, input_format="markdown", output_format="json"):
    if file_path == "-":
        eprint("> Parsing chat logs from stdin")
        data = sys.stdin.read()
    else:
        eprint(f"> Parsing chat logs from file: {file_path}")
        with open(file_path, "r") as file:
            data = file.read()

    if input_format == "markdown":
        eprint("> Parsing chat logs from markdown")
        data = parse.parse_chat_markdown(data)
    elif input_format == "json":
        eprint("> Parsing chat logs from json")
        data = json.loads(data)

    if output_format == "json":
        eprint("> Converting chat logs to json")
        print(json.dumps(data, indent=4))
    elif output_format == "markdown":
        eprint("> Converting chat logs to markdown")
        print(parse.to_chat_markdown(data))


def respond_command(
    file_path, input_format="markdown", inplace=False, model="gpt-3.5-turbo"
):
    if file_path == "-":
        eprint("> Parsing chat logs from stdin")
        contents = sys.stdin.read()
    else:
        eprint(f"> Parsing chat logs from file: {file_path}")
        with open(file_path, "r") as file:
            contents = file.read()

    data: Dict[str, Any] = {}
    if input_format == "markdown":
        eprint("> Parsing chat logs from markdown")
        data = parse.parse_chat_markdown(contents)
    elif input_format == "json":
        eprint("> Parsing chat logs from json")
        data = json.loads(contents)
    elif input_format == "text":
        eprint("> Parsing chat logs from text")
        data = {
            "metadata": {},
            "messages": [
                {
                    "role": "user",
                    "content": contents,
                }
            ],
        }

    eprint("> Getting GPT to respond")
    model = data.get("metadata", {}).get("model", model)
    response = gpt.get_response(data.get("messages", []), model=model)
    if not inplace:
        for chunk in response:
            print(chunk, end="")
            sys.stdout.flush()
        print("")
        sys.stdout.flush()
    else:
        message = ""
        for chunk in response:
            message += chunk

        open(file_path, "w").write(
            parse.to_chat_markdown(
                {
                    "metadata": data.get("metadata", {}),
                    "messages": data.get("messages", [])
                    + [
                        {
                            "role": "assistant",
                            "content": message,
                        }
                    ],
                }
            )
        )


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
    respond_parser.add_argument(
        "file_path",
        nargs="?",
        default="-",
        help="file path to parse, reads from stdin if not provided",
    )
    respond_parser.add_argument(
        "-i", "--inplace", action="store_true", help="edit the file in place"
    )
    respond_parser.add_argument(
        "-m", "--model", default="gpt-3.5-turbo", help="model to use"
    )
    respond_parser.add_argument(
        "-if",
        "--input-format",
        choices=["json", "markdown", "text"],
        default="markdown",
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.command == "parse":
        parse_command(
            args.file_path,
            input_format=args.input_format,
            output_format=args.output_format,
        )
    elif args.command == "respond":
        respond_command(
            args.file_path,
            input_format=args.input_format,
            inplace=args.inplace,
            model=args.model,
        )
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
