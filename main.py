"""
main.py  –  Research Paper Generator Agent  (Orchestrator)
────────────────────────────────────────────────────────────
Run this file to generate a complete research paper.

Usage
-----
  python main.py

Edit the INPUT SECTION below to supply your paper details,
OR call run_pipeline() programmatically from another script.
"""

import sys
import os
import time

# ── Make sub-packages importable ─────────────────────────────────────────────
sys.path.insert(0, os.path.dirname(__file__))

from agents.input_processor            import process_inputs
from agents.template_analyzer          import analyze_template
from agents.literature_review_generator import generate_literature_review
from agents.citation_manager           import build_references_section, format_references
from agents.section_writer             import write_all_sections
from agents.word_document_generator    import generate_word_document


# ══════════════════════════════════════════════════════════════════════════════
#  INPUT SECTION – Edit everything below this line
# ══════════════════════════════════════════════════════════════════════════════

TITLE = "Real-Time Smart Waste Management System Using GSM and WEB Technologies"

# Paths to your uploaded files (leave "" if not available)
SAMPLE_PAPER_PATH = "inputs/REMOTE_PHYSIOTHERAPY123.pdf"   # .pdf or .docx
WORKFLOW_PATH     = "inputs/review_paper.pdf"        # .txt, .docx, or .pdf
PPT_PATH          = "inputs/review.pptx"  # .pptx or ""

# Plain-text descriptions (edit directly here OR load from a file)
HARDWARE = """
- Arduino UNO microcontroller
- ultrasonic distance sensor (HC-SR04) X 2
- Servo mortor
- GSM module (SIM800L)
- 3.7V Li-ion battery pack
"""

SOFTWARE = """
 -HTML 
 -CSS 
-JavaScript 
 -Database 
"""

RESULTS = """
-Real-time monitoring of multiple units
-Reduced overflow problems
-Improved management
-Quick detection of device failure
-Better efficiency and planning

"""

DIAGRAMS_DESCRIPTION = """

"""

# Paths to diagram images (optional, will be embedded in the document)
DIAGRAM_IMAGE_PATHS = [
    
]

AUTHORS = "Dr. V. Govindharaj ASP/ECE, Karthick Sanjay M S, Mohammed Athipkhan M, Mohammad Musthafa Mishal M"

# ══════════════════════════════════════════════════════════════════════════════


def run_pipeline(
    title: str               = TITLE,
    sample_paper_path: str   = SAMPLE_PAPER_PATH,
    workflow_path: str       = WORKFLOW_PATH,
    ppt_path: str            = PPT_PATH,
    hardware: str            = HARDWARE,
    software: str            = SOFTWARE,
    results: str             = RESULTS,
    diagrams_description: str = DIAGRAMS_DESCRIPTION,
    diagram_image_paths: list = DIAGRAM_IMAGE_PATHS,
    authors: str             = AUTHORS,
) -> str:
    """
    Full pipeline: Input → Template → LitReview → Sections → .docx

    Returns the absolute path to the generated Word document.
    """
    t0 = time.time()
    print("=" * 60)
    print("  Research Paper Generator Agent")
    print("=" * 60)

    # ── Agent 1: Process inputs ───────────────────────────────────────────
    inputs = process_inputs(
        title               = title,
        sample_paper_path   = sample_paper_path,
        workflow_path       = workflow_path,
        ppt_path            = ppt_path,
        hardware            = hardware,
        software            = software,
        results             = results,
        diagrams_description = diagrams_description,
        diagram_image_paths = diagram_image_paths,
    )

    # ── Agent 2: Analyze template ─────────────────────────────────────────
    template = analyze_template(inputs)

    # ── Agent 3: Generate literature review + references ──────────────────
    lit_review_data = generate_literature_review(inputs, template)

    # ── Agent 4: Format references ────────────────────────────────────────
    formatted_refs = format_references(
        lit_review_data["references"],
        style=template.get("style", "IEEE"),
    )

    # ── Agent 5: Write all sections ───────────────────────────────────────
    # Inject pre-generated lit review so SectionWriter can refine it
    section_texts = write_all_sections(inputs, template, lit_review_data)
    section_texts["References"] = build_references_section(
        lit_review_data["references"], style=template.get("style", "IEEE")
    )

    # ── Agent 6: Generate Word document ──────────────────────────────────
    output_path = generate_word_document(
        inputs         = inputs,
        template       = template,
        section_texts  = section_texts,
        references     = lit_review_data["references"],
        formatted_refs = formatted_refs,
        authors        = authors,
    )

    elapsed = time.time() - t0
    print("=" * 60)
    print(f"  Done in {elapsed:.1f}s")
    print(f"  Output: {output_path}")
    print("=" * 60)
    return output_path


if __name__ == "__main__":
    run_pipeline()
