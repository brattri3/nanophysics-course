#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Acquisition of Authentic Scientific Visual Assets & 16:9 Split-Screen Generator
for Lecture 03 ("Thermodynamics of Disperse Systems and Colloidal Solutions").

Replaces artificial AI illustrations with genuine historical & scientific assets:
1. Faraday ruby gold sol in laboratory flask (The Royal Institution / Wikimedia Commons CC BY-SA 3.0)
2. Bare Fe3O4 nanoparticle aggregation TEM micrograph (S. Ota et al., CC BY 4.0)

Generates:
- course_materials/semester_4/lectures/figures_l03/fig_01_faraday_gold_sol.png
- course_materials/semester_4/lectures/figures_l03/fig_01_iron_oxide_aggregation.jpg
- course_materials/semester_4/lectures/figures_l03/fig_01_split_faraday_vs_fe3o4.png (1920x1080 16:9 composite)
"""

import os
import sys
import subprocess
import urllib.request
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageOps

# Base directories
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
FIGURES_DIR = PROJECT_ROOT / "course_materials" / "semester_4" / "lectures" / "figures_l03"

FARADAY_URL = "https://upload.wikimedia.org/wikipedia/commons/9/90/Goldkolloidl%C3%B6sung.png"
FE3O4_URL = "https://upload.wikimedia.org/wikipedia/commons/7/7d/Transmission-electron-microscopic-TEM-image-of-the-water-based-magnetite-nanoparticles.jpg"

FARADAY_FILE = FIGURES_DIR / "fig_01_faraday_gold_sol.png"
FE3O4_FILE = FIGURES_DIR / "fig_01_iron_oxide_aggregation.jpg"
COMPOSITE_FILE = FIGURES_DIR / "fig_01_split_faraday_vs_fe3o4.png"

# SUAI Official Brand Palette
COLOR_NAVY = (0, 44, 95)         # #002C5F
COLOR_BLUE = (0, 90, 170)        # #005AAA
COLOR_CRIMSON = (231, 15, 71)    # #E70F47
COLOR_CYAN = (0, 190, 243)       # #00BEF3
COLOR_GREEN = (0, 154, 73)       # #009A49
COLOR_ORANGE = (255, 100, 24)    # #FF6418
COLOR_CHARCOAL = (36, 40, 52)    # #242834
COLOR_MUTED = (90, 105, 120)     # #5A6978
COLOR_BG_CARD = (244, 247, 250)  # #F4F7FA
COLOR_CARD_BORDER = (200, 215, 230) # #C8D7E6
COLOR_WHITE = (255, 255, 255)
COLOR_GREEN_BG = (232, 245, 233) # #E8F5E9
COLOR_RED_BG = (255, 235, 238)   # #FFEBEE


def download_file(url: str, dest: Path) -> bool:
    """Download a file with curl or urllib fallback."""
    if dest.exists() and dest.stat().st_size > 10000:
        print(f"[OK] Asset already present: {dest.name} ({dest.stat().st_size} bytes)")
        return True

    dest.parent.mkdir(parents=True, exist_ok=True)
    print(f"[DOWNLOADING] {url} -> {dest.name}...")

    # Attempt 1: curl.exe
    try:
        cmd = ["curl.exe", "-L", "-A", "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", url, "-o", str(dest)]
        res = subprocess.run(cmd, capture_output=True, timeout=60)
        if res.returncode == 0 and dest.exists() and dest.stat().st_size > 10000:
            print(f"[SUCCESS] Downloaded via curl: {dest.name} ({dest.stat().st_size} bytes)")
            return True
    except Exception as e:
        print(f"[WARN] curl failed: {e}")

    # Attempt 2: urllib
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=45) as response, open(dest, "wb") as out_file:
            data = response.read()
            out_file.write(data)
        if dest.exists() and dest.stat().st_size > 10000:
            print(f"[SUCCESS] Downloaded via urllib: {dest.name} ({dest.stat().st_size} bytes)")
            return True
    except Exception as e:
        print(f"[ERROR] urllib failed: {e}")

    return dest.exists() and dest.stat().st_size > 10000


def get_font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    """Load Arial or Arial Bold from Windows standard font directory."""
    font_name = "arialbd.ttf" if bold else "arial.ttf"
    font_paths = [
        Path("C:/Windows/Fonts") / font_name,
        Path("C:/WINNT/Fonts") / font_name,
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for p in font_paths:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                pass
    return ImageFont.load_default()


def create_split_screen_composite():
    """
    Creates a professional, academic 16:9 split-screen comparison:
    Left: Faraday ruby gold sol (colloidal stability >170 years)
    Right: Bare Fe3O4 TEM micrograph (spontaneous aggregation / sedimentation)
    """
    width, height = 1920, 1080
    canvas = Image.new("RGB", (width, height), COLOR_WHITE)
    draw = ImageDraw.Draw(canvas)

    # 1. Subtle background grid / card container
    # Top banner bar (Deep Navy)
    banner_height = 88
    draw.rectangle([0, 0, width, banner_height], fill=COLOR_NAVY)

    # Top brand signature gradient line (SUAI Blue -> Sky Cyan -> Crimson)
    # y = 88..92
    grad_y = banner_height
    grad_h = 4
    for x in range(width):
        ratio = x / width
        if ratio < 0.54:
            t = ratio / 0.54
            r = int(COLOR_BLUE[0] + t * (COLOR_CYAN[0] - COLOR_BLUE[0]))
            g = int(COLOR_BLUE[1] + t * (COLOR_CYAN[1] - COLOR_BLUE[1]))
            b = int(COLOR_BLUE[2] + t * (COLOR_CYAN[2] - COLOR_BLUE[2]))
        else:
            t = (ratio - 0.54) / 0.46
            r = int(COLOR_CYAN[0] + t * (COLOR_CRIMSON[0] - COLOR_CYAN[0]))
            g = int(COLOR_CYAN[1] + t * (COLOR_CRIMSON[1] - COLOR_CYAN[1]))
            b = int(COLOR_CYAN[2] + t * (COLOR_CRIMSON[2] - COLOR_CYAN[2]))
        draw.line([(x, grad_y), (x, grad_y + grad_h)], fill=(r, g, b))

    # Top banner typography
    font_title = get_font(30, bold=True)
    font_tag = get_font(18, bold=True)
    font_sub = get_font(18, bold=False)

    title_text = "ТЕРМОДИНАМИКА ДИСПЕРСНЫХ СИСТЕМ: УСТОЙЧИВОСТЬ VS СПОНТАННАЯ АГРЕГАЦИЯ"
    draw.text((40, 26), title_text, font=font_title, fill=COLOR_WHITE)
    draw.text((width - 320, 34), "НАНОМАСШТАБ 1–100 НМ", font=font_tag, fill=COLOR_CYAN)

    # 2. Layout Geometry: Two large panels
    margin_x = 40
    gap = 30
    panel_top = 112
    panel_bottom = 1000
    panel_height = panel_bottom - panel_top
    panel_width = (width - 2 * margin_x - gap) // 2  # ~885 px

    left_panel_box = [margin_x, panel_top, margin_x + panel_width, panel_bottom]
    right_panel_box = [margin_x + panel_width + gap, panel_top, width - margin_x, panel_bottom]

    # Fonts for cards
    font_card_badge = get_font(21, bold=True)
    font_card_head = get_font(24, bold=True)
    font_body_bold = get_font(19, bold=True)
    font_body = get_font(18, bold=False)
    font_caption = get_font(15, bold=False)

    # ==========================
    # LEFT PANEL: FARADAY GOLD SOL
    # ==========================
    # Panel background
    draw.rounded_rectangle(left_panel_box, radius=16, fill=COLOR_BG_CARD, outline=COLOR_CARD_BORDER, width=2)

    # Header Card within Left Panel
    header_box_l = [left_panel_box[0] + 16, panel_top + 16, left_panel_box[2] - 16, panel_top + 130]
    draw.rounded_rectangle(header_box_l, radius=12, fill=COLOR_GREEN_BG, outline=COLOR_GREEN, width=2)

    # Green badge
    draw.rectangle([header_box_l[0] + 16, header_box_l[1] + 14, header_box_l[0] + 310, header_box_l[1] + 44], fill=COLOR_GREEN)
    draw.text((header_box_l[0] + 24, header_box_l[1] + 18), "ЭТАЛОН УСТОЙЧИВОСТИ", font=font_card_badge, fill=COLOR_WHITE)

    draw.text((header_box_l[0] + 16, header_box_l[1] + 54), "Рубиновый гидрозоль золота (Майкл Фарадей, 1857 г.)", font=font_card_head, fill=COLOR_NAVY)
    draw.text((header_box_l[0] + 16, header_box_l[1] + 86), "Сохраняет оптическую прозрачность и термодинамический баланс свыше 170 лет", font=font_body, fill=COLOR_CHARCOAL)

    # Image area for Faraday flask
    img_box_l = [left_panel_box[0] + 16, panel_top + 146, left_panel_box[2] - 16, panel_bottom - 130]
    draw.rounded_rectangle(img_box_l, radius=10, fill=(250, 250, 252), outline=COLOR_CARD_BORDER, width=1)

    if FARADAY_FILE.exists():
        with Image.open(FARADAY_FILE) as f_img:
            # Crop/fit flask to fit gracefully inside img_box_l
            target_w = img_box_l[2] - img_box_l[0] - 8
            target_h = img_box_l[3] - img_box_l[1] - 8

            # The flask image is tall (844x1580). Crop around the liquid flask body
            # Let's crop from 10% top to 92% bottom to focus on the flask and ruby sol
            crop_box = (0, int(f_img.height * 0.08), f_img.width, int(f_img.height * 0.94))
            cropped_f = f_img.crop(crop_box)

            # Fit to target
            aspect = cropped_f.width / cropped_f.height
            if target_w / target_h > aspect:
                new_h = target_h
                new_w = int(target_h * aspect)
            else:
                new_w = target_w
                new_h = int(target_w / aspect)

            resized_f = cropped_f.resize((new_w, new_h), Image.Resampling.LANCZOS)

            # Center inside image box
            pos_x = img_box_l[0] + (img_box_l[2] - img_box_l[0] - new_w) // 2
            pos_y = img_box_l[1] + (img_box_l[3] - img_box_l[1] - new_h) // 2
            canvas.paste(resized_f, (pos_x, pos_y))

    # Mechanism & Citation Footers for Left Panel
    foot_l = [left_panel_box[0] + 16, panel_bottom - 116, left_panel_box[2] - 16, panel_bottom - 16]
    draw.rounded_rectangle(foot_l, radius=10, fill=COLOR_WHITE, outline=COLOR_CARD_BORDER, width=1)
    draw.text((foot_l[0] + 16, foot_l[1] + 12), "Физический барьер: двойной электрический слой (ДЭС)", font=font_body_bold, fill=COLOR_BLUE)
    draw.text((foot_l[0] + 16, foot_l[1] + 38), "Высокий дзета-потенциал (|ζ| > 30 мВ) формирует отталкивание U_R, блокируя минимум ДЛФО", font=font_caption, fill=COLOR_CHARCOAL)
    draw.text((foot_l[0] + 16, foot_l[1] + 64), "Источник: Королевский институт Великобритании (The Royal Institution) / Wikimedia CC BY-SA 3.0", font=font_caption, fill=COLOR_MUTED)

    # ==========================
    # RIGHT PANEL: BARE FE3O4 AGGREGATION
    # ==========================
    # Panel background
    draw.rounded_rectangle(right_panel_box, radius=16, fill=COLOR_BG_CARD, outline=COLOR_CARD_BORDER, width=2)

    # Header Card within Right Panel
    header_box_r = [right_panel_box[0] + 16, panel_top + 16, right_panel_box[2] - 16, panel_top + 130]
    draw.rounded_rectangle(header_box_r, radius=12, fill=COLOR_RED_BG, outline=COLOR_CRIMSON, width=2)

    # Red badge
    draw.rectangle([header_box_r[0] + 16, header_box_r[1] + 14, header_box_r[0] + 290, header_box_r[1] + 44], fill=COLOR_CRIMSON)
    draw.text((header_box_r[0] + 24, header_box_r[1] + 18), "ПРОБЛЕМА АГРЕГАЦИИ", font=font_card_badge, fill=COLOR_WHITE)

    draw.text((header_box_r[0] + 16, header_box_r[1] + 54), "Наночастицы оксида железа Fe3O4 (просвечивающая ЭМ, ПЭМ)", font=font_card_head, fill=COLOR_NAVY)
    draw.text((header_box_r[0] + 16, header_box_r[1] + 86), "Спонтанное схлопывание наночастиц 10–20 нм в микронные агломераты и осадок", font=font_body, fill=COLOR_CHARCOAL)

    # Image area for Fe3O4 TEM
    img_box_r = [right_panel_box[0] + 16, panel_top + 146, right_panel_box[2] - 16, panel_bottom - 130]
    draw.rounded_rectangle(img_box_r, radius=10, fill=(245, 245, 248), outline=COLOR_CARD_BORDER, width=1)

    if FE3O4_FILE.exists():
        with Image.open(FE3O4_FILE) as fe_img:
            target_w = img_box_r[2] - img_box_r[0] - 8
            target_h = img_box_r[3] - img_box_r[1] - 8

            aspect = fe_img.width / fe_img.height
            if target_w / target_h > aspect:
                new_h = target_h
                new_w = int(target_h * aspect)
            else:
                new_w = target_w
                new_h = int(target_w / aspect)

            resized_fe = fe_img.resize((new_w, new_h), Image.Resampling.LANCZOS)
            pos_x = img_box_r[0] + (img_box_r[2] - img_box_r[0] - new_w) // 2
            pos_y = img_box_r[1] + (img_box_r[3] - img_box_r[1] - new_h) // 2
            canvas.paste(resized_fe, (pos_x, pos_y))

    # Mechanism & Citation Footers for Right Panel
    foot_r = [right_panel_box[0] + 16, panel_bottom - 116, right_panel_box[2] - 16, panel_bottom - 16]
    draw.rounded_rectangle(foot_r, radius=10, fill=COLOR_WHITE, outline=COLOR_CARD_BORDER, width=1)
    draw.text((foot_r[0] + 16, foot_r[1] + 12), "Физический механизм: избыток ΔGs = σ · S > 0 и силы Ван-дер-Ваальса", font=font_body_bold, fill=COLOR_CRIMSON)
    draw.text((foot_r[0] + 16, foot_r[1] + 38), "Без защитной оболочки частицы проваливаются в глубокий первичный минимум потенциала ДЛФО", font=font_caption, fill=COLOR_CHARCOAL)
    draw.text((foot_r[0] + 16, foot_r[1] + 64), "Микрофотография: S. Ota et al., CC BY 4.0 / Open-Access (DOI: 10.3390/nano8080629)", font=font_caption, fill=COLOR_MUTED)

    # 3. Bottom Global Takeaway Banner
    bottom_banner_box = [margin_x, panel_bottom + 14, width - margin_x, height - 16]
    draw.rounded_rectangle(bottom_banner_box, radius=8, fill=(238, 244, 250), outline=COLOR_BLUE, width=1)
    badge_w = 90
    draw.rectangle([bottom_banner_box[0] + 10, bottom_banner_box[1] + 8, bottom_banner_box[0] + 10 + badge_w, bottom_banner_box[3] - 8], fill=COLOR_NAVY)
    draw.text((bottom_banner_box[0] + 20, bottom_banner_box[1] + 13), "ИТОГ", font=get_font(18, bold=True), fill=COLOR_WHITE)
    draw.text(
        (bottom_banner_box[0] + 115, bottom_banner_box[1] + 13),
        "Ключевая задача нанотехнологий — преодоление термодинамической нестабильности (ΔGs > 0) путем создания электростатических (ДЭС) или стерических барьеров.",
        font=get_font(16, bold=True),
        fill=COLOR_NAVY
    )

    # Save high-resolution PNG
    canvas.save(COMPOSITE_FILE, format="PNG", dpi=(300, 300), optimize=True)
    print(f"[SUCCESS] Composite generated: {COMPOSITE_FILE} ({COMPOSITE_FILE.stat().st_size} bytes, {width}x{height})")


def main():
    print("=== Downloading Authentic Scientific Visuals ===")
    ok_faraday = download_file(FARADAY_URL, FARADAY_FILE)
    ok_fe3o4 = download_file(FE3O4_URL, FE3O4_FILE)

    if not ok_faraday or not ok_fe3o4:
        print(f"[ERROR] Asset download incomplete: faraday={ok_faraday}, fe3o4={ok_fe3o4}")
        sys.exit(1)

    print("=== Generating High-Resolution 16:9 Split-Screen Visual ===")
    create_split_screen_composite()
    print("=== Complete! ===")


if __name__ == "__main__":
    main()
