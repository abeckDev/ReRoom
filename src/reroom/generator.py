"""Image generation for redesigned rooms (Stage 3).

Builds a detailed prompt from the source and target analyses, then
calls GPT-Image-1 (or DALL-E 3) to produce photorealistic images.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

from openai import AzureOpenAI

from reroom.config import Config

def build_generation_prompt(
    source_analysis: dict,
    target_analysis: dict,
) -> str:
    """Build a detailed image-generation prompt.

    Merges the design description from the source room with the
    architectural constraints of the target room.

    Args:
        source_analysis: Output of analyze_source_room().
        target_analysis: Output of analyze_target_room().

    Returns:
        A prompt string ready for the image generation model.
    """
    furniture_json = json.dumps(
        source_analysis.get("furniture", []), indent=2
    )
    decorative_json = json.dumps(
        source_analysis.get("decorative_elements", []), indent=2
    )
    windows_json = json.dumps(target_analysis.get("windows", []))
    doors_json = json.dumps(target_analysis.get("doors", []))

    return f"""Transform this room photograph into a professionally designed living space.

KEEP EXACTLY from the target room:
- The room shape, dimensions, and architecture ({target_analysis.get('room_shape', 'rectangular')})
- Window positions: {windows_json}
- Door positions: {doors_json}
- The camera perspective and angle of the original photo

REMOVE from the target room:
- ALL existing clutter, mess, boxes, and temporary items
- Any existing mismatched furniture

APPLY this design concept from the source room:
- Interior style: {source_analysis.get('style', 'modern')}
- Mood: {source_analysis.get('mood', 'warm and inviting')}
- Color palette: {json.dumps(source_analysis.get('color_palette', []))}
- Wall treatment: {source_analysis.get('walls', 'neutral painted walls')}
- Flooring: {source_analysis.get('flooring', 'hardwood')}
- Lighting style: {source_analysis.get('lighting', 'warm ambient')}

PLACE these furniture items (adapted to fit the target room dimensions):
{furniture_json}

DECORATIVE ELEMENTS to include:
{decorative_json}

The result must be a photorealistic interior photograph that looks like a
real, professionally staged room. Maintain the exact camera perspective of

    input image."""

def generate_redesigned_room(
    source_analysis: dict,
    target_analysis: dict,
    target_image_path: str | Path,
    image_client: AzureOpenAI,
    config: Config,
    output_dir: str | Path = "output",
    num_variations: int = 1,
) -> list[str]:
    """Generate redesigned room images.

    Calls GPT-Image-1 to create photorealistic renderings of the target
    room with the source room's design applied.

    Args:
        source_analysis: Output of analyze_source_room().
        target_analysis: Output of analyze_target_room().
        target_image_path: Path to the target room image (for reference).
        image_client: An AzureOpenAI client configured for image generation.
        config: Application configuration.
        output_dir: Directory where generated images will be saved.
        num_variations: Number of image variations to generate.

    Returns:
        A list of file paths to the generated images.
    """
    prompt = build_generation_prompt(source_analysis, target_analysis)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    generated_paths: list[str] = []

    for i in range(num_variations):
        response = image_client.images.generate(
            model=config.image_model,
            prompt=prompt,
            n=1,
            size=config.image_size,
            quality=config.image_quality,
        )

        image_data = base64.b64decode(response.data[0].b64_json)

        suffix = f"_v{i + 1}" if num_variations > 1 else ""
        file_path = output_path / f"redesigned_room{suffix}.png"

        with open(file_path, "wb") as f:
            f.write(image_data)

        generated_paths.append(str(file_path))

    return generated_paths
