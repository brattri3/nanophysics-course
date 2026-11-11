"""
Empirical Challenger Test Suite for Lecture 04: Slide Outlines and Text Constraints
Nanophysics Course - SUAI (Semester 4)
Target files:
- course_materials/semester_4/lectures/lecture_04_speech.md
- course_materials/semester_4/lectures/lecture_04_plan.md
"""

import sys
import os
import re
from pathlib import Path

# UTF-8 stdout configuration for Windows
if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

REPO_ROOT = Path(__file__).resolve().parent.parent
SPEECH_PATH = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_04_speech.md"
PLAN_PATH = REPO_ROOT / "course_materials" / "semester_4" / "lectures" / "lecture_04_plan.md"

def load_files():
    if not SPEECH_PATH.exists():
        raise FileNotFoundError(f"Speech file not found: {SPEECH_PATH}")
    if not PLAN_PATH.exists():
        raise FileNotFoundError(f"Plan file not found: {PLAN_PATH}")
    speech_text = SPEECH_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
    plan_text = PLAN_PATH.read_text(encoding="utf-8").replace("\r\n", "\n")
    return speech_text, plan_text

def split_into_slides(text):
    parts = re.split(r'(?m)^### Слайд\s+(\d+)\.\s*(.*?)$', text)
    preamble = parts[0]
    slides = {}
    i = 1
    while i < len(parts):
        num = int(parts[i])
        title = parts[i+1].strip()
        body = parts[i+2]
        slides[num] = {"title": title, "body": body}
        i += 3
    return preamble, slides

def extract_slide_outline(speech_slide_body):
    m = re.search(r'#### Заготовка содержания слайда\s*\((.*?)\)\n(.*?)(?=\n\*\*Живая речь лектора|\Z)', speech_slide_body, re.DOTALL)
    if not m:
        return None, ""
    layout = m.group(1).strip()
    outline = m.group(2).strip()
    return layout, outline

