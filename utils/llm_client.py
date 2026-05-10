"""
llm_client.py  –  Thin wrapper around Groq / Anthropic / OpenAI so every
agent calls the same interface:  ask(prompt, system="...", max_tokens=1500) → str

DEFAULT provider is Groq (free tier available at https://console.groq.com).
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from config.config import (
    LLM_PROVIDER,
    GROQ_API_KEY,    GROQ_MODEL,
    ANTHROPIC_API_KEY, ANTHROPIC_MODEL,
    OPENAI_API_KEY,    OPENAI_MODEL,
)


def ask(prompt: str,
        system: str = "You are an expert academic research writer.",
        max_tokens: int = 1500) -> str:
    """Send a prompt and return the model's reply as a plain string."""

    if LLM_PROVIDER == "groq":
        return _ask_groq(prompt, system, max_tokens)
    elif LLM_PROVIDER == "anthropic":
        return _ask_anthropic(prompt, system, max_tokens)
    elif LLM_PROVIDER == "openai":
        return _ask_openai(prompt, system, max_tokens)
    else:
        raise ValueError(f"Unknown LLM_PROVIDER: {LLM_PROVIDER!r}. "
                         "Choose 'groq', 'anthropic', or 'openai'.")


# ─── Groq (FREE tier) ─────────────────────────────────────────────────────────
def _ask_groq(prompt: str, system: str, max_tokens: int) -> str:
    from groq import Groq
    client = Groq(api_key=GROQ_API_KEY)
    response = client.chat.completions.create(
        model=GROQ_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()


# ─── Anthropic (paid) ─────────────────────────────────────────────────────────
def _ask_anthropic(prompt: str, system: str, max_tokens: int) -> str:
    import anthropic
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)
    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    return message.content[0].text.strip()


# ─── OpenAI (paid) ────────────────────────────────────────────────────────────
def _ask_openai(prompt: str, system: str, max_tokens: int) -> str:
    from openai import OpenAI
    client = OpenAI(api_key=OPENAI_API_KEY)
    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system},
            {"role": "user",   "content": prompt},
        ],
    )
    return response.choices[0].message.content.strip()
