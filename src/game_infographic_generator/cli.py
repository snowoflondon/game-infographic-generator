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
    single = commands.add_parser("single-game", help="Render a single-game PNG")
    single.add_argument("path", type=Path)
    single.add_argument("output", type=Path)
    single.add_argument("--artwork", type=Path, help="Approved local PNG, JPEG or WebP")
    single.add_argument("--presentation", type=Path, help="Condensed presentation JSON required with --artwork")
    rankings = commands.add_parser("rankings", help="Render exactly ten personal rankings")
    rankings.add_argument("path", type=Path, help="Rankings manifest JSON")
    rankings.add_argument("output", type=Path)
    rankings.add_argument("--check", action="store_true", help="Validate manifest and local inputs without launching Chromium or exporting")
    args = parser.parse_args(argv)
    if args.command is None:
        print("Game Infographic Agent ready")
        return 0
    if args.command == "rankings":
        from .rankings_models import RankingsInput
        from .rendering.rankings import RankingsRenderingError, build_rankings_html, input_paths, render_rankings

        try:
            ranking = RankingsInput.model_validate_json(args.path.read_text(encoding="utf-8"))
            if args.output.suffix.lower() != ".png":
                raise RankingsRenderingError("Output path must end in .png")
            if args.output.resolve() in {args.path.resolve(), *input_paths(ranking, args.path.resolve().parent)}:
                raise RankingsRenderingError("Output must not overwrite rankings inputs")
            if args.check:
                build_rankings_html(ranking, args.path.resolve().parent)
                print(f"Valid rankings and local inputs: {args.path}; no PNG exported")
            else:
                width, height = render_rankings(ranking, args.output, args.path.resolve().parent)
                print(f"Saved {args.output} ({width} x {height} pixels)")
        except (OSError, UnicodeError, ValidationError, RankingsRenderingError) as exc:
            print(f"Rankings failed: {exc}", file=sys.stderr)
            return 1
        return 0
    try:
        metadata = GameMetadata.model_validate_json(args.path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, ValidationError) as exc:
        print(f"Validation failed: {exc}", file=sys.stderr)
        return 1
    if args.command == "single-game":
        from .rendering.single_game import RenderingError, render_single_game
        from .rendering.presentation import ArtworkPresentation

        try:
            if args.output.resolve() in {args.path.resolve(), args.artwork.resolve() if args.artwork else None}:
                raise RenderingError("Output must not overwrite metadata or artwork")
            presentation = ArtworkPresentation.model_validate_json(args.presentation.read_text(encoding='utf-8')) if args.presentation else None
            if args.presentation and args.output.resolve() == args.presentation.resolve():
                raise RenderingError('Output must not overwrite presentation input')
            width, height = render_single_game(metadata, args.output, args.artwork, presentation)
        except (OSError, UnicodeError, ValidationError, RenderingError) as exc:
            print(f"Rendering failed: {exc}", file=sys.stderr)
            return 1
        print(f"Saved {args.output} ({width} x {height} pixels)")
    else:
        print(f"Valid game metadata: {args.path}")
    return 0