# =====================================================================
# CHECK 1: Occam's Razor (Word Count & Declarative Phrases)
# =====================================================================
def run_check_1():
    print("=" * 70)
    print("CHECK 1: Occam's Razor Word Count & Phrases (Target: 35-45 words, 2-3 phrases)")
    print("=" * 70)
    speech_text, plan_text = load_files()
    _, speech_slides = split_into_slides(speech_text)
    
    table = []
    flags = []
    
    for num in range(1, 25):
        s = speech_slides.get(num)
        if not s:
            flags.append((num, "MISSING_SLIDE", "Slide missing"))
            continue
            
        layout, outline = extract_slide_outline(s["body"])
        if not outline:
            flags.append((num, "NO_OUTLINE", "No outline block"))
            continue
            
        # 1. Claimed words
        cl = re.findall(r'\((\d+)\s+слов[а-я]*\)', outline)
        claimed_val = int(cl[0]) if cl else None
        
        # 2. Extract content bullets
        # Bullets start with '  - ' under '* **Содержание' or '* **Центрированная проблема' or '* **Содержание дорожной карты'
        bullet_lines = []
        for line in outline.splitlines():
            sline = line.strip()
            if sline.startswith(('-', '1.', '2.', '3.', '4.', '5.', '6.')):
                # exclude top level metadata bullets
                if not sline.startswith(('* **', '#')):
                    bullet_lines.append(sline)
                    
        # Count words in bullets (removing LaTeX math, markdown punctuation)
        raw_bullet_text = " ".join(bullet_lines)
        clean_bullet_text = re.sub(r'\$[^\$]+\$', ' ', raw_bullet_text) # remove inline math
        clean_bullet_text = re.sub(r'[\*_`#\(\)\{\}\[\]\<\>\\\/=\+\:\,\.\;\!\?«»"–—]', ' ', clean_bullet_text)
        b_words = clean_bullet_text.split()
        
        # Also count words WITH math symbols as single tokens
        math_tokens_text = re.sub(r'[\*_`#\(\)\{\}\[\]\<\>\\\/=\+\:\,\.\;\!\?«»"–—]', ' ', raw_bullet_text)
        math_tokens = math_tokens_text.split()
        
        # 3. Visible slide words (Title + Subtitle + Bullets + Takeaway)
        title_m = re.search(r'\* \*\*Заголовок:\*\*\s*(.*?)$', outline, re.MULTILINE)
        sub_m = re.search(r'\* \*\*Подзаголовок:\*\*\s*(.*?)$', outline, re.MULTILINE)
        take_m = re.search(r'\* \*\*Takeaway Баннер:\*\*\s*(.*?)$', outline, re.MULTILINE)
        
        t_text = title_m.group(1) if title_m else ""
        sub_text = sub_m.group(1) if sub_m else ""
        take_text = take_m.group(1) if take_m else ""
        
        full_slide_text = f"{t_text} {sub_text} {raw_bullet_text} {take_text}"
        clean_full = re.sub(r'\$[^\$]+\$', ' ', full_slide_text)
        clean_full = re.sub(r'[\*_`#\(\)\{\}\[\]\<\>\\\/=\+\:\,\.\;\!\?«»"–—]', ' ', clean_full)
        full_words = clean_full.split()
        
        num_phrases = len(bullet_lines)
        
        # Assessment
        status = "OK"
        if num == 1:
            status = "TITLE_SLIDE"
        elif num in [4, 8, 13, 19]:
            # Section divider
            if len(b_words) < 20 or len(b_words) > 45:
                status = f"DIVIDER_COUNT_WARN({len(b_words)})"
        else:
            # Content slide
            # Check target 35-45 words
            word_count = len(b_words)
            if word_count < 35 or word_count > 45:
                status = f"COUNT_OUT_OF_TARGET({word_count})"
                flags.append((num, layout, f"Word count {word_count} outside target 35-45 (claimed {claimed_val})"))
            if num_phrases not in [2, 3]:
                # Flag if not 2-3 declarative phrases
                flags.append((num, layout, f"Phrases count = {num_phrases} (target: 2-3 declarative phrases)"))
                
        table.append((num, layout, claimed_val, len(b_words), len(math_tokens), len(full_words), num_phrases, status))

    print(f"{'Slide':5s} | {'Layout':28s} | {'Claimed':7s} | {'Words':5s} | {'+Math':5s} | {'Visible':7s} | {'Phrases':7s} | Status")
    print("-" * 95)
    for num, layout, cl_val, w_cnt, w_math, v_cnt, n_phr, stat in table:
        cl_s = str(cl_val) if cl_val is not None else "-"
        print(f"Slide {num:02d} | {layout:28s} | {cl_s:7s} | {w_cnt:<5d} | {w_math:<5d} | {v_cnt:<7d} | {n_phr:<7d} | {stat}")
        
    print(f"\nTotal flags on Occam's Razor: {len(flags)}")
    for f_item in flags:
        print(f"  Flag: Slide {f_item[0]:02d} ({f_item[1]}): {f_item[2]}")
    return len(flags) == 0

