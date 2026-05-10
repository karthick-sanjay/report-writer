"""
agents/literature_review_generator.py
──────────────────────────────────────
Agent 3 – Literature Review Generator

Uses the LLM to:
  1. Generate a thematic literature review paragraph
  2. Produce a structured list of plausible academic references
     (year 2018-2024, DOIs are placeholders but formatted correctly)

NOTE: This agent generates *plausible* academic citations using the LLM.
For a production system you would replace or augment this with a real
academic search API (Semantic Scholar, CrossRef, OpenAlex – all free).
"""

import json
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.llm_client import ask
from config.config    import NUM_REFERENCES


def generate_literature_review(inputs: dict, template: dict) -> dict:
    """
    Returns
    -------
    dict {
        "review_text": str,      # full literature review prose with [N] citations
        "references":  list[dict] # [{id, authors, title, journal, year, doi}, …]
    }
    """
    title    = inputs["title"]
    workflow = inputs["workflow_text"][:1500]
    style    = template.get("style", "IEEE")
    n        = NUM_REFERENCES

    print(f"[LitReviewGenerator] Generating {n} references for: {title!r} …")

    # ── Step 1: generate references ──────────────────────────────────────────
    ref_prompt = f"""
You are an academic researcher. Generate {n} realistic research paper references
related to the topic: "{title}".
The methodology involves: {workflow}

Return ONLY a JSON array (no markdown fences) where each element is:
{{
  "id": <int starting at 1>,
  "authors": "<Last, F., Last2, F2>",
  "title": "<paper title>",
  "journal": "<venue name>",
  "year": <int 2018-2024>,
  "volume": "<vol>",
  "pages": "<pp–pp>",
  "doi": "10.xxxx/xxxxxxxx"
}}

Make the titles and journals realistic and directly relevant to the topic.
Return exactly {n} entries.
"""
    raw_refs = ask(ref_prompt, max_tokens=2000)

    # Strip any accidental markdown fences
    raw_refs = raw_refs.strip().lstrip("```json").lstrip("```").rstrip("```").strip()

    try:
        references = json.loads(raw_refs)
    except json.JSONDecodeError:
        # Fallback: create placeholder refs
        references = [
            {
                "id": i,
                "authors": f"Author{i}, A.",
                "title": f"Related work on {title} – study {i}",
                "journal": "Journal of Advanced Research",
                "year": 2020 + (i % 4),
                "volume": str(i),
                "pages": f"{i*10}–{i*10+8}",
                "doi": f"10.1000/placeholder{i:03d}",
            }
            for i in range(1, n + 1)
        ]

    # ── Step 2: generate literature review prose ──────────────────────────────
    ref_list_str = "\n".join(
        f"[{r['id']}] {r['authors']} ({r['year']}), {r['title']!r}, {r['journal']}"
        for r in references
    )

    review_prompt = f"""
Write a detailed academic Literature Review section (~700 words) for a paper titled:
"{title}"

Use ALL of these references by their [N] number inline (e.g. [3], [7,8]):
{ref_list_str}

The literature review must:
- Group related works thematically (not just list them one by one)
- Identify gaps that the proposed work addresses
- Use academic, formal language ({style} style)
- Ensure every reference number [N] appears at least once

Write only the body text of the Literature Review – no heading.
"""
    review_text = ask(review_prompt, max_tokens=1200)

    print(f"[LitReviewGenerator] Done – {len(references)} references generated.")
    return {
        "review_text": review_text,
        "references":  references,
    }
