"""Room analysis using GPT-4o vision (Stages 1 & 2).

Stage 1: Analyze a source room to extract design style, furniture,
         color palette, and decorative elements.
Stage 2: Analyze a target room to extract architectural structure
         (shape, windows, doors) while ignoring clutter.
"""

from __future__ import annotations

import base64
import io
import json
from pathlib import Path

from PIL import Image
from pillow_heif import register_heif_opener
from openai import AzureOpenAI

from reroom.config import Config

# Register HEIF opener with Pillow
register_heif_opener()

def _parse_json_response(content: str) -> dict:
    """Parse JSON from model response, handling markdown code blocks."""
    if not content:
        raise ValueError("Empty response from model")
    
    # Remove markdown code fences if present
    content = content.strip()
    if content.startswith("```json"):
        content = content[7:]  # Remove ```json
    elif content.startswith("```"):
        content = content[3:]  # Remove ```
    
    if content.endswith("```"):
        content = content[:-3]  # Remove closing ```
    
    content = content.strip()
    
    try:
        return json.loads(content)
    except json.JSONDecodeError as e:
        print(f"\nFailed to parse JSON response.")
        print(f"Raw content:\n{content}")
        raise ValueError(f"Model returned invalid JSON: {e}") from e

def _encode_image(image_path: str | Path) -> str:
    """Read an image file, convert to JPEG if needed, and return base64 string.
    
    Azure OpenAI accepts: webp, gif, jpeg, png (not HEIC).
    This function converts HEIC and other formats to JPEG.
    """
    # Open the image (works with HEIC thanks to pillow-heif)
    image = Image.open(image_path)
    
    # Convert to RGB if needed (handles RGBA, grayscale, etc.)
    if image.mode not in ("RGB", "L"):
        image = image.convert("RGB")
    
    # Save to JPEG in memory
    buffer = io.BytesIO()
    image.save(buffer, format="JPEG", quality=95)
    buffer.seek(0)
    
    return base64.b64encode(buffer.read()).decode("utf-8")

def analyze_source_room(
    image_path: str | Path,
    client: AzureOpenAI,
    config: Config,
) -> dict:
    """Extract design concept from a source room photograph.

    Uses GPT-4o vision to produce a structured JSON description of the
    room's interior design including furniture, colors, style, and mood.

    Args:
        image_path: Path to the source room image.
        client: An AzureOpenAI client.
        config: Application configuration.

    Returns:
        A dict with keys: style, mood, color_palette, furniture,
        flooring, walls, lighting, decorative_elements.
    """
    b64 = _encode_image(image_path)

    response = client.chat.completions.create(
        model=config.analysis_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interior designer. Analyze the room image "
                    "and return a structured JSON description including: furniture "
                    "items (type, color, material, approximate size, position in "
                    "the room), color palette, design style, lighting description, "
                    "flooring, wall treatment, and overall mood."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this room in detail. Return JSON with keys: "
                            "style, mood, color_palette (list of hex strings), "
                            "furniture (list of objects with type/color/material/"
                            "size/position), flooring, walls, lighting, "
                            "decorative_elements (list of strings)."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            },
        ],
    )

    return _parse_json_response(response.choices[0].message.content)

def analyze_target_room(
    image_path: str | Path,
    client: AzureOpenAI,
    config: Config,
) -> dict:
    """Extract architectural structure from a target room photograph.

    Uses GPT-4o vision to understand the room's shell (shape, windows,
    doors, flooring) while deliberately ignoring any clutter, mess, or
    existing furniture.

    Args:
        image_path: Path to the target room image.
        client: An AzureOpenAI client.
        config: Application configuration.

    Returns:
        A dict with keys: room_shape, approximate_dimensions, windows,
        doors, flooring, ceiling_height_estimate, built_in_features,
        natural_light_direction.
    """
    b64 = _encode_image(image_path)

    response = client.chat.completions.create(
        model=config.analysis_model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert interior designer and spatial analyst. "
                    "Analyze the room image IGNORING any clutter, mess, or "
                    "existing furniture. Focus on the architectural shell: room "
                    "shape, approximate dimensions, window positions and sizes, "
                    "door positions, flooring type, ceiling height, and any "
                    "built-in features."
                ),
            },
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": (
                            "Analyze this room's architectural structure (ignore "
                            "all clutter and furniture). Return JSON with keys: "
                            "room_shape, approximate_dimensions, windows (list "
                            "with position/size), doors (list with position), "
                            "flooring, ceiling_height_estimate, built_in_features "
                            "(list), natural_light_direction."
                        ),
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            },
        ],
    )

    return _parse_json_response(response.choices[0].message.content)