# =====================================================================
# CHECK 2: Ban on Q&A
# =====================================================================
def run_check_2():
    print("\n" + "=" * 70)
    print("CHECK 2: Ban on Q&A (0 Question Marks in Titles, Cards, Bullets, Rhetorical Qs)")
    print("=" * 70)
    speech_text, plan_text = load_files()
    _, speech_slides = split_into_slides(speech_text)
    _, plan_slides = split_into_slides(plan_text)
    
    findings = []
    
    # 1. Slide outlines in speech
    for num, s in speech_slides.items():
        if "?" in s["title"]:
            findings.append(("speech_title", num, s["title"]))
        layout, outline = extract_slide_outline(s["body"])
        if outline:
            for line in outline.splitlines():
                if "?" in line:
                    findings.append(("speech_outline", num, line.strip()))
                    
    # 2. Spoken text in speech (rhetorical questions & Q&A)
    for num, s in speech_slides.items():
        # find speech quotes > «...»
        quotes = re.findall(r'>\s*«(.*?)»', s["body"], re.DOTALL)
        for q in quotes:
            for sentence in re.split(r'[\.\!\n]\s*', q):
                if "?" in sentence:
                    findings.append(("speech_spoken_rhetorical_q", num, sentence.strip()))
        # check transitions
        trans = re.findall(r'\* \*\*Смысловой переход.*?\*\*:\s*(.*?)$', s["body"], re.MULTILINE)
        for t in trans:
            if "?" in t:
                findings.append(("speech_transition_q", num, t.strip()))
                
    # 3. Plan file titles, cards, bullets, transitions
    for num, s in plan_slides.items():
        if "?" in s["title"]:
            findings.append(("plan_title", num, s["title"]))
        for line in s["body"].splitlines():
            sline = line.strip()
            if sline.startswith(("* **Связь", "* **Переход", "- **Связь")):
                if "?" in sline:
                    findings.append(("plan_transition_q", num, sline))
            elif sline.startswith(("*", "-", "#", "1.", "2.", "3.", "4.", "5.", "6.")):
                if "?" in sline:
                    findings.append(("plan_card_bullet_q", num, sline))
                    
    print(f"Total question mark findings: {len(findings)}")
    for cat, num, text in findings:
        print(f"  [{cat}] Slide {num:02d}: {text}")
    return len(findings) == 0

# =====================================================================
# CHECK 3: Metadata Leak Test (Slides 2 to 24)
# =====================================================================
def run_check_3():
    print("\n" + "=" * 70)
    print("CHECK 3: Metadata Leak Test (Slides 2 to 24: ГУАП, Кафедра, Попов, 4 семестр, Название курса)")
    print("=" * 70)
    speech_text, plan_text = load_files()
    _, speech_slides = split_into_slides(speech_text)
    _, plan_slides = split_into_slides(plan_text)
    
    forbidden = [
        (re.compile(r"ГУАП", re.IGNORECASE), "ГУАП"),
        (re.compile(r"Кафедра", re.IGNORECASE), "Кафедра"),
        (re.compile(r"Попов", re.IGNORECASE), "Попов"),
        (re.compile(r"4\s*семестр", re.IGNORECASE), "4 семестр"),
        (re.compile(r"Физические основы нанотехнологий", re.IGNORECASE), "Название курса"),
    ]
    
    leaks = []
    for num in range(2, 25):
        # Check speech
        if num in speech_slides:
            content = speech_slides[num]["title"] + "\n" + speech_slides[num]["body"]
            for pat, name in forbidden:
                for m in pat.finditer(content):
                    leaks.append(("speech", num, name, m.group(0)))
        # Check plan
        if num in plan_slides:
            content = plan_slides[num]["title"] + "\n" + plan_slides[num]["body"]
            for pat, name in forbidden:
                for m in pat.finditer(content):
                    leaks.append(("plan", num, name, m.group(0)))
                    
    print(f"Total metadata leaks detected: {len(leaks)}")
    for src, num, name, val in leaks:
        print(f"  Leak in [{src}] Slide {num:02d}: {name} ('{val}')")
    return len(leaks) == 0

