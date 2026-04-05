"""Room analysis using GPT-4o vision (Stages 1 & 2).

Stage 1: Analyze a source room to extract design style, furniture,
         color palette, and decorative elements.
Stage 2: Analyze a target room to extract architectural structure
         (shape, windows, doors) while ignoring clutter.
"""

from __future__ import annotations

import base64
import json
from pathlib import Path

from azure.ai.inference import ChatCompletionsClient

from reroom.config import Config

def _encode_image(image_path: str | Path) -> str:
    """Read an image file and return its base64-encoded string."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def analyze_source_room(
    image_path: str | Path,
    client: ChatCompletionsClient,
    config: Config,
) -> dict:
    """Extract design concept from a source room photograph.

    Uses GPT-4o vision to produce a structured JSON description of the
    room's interior design including furniture, colors, style, and mood.

    Args:
        image_path: Path to the source room image.
        client: An Azure AI Foundry ChatCompletionsClient.
        config: Application configuration.

    Returns:
        A dict with keys: style, mood, color_palette, furniture,
        flooring, walls, lighting, decorative_elements.
    """
    b64 = _encode_image(image_path)

    response = client.complete(
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
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)

def analyze_target_room(
    image_path: str | Path,
    client: ChatCompletionsClient,
    config: Config,
) -> dict:
    """Extract architectural structure from a target room photograph.

    Uses GPT-4o vision to understand the room's shell (shape, windows,
    doors, flooring) while deliberately ignoring any clutter, mess, or
    existing furniture.

    Args:
        image_path: Path to the target room image.
        client: An Azure AI Foundry ChatCompletionsClient.
        config: Application configuration.

    Returns:
        A dict with keys: room_shape, approximate_dimensions, windows,
        doors, flooring, ceiling_height_estimate, built_in_features,
        natural_light_direction.
    """
    b64 = _encode_image(image_path)

    response = client.complete(
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
        response_format={"type": "json_object"},
    )

    return json.loads(response.choices[0].message.content)
