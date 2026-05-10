"""
agents/section_writer.py
─────────────────────────
Agent 5 – Section Writer

Generates original academic prose for every section detected by the
Template Analyzer.  Each section is written in one LLM call so that
the context stays focused and quality stays high.
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.llm_client import ask
from config.config    import MAX_TOKENS_PER_SECTION


# ── Per-section prompt templates ──────────────────────────────────────────────

def _system_prompt() -> str:
    return (
        "You are an expert academic writer. Write formal, precise, and original "
        "research paper content. Do NOT use bullet points in prose sections. "
        "Do NOT include a section heading in your output – only the body text."
    )


def _build_prompt(section: str, inputs: dict, template: dict,
                  lit_review_data: dict) -> str:
    title    = inputs["title"]
    workflow = inputs["workflow_text"]
    hardware = inputs["hardware"]
    software = inputs["software"]
    results  = inputs["results"]
    diagrams = inputs["diagrams_description"]
    ppt      = inputs["ppt_text"]
    style    = template.get("style", "IEEE")
    guidance = template.get("section_styles", {}).get(section, "")
    review   = lit_review_data.get("review_text", "")
    refs     = lit_review_data.get("references", [])

    ref_summary = "\n".join(
        f"[{r['id']}] {r['authors']} ({r['year']}), {r['title']!r}"
        for r in refs[:8]
    )

    context = f"""
Paper title: {title}
Formatting style: {style}
Writing guidance for this section: {guidance}

Project workflow / methodology:
{workflow[:1200]}

Hardware used: {hardware}
Software used: {software}

Experimental results summary:
{results[:800]}

Diagrams / architecture description:
{diagrams[:600]}

Presentation highlights:
{ppt[:800]}

Available references (use [N] inline where appropriate):
{ref_summary}
"""

    prompts = {
        "Abstract": (
            f"Write a concise Abstract (~200-250 words) for a research paper titled:\n"
            f"\"{title}\"\n\n{context}\n\n"
            "Cover: motivation, approach, key results, and significance. No citations."
        ),
        "Keywords": (
            f"Generate 6-8 relevant academic Keywords (comma-separated) for:\n\"{title}\"\n\n{context}"
        ),
        "Introduction": (
            f"Write the Introduction section (~450 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Cover: problem statement, motivation, research objectives, contributions, and paper organisation."
        ),
        "Literature Review": (
            f"Expand and polish this Literature Review for:\n\"{title}\"\n\n"
            f"Existing draft:\n{review}\n\n"
            "Ensure every sentence that makes a claim has an inline [N] citation. "
            "Group works thematically. Identify the research gap clearly."
        ),
        "Methodology": (
            f"Write the Methodology section (~600 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Describe the step-by-step approach, tools, algorithms, and design decisions. "
            "Use subsections if needed (e.g., 3.1 Data Collection, 3.2 Model Design)."
        ),
        "System Architecture": (
            f"Write the System Architecture section (~400 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Describe each component, data flow, and integration. "
            "Refer to 'Figure 1' for the architecture diagram."
        ),
        "Implementation": (
            f"Write the Implementation section (~500 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Cover programming environment setup, key code modules, integration steps, "
            "and any challenges encountered."
        ),
        "Results and Discussion": (
            f"Write the Results and Discussion section (~600 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Present quantitative results, compare with baselines or related work, "
            "and discuss implications. Refer to Table 1 or Figure 2 where appropriate."
        ),
        "Conclusion": (
            f"Write the Conclusion section (~250 words) for:\n\"{title}\"\n\n{context}\n\n"
            "Summarise key contributions, limitations, and future work directions."
        ),
    }

    return prompts.get(
        section,
        f"Write the '{section}' section (~400 words) for the paper titled:\n\"{title}\"\n\n{context}"
    )


# ── public API ────────────────────────────────────────────────────────────────

def write_all_sections(inputs: dict, template: dict, lit_review_data: dict) -> dict[str, str]:
    """
    Returns
    -------
    dict  { section_name: generated_text }
    """
    sections = template["sections"]
    output: dict[str, str] = {}

    for section in sections:
        if section.lower() == "references":
            continue  # handled separately by CitationManager

        print(f"[SectionWriter] Writing: {section} …")
        prompt = _build_prompt(section, inputs, template, lit_review_data)
        text   = ask(prompt, system=_system_prompt(), max_tokens=MAX_TOKENS_PER_SECTION)
        output[section] = text.strip()

    return output
