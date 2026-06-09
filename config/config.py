"""
Central configuration for Research Paper Generator Agent.
Edit this file to set your API key and preferences.

FREE option -> use Groq (fast, generous free tier)
  Sign up at: https://console.groq.com  (no credit card needed)
"""

import os

# LLM Provider
# Options: "groq" (FREE)  |  "anthropic" (paid)  |  "openai" (paid)
LLM_PROVIDER = "groq"

# Groq (FREE)
# Get your free key at https://console.groq.com -> API Keys
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")

# Best FREE Groq models for academic writing (pick one):
#   "llama-3.3-70b-versatile"  <- best quality, recommended
#   "llama3-70b-8192"          <- good quality, 8k context
#   "llama3-8b-8192"           <- fast & light, 8k context
#   "mixtral-8x7b-32768"       <- long context, 32k window
GROQ_MODEL = "llama-3.3-70b-versatile"

# Anthropic (paid - optional fallback)
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "your_anthropic_api_key_here")
ANTHROPIC_MODEL   = "claude-opus-4-5"

# OpenAI (paid - optional fallback)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key_here")
OPENAI_MODEL   = "gpt-4o"

# Output
OUTPUT_DIR      = "outputs"
OUTPUT_FILENAME = "generated_paper.docx"

# Literature Review
NUM_REFERENCES = 15

# Token limits
# Groq free tier: 6000 tokens/min on llama-3.3-70b
# Keep at 1500 to stay safely within rate limits
MAX_TOKENS_PER_SECTION = 1500