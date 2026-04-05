"""Azure AI client initialization for ReRoom.

Provides factory functions that create properly configured clients
for the Azure AI Foundry (GPT-4o vision) and Azure OpenAI (image
generation) services.
"""

from __future__ import annotations

from azure.ai.inference import ChatCompletionsClient
from azure.core.credentials import AzureKeyCredential
from openai import AzureOpenAI

from reroom.config import Config

def create_analysis_client(config: Config) -> ChatCompletionsClient:
    """Create an Azure AI Foundry ChatCompletionsClient for GPT-4o vision.

    Args:
        config: Application configuration with Azure credentials.

    Returns:
        A configured ChatCompletionsClient instance.
    """
    return ChatCompletionsClient(
        endpoint=config.azure_ai_foundry_endpoint,
        credential=AzureKeyCredential(config.azure_ai_foundry_api_key),
    )

def create_image_client(config: Config) -> AzureOpenAI:
    """Create an Azure OpenAI client for image generation.

    Args:
        config: Application configuration with Azure credentials.

    Returns:
        A configured AzureOpenAI instance.
    """
    return AzureOpenAI(
        azure_endpoint=config.azure_openai_endpoint,
        api_key=config.azure_openai_api_key,
        api_version="2025-04-01-preview",
    )