# =====================================================================
# CHECK 4: Section Dividers (Slides 4, 8, 13, 19)
# =====================================================================
def run_check_4():
    print("\n" + "=" * 70)
    print("CHECK 4: Section Dividers (Slides 4, 8, 13, 19: #002C5F, Centered Problem, 1-2 Sentences)")
    print("=" * 70)
    speech_text, plan_text = load_files()
    _, speech_slides = split_into_slides(speech_text)
    _, plan_slides = split_into_slides(plan_text)
    
    dividers = [4, 8, 13, 19]
    divider_issues = []
    
    for num in dividers:
        sp = speech_slides.get(num)
        pl = plan_slides.get(num)
        if not sp or not pl:
            divider_issues.append((num, "MISSING_DIVIDER_SLIDE"))
            continue
            
        # 1. Background #002C5F
        sp_has_bg = "#002C5F" in sp["body"]
        pl_has_bg = "#002C5F" in pl["body"]
        
        # 2. Outline check
        layout, outline = extract_slide_outline(sp["body"])
        has_centered_tag = "Центрированная проблема" in outline
        
        # 3. Explanation sentences
        prob_m = re.search(r'\* \*\*Центрированная проблема.*?\*\*:\s*\n\s*-\s*(.*?)(?=\n\* \*\*|\Z)', outline, re.DOTALL)
        prob_text = prob_m.group(1).strip() if prob_m else ""
        # split by punctuation
        sentences = [s.strip() for s in re.split(r'[\.\!\?]\s+', prob_text) if s.strip()]
        
        print(f"Slide {num:02d} | BG speech: {sp_has_bg} | BG plan: {pl_has_bg} | Centered Tag: {has_centered_tag} | Sentences: {len(sentences)}")
        print(f"   Problem text: {prob_text[:120]}...")
        
        if not (sp_has_bg and pl_has_bg):
            divider_issues.append((num, "MISSING_BG_002C5F"))
        if not has_centered_tag:
            divider_issues.append((num, "MISSING_CENTERED_TAG"))
        if not (1 <= len(sentences) <= 2):
            divider_issues.append((num, f"EXPLANATION_SENTENCE_COUNT_{len(sentences)}"))
            
    print(f"\nTotal section divider issues: {len(divider_issues)}")
    for iss in divider_issues:
        print(f"  Issue Slide {iss[0]:02d}: {iss[1]}")
    return len(divider_issues) == 0

# =====================================================================
# CHECK 5: First-Mention Acronyms
# =====================================================================
def run_check_5():
    print("\n" + "=" * 70)
    print("CHECK 5: First-Mention Acronyms Verification")
    print("=" * 70)
    speech_text, plan_text = load_files()
    
    targets = [
        ("СЭМ", r"сканирующ\w*\s+электронн\w*\s+микроскоп\w*"),
        ("АСМ", r"атомно-силов\w*\s+микроскоп\w*"),
        ("МЛЭ", r"молекулярно-лучев\w*\s+эпитакси\w*"),
        ("ДБЭО", r"дифракци\w*\s+быстрых\s+электронов\s+на\s+отражение"),
        ("RHEED", r"reflection\s+high-energy\s+electron\s+diffraction|дифракци\w*\s+быстрых\s+электронов"),
        ("HEMT", r"транзистор\w*\s+с\s+высокой\s+подвижностью\s+электронов|high\s+electron\s+mobility\s+transistor"),
        ("ДЭГ", r"двумерн\w*\s+электронн\w*\s+газ\w*"),
        ("БЭТ", r"брунауэр\w*\s*—?\s*эммет\w*\s*—?\s*теллер\w*"),
        ("BJH", r"баррет\w*\s*—?\s*джойнер\w*\s*—?\s*халенд\w*"),
        ("ИЮПАК", r"международн\w*\s+союз\w*\s+теоретической\s+и\s+прикладной\s+химии"),
        ("IUPAC", r"международн\w*\s+союз\w*\s+теоретической\s+и\s+прикладной\s+химии"),
        ("FM-рост", r"франк\w*\s*—?\s*ван\s+дер\s+мерве"),
        ("VW-рост", r"фольмер\w*\s*—?\s*вебер\w*"),
        ("SK-рост", r"странск\w*\s*—?\s*крастанов\w*"),
    ]
    
    issues = []
    
    for acr, exp_pat in targets:
        print(f"\n--- Acronym: {acr} ---")
        for fname, txt in [("speech", speech_text), ("plan", plan_text)]:
            lines = txt.splitlines()
            found = False
            for idx, line in enumerate(lines, 1):
                # Search word boundary for acronym
                # Note: for FM-рост, handle hyphen
                pat = re.compile(r'(?<![\w])' + re.escape(acr) + r'(?![\w])')
                m = pat.search(line)
                if m:
                    found = True
                    # Check 1: Is acronym bolded?
                    is_bold = bool(re.search(r'\*\*[^*]*' + re.escape(acr) + r'[^*]*\*\*', line))
                    # Check 2: Is full expansion present in the same line/sentence or nearby?
                    has_expansion = bool(re.search(exp_pat, line, re.IGNORECASE))
                    
                    print(f"  [{fname}:L{idx:03d}] Bolded: {is_bold} | Expanded: {has_expansion}")
                    print(f"     Line: {line.strip()[:110]}")
                    
                    if not is_bold:
                        issues.append((fname, acr, idx, "FIRST_MENTION_NOT_BOLDED", line.strip()[:80]))
                    if not has_expansion:
                        issues.append((fname, acr, idx, "FIRST_MENTION_MISSING_FULL_RUSSIAN_EXPANSION", line.strip()[:80]))
                    break
            if not found:
                issues.append((fname, acr, 0, "NOT_FOUND_IN_FILE", ""))
                
    print(f"\nTotal first-mention acronym issues: {len(issues)}")
    for fname, acr, idx, err, text in issues:
        print(f"  [{fname}] '{acr}' at L{idx}: {err} -> {text}")
    return len(issues) == 0

