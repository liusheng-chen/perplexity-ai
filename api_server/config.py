"""
Configuration for the OpenAI Compatible API Server
"""
import os
from typing import Dict, Any

# Server configuration
SERVER_HOST = os.getenv("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.getenv("SERVER_PORT", "8000"))

# Model mapping: OpenAI model name -> Perplexity configuration
MODEL_MAPPING = {
    "perplexity-auto": {
        "mode": "reasoning",
        "model": "claude 3.7 sonnet",
        "description": "Perplexity Auto mode - fastest responses (using reasoning + claude)"
    },
    "perplexity-pro": {
        "mode": "pro", 
        "model": None,
        "description": "Perplexity Pro mode - enhanced capabilities"
    },
    "perplexity-reasoning": {
        "mode": "reasoning",
        "model": None,
        "description": "Perplexity Reasoning mode - step-by-step thinking"
    },
    "perplexity-research": {
        "mode": "deep research",
        "model": None,
        "description": "Perplexity Deep Research mode - comprehensive analysis"
    },
    # Pro models with specific model selection
    "perplexity-pro-gpt4o": {
        "mode": "pro",
        "model": "gpt-4o",
        "description": "Perplexity Pro with GPT-4o"
    },
    "perplexity-pro-claude": {
        "mode": "pro", 
        "model": "claude 3.7 sonnet",
        "description": "Perplexity Pro with Claude 3.7 Sonnet"
    },
    "perplexity-reasoning-r1": {
        "mode": "reasoning",
        "model": "r1", 
        "description": "Perplexity Reasoning with R1"
    },
    "perplexity-reasoning-o3": {
        "mode": "reasoning",
        "model": "o3-mini",
        "description": "Perplexity Reasoning with O3-mini"
    }
}

# Default sources for different modes
DEFAULT_SOURCES = {
    "auto": ["web"],
    "pro": ["web"],
    "reasoning": ["web"],
    "deep research": ["web", "scholar"]
}

# API configuration
API_VERSION = "v1"
DEFAULT_MODEL = "perplexity-auto"
MAX_TOKENS_DEFAULT = 4096
TEMPERATURE_DEFAULT = 0.7

# Supported parameters
SUPPORTED_PARAMETERS = {
    "model",
    "messages", 
    "max_tokens",
    "temperature",
    "stream",
    "stop",
    "presence_penalty",
    "frequency_penalty",
    "top_p",
    "n"
}
