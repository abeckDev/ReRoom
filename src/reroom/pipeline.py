"""Full pipeline orchestrator for ReRoom.

Ties together the three stages — source analysis, target analysis,
and image generation — into a single convenient function.
"""

from __future__ import annotations

import json
from pathlib import Path

from reroom.analyzer import analyze_source_room, analyze_target_room
from reroom.clients import create_analysis_client, create_image_client
from reroom.config import Config, load_config
from reroom.generator import generate_redesigned_room

def run_pipeline(
    source_image: str | Path,
    target_image: str | Path,
    output_dir: str | Path = "output",
    variations: int = 1,
    config: Config | None = None,
) -> list[str]:
    """Run the full ReRoom design-transfer pipeline.

    1. Analyze the source room's design (GPT-4o vision).
    2. Analyze the target room's architecture (GPT-4o vision).
    3. Generate redesigned room images (GPT-Image-1).

    Args:
        source_image: Path to the source (designed) room image.
        target_image: Path to the target (new / messy) room image.
        output_dir: Directory for generated images (created if needed).
        variations: Number of design variations to generate.
        config: Optional pre-built Config; loaded from env if None.

    Returns:
        A list of file paths to the generated images.
    """
    if config is None:
        config = load_config()

    analysis_client = create_analysis_client(config)
    image_client = create_image_client(config)

    # Stage 1 — Source room design extraction
    print("🔍 Stage 1: Analyzing source room design...")
    source_analysis = analyze_source_room(source_image, analysis_client, config)
    print(f"   Style detected: {source_analysis.get('style', 'N/A')}")
    print(f"   Furniture items: {len(source_analysis.get('furniture', []))}")
    print(f"   Color palette: {source_analysis.get('color_palette', [])}")

    # Stage 2 — Target room structure extraction
    print("\n🏗️  Stage 2: Analyzing target room structure...")
    target_analysis = analyze_target_room(target_image, analysis_client, config)
    print(f"   Room shape: {target_analysis.get('room_shape', 'N/A')}")
    print(f"   Windows: {len(target_analysis.get('windows', []))}")
    print(f"   Doors: {len(target_analysis.get('doors', []))}")

    # Save analyses for debugging / iteration
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "source_analysis.json").write_text(
        json.dumps(source_analysis, indent=2, ensure_ascii=False)
    )
    (out / "target_analysis.json").write_text(
        json.dumps(target_analysis, indent=2, ensure_ascii=False)
    )

    # Stage 3 — Image generation
    print(f"\n🎨 Stage 3: Generating redesigned room ({variations} variation(s))...")
    results = generate_redesigned_room(
        source_analysis=source_analysis,
        target_analysis=target_analysis,
        target_image_path=target_image,
        image_client=image_client,
        config=config,
        output_dir=output_dir,
        num_variations=variations,
    )

    for path in results:
        print(f"   ✅ Saved: {path}")

    print("\n🏠 Done! Your redesigned room is ready.")
    return results
