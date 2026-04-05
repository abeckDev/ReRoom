"""CLI entry point for ReRoom.

Usage:
    python -m reroom --source designed_room.jpg --target messy_room.jpg
    python -m reroom --source designed_room.jpg --target messy_room.jpg --variations 3
"""

from __future__ import annotations

import argparse
import sys

from reroom.pipeline import run_pipeline

def main(argv: list[str] | None = None) -> None:
    """Parse arguments and run the ReRoom pipeline."""
    parser = argparse.ArgumentParser(
        prog="reroom",
        description="ReRoom — Reimage your Room via AI. Transfer the design "
        "concept from a source room photo into a target room photo.",
    )
    parser.add_argument(
        "--source",
        required=True,
        help="Path to the source (designed) room image.",
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path to the target (new / messy) room image.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory for generated images (default: output).",
    )
    parser.add_argument(
        "--variations",
        type=int,
        default=1,
        help="Number of design variations to generate (default: 1).",
    )

    args = parser.parse_args(argv)

    run_pipeline(
        source_image=args.source,
        target_image=args.target,
        output_dir=args.output_dir,
        variations=args.variations,
    )


if __name__ == "__main__":
    main()