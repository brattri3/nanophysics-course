# Project: Full Rebuild of Lecture 03 (26 Slides, 4 Sections)

## Architecture
- **Target Presentation**: `course_materials/semester_4/lectures/lecture_03_colloids.pptx` (16:9 widescreen, strictly 26 slides).
- **Target Lecturer Speech**: `course_materials/semester_4/lectures/lecture_03_speech.md` (fully synchronized with 26 slides and speaker notes, 0 questions, 0 lab mentions).
- **Generator Scripts**:
  - Main builder: `scripts/presentation_generator/build_lecture_03_colloids.py`
  - Figure generator P1: `scripts/presentation_generator/generate_lecture_03_figures_p1.py`
  - Figure generator P2: `scripts/presentation_generator/generate_lecture_03_figures_p2.py`
  - Problem icons: `scripts/presentation_generator/generate_problem_icons.py`
  - Visual downloader / authenticator: `scripts/presentation_generator/download_authentic_visuals.py`
- **Visual Assets**:
  - `course_materials/semester_4/lectures/figures_l03/`
  - `course_materials/semester_4/lectures/figures_l03/icons/` (6 problem icons)
  - Corporate Template: `course_materials/templates/guap_16-9_2023.pptx`
- **Verification Tooling**:
  - PPTX Compiler: `uv run --no-project --with python-pptx --with pillow --with matplotlib --with pywin32 python scripts/presentation_generator/build_lecture_03_colloids.py`
  - Slide Preview Exporter: `uv run --no-project --with python-pptx --with pillow --with pywin32 python .agents/skills/scientific-presentation-creator/scripts/export_slide_previews.py --pptx course_materials/semester_4/lectures/lecture_03_colloids.pptx --out previews_l03`

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Introductory Visual Contrast Hook (R1) | Split-screen slide 2 comparing Faraday's 1857 ruby gold colloid vs clumping Fe3O4 + 6 problem icons | M1 | ORIGINAL_REQUEST §R1 |
| 2 | Assertive Academic Style (R2) | 0 rhetorical questions, 0 audience questions, 0 exam/lab jargon throughout all 26 slides & speech | M1, M2, M3, M4 | ORIGINAL_REQUEST §R2 |
| 3 | Single-Point Occurrence (R1, R2) | Lecturer name (Popov D.A.), Department 3, and course title strictly on Slide 1 only | M1 | ORIGINAL_REQUEST §R1 |
| 4 | Dark Blue Section Dividers Layout S (R1, R2) | Fullscreen #002C5F dividers on Slides 4, 10, 16, 21 with dual problem icons and 2-3 assertive sentences | M1, M2, M3, M4 | ORIGINAL_REQUEST §R1 |
| 5 | Full-Width Modular Slides without Pictures (R1, R2) | 12.133" modular layouts on Slides 6, 12, 24 eliminating empty space via structured cards & chains | M1, M2, M4 | ORIGINAL_REQUEST §R1 |
| 6 | R3 Terminology & Abbreviations Standard (R2) | Full term definition on first occurrence with abbreviation in parentheses, bold + #005AAA highlight | M1, M2, M3, M4 | ORIGINAL_REQUEST §R2 |
| 7 | Full Speech & Speaker Notes Synchronization (R3) | Complete 26-slide rewrite of lecture_03_speech.md and non-empty matching notes embedded in PPTX | M1, M2, M3, M4 | ORIGINAL_REQUEST §R3 |
| 8 | Section-by-Section Triple Review Loop (R4) | Independent review by lecture-pedagogue, guap-student-reviewer, and auditor after each section | M1, M2, M3, M4 | ORIGINAL_REQUEST §R4 |
| 9 | End-to-End Compilation & 1920x1080 Previews (R1, R5) | Clean generation of 26 slides, 26 1920x1080 previews, git commit and push to origin main | M5 | ORIGINAL_REQUEST §R5 |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M0 | Phase 0 Survey & Scope Synthesis | Map codebase, 26-slide inventory, and speech sync strategy | none | DONE |
| M1 | Intro Block & Section 1: Self-aggregation & Capillary Collapse | Slides 1–3 (Title, Hook, Roadmap) + Slides 4–9 (Divider S, Specific Surface, Modular Defs, Sol-Gel/Aerogel, Zeolites, Summary Table). Notes & Speech sync. Triple review passed CLEAN. | M0 | DONE |
| M2 | Section 2: Charge Loss & Protection | Slides 10–15 (Divider S, Micelle Anatomy, 4-step Builder, Helmholtz/Gouy-Chapman, Stern & Debye screening, Technical Regulation). Notes & Speech sync. Triple review passed CLEAN. | M1 | DONE |
| M3 | Section 3: Stability Diagnostics & Microfluidics | Slides 16–20 (Divider S, Zeta potential & 30 mV, 2x2 Reuss phenomena, Henry equation, Lab-on-a-chip & EPD). Notes & Speech sync. Triple review passed CLEAN. | M2 | DONE |
| M4 | Section 4: Sedimentation, DLVO Barrier & Surfactants | Slides 21–26 (Divider S, Stokes-Perrin sedimentation, DLVO theory, Schulze-Hardy 1/z^6 & Smoluchowski, Surfactant steric stabilization, Master 6-challenge matrix). Notes & Speech sync. Triple review passed CLEAN. | M3 | DONE |
| M5 | Final Assembly, E2E Compilation & Multi-Role Acceptance | Full run of `build_lecture_03_colloids.py`, export of Full HD slide previews (all 26 slides), visual audit, multi-role review (`guap-student-reviewer`, `lecture-pedagogue`, auditor), git commit and push to origin main. | M1, M2, M3, M4 | DONE |

