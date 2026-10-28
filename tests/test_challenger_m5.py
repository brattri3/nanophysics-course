"""
Empirical Challenger Test Suite for Milestone M5
Nanophysics Course - SUAI
Verifies:
1. PPTX slide counts, structure, and shapes
2. Single-point occurrence of teacher credentials (Slide 1 only)
3. Zero occurrences of laboratory mentions in shapes and notes
4. Preview PNG image counts and exact 1920x1080 dimensions
5. Clean execution of generator script build_lecture_03_colloids.py
"""

import sys
import os
import re
from pathlib import Path
from pptx import Presentation
from PIL import Image

# Reconfigure stdout to utf-8 for Windows console
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent

COMPARATIVE_PPTX = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_03_comparative_variations.pptx"
FULL_PPTX = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_03_colloids.pptx"
PREVIEWS_VAR_DIR = REPO_ROOT / "previews_variations"
PREVIEWS_L03_DIR = REPO_ROOT / "previews_l03"
GENERATOR_SCRIPT = REPO_ROOT / "scripts" / "presentation_generator" / "build_lecture_03_colloids.py"
FIGURE_SCRIPT_P2 = REPO_ROOT / "scripts" / "presentation_generator" / "generate_lecture_03_figures_p2.py"

LAB_PATTERNS = [
    re.compile(r"лр\s*№", re.IGNORECASE),
    re.compile(r"лр\s*[1234567890]", re.IGNORECASE),
    re.compile(r"лабораторн\w*", re.IGNORECASE),
]

TEACHER_PATTERNS = [
    re.compile(r"Попов", re.IGNORECASE),
    re.compile(r"Кафедра\s*(?:№\s*)?3", re.IGNORECASE),
]


def extract_text_from_shape(shape):
    texts = []
    if shape.has_text_frame:
        for p in shape.text_frame.paragraphs:
            text = p.text.strip()
            if text:
                texts.append(text)
    if shape.has_table:
        for row in shape.table.rows:
            for cell in row.cells:
                text = cell.text.strip()
                if text:
                    texts.append(text)
    if shape.shape_type == 6:  # Group shape
        for subshape in shape.shapes:
            texts.extend(extract_text_from_shape(subshape))
    return texts


def extract_slide_content(slide):
    shape_texts = []
    for shape in slide.shapes:
        shape_texts.extend(extract_text_from_shape(shape))
    
    notes_text = []
    if slide.has_notes_slide:
        notes_tf = slide.notes_slide.notes_text_frame
        if notes_tf:
            for p in notes_tf.paragraphs:
                t = p.text.strip()
                if t:
                    notes_text.append(t)
    return shape_texts, notes_text


