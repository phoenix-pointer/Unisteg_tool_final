# src/universal_steg/cli.py

import argparse
import sys

from . import core


def build_parser() -> argparse.ArgumentParser:
    """
    Build and return the top-level argument parser.
    """
    parser = argparse.ArgumentParser(
        prog="universal-steg",
        description="Universal Steganography tool with pluggable encoders/decoders.",
    )

    subparsers = parser.add_subparsers(
        title="commands",
        dest="command",
        required=True,
        help="Available commands",
    )

    # universal-steg analyze <FILE>
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Automatically analyze a file with all suitable plugins.",
    )
    analyze_parser.add_argument(
        "file",
        help="Path to the file to analyze.",
    )
    analyze_parser.set_defaults(func=cmd_analyze)

    # universal-steg analyze-with <PLUGIN> <FILE>
    analyze_with_parser = subparsers.add_parser(
        "analyze-with",
        help="Analyze a file with a specific plugin by name.",
    )
    analyze_with_parser.add_argument(
        "plugin",
        help="Name of the plugin (see 'list-plugins').",
    )
    analyze_with_parser.add_argument(
        "file",
        help="Path to the file to analyze.",
    )
    analyze_with_parser.set_defaults(func=cmd_analyze_with)

    # universal-steg encode <PLUGIN> <COVER_FILE> <SECRET> <DEST>
    encode_parser = subparsers.add_parser(
        "encode",
        help="Encode secret data into a cover file using a specific plugin.",
    )
    encode_parser.add_argument(
        "plugin",
        help="Name of the plugin to use.",
    )
    encode_parser.add_argument(
        "cover",
        help="Path to the cover file (image/audio/etc.).",
    )
    encode_parser.add_argument(
        "secret",
        help="Secret data to hide (string).",
    )
    encode_parser.add_argument(
        "dest",
        help="Destination path for the stego file.",
    )
    encode_parser.set_defaults(func=cmd_encode)

    # universal-steg list-plugins
    list_parser = subparsers.add_parser(
        "list-plugins",
        help="List all available plugins.",
    )
    list_parser.set_defaults(func=cmd_list_plugins)

    return parser


def cmd_analyze(args: argparse.Namespace) -> int:
    """
    Handler for: universal-steg analyze <FILE>
    """
    result = core.analyze_file(args.file)
    if result is not None:
        print(result)
    return 0


def cmd_analyze_with(args: argparse.Namespace) -> int:
    """
    Handler for: universal-steg analyze-with <PLUGIN> <FILE>
    """
    result = core.analyze_with_plugin(args.file, args.plugin)
    if result is not None:
        print(result)
    return 0


def cmd_encode(args: argparse.Namespace) -> int:
    """
    Handler for: universal-steg encode <PLUGIN> <COVER_FILE> <SECRET> <DEST>
    """
    # SECRET is passed as a string; plugins can accept str or encode to bytes.
    msg = core.encode(args.cover, args.plugin, args.secret, args.dest)
    # core.encode returns either an error string or None on success.
    if isinstance(msg, str):
        print(msg)
    else:
        print(f"[{args.plugin}] Encoding completed -> {args.dest}")
    return 0


def cmd_list_plugins(args: argparse.Namespace) -> int:
    """
    Handler for: universal-steg list-plugins
    """
    plugins = core.list_plugins()
    if not plugins:
        print("No plugins found.")
        return 0

    print("Available plugins:")
    for name in plugins:
        print(f"  - {name}")
    return 0


def main(argv: list[str] | None = None) -> int:
    """
    Main entry point for the CLI.
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = build_parser()
    args = parser.parse_args(argv)

    func = getattr(args, "func", None)
    if func is None:
        parser.print_help()
        return 1

    return func(args)


if __name__ == "__main__":
    raise SystemExit(main())