## Interface Contracts
### Slide Structure Contract (Layout A)
- Left Text Card: `left = Inches(0.60)`, `top = Inches(1.25)`, `width = Inches(5.35)`, `height = Inches(5.15)`.
  - Max 2–3 cards or 1 unified card with 2–3 concise declarative bullet points.
  - Heading: 13.2 pt bold `#003366`. Body: 11.4 pt regular `#1F2937`.
- Right Figure: `left = Inches(6.15)`, `top = Inches(1.25)`, `width = Inches(6.58)`, `height = Inches(5.15)`.
- Bottom Takeaway Banner: `left = Inches(0.60)`, `top = Inches(6.65)`, `width = Inches(12.133)`, `height = Inches(0.55)`.

### Slide Structure Contract (Layout B: Modular Full-Width)
- Width: `Inches(12.133)`, Left: `Inches(0.60)`.
- Cards: structured horizontally or in grid. No empty right-hand margins.

### Slide Structure Contract (Layout S: Dark Blue Divider)
- Background: Fullscreen `#002C5F`.
- Center problem icons: dual 1.40" icons. Title 26 pt bold white.
- Explanatory thesis: strictly 2–3 assertive sentences. Navigation pills.

### Generator CLI Contract
- Must support standalone compilation:
  `uv run --no-project --with python-pptx --with pillow --with matplotlib --with pywin32 python scripts/presentation_generator/build_lecture_03_colloids.py`
- Must produce valid `course_materials/semester_4/lectures/lecture_03_colloids.pptx`.

## Code Layout
- `scripts/presentation_generator/build_lecture_03_colloids.py` — Primary presentation generator script
- `scripts/presentation_generator/generate_lecture_03_figures_p1.py` — Figures 1–9
- `scripts/presentation_generator/generate_lecture_03_figures_p2.py` — Figures 10–17+
- `course_materials/semester_4/lectures/figures_l03/` — Destination directory for rendered PNG/JPG figures
- `course_materials/semester_4/lectures/lecture_03_colloids.pptx` — Generated PPTX slide deck
- `course_materials/semester_4/lectures/lecture_03_speech.md` — Synchronized lecturer speech and speaker notes reference