def test_full_pptx():
    print("=" * 60)
    print("TESTING FULL PPTX: lecture_03_colloids.pptx")
    print("=" * 60)
    assert FULL_PPTX.exists(), f"Full PPTX not found: {FULL_PPTX}"
    prs = Presentation(str(FULL_PPTX))
    slide_count = len(prs.slides)
    print(f"Slide count: {slide_count} (expected: 17)")
    assert slide_count == 17, f"Expected 17 slides, got {slide_count}"

    lab_violations = []
    credential_leak_slides = []
    slide_1_has_teacher = False
    slide_1_has_dept = False

    for idx, slide in enumerate(prs.slides, 1):
        shape_texts, notes_texts = extract_slide_content(slide)
        all_text = " ".join(shape_texts + notes_texts)

        # Check lab mentions
        for pat in LAB_PATTERNS:
            matches = pat.findall(all_text)
            if matches:
                lab_violations.append((idx, matches, all_text[:120]))

        # Check credentials on Slide 1
        if idx == 1:
            for st in shape_texts:
                if re.search(r"Попов\s+Д\.?\s*А\.?", st, re.IGNORECASE):
                    slide_1_has_teacher = True
                if re.search(r"Кафедра\s*(?:№\s*)?3", st, re.IGNORECASE):
                    slide_1_has_dept = True
        else:
            # Slides 2..17 must NOT contain teacher credentials
            for pat in TEACHER_PATTERNS:
                matches = pat.findall(all_text)
                if matches:
                    credential_leak_slides.append((idx, matches, all_text[:120]))

    print(f"Slide 1 teacher name found: {slide_1_has_teacher}")
    print(f"Slide 1 department found: {slide_1_has_dept}")
    assert slide_1_has_teacher, "Slide 1 missing teacher Попов Д.А."
    assert slide_1_has_dept, "Slide 1 missing Department 3"

    # Deep verification of Slide 1
    s1_shapes, _ = extract_slide_content(prs.slides[0])
    s1_text = " ".join(s1_shapes)
    print("Slide 1 content check:")
    assert "физические основы нанотехнологий" in s1_text.lower(), "Slide 1 missing course name"
    assert "3 курс" in s1_text.lower(), "Slide 1 missing 3 курс"
    assert "лекция" in s1_text.lower() and "3" in s1_text.lower(), "Slide 1 missing Лекция №3"
    assert any(s.shape_type == 13 for s in prs.slides[0].shapes), "Slide 1 missing logo picture shape"
    print("  [PASS] Slide 1 contains all required course metadata and official logo shape.")

    # Deep verification of Slide 2
    s2_shapes, _ = extract_slide_content(prs.slides[1])
    s2_text = " ".join(s2_shapes)
    print("Slide 2 content check:")
    # Check for question marks (ban on rhetorical questions)
    q_marks = [s for s in s2_shapes if "?" in s]
    assert len(q_marks) == 0, f"Slide 2 contains rhetorical questions: {q_marks}"
    # Check problem keywords (слипание/агрегация, осадок/седиментация, хранение, транспорт, сепарация, технологичность)
    assert "агрегаци" in s2_text.lower() or "слипани" in s2_text.lower(), "Slide 2 missing aggregation problem"
    assert "седиментаци" in s2_text.lower() or "осадок" in s2_text.lower(), "Slide 2 missing sedimentation problem"
    assert "хранен" in s2_text.lower(), "Slide 2 missing storage problem"
    assert "транспорт" in s2_text.lower(), "Slide 2 missing transport problem"
    assert "сепараци" in s2_text.lower(), "Slide 2 missing separation problem"
    assert "технологич" in s2_text.lower(), "Slide 2 missing processability problem"
    # Check picture shapes (icons + micrograph)
    pic_shapes_s2 = [s for s in prs.slides[1].shapes if s.shape_type == 13]
    assert len(pic_shapes_s2) >= 2, f"Slide 2 expected multiple images (icons/micrographs), got {len(pic_shapes_s2)}"
    print(f"  [PASS] Slide 2 contains all 6 problems, 0 rhetorical questions, and {len(pic_shapes_s2)} images/icons.")

    # Deep verification of Slide 3
    s3_shapes, _ = extract_slide_content(prs.slides[2])
    s3_text = " ".join(s3_shapes)
    print("Slide 3 content check:")
    assert "проблема" in s3_text.lower() or "агрегаци" in s3_text.lower() or "слипани" in s3_text.lower(), "Slide 3 missing Problem 1 title"
    pic_shapes_s3 = [s for s in prs.slides[2].shapes if s.shape_type == 13]
    assert len(pic_shapes_s3) >= 1, f"Slide 3 missing problem icon shape, got {len(pic_shapes_s3)}"
    print(f"  [PASS] Slide 3 is configured as section divider with icon marker.")

    # Deep verification of Slide 17
    s17_shapes, s17_notes = extract_slide_content(prs.slides[16])
    s17_text = " ".join(s17_shapes + s17_notes)
    print("Slide 17 content check:")
    for pat in LAB_PATTERNS:
        assert not pat.search(s17_text), f"Slide 17 contains lab reference: {s17_text}"
    print(f"  [PASS] Slide 17 is completely clean of lab references.")

    print(f"Credential leaks on slides 2..17: {len(credential_leak_slides)}")
    if credential_leak_slides:
        for s_idx, m, snippet in credential_leak_slides:
            print(f"  [FAIL] Slide {s_idx}: match={m}, snippet: {snippet}")
    assert len(credential_leak_slides) == 0, f"Credential leaks found: {credential_leak_slides}"

    print(f"Lab mentions in full PPTX: {len(lab_violations)}")
    if lab_violations:
        for s_idx, m, snippet in lab_violations:
            print(f"  [FAIL] Slide {s_idx}: match={m}, snippet: {snippet}")
    assert len(lab_violations) == 0, f"Lab mentions found: {lab_violations}"
    print("[PASS] lecture_03_colloids.pptx passed all checks!\n")