# =====================================================================
# CHECK 6: Forbidden Words
# =====================================================================
def run_check_6():
    print("\n" + "=" * 70)
    print("CHECK 6: Forbidden Words ('лабораторная работа', 'ЛР')")
    print("=" * 70)
    speech_text, plan_text = load_files()
    
    forbidden = [
        re.compile(r"лабораторн\w*", re.IGNORECASE),
        re.compile(r"\bЛР\b", re.IGNORECASE),
        re.compile(r"ЛР\s*№", re.IGNORECASE),
        re.compile(r"ЛР\s*\d+", re.IGNORECASE),
    ]
    
    findings = []
    for fname, txt in [("speech", speech_text), ("plan", plan_text)]:
        for idx, line in enumerate(txt.splitlines(), 1):
            for pat in forbidden:
                m = pat.search(line)
                if m:
                    findings.append((fname, idx, m.group(0), line.strip()))
                    
    print(f"Total forbidden word findings: {len(findings)}")
    for f in findings:
        print(f"  [{f[0]}:L{f[1]}] Matched '{f[2]}': {f[3]}")
    return len(findings) == 0

if __name__ == "__main__":
    c6 = run_check_6()
    c3 = run_check_3()
    c4 = run_check_4()
    c2 = run_check_2()
    c1 = run_check_1()
    c5 = run_check_5()
    
    print("\n" + "=" * 70)
    print("CHALLENGER 2 SUMMARY MATRIX")
    print("=" * 70)
    print(f"Check 1 (Occam's razor 35-45 words & phrases): {'PASS' if c1 else 'FAIL'}")
    print(f"Check 2 (Ban on Q&A & Rhetorical Questions):   {'PASS' if c2 else 'FAIL'}")
    print(f"Check 3 (Metadata leak slides 2..24):          {'PASS' if c3 else 'FAIL'}")
    print(f"Check 4 (Section dividers 4, 8, 13, 19):       {'PASS' if c4 else 'FAIL'}")
    print(f"Check 5 (First-mention acronyms expansion):     {'PASS' if c5 else 'FAIL'}")
    print(f"Check 6 (Forbidden words 0 occurrences):       {'PASS' if c6 else 'FAIL'}")
    print("=" * 70)
