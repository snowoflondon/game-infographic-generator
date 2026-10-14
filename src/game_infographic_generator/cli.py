"""Command-line entry point and metadata validation."""

import argparse
from pathlib import Path
import sys
from typing import Optional

from pydantic import ValidationError

from .models import GameMetadata


def main(argv: Optional[list[str]] = None) -> int:
    """Validate a JSON file or print the agent's readiness message."""
    parser = argparse.ArgumentParser(prog="game-infographic-generator")
    commands = parser.add_subparsers(dest="command")
    validate = commands.add_parser("validate", help="Validate game metadata JSON")
    validate.add_argument("path", type=Path)
    args = parser.parse_args(argv)
    if args.command is None:
        print("Game Infographic Agent ready")
        return 0
    try:
        GameMetadata.model_validate_json(args.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    print(f"Valid game metadata: {args.path}")
    return 0
