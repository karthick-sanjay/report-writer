"""
agents/citation_manager.py
───────────────────────────
Agent 4 – Citation Manager

Formats the raw reference list (from LitReviewGenerator) into a
properly formatted References section string in the detected style
(IEEE, APA, or Generic).

Also exposes a helper used by Section Writer to add inline citations.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))


def _fmt_ieee(r: dict) -> str:
    """[N] A. Last et al., 'Title,' Journal, vol. V, pp. PP, YYYY."""
    authors = r.get("authors", "Unknown")
    title   = r.get("title",   "Untitled")
    journal = r.get("journal", "Unknown Journal")
    year    = r.get("year",    "n.d.")
    vol     = r.get("volume",  "")
    pages   = r.get("pages",   "")
    doi     = r.get("doi",     "")
    vol_str = f", vol. {vol}" if vol else ""
    pg_str  = f", pp. {pages}" if pages else ""
    doi_str = f", doi: {doi}"  if doi   else ""
    return f"[{r['id']}] {authors}, \"{title},\" {journal}{vol_str}{pg_str}, {year}{doi_str}."


def _fmt_apa(r: dict) -> str:
    """Last, F. (YYYY). Title. Journal, V, PP. https://doi.org/..."""
    authors = r.get("authors", "Unknown")
    title   = r.get("title",   "Untitled")
    journal = r.get("journal", "Unknown Journal")
    year    = r.get("year",    "n.d.")
    vol     = r.get("volume",  "")
    pages   = r.get("pages",   "")
    doi     = r.get("doi",     "")
    vol_str = f", {vol}" if vol else ""
    pg_str  = f", {pages}" if pages else ""
    doi_str = f" https://doi.org/{doi}" if doi else ""
    return f"{authors} ({year}). {title}. *{journal}*{vol_str}{pg_str}.{doi_str}"


def format_references(references: list[dict], style: str = "IEEE") -> list[str]:
    """
    Parameters
    ----------
    references : list of dicts from LitReviewGenerator
    style      : "IEEE", "APA", or anything else → IEEE fallback

    Returns
    -------
    list of formatted reference strings (one per reference)
    """
    formatter = _fmt_apa if style.upper() == "APA" else _fmt_ieee
    return [formatter(r) for r in references]


def build_references_section(references: list[dict], style: str = "IEEE") -> str:
    """Return the full References section as a single string."""
    lines = format_references(references, style)
    return "\n".join(lines)
