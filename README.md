# 🏠 ReRoom

> *Your style. Any space.*

**ReRoom** is an AI-powered room design transfer application built on [Microsoft Azure AI Foundry](https://ai.azure.com/). Give it a photo of a beautifully designed room and a photo of a new (potentially messy) room — ReRoom will reimagine the new space with the design concept, furniture, and style from the source room.

---

## ✨ How It Works

ReRoom uses a **3-stage AI pipeline** to analyze, understand, and generate room designs:

```
┌─────────────────┐      ┌─────────────────┐
│   Source Room    │      │   Target Room    │
│  (designed)      │      │  (messy / new)   │
└────────┬────────┘      └────────┬────────┘
         │                        │
         ▼                        ▼
┌─────────────────┐      ┌─────────────────────┐
│  Stage 1         │      │  Stage 2             │
│  Extract style,  │      │  Analyze room        │
│  furniture &     │      │  structure, ignore   │
│  design concept  │      │  clutter & mess      │
│  (GPT-4o Vision) │      │  (GPT-4o Vision)     │
└────────┬────────┘      └────────┬────────────┘
         │                        │
         └──────────┬─────────────┘
                    ▼
         ┌─────────────────────┐
         │  Stage 3             │
         │  Generate redesigned │
         │  room image          │
         │  (GPT-Image-1)       │
         └──────────┬──────────┘
                    ▼
         ┌─────────────────────┐
         │  🖼️ Output:          │
         │  New room with       │
         │  source design       │
         └─────────────────────┘
```

### Stage 1 — Analyze Source Room (Design Extraction)
Uses **GPT-4o (vision)** to extract a structured description of the source room's design, including:
- Furniture items (type, color, material, position)
- Color palette (hex values)
- Design style & mood
- Lighting, flooring, wall treatment
- Decorative elements

### Stage 2 — Analyze Target Room (Structure Extraction)
Uses **GPT-4o (vision)** to understand the target room's architectural shell — ignoring any clutter, mess, or existing furniture:
- Room shape & approximate dimensions
- Window and door positions
- Flooring type, ceiling height
- Built-in features & natural light direction

### Stage 3 — Generate Redesigned Room
Combines both analyses into a detailed prompt and uses **GPT-Image-1** (or DALL·E 3 as fallback) to produce a photorealistic image of the target room transformed with the source room's design.

---

## 🤖 Models Used

| Stage | Model | Purpose |
|-------|-------|---------|
| Design Extraction | **GPT-4o** | Best multimodal understanding; extracts structured JSON from images |
| Structure Analysis | **GPT-4o** | Spatial reasoning about room layout while ignoring clutter |
| Image Generation | **GPT-Image-1** | Highest quality photorealistic generation with instruction following |
| *Fallback Generation* | **DALL·E 3** | Alternative if GPT-Image-1 is unavailable in your region |

All models are accessed through **Microsoft Azure AI Foundry**.

---

## 📋 Prerequisites

- **Python 3.10+**
- An **Azure AI Foundry** account with access to GPT-4o
- An **Azure OpenAI** resource with access to GPT-Image-1 or DALL·E 3

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abeckDev/ReRoom.git
cd ReRoom

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your Azure credentials
```

---

## ⚙️ Configuration

Copy `.env.example` to `.env` and fill in your Azure credentials:

```env
AZURE_AI_FOUNDRY_ENDPOINT=https://your-endpoint.services.ai.azure.com/
AZURE_AI_FOUNDRY_API_KEY=your-foundry-api-key
AZURE_OPENAI_ENDPOINT=https://your-openai-endpoint.openai.azure.com/
AZURE_OPENAI_API_KEY=your-openai-api-key
```

| Variable | Description |
|----------|-------------|
| `AZURE_AI_FOUNDRY_ENDPOINT` | Your Azure AI Foundry endpoint URL |
| `AZURE_AI_FOUNDRY_API_KEY` | API key for Azure AI Foundry (GPT-4o access) |
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI service endpoint |
| `AZURE_OPENAI_API_KEY` | API key for Azure OpenAI (image generation) |

---

## 🎯 Usage

### Command Line

```bash
# Basic usage
python -m reroom --source designed_room.jpg --target messy_room.jpg

# Generate multiple variations
python -m reroom --source designed_room.jpg --target messy_room.jpg --variations 3

# Custom output directory
python -m reroom --source designed_room.jpg --target messy_room.jpg --output-dir my_results
```

### As a Python Library

```python
from reroom.pipeline import run_pipeline

results = run_pipeline(
    source_image="designed_room.jpg",
    target_image="messy_room.jpg",
    output_dir="output",
    variations=2,
)

for path in results:
    print(f"Generated: {path}")
```

---

## 📁 Project Structure

```
ReRoom/
├── src/
│   └── reroom/
│       ├── __init__.py        # Package initialization
│       ├── __main__.py        # CLI entry point
│       ├── analyzer.py        # GPT-4o vision analysis (Stages 1 & 2)
│       ├── clients.py         # Azure AI client initialization
│       ├── config.py          # Environment & configuration management
│       ├── generator.py       # Image generation (Stage 3)
│       └── pipeline.py        # Full pipeline orchestrator
├── .env.example               # Environment variable template
├── .gitignore                 # Git ignore rules
├── LICENSE                    # MIT License
├── README.md                  # This file
├── pyproject.toml             # Python project metadata
└── requirements.txt           # Python dependencies
```

---

## 💡 Tips for Better Results

1. **Use well-lit source photos** — The clearer the design in the source, the better the extraction.
2. **Generate multiple variations** — Use `--variations 3` and pick the best result.
3. **Iterate on results** — The pipeline is designed for quick re-runs with different source images.
4. **Source room angle matters** — Similar camera angles between source and target yield the most coherent results.
5. **Two-pass approach** — For very cluttered target rooms, consider running twice: first to "clean" the room, then to furnish it.

---

## 🗺️ Roadmap

- [x] Core 3-stage AI pipeline
- [x] CLI interface
- [ ] Web UI (Streamlit / Gradio)
- [ ] iPad app with Apple Pencil annotation support
- [ ] AR preview using ARKit (iPad)
- [ ] Side-by-side comparison view
- [ ] Design style presets (Scandinavian, Industrial, Bohemian, etc.)
- [ ] Feedback loop ("move the sofa to the left wall")

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  Made with 🏠 by the ReRoom team
</p>