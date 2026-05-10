"""
agents/template_analyzer.py
────────────────────────────
Agent 2 – Template Analyzer

Reads the sample paper text and uses the LLM to:
  1. Identify the section headings (Abstract, Introduction, …)
  2. Detect the formatting style (IEEE, ACM, APA, etc.)
  3. Extract per-section tone/length guidelines

Returns a list of section dicts that drive all the writers.
"""

import re
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.llm_client import ask

# Default section order if detection fails
DEFAULT_SECTIONS = [
    "Abstract",
    "Keywords",
    "Introduction",
    "Literature Review",
    "Methodology",
    "System Architecture",
    "Implementation",
    "Results and Discussion",
    "Conclusion",
    "References",
]


def _detect_sections_from_text(text: str) -> list[str]:
    """
    Heuristic scan: look for lines that are ALL-CAPS or Title Case and
    are likely section headings (short, no period at end).
    """
    heading_re = re.compile(
        r"^(?:\d+[\.\)]?\s*)?([A-Z][A-Za-z &/-]{2,50})$"
    )
    found = []
    for line in text.splitlines():
        line = line.strip()
        m = heading_re.match(line)
        if m and line not in found:
            found.append(m.group(1).strip())
    return found if len(found) >= 4 else []


def analyze_template(inputs: dict) -> dict:
    """
    Parameters
    ----------
    inputs : dict  (from InputProcessor)

    Returns
    -------
    dict {
        "sections":       [str, …],          # ordered list of section names
        "style":          str,               # IEEE / ACM / APA / Generic
        "section_styles": {name: guidance},  # tone & length per section
    }
    """
    sample_text = inputs.get("sample_paper_text", "")

    print("[TemplateAnalyzer] Analysing sample paper structure …")

    if sample_text:
        prompt = f"""
You are analysing an academic research paper. 
Given the paper text below, extract:
1. An ordered list of all section headings (e.g. Abstract, Introduction, …)
2. The citation/formatting style (IEEE, ACM, APA, or Generic)
3. A one-line description of the tone and approximate paragraph length for each section.

Respond in this EXACT format (no extra text):
SECTIONS: Abstract | Keywords | Introduction | Literature Review | Methodology | Results and Discussion | Conclusion | References
STYLE: IEEE
GUIDANCE:
Abstract: ~250 words, passive voice, no citations
Keywords: 5-8 comma-separated terms
Introduction: 400-600 words, motivates the problem, ends with paper organisation
Literature Review: 600-900 words, groups related work by theme, uses in-text citations
Methodology: 500-800 words, active voice, numbered steps or subsections
Results and Discussion: 600-900 words, refers to figures/tables, compares with baseline
Conclusion: 200-350 words, summarises contributions and future work
References: IEEE numbered list format

Paper text (first 3000 chars):
{sample_text[:3000]}
"""
        raw = ask(prompt, max_tokens=600)
    else:
        raw = ""

    # ── Parse response ─────────────────────────────────────────────────────
    sections = []
    style    = "Generic"
    guidance: dict[str, str] = {}

    if raw:
        for line in raw.splitlines():
            if line.startswith("SECTIONS:"):
                sections = [s.strip() for s in line[9:].split("|") if s.strip()]
            elif line.startswith("STYLE:"):
                style = line[6:].strip()
            elif ":" in line and not line.startswith("GUIDANCE"):
                parts = line.split(":", 1)
                guidance[parts[0].strip()] = parts[1].strip()

    # Fallback
    if not sections:
        sections = _detect_sections_from_text(sample_text) or DEFAULT_SECTIONS

    # Make sure DEFAULT_SECTIONS items present but not in detected list are added
    for sec in DEFAULT_SECTIONS:
        if sec not in sections:
            sections.append(sec)

    print(f"[TemplateAnalyzer] Detected {len(sections)} sections | style: {style}")

    return {
        "sections":       sections,
        "style":          style,
        "section_styles": guidance,
    }
