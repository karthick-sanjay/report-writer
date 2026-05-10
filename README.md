# Research Paper Generator Agent

Automatically generates a complete, formatted academic research paper (.docx)
from your project details using an LLM (Claude or OpenAI).

---

## Folder Structure

```
research_paper_agent/
│
├── main.py                          # ← Run this to generate your paper
├── requirements.txt
├── README.md
│
├── config/
│   └── config.py                    # API keys, model choice, output settings
│
├── agents/
│   ├── input_processor.py           # Agent 1 – reads all your input files
│   ├── template_analyzer.py         # Agent 2 – extracts structure from sample paper
│   ├── literature_review_generator.py # Agent 3 – generates lit review + references
│   ├── citation_manager.py          # Agent 4 – formats reference list
│   ├── section_writer.py            # Agent 5 – writes every paper section
│   └── word_document_generator.py   # Agent 6 – assembles the final .docx
│
├── utils/
│   └── llm_client.py                # Thin wrapper for Anthropic / OpenAI
│
├── inputs/                          # ← Put YOUR files here
│   ├── sample_paper.pdf             # (or .docx) – used as structure template
│   ├── workflow.txt                 # (or .pdf/.docx) – your methodology
│   ├── presentation.pptx            # (optional) – your project PPT
│   └── diagrams/                    # (optional) – architecture images (.png/.jpg)
│
└── outputs/
    └── generated_paper.docx         # ← Generated paper appears here
```

---

## Step 1 – Prerequisites

- **Python 3.10+** (check with `python --version`)
- **pip** (comes with Python)
- An **Anthropic API key** from https://console.anthropic.com  
  OR an **OpenAI API key** from https://platform.openai.com

---

## Step 2 – Installation

Open a terminal in the `research_paper_agent/` folder and run:

```bash
pip install -r requirements.txt
```

---

## Step 3 – Add Your API Key

**Option A – environment variable (recommended):**

```bash
# macOS / Linux
export ANTHROPIC_API_KEY="sk-ant-..."

# Windows CMD
set ANTHROPIC_API_KEY=sk-ant-...

# Windows PowerShell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

**Option B – edit config directly:**

Open `config/config.py` and paste your key:
```python
ANTHROPIC_API_KEY = "sk-ant-your-key-here"
```

---

## Step 4 – Add Your Input Files

Copy your files into the `inputs/` folder:

| File | Purpose | Format |
|------|---------|--------|
| `sample_paper.pdf` | Structural template | PDF or DOCX |
| `workflow.txt` | Your methodology | TXT, DOCX, or PDF |
| `presentation.pptx` | Project PPT | PPTX (optional) |
| `diagrams/*.png` | Architecture diagrams | PNG or JPG (optional) |

---

## Step 5 – Edit main.py

Open `main.py` and fill in the INPUT SECTION at the top:

```python
TITLE   = "Your Paper Title Here"
HARDWARE = "List your hardware components..."
SOFTWARE = "List your software components..."
RESULTS  = "Describe your experimental results..."
DIAGRAMS_DESCRIPTION = "Describe your system architecture..."
AUTHORS  = "Your Name, Co-Author Name"
```

---

## Step 6 – Run

```bash
python main.py
```

Watch the progress in your terminal. The finished paper will be saved to:

```
outputs/generated_paper.docx
```

---

## Example Output Timeline

```
============================================================
  Research Paper Generator Agent
============================================================
[InputProcessor] Reading sample paper …
[InputProcessor] Reading workflow / methodology …
[TemplateAnalyzer] Analysing sample paper structure …
[TemplateAnalyzer] Detected 10 sections | style: IEEE
[LitReviewGenerator] Generating 15 references …
[SectionWriter] Writing: Abstract …
[SectionWriter] Writing: Keywords …
[SectionWriter] Writing: Introduction …
[SectionWriter] Writing: Literature Review …
[SectionWriter] Writing: Methodology …
[SectionWriter] Writing: System Architecture …
[SectionWriter] Writing: Implementation …
[SectionWriter] Writing: Results and Discussion …
[SectionWriter] Writing: Conclusion …
[WordDocGenerator] Saved → /path/to/outputs/generated_paper.docx
============================================================
  Done in 87.3s
  Output: /path/to/outputs/generated_paper.docx
============================================================
```

---

## Switching to OpenAI

Open `config/config.py` and change:
```python
LLM_PROVIDER = "openai"
OPENAI_API_KEY = "sk-..."
```

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| `ModuleNotFoundError: anthropic` | Run `pip install -r requirements.txt` |
| `AuthenticationError` | Check your API key is set correctly |
| `FileNotFoundError` for input files | Make sure files exist in `inputs/` folder |
| PDF won't open | Ensure PyMuPDF installed: `pip install PyMuPDF` |
| PPTX won't open | Ensure python-pptx installed: `pip install python-pptx` |
| Output .docx is empty | Check terminal for errors; try without sample paper first |

---

## Customising the Output

- **Paper authors**: Change `AUTHORS` in `main.py`
- **Number of references**: Change `NUM_REFERENCES` in `config/config.py`
- **Word document styling**: Edit `agents/word_document_generator.py`
- **Section content prompts**: Edit `agents/section_writer.py → _build_prompt()`
- **Output filename**: Change `OUTPUT_FILENAME` in `config/config.py`