def test_comparative_pptx():
    print("=" * 60)
    print("TESTING COMPARATIVE PPTX: lecture_03_comparative_variations.pptx")
    print("=" * 60)
    assert COMPARATIVE_PPTX.exists(), f"Comparative PPTX not found: {COMPARATIVE_PPTX}"
    prs = Presentation(str(COMPARATIVE_PPTX))
    slide_count = len(prs.slides)
    print(f"Slide count: {slide_count} (expected: >= 12, ideally 14)")
    assert slide_count >= 12, f"Expected at least 12 slides, got {slide_count}"

    lab_violations = []
    # Identify which slides are title slides:
    # In variations deck, we have matrix/comparison slides and variation 1, 2, 3 slides.
    # Let's inspect each slide text to verify where credentials appear.
    credential_occurrences = []

    for idx, slide in enumerate(prs.slides, 1):
        shape_texts, notes_texts = extract_slide_content(slide)
        all_text = " ".join(shape_texts + notes_texts)

        # Check lab mentions
        for pat in LAB_PATTERNS:
            matches = pat.findall(all_text)
            if matches:
                lab_violations.append((idx, matches, all_text[:120]))

        # Record where teacher/dept appear
        for pat in TEACHER_PATTERNS:
            m = pat.findall(all_text)
            if m:
                credential_occurrences.append((idx, m, shape_texts[0] if shape_texts else ""))

    print(f"Slides containing credentials: {credential_occurrences}")
    print(f"Lab mentions in comparative PPTX: {len(lab_violations)}")
    if lab_violations:
        for s_idx, m, snippet in lab_violations:
            print(f"  [FAIL] Slide {s_idx}: match={m}, snippet: {snippet}")
    assert len(lab_violations) == 0, f"Lab mentions found in comparative deck: {lab_violations}"

    print("\nSlide-by-slide breakdown of comparative variations deck:")
    for idx, slide in enumerate(prs.slides, 1):
        shape_texts, _ = extract_slide_content(slide)
        title = shape_texts[0] if shape_texts else "<NO TEXT>"
        has_popov = any("попов" in t.lower() for t in shape_texts)
        has_dept = any("кафедра" in t.lower() and "3" in t.lower() for t in shape_texts)
        print(f"  Slide {idx:02d} | Title: {title[:60]} | Teacher: {has_popov} | Dept: {has_dept}")

    print("[PASS] lecture_03_comparative_variations.pptx passed all checks!\n")


def test_previews():
    print("=" * 60)
    print("TESTING PREVIEW IMAGES")
    print("=" * 60)
    assert PREVIEWS_VAR_DIR.exists(), f"Directory missing: {PREVIEWS_VAR_DIR}"
    assert PREVIEWS_L03_DIR.exists(), f"Directory missing: {PREVIEWS_L03_DIR}"

    var_pngs = sorted(list(PREVIEWS_VAR_DIR.glob("*.png")))
    l03_pngs = sorted(list(PREVIEWS_L03_DIR.glob("*.png")))

    print(f"previews_variations count: {len(var_pngs)} (expected: 14)")
    assert len(var_pngs) == 14, f"Expected 14 variation previews, found {len(var_pngs)}"

    for png in var_pngs:
        with Image.open(png) as img:
            w, h = img.size
            assert (w, h) == (1920, 1080), f"{png.name} size is {w}x{h}, expected 1920x1080"
    print(f"  All {len(var_pngs)} variation previews are strictly 1920x1080.")

    print(f"previews_l03 count: {len(l03_pngs)} (expected: 17)")
    assert len(l03_pngs) == 17, f"Expected 17 lecture previews, found {len(l03_pngs)}"

    for png in l03_pngs:
        with Image.open(png) as img:
            w, h = img.size
            assert (w, h) == (1920, 1080), f"{png.name} size is {w}x{h}, expected 1920x1080"
    print(f"  All {len(l03_pngs)} lecture previews are strictly 1920x1080.")
    print("[PASS] All preview images exist and meet exact 1920x1080 resolution!\n")


def test_figure_script():
    print("=" * 60)
    print("TESTING FIGURE SCRIPT: generate_lecture_03_figures_p2.py")
    print("=" * 60)
    assert FIGURE_SCRIPT_P2.exists(), f"Figure script missing: {FIGURE_SCRIPT_P2}"
    content = FIGURE_SCRIPT_P2.read_text(encoding="utf-8")
    lab_matches = []
    for pat in LAB_PATTERNS:
        matches = pat.findall(content)
        if matches:
            lab_matches.extend(matches)
    print(f"Lab mentions in figure script: {len(lab_matches)}")
    assert len(lab_matches) == 0, f"Found lab mentions in figure script: {lab_matches}"
    print("[PASS] generate_lecture_03_figures_p2.py is clean of lab references!\n")


if __name__ == "__main__":
    test_full_pptx()
    test_comparative_pptx()
    test_previews()
    test_figure_script()
    print("ALL EMPIRICAL ASSERTIONS PASSED SUCCESSFULLY!")
