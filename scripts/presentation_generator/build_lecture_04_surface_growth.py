"""
Генератор презентации Лекции №4 (24 слайда, 16:9):
«Поверхностные явления и механизмы роста плёнок».

Строгое соблюдение дизайн-кода ГУАП (SUAI):
- Гибрид Вариации C и A: светлый академический фон (#F8FAFC) с тёмно-синими разделителями разделов (#002C5F).
- Single-Point Occurrence (SPO): название вуза, кафедры, курса и ФИО лектора ТОЛЬКО на Слайде 1.
- Бритва Оккама: 2–3 лаконичных утверждения на слайд, 0 знаков вопроса (?), 0 упоминаний ЛР.
- Правило R3: выделение аббревиатур полужирным синим цветом (#005AAA).
- Синхронизированные 4-компонентные заметки докладчика (Speaker Notes) из lecture_04_speech.md.
"""

import os
import re
import sys
import shutil
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor

SKILL_SCRIPTS = os.path.abspath(".agents/skills/scientific-presentation-creator/scripts")
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

from template_deck_builder import (
    SUAI_PALETTE,
    find_asset,
    create_base_presentation,
    add_signature_gradient_line,
)

SUAI_NAVY = RGBColor(0x00, 0x2C, 0x5F)
SUAI_BLUE = RGBColor(0x00, 0x5A, 0xAA)
SUAI_CYAN = RGBColor(0x00, 0xBE, 0xF3)
BG_LIGHT = RGBColor(0xF8, 0xFA, 0xFC)
CARD_WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BORDER_GRAY = RGBColor(0xC8, 0xD7, 0xE6)
TEXT_DARK = RGBColor(0x1E, 0x29, 0x3B)
TEXT_MUTED = RGBColor(0x52, 0x60, 0x6D)
ACCENT_RED = RGBColor(0xC0, 0x39, 0x2B)
ACCENT_GREEN = RGBColor(0x1B, 0x78, 0x37)
ACCENT_ORANGE = RGBColor(0xD9, 0x77, 0x06)
ACCENT_PURPLE = RGBColor(0x6D, 0x28, 0xD9)
FONT_HEADING = "Arial"
FONT_BODY = "Arial"


class ScientificDeckBuilder:
    """Адаптер конструктора презентации ГУАП с контролем клиренса шапки (>= 25 px) и SPO."""
    def __init__(self, lecture_title: str, total_slides: int = 24):
        self.prs = create_base_presentation()
        self.blank_layout = self.prs.slide_layouts[6]
        self.lecture_title = lecture_title
        self.total_slides = total_slides
        self.slide_Counter = 0
        self.draw_problem_icon = None

    def new_slide(self):
        slide = self.prs.slides.add_slide(self.blank_layout)
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_LIGHT
        bg.line.fill.background()
        self.slide_Counter += 1
        return slide

    def add_header(self, slide, title_text: str, subtitle_text: str = "", problem_id: str = None):
        tb = slide.shapes.add_textbox(Inches(0.55), Inches(0.22), Inches(11.40), Inches(0.58))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0

        p = tf.paragraphs[0]
        title_pt = 17.5 if len(title_text) > 54 else 19.0
        format_para_with_r3(p, title_text, font_size=title_pt, color=SUAI_NAVY, bold_prefix_color=SUAI_NAVY)
        for r in p.runs:
            r.font.name = FONT_HEADING
            r.font.bold = True
        p.space_after = Pt(1)

        if subtitle_text:
            p2 = tf.add_paragraph()
            format_para_with_r3(p2, subtitle_text, font_size=10.5, color=TEXT_MUTED, bold_prefix_color=SUAI_BLUE)

        if problem_id and self.draw_problem_icon:
            self.draw_problem_icon(slide, 12.18, 0.24, 0.56, problem_id, SUAI_BLUE)

        add_signature_gradient_line(slide, left=0.55, top=1.06, width=12.233, height=0.025)

    def add_figure(self, slide, img_path: str, x: float, y: float, w: float, h: float, caption: str = ""):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
        card.fill.solid()
        card.fill.fore_color.rgb = CARD_WHITE
        card.line.color.rgb = BORDER_GRAY
        card.line.width = Pt(1.0)
        card.adjustments[0] = 0.02

        cap_h = 0.38 if caption else 0.06
        avail_w = w - 0.16
        avail_h = h - cap_h - 0.10

        if os.path.exists(img_path):
            from PIL import Image as PILImage
            with PILImage.open(img_path) as im:
                iw, ih = im.size
            aspect = iw / ih
            if avail_w / avail_h > aspect:
                pic_h = avail_h
                pic_w = pic_h * aspect
            else:
                pic_w = avail_w
                pic_h = pic_w / aspect
            px = x + (w - pic_w) / 2.0
            py = y + 0.06 + (avail_h - pic_h) / 2.0
            slide.shapes.add_picture(img_path, Inches(px), Inches(py), width=Inches(pic_w), height=Inches(pic_h))

        if caption:
            tb_c = slide.shapes.add_textbox(Inches(x + 0.08), Inches(y + h - 0.36), Inches(w - 0.16), Inches(0.32))
            tf_c = tb_c.text_frame
            tf_c.word_wrap = True
            tf_c.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_c.margin_top = tf_c.margin_bottom = tf_c.margin_left = tf_c.margin_right = 0
            pc = tf_c.paragraphs[0]
            pc.alignment = PP_ALIGN.CENTER
            format_para_with_r3(pc, caption, font_size=9.0, color=TEXT_MUTED, bold_prefix_color=SUAI_NAVY)

    def add_takeaway_banner(self, slide, text: str, y: float = 6.22, h: float = 0.56):
        box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(y), Inches(12.233), Inches(h))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(0xEE, 0xF4, 0xFA)
        box.line.color.rgb = SUAI_BLUE
        box.line.width = Pt(1.2)
        box.adjustments[0] = 0.08

        tb = slide.shapes.add_textbox(Inches(0.75), Inches(y + 0.06), Inches(11.833), Inches(h - 0.12))
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        format_para_with_r3(p, text, font_size=12, color=SUAI_NAVY, bold_prefix_color=SUAI_NAVY)
        for r in p.runs:
            r.font.bold = True

    def add_footer(self, slide):
        tb = slide.shapes.add_textbox(Inches(0.55), Inches(7.02), Inches(12.233), Inches(0.28))
        tf = tb.text_frame
        tf.margin_top = tf.margin_bottom = tf.margin_left = tf.margin_right = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.RIGHT
        p.text = f"{self.lecture_title}   |   Слайд {self.slide_Counter} из {self.total_slides}"
        p.font.name = FONT_BODY
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MUTED

    def save(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.prs.save(path)


FIG_DIR = os.path.abspath("course_materials/semester_4/lectures/figures_l04")
LOGO_PATH = find_asset("guap_image4.png") or find_asset("guap_logo_extracted.png")
SPEECH_MD_PATH = os.path.abspath("course_materials/semester_4/lectures/lecture_04_speech.md")
OUT_PPTX = os.path.abspath("course_materials/semester_4/lectures/lecture_04_surface_growth.pptx")
OUT_PPTX_ALT = os.path.abspath("course_materials/semester_4/lectures/lecture_04_surface_films.pptx")

ABBREV_RX = re.compile(
    r'\b(СЭМ|ПЭМ|АСМ|МЛЭ|ДБЭО|RHEED|HEMT|ДЭГ|КТ|БЭТ|BJH|ИЮПАК|IUPAC|ПАВ|FM|VW|SK)\b'
)
SUBSCRIPT_RX = re.compile(r'_(?:\{([^}]+)\}|([A-Za-zА-Яа-яЁё0-9∞⊥∥,−+-]+))')


def parse_speech_notes(md_path: str) -> dict:
    """Извлекает 4-компонентные заметки докладчика для всех 24 слайдов из lecture_04_speech.md."""
    if not os.path.exists(md_path):
        return {}
    with open(md_path, "r", encoding="utf-8") as f:
        text = f.read()

    notes = {}
    blocks = re.split(r'\n### Слайд (\d+)\.', text)
    for i in range(1, len(blocks), 2):
        slide_num = int(blocks[i])
        body = blocks[i + 1]

        # Заголовок / тезис
        title_m = re.search(r'\* \*\*Заголовок:\*\*\s*(.+)', body)
        takeaway_m = re.search(r'\* \*\*Takeaway Баннер:\*\*\s*(.+)', body)
        vis_m = re.search(r'\* \*\*(?:Визуальный блок|Иконка-маркер|Навигационная плашка).*?:\*\*\s*(.+)', body)
        trans_m = re.search(r'\* \*\*Смысловой переход.*?:\*\*\s*(.+)', body)

        # Живая речь
        speech_lines = []
        for line in body.splitlines():
            if line.strip().startswith(">"):
                clean_l = line.strip().lstrip(">").strip()
                if clean_l:
                    speech_lines.append(clean_l)
        speech_text = "\n".join(speech_lines)

        thesis = takeaway_m.group(1).strip() if takeaway_m else (title_m.group(1).strip() if title_m else "Ключевой физический тезис слайда.")
        vis_acc = vis_m.group(1).strip() if vis_m else "Аналитическая диаграмма и ключевые формулы на слайде."
        trans_txt = trans_m.group(1).strip() if trans_m else "Завершение лекции и переход к вопросам аудитории."

        structured_note = (
            f"1. Физический тезис: {thesis}\n\n"
            f"2. Визуальные акценты: {vis_acc}\n\n"
            f"3. Инженерный контекст (Речь лектора):\n{speech_text}\n\n"
            f"4. Смысловой переход: {trans_txt}"
        )
        notes[slide_num] = structured_note
    return notes


def draw_l4_problem_icon(slide, x: float, y: float, size: float, problem_id: str, accent: RGBColor):
    """Отрисовка геометрической векторной иконки для проблем P1–P6 Лекции №4."""
    badge = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(x), Inches(y), Inches(size), Inches(size)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = RGBColor(0xEE, 0xF5, 0xFC)
    badge.line.color.rgb = accent
    badge.line.width = Pt(1.5)
    badge.adjustments[0] = 0.22

    cx = x + size / 2.0
    cy = y + size / 2.0
    r = size * 0.28

    if problem_id in ("P1", "1"):
        # Капля на подложке (смачивание / отслаивание)
        sub = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r), Inches(cy + r * 0.35), Inches(2 * r), Inches(r * 0.35))
        sub.fill.solid()
        sub.fill.fore_color.rgb = SUAI_NAVY
        sub.line.fill.background()
        drop = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r * 0.7), Inches(cy - r * 0.65), Inches(1.4 * r), Inches(1.1 * r))
        drop.fill.solid()
        drop.fill.fore_color.rgb = accent
        drop.line.fill.background()
    elif problem_id in ("P2", "2"):
        # Мениск Лапласа в нанопоре
        left_w = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r * 0.9), Inches(cy - r * 0.8), Inches(r * 0.35), Inches(1.6 * r))
        right_w = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx + r * 0.55), Inches(cy - r * 0.8), Inches(r * 0.35), Inches(1.6 * r))
        liq = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r * 0.55), Inches(cy - r * 0.1), Inches(1.1 * r), Inches(0.9 * r))
        for sh, col in [(left_w, SUAI_NAVY), (right_w, SUAI_NAVY), (liq, accent)]:
            sh.fill.solid()
            sh.fill.fore_color.rgb = col
            sh.line.fill.background()
    elif problem_id in ("P3", "3"):
        # Созревание Оствальда (малая точка -> крупная точка)
        s_dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx - r * 0.95), Inches(cy - r * 0.35), Inches(0.7 * r), Inches(0.7 * r))
        b_dot = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + r * 0.05), Inches(cy - r * 0.75), Inches(1.4 * r), Inches(1.4 * r))
        s_dot.fill.solid()
        s_dot.fill.fore_color.rgb = ACCENT_RED
        s_dot.line.fill.background()
        b_dot.fill.solid()
        b_dot.fill.fore_color.rgb = accent
        b_dot.line.fill.background()
    elif problem_id in ("P4", "4"):
        # Островковый 3D-разрыв против 2D-слоя
        sub = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r), Inches(cy + r * 0.35), Inches(2 * r), Inches(r * 0.3))
        sub.fill.solid()
        sub.fill.fore_color.rgb = SUAI_NAVY
        sub.line.fill.background()
        for dx in (-0.65, 0.25):
            isl = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(cx + dx * r), Inches(cy - r * 0.45), Inches(0.65 * r), Inches(0.8 * r))
            isl.fill.solid()
            isl.fill.fore_color.rgb = accent
            isl.line.fill.background()
    elif problem_id in ("P5", "5"):
        # Самоорганизованные 3D пирамиды КТ на смачивающем слое (SK)
        wl = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r), Inches(cy + r * 0.25), Inches(2 * r), Inches(r * 0.35))
        wl.fill.solid()
        wl.fill.fore_color.rgb = SUAI_BLUE
        wl.line.fill.background()
        qd = slide.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(cx - r * 0.75), Inches(cy - r * 0.65), Inches(1.5 * r), Inches(0.92 * r))
        qd.fill.solid()
        qd.fill.fore_color.rgb = accent
        qd.line.fill.background()
    else:
        # P6: Адсорбция молекул газа на пористой поверхности (БЭТ)
        surf = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(cx - r), Inches(cy + r * 0.35), Inches(2 * r), Inches(r * 0.3))
        surf.fill.solid()
        surf.fill.fore_color.rgb = SUAI_NAVY
        surf.line.fill.background()
        for dx, dy in [(-0.6, -0.1), (0.0, -0.1), (0.6, -0.1), (-0.3, -0.65), (0.3, -0.65)]:
            mol = slide.shapes.add_shape(MSO_SHAPE.OVAL, Inches(cx + dx * r - r * 0.22), Inches(cy + dy * r), Inches(0.44 * r), Inches(0.44 * r))
            mol.fill.solid()
            mol.fill.fore_color.rgb = accent
            mol.line.fill.background()


def _emit_segment_with_subscripts(para, segment: str, font_name: str, font_size: float,
                                  bold: bool, color: RGBColor):
    """Разбивает строковый сегмент на обычные ранги и нижние индексы (без сырых символов '_' и '{}')."""
    if not segment:
        return
    last_s = 0
    for sm in SUBSCRIPT_RX.finditer(segment):
        if sm.start() > last_s:
            r = para.add_run()
            r.text = segment[last_s:sm.start()]
            r.font.name = font_name
            r.font.size = Pt(font_size)
            r.font.bold = bold
            r.font.color.rgb = color
        sub_txt = sm.group(1) if sm.group(1) is not None else sm.group(2)
        r_sub = para.add_run()
        r_sub.text = sub_txt
        r_sub.font.name = font_name
        r_sub.font.size = Pt(font_size)
        r_sub.font.bold = bold
        r_sub.font.color.rgb = color
        r_sub._r.get_or_add_rPr().set("baseline", "-25000")
        last_s = sm.end()
    if last_s < len(segment):
        r = para.add_run()
        r.text = segment[last_s:]
        r.font.name = font_name
        r.font.size = Pt(font_size)
        r.font.bold = bold
        r.font.color.rgb = color


def _emit_text_with_r3_and_subscripts(para, text_str: str, font_name: str, font_size: float,
                                      bold: bool, color: RGBColor):
    """Форматирует строку с выделением аббревиатур R3 (#005AAA bold) и нижних индексов."""
    last_idx = 0
    for m in ABBREV_RX.finditer(text_str):
        if m.start() > last_idx:
            _emit_segment_with_subscripts(para, text_str[last_idx:m.start()], font_name, font_size, bold, color)
        r_abb = para.add_run()
        r_abb.text = m.group(0)
        r_abb.font.name = FONT_HEADING
        r_abb.font.size = Pt(font_size)
        r_abb.font.bold = True
        r_abb.font.color.rgb = SUAI_BLUE
        last_idx = m.end()
    if last_idx < len(text_str):
        _emit_segment_with_subscripts(para, text_str[last_idx:], font_name, font_size, bold, color)


def format_para_with_r3(para, text: str, font_size: float = 13, color: RGBColor = TEXT_DARK,
                        bold_prefix_color: RGBColor = SUAI_NAVY):
    """Форматирование абзаца с умной подсветкой короткого префикса до ':', нижних индексов и аббревиатур R3."""
    para.text = ""
    if ":" in text:
        prefix, rest = text.split(":", 1)
        if rest.strip() and len(prefix) <= 54 and prefix.count("(") == prefix.count(")"):
            _emit_text_with_r3_and_subscripts(para, prefix + ":", FONT_HEADING, font_size, True, bold_prefix_color)
            target_str = rest
        else:
            target_str = text
    else:
        target_str = text

    _emit_text_with_r3_and_subscripts(para, target_str, FONT_BODY, font_size, False, color)


def add_r3_card(builder: ScientificDeckBuilder, slide, x: float, y: float, w: float, h: float,
                title: str, items: list, accent: RGBColor = SUAI_BLUE, font_size: int = 12):
    """Карточка контента с поддержкой подсветки аббревиатур R3 (#005AAA bold)."""
    card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(x), Inches(y), Inches(w), Inches(h))
    card.fill.solid()
    card.fill.fore_color.rgb = CARD_WHITE
    card.line.color.rgb = BORDER_GRAY
    card.line.width = Pt(1.0)
    card.adjustments[0] = 0.02

    stripe = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(x), Inches(y + 0.06), Inches(0.08), Inches(h - 0.12))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = accent
    stripe.line.fill.background()

    tb = slide.shapes.add_textbox(Inches(x + 0.20), Inches(y + 0.08), Inches(w - 0.30), Inches(h - 0.14))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0

    p0 = tf.paragraphs[0]
    p0.space_after = Pt(4)
    format_para_with_r3(p0, title, font_size=font_size + 1, color=accent, bold_prefix_color=accent)
    for r in p0.runs:
        r.font.bold = True

    for item in items:
        p = tf.add_paragraph()
        p.space_after = Pt(3)
        format_para_with_r3(p, "• " + item, font_size=font_size, color=TEXT_DARK, bold_prefix_color=SUAI_NAVY)


def add_section_divider_l4(builder: ScientificDeckBuilder, sec_label: str, title: str,
                           problem_stmt: str, pills: str, takeaway: str, problem_ids: list):
    """Темно-синий слайд-разделитель раздела (#002C5F, Layout S) с векторными иконками проблем и строгим вертикальным зазором >= 0.15\"."""
    slide = builder.prs.slides.add_slide(builder.blank_layout)
    bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.5))
    bg.fill.solid()
    bg.fill.fore_color.rgb = SUAI_NAVY
    bg.line.fill.background()

    top_str = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.09))
    top_str.fill.solid()
    top_str.fill.fore_color.rgb = SUAI_CYAN
    top_str.line.fill.background()

    # Иконки проблем наверху по центру (y = 0.45..1.20)
    n_ic = len(problem_ids)
    total_w = n_ic * 0.76 + (n_ic - 1) * 0.24
    start_x = (13.333 - total_w) / 2.0
    for idx, pid in enumerate(problem_ids):
        draw_l4_problem_icon(slide, start_x + idx * 1.00, 0.42, 0.76, pid, SUAI_CYAN)

    # Надзаголовок РАЗДЕЛ X (y = 1.42..1.80)
    tb_sec = slide.shapes.add_textbox(Inches(1.2), Inches(1.42), Inches(10.933), Inches(0.38))
    tf_sec = tb_sec.text_frame
    tf_sec.word_wrap = True
    p_sec = tf_sec.paragraphs[0]
    p_sec.text = sec_label
    p_sec.alignment = PP_ALIGN.CENTER
    p_sec.font.name = FONT_HEADING
    p_sec.font.size = Pt(14)
    p_sec.font.bold = True
    p_sec.font.color.rgb = SUAI_CYAN

    # Заголовок раздела (y = 2.00..3.05)
    tb_t = slide.shapes.add_textbox(Inches(1.0), Inches(2.00), Inches(11.333), Inches(1.05))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = FONT_HEADING
    p_t.font.size = Pt(28)
    p_t.font.bold = True
    p_t.font.color.rgb = CARD_WHITE

    # Центрированная карточка проблемы (y = 3.30..4.95)
    p_card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(3.30), Inches(10.733), Inches(1.60))
    p_card.fill.solid()
    p_card.fill.fore_color.rgb = RGBColor(0x07, 0x3B, 0x7A)
    p_card.line.color.rgb = SUAI_CYAN
    p_card.line.width = Pt(1.5)
    p_card.adjustments[0] = 0.04

    tb_p = slide.shapes.add_textbox(Inches(1.55), Inches(3.44), Inches(10.233), Inches(1.32))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    p_prob = tf_p.paragraphs[0]
    p_prob.text = problem_stmt
    p_prob.alignment = PP_ALIGN.CENTER
    p_prob.font.name = FONT_BODY
    p_prob.font.size = Pt(16)
    p_prob.font.bold = False
    p_prob.font.color.rgb = CARD_WHITE

    # Навигационные плашки этапов (4 отдельные плашки в ряд без переполнения границ, y = 5.16..5.72)
    pill_items = [s.strip() for s in re.split(r'\s+→\s+', pills) if s.strip()]
    n_p = max(1, len(pill_items))
    gap_p = 0.22
    total_pw = 11.433
    w_p = (total_pw - gap_p * (n_p - 1)) / n_p
    x0_p = (13.333 - total_pw) / 2.0
    for idx_p, p_item in enumerate(pill_items):
        px = x0_p + idx_p * (w_p + gap_p)
        pill_box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(5.16), Inches(w_p), Inches(0.54))
        pill_box.fill.solid()
        pill_box.fill.fore_color.rgb = RGBColor(0x04, 0x22, 0x48)
        pill_box.line.color.rgb = RGBColor(0x38, 0xBD, 0xF8)
        pill_box.line.width = Pt(1.2)
        pill_box.adjustments[0] = 0.22
        tf_pl = pill_box.text_frame
        tf_pl.word_wrap = True
        tf_pl.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf_pl.margin_left = tf_pl.margin_right = Inches(0.08)
        tf_pl.margin_top = tf_pl.margin_bottom = Inches(0.04)
        p_pl = tf_pl.paragraphs[0]
        p_pl.alignment = PP_ALIGN.CENTER
        step_str = f"{idx_p + 1}. {p_item}"
        _emit_segment_with_subscripts(p_pl, step_str, FONT_HEADING, 11.0, True, SUAI_CYAN)

    # Нижний вывод (y = 6.00..6.55)
    tb_tk = slide.shapes.add_textbox(Inches(1.3), Inches(6.00), Inches(10.733), Inches(0.50))
    tf_tk = tb_tk.text_frame
    tf_tk.word_wrap = True
    p_tk = tf_tk.paragraphs[0]
    p_tk.text = "Инженерная цель: " + takeaway
    p_tk.alignment = PP_ALIGN.CENTER
    p_tk.font.name = FONT_BODY
    p_tk.font.size = Pt(13)
    p_tk.font.bold = True
    p_tk.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

    # Футер (y = 7.05)
    builder.slide_Counter += 1
    tb_f = slide.shapes.add_textbox(Inches(0.6), Inches(7.05), Inches(12.133), Inches(0.30))
    tf_f = tb_f.text_frame
    p_f = tf_f.paragraphs[0]
    p_f.text = f"{builder.lecture_title}   |   Слайд {builder.slide_Counter} из {builder.total_slides}"
    p_f.alignment = PP_ALIGN.RIGHT
    p_f.font.name = FONT_BODY
    p_f.font.size = Pt(9.5)
    p_f.font.color.rgb = RGBColor(0x94, 0xA3, 0xB8)
    return slide


def build_deck():
    builder = ScientificDeckBuilder(
        lecture_title="Лекция 4. Поверхностные явления и механизмы роста плёнок",
        total_slides=24
    )
    builder.draw_problem_icon = draw_l4_problem_icon

    # =========================================================================
    # СЛАЙД 1: Титульный слайд (Single-Point Occurrence реквизитов ГУАП/кафедры/лектора)
    # =========================================================================
    s1 = builder.new_slide()
    stripe = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.14))
    stripe.fill.solid()
    stripe.fill.fore_color.rgb = SUAI_NAVY
    stripe.line.fill.background()

    if os.path.exists(LOGO_PATH):
        s1.shapes.add_picture(LOGO_PATH, Inches(0.65), Inches(0.46), height=Inches(0.58))

    tb_uni = s1.shapes.add_textbox(Inches(2.95), Inches(0.42), Inches(9.73), Inches(0.82))
    tf_uni = tb_uni.text_frame
    tf_uni.word_wrap = True
    p_u1 = tf_uni.paragraphs[0]
    p_u1.text = "Санкт-Петербургский государственный университет аэрокосмического приборостроения (ГУАП)"
    p_u1.font.name = FONT_HEADING
    p_u1.font.size = Pt(14)
    p_u1.font.bold = True
    p_u1.font.color.rgb = SUAI_NAVY
    p_u2 = tf_uni.add_paragraph()
    p_u2.text = "Кафедра №3   |   Дисциплина: «Физические основы нанотехнологий» (4 семестр)"
    p_u2.font.name = FONT_BODY
    p_u2.font.size = Pt(12.5)
    p_u2.font.bold = True
    p_u2.font.color.rgb = SUAI_BLUE

    # Главный баннер названия лекции
    hero = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.65), Inches(1.48), Inches(12.033), Inches(2.35))
    hero.fill.solid()
    hero.fill.fore_color.rgb = SUAI_NAVY
    hero.line.color.rgb = SUAI_BLUE
    hero.line.width = Pt(1.5)
    hero.adjustments[0] = 0.03

    tb_h = s1.shapes.add_textbox(Inches(0.95), Inches(1.65), Inches(11.433), Inches(2.00))
    tf_h = tb_h.text_frame
    tf_h.word_wrap = True
    p_h0 = tf_h.paragraphs[0]
    p_h0.text = "ЛЕКЦИЯ №4   •   РАЗДЕЛ 2 «ОСОБЕННОСТИ ТЕРМОДИНАМИКИ НАНОСТРУКТУР» (ЧАСТЬ 3 ИЗ 4)"
    p_h0.font.name = FONT_HEADING
    p_h0.font.size = Pt(13)
    p_h0.font.bold = True
    p_h0.font.color.rgb = SUAI_CYAN
    p_h0.space_after = Pt(8)

    p_h1 = tf_h.add_paragraph()
    p_h1.text = "Поверхностные явления и механизмы роста плёнок"
    p_h1.font.name = FONT_HEADING
    p_h1.font.size = Pt(31)
    p_h1.font.bold = True
    p_h1.font.color.rgb = CARD_WHITE
    p_h1.space_after = Pt(8)

    p_h2 = tf_h.add_paragraph()
    p_h2.text = "От межфазной энергии Гиббса и капиллярности Лапласа – Кельвина к гетероэпитаксии и методу Брунауэра – Эммета – Теллера (БЭТ)"
    p_h2.font.name = FONT_BODY
    p_h2.font.size = Pt(14.5)
    p_h2.font.color.rgb = RGBColor(0xE2, 0xE8, 0xF0)

    # Карточки места в курсе и лектора
    add_r3_card(
        builder, s1, 0.65, 4.08, 7.65, 2.55,
        "Место лекции в архитектуре курса:",
        [
            "Логическое продолжение Лекции №3 (коллоиды и поверхностно-активные вещества (ПАВ)): переход к твердотельным межфазным границам.",
            "Модельные системы: квантовые точки (КТ) InAs/GaAs в молекулярно-лучевой эпитаксии (МЛЭ), гетеропары AlGaAs/GaAs и мезопористый SiO₂.",
            "Фундамент для следующей темы курса — Лекции №5 «Кристаллографические дефекты и дислокации несоответствия»."
        ],
        accent=SUAI_BLUE, font_size=12
    )
    add_r3_card(
        builder, s1, 8.50, 4.08, 4.18, 2.55,
        "Лектор и регламент:",
        [
            "Лектор: доцент Попов Д.А.",
            "Кафедра №3 ГУАП, Санкт-Петербург.",
            "Формат: проблемно-ориентированная лекция (4 раздела, 24 слайда, 90 минут)."
        ],
        accent=ACCENT_GREEN, font_size=12
    )
    builder.slide_Counter = 1
    builder.add_footer(s1)

    # =========================================================================
    # СЛАЙД 2: Шесть технологических барьеров (Layout P)
    # =========================================================================
    s2 = builder.new_slide()
    builder.add_header(
        s2,
        "Шесть технологических вызовов инженерии поверхности",
        "Проблемная постановка лекции | От брака нанопленок к физическим законам"
    )
    problems_s2 = [
        ("P1", "1. Отслаивание и разрыв дорожек", "Стягивание наночернил в капли и деламинация покрытий при слабой работе адгезии Wa < Wc.", ACCENT_RED),
        ("P2", "2. Схлопывание нанопор (ΔP ~ 720 атм)", "Разрушение гелей и каркасов гигантским капиллярным давлением Лапласа при сушке.", ACCENT_ORANGE),
        ("P3", "3. Деградация квантовых точек", "Растворение малых КТ в пользу крупных (созревание Оствальда) и размытие спектра.", ACCENT_PURPLE),
        ("P4", "4. Островковый разрыв пленок", "Распад ультратонких пленок металлов на изолированные 3D-капли с потерей проводимости.", SUAI_BLUE),
        ("P5", "5. Предел литографии (< 20 нм)", "Потребность в безлитографической самоорганизации плотных массивов когерентных 3D КТ.", ACCENT_GREEN),
        ("P6", "6. Недоступность площади S_уд", "Невозможность измерить оптикой внутреннюю поверхность нанопорошков (до 1000 м²/г).", SUAI_NAVY),
    ]
    for idx, (pid, ptitle, pdesc, pcol) in enumerate(problems_s2):
        row = idx // 2
        col = idx % 2
        cx = 0.55 + col * 3.25
        cy = 1.62 + row * 1.50
        cw, ch = 3.12, 1.38
        c_sh = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(cy), Inches(cw), Inches(ch))
        c_sh.fill.solid()
        c_sh.fill.fore_color.rgb = CARD_WHITE
        c_sh.line.color.rgb = BORDER_GRAY
        c_sh.adjustments[0] = 0.04
        draw_l4_problem_icon(s2, cx + 0.10, cy + 0.12, 0.52, pid, pcol)

        tb_p = s2.shapes.add_textbox(Inches(cx + 0.70), Inches(cy + 0.08), Inches(cw - 0.78), Inches(ch - 0.14))
        tf_p = tb_p.text_frame
        tf_p.word_wrap = True
        tf_p.margin_left = tf_p.margin_right = tf_p.margin_top = tf_p.margin_bottom = 0
        pp0 = tf_p.paragraphs[0]
        pp0.space_after = Pt(2)
        format_para_with_r3(pp0, ptitle, font_size=11, color=pcol, bold_prefix_color=pcol)
        for r in pp0.runs:
            r.font.bold = True
        pp1 = tf_p.add_paragraph()
        format_para_with_r3(pp1, pdesc, font_size=10, color=TEXT_DARK)

    builder.add_figure(
        s2, os.path.join(FIG_DIR, "fig_02_problem_cases.png"),
        x=7.08, y=1.58, w=5.70, h=4.52,
        caption="Рис. 1. Микрофотографии атомно-силовой (АСМ), просвечивающей (ПЭМ) и сканирующей микроскопии (СЭМ)"
    )
    builder.add_takeaway_banner(
        s2, "Инженерный вывод: все шесть видов технологического брака управляются четырьмя законами термодинамики поверхности.",
        y=6.22, h=0.58
    )
    builder.add_footer(s2)

    # =========================================================================
    # СЛАЙД 3: Инженерный маршрут лекции (Layout Roadmap)
    # =========================================================================
    s3 = builder.new_slide()
    builder.add_header(
        s3,
        "Четыре рубежа преодоления межфазных барьеров наномасштаба",
        "Маршрутная карта лекции | Логика сквозного инженерного поиска"
    )
    add_r3_card(
        builder, s3, 0.55, 1.62, 5.25, 1.42,
        "Разделы 1–2: Смачивание и кривизна",
        [
            "Поверхностная энергия σ, работы Дюпре W_c и W_a, краевой угол Юнга θ и критерий растекания Гаркинса S ≥ 0.",
            "Давление Лапласа ΔP = 2σ/R, закон Кельвина, созревание Оствальда в КТ и порометрия Баррета – Джойнера – Халенды (BJH)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s3, 0.55, 3.16, 5.25, 1.42,
        "Раздел 3: Гетероэпитаксиальный рост",
        [
            "Критерий Бауэра Δσ, упругая деформация E_упр ∝ ε²h и дифракция быстрых электронов на отражение (ДБЭО / RHEED).",
            "Режимы Франка – ван дер Мерве (FM, 2D), Фольмера – Вебера (VW, 3D) и Странского – Крастанова (SK, 2D→3D КТ)."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    add_r3_card(
        builder, s3, 0.55, 4.70, 5.25, 1.38,
        "Раздел 4: Адсорбция и метрология БЭТ",
        [
            "Разграничение физисорбции (силы Ван-дер-Ваальса) и хемосорбции (ковалентный монослой).",
            "Изотерма Ленгмюра, теория БЭТ и классификация Международного союза теоретической и прикладной химии (ИЮПАК / IUPAC)."
        ],
        accent=ACCENT_PURPLE, font_size=11
    )
    builder.add_figure(
        s3, os.path.join(FIG_DIR, "fig_03_roadmap.png"),
        x=5.95, y=1.58, w=6.80, h=4.50,
        caption="Рис. 2. Структурно-логическая схема связи 4 разделов лекции"
    )
    builder.add_takeaway_banner(
        s3, "Ключевой тезис: термодинамика поверхности объединяет капиллярные, ростовые и сорбционные процессы в единый аппарат.",
        y=6.22, h=0.58
    )
    builder.add_footer(s3)

    # =========================================================================
    # СЛАЙД 4: РАЗДЕЛ 1 — Разделитель (Layout S, #002C5F)
    # =========================================================================
    add_section_divider_l4(
        builder,
        sec_label="РАЗДЕЛ 1   •   ПРОБЛЕМА №1",
        title="Термодинамика поверхности, когезия, адгезия и смачивание",
        problem_stmt="Наномасштабный контакт разнородных фаз определяется балансом сил притяжения: преобладание когезии вызывает отслаивание функциональных покрытий и распад печатных дорожек наночернил на изолированные капли.",
        pills="Поверхностное натяжение σ  →  Работы Wc и Wa Дюпре  →  Угол Юнга θ  →  Критерий Гаркинса S",
        takeaway="Управлять смачиванием и адгезией пленок через направленную модификацию поверхностной энергии.",
        problem_ids=["P1"]
    )

    # =========================================================================
    # СЛАЙД 5: Поверхностная свободная энергия, когезия и адгезия Дюпре
    # =========================================================================
    s5 = builder.new_slide()
    builder.add_header(
        s5,
        "Поверхностное натяжение, когезия и работа адгезии Дюпре",
        "Раздел 1. Микроскопическая природа и термодинамика межфазных границ",
        problem_id="P1"
    )
    add_r3_card(
        builder, s5, 0.55, 1.62, 5.55, 1.45,
        "1. Микроскопическая причина и определение Гиббса:",
        [
            "Координационный дефицит на поверхности (Zs < Zb) порождает нескомпенсированную силу притяжения внутрь объема.",
            "Удельная поверхностная энергия: σ = (∂G / ∂A)_{T,P,N} [Дж/м² ≡ Н/м] — обратимая работа создания 1 м² поверхности."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s5, 0.55, 3.18, 5.55, 1.40,
        "2. Работа когезии однородной фазы (W_c):",
        [
            "Разрыв единичного сечения однородной жидкости или кристалла рождает две идентичные поверхности площадью по 1 м².",
            "Формула когезии: W_c = 2σ_l (характеризует прочность внутренних связей материала)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s5, 0.55, 4.68, 5.55, 1.40,
        "3. Работа адгезии разнородных фаз (уравнение Дюпре):",
        [
            "При отрыве пленки от подложки исчезает межфазная граница σ_sl и возникают две свободные границы σ_s и σ_l.",
            "Уравнение А. Дюпре (1869): W_a = σ_s + σ_l − σ_sl (чем ниже межфазное натяжение σ_sl, тем прочнее сцепление)."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s5, os.path.join(FIG_DIR, "fig_05_surface_energy_dupre.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 3. Дефицит координации атомов поверхности (а) и схема работ W_c и W_a Дюпре (б)"
    )
    builder.add_takeaway_banner(
        s5, "Вывод: прочное сцепление нанопленки с подложкой достигается максимизацией W_a через снижение межфазной энергии σ_sl.",
        y=6.22, h=0.58
    )
    builder.add_footer(s5)

    # =========================================================================
    # СЛАЙД 6: Закон Юнга и критерий растекания Гаркинса
    # =========================================================================
    s6 = builder.new_slide()
    builder.add_header(
        s6,
        "Краевой угол смачивания Юнга и критерий растекания Гаркинса",
        "Раздел 1. Равновесие трехфазной линии контакта и режимы смачивания",
        problem_id="P1"
    )
    add_r3_card(
        builder, s6, 0.55, 1.62, 5.55, 1.45,
        "1. Уравнение Т. Юнга (1805):",
        [
            "Баланс горизонтальных проекций натяжений на линии трех фаз дает равновесный краевой угол θ.",
            "cos θ = (σ_s − σ_sl) / σ_l. При θ < 90° наблюдается смачивание (гидрофильность), при θ > 90° — несмачивание."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s6, 0.55, 3.18, 5.55, 1.40,
        "2. Объединенное уравнение Дюпре – Юнга:",
        [
            "Подстановка σ_s − σ_sl = σ_l·cos θ исключает неизмеримые энергии твердых границ.",
            "W_a = σ_l·(1 + cos θ) — прямое определение работы адгезии по оптическому измерению угла θ и натяжения жидкости σ_l."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    add_r3_card(
        builder, s6, 0.55, 4.68, 5.55, 1.40,
        "3. Коэффициент растекания У. Гаркинса (S):",
        [
            "Разность работ адгезии и когезии: S = Wa − Wc = σ_s − σ_l − σ_sl = σ_l·(cos θ − 1).",
            "При S ≥ 0 (Wa ≥ Wc, θ = 0°) капля спонтанно растекается в тонкую сплошную пленку."
        ],
        accent=ACCENT_RED, font_size=11
    )
    builder.add_figure(
        s6, os.path.join(FIG_DIR, "fig_06_young_harkins_droplet.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 4. Векторная диаграмма Юнга (а) и аналитические зависимости Wa и S Гаркинса от угла θ (б)"
    )
    builder.add_takeaway_banner(
        s6, "Вывод: конкуренция адгезии Wa и когезии Wc однозначно задает форму жидкой фазы — от сплошной пленки до сферы.",
        y=6.22, h=0.58
    )
    builder.add_footer(s6)

    # =========================================================================
    # СЛАЙД 7: Инженерия смачивания — O2-плазма и эффект лотоса
    # =========================================================================
    s7 = builder.new_slide()
    builder.add_header(
        s7,
        "Инженерия смачивания: от плазменной активации до эффекта лотоса",
        "Раздел 1. Практика управления краевым углом в нанотехнологиях",
        problem_id="P1"
    )
    add_r3_card(
        builder, s7, 0.55, 1.62, 5.55, 2.15,
        "Кейс 1. Кислородная плазма в печатной наноэлектронике:",
        [
            "На необработанном полиимиде серебряные наночернила (Ag) имеют угол θ ≈ 65°, что ведет к разрыву проводящих дорожек.",
            "Обработка в O₂-плазме прививает полярные группы −OH и −COOH, повышая энергию подложки σ_s.",
            "Результат: скачкообразное снижение угла θ с 65° до 15° (S → 0) и формирование бездефектных шин."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s7, 0.55, 3.92, 5.55, 2.15,
        "Кейс 2. Супергидрофобность Касси – Бакстера (эффект лотоса):",
        [
            "Массив гидрофобных кремниевых наностолбиков удерживает воздушные карманы под каплей воды.",
            "Уравнение Касси – Бакстера: cos θ* = f_s·(cos θ + 1) − 1, где f_s ≪ 1 — доля площади вершин нанорельефа.",
            "При f_s ≈ 0.08 кажущийся угол достигает θ* > 160°: капля скатывается, обеспечивая самоочищение."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s7, os.path.join(FIG_DIR, "fig_07_wetting_engineering_lotus.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 5. Растекание Ag-наночернил после O₂-плазмы (а) и супергидрофобный режим Касси – Бакстера (б)"
    )
    builder.add_takeaway_banner(
        s7, "Инженерный итог Раздела 1: плазменная химия и нанотекстурирование позволяют менять угол смачивания от 0° до 165°.",
        y=6.22, h=0.58
    )
    builder.add_footer(s7)

    # =========================================================================
    # СЛАЙД 8: РАЗДЕЛ 2 — Разделитель (Layout S, #002C5F)
    # =========================================================================
    add_section_divider_l4(
        builder,
        sec_label="РАЗДЕЛ 2   •   ПРОБЛЕМЫ №2 и №3",
        title="Кривизна поверхности в наномасштабе: законы Лапласа и Кельвина",
        problem_stmt="Искривление границы раздела в наномасштабе порождает мегапаскальные скачки давления и смещает фазовое равновесие: малые квантовые точки спонтанно растворяются в пользу крупных, а нанопоры заполняются жидкостью задолго до насыщения пара.",
        pills="Давление Лапласа ΔP = 2σ/R  →  Уравнение Кельвина  →  Созревание Оствальда  →  Конденсация и BJH",
        takeaway="Подавить деградацию ансамблей квантовых точек и использовать капиллярную конденсацию для порометрии.",
        problem_ids=["P2", "P3"]
    )

    # =========================================================================
    # СЛАЙД 9: Капиллярное давление Лапласа
    # =========================================================================
    s9 = builder.new_slide()
    builder.add_header(
        s9,
        "Капиллярное давление Лапласа: мегапаскали внутри наноструктур",
        "Раздел 2. Механика искривленных межфазных границ в наномасштабе",
        problem_id="P2"
    )
    add_r3_card(
        builder, s9, 0.55, 1.62, 5.55, 1.45,
        "1. Уравнение Юнга – Лапласа (1805):",
        [
            "Искривленная межфазная граница оказывает добавочное давление, направленное к центру кривизны:",
            "ΔP_L = σ·(1/R₁ + 1/R₂). Для сферической капли или поры радиуса R: ΔP_L = 2σ / R."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s9, 0.55, 3.18, 5.55, 1.40,
        "2. Численный масштаб в наномире:",
        [
            "При переходе к нанометровым радиусам множитель 1/R взрывным образом увеличивает давление.",
            "Для воды (σ = 72.8 мН/м) при R = 2 нм: ΔP_L = 72.8 МПа ≈ 720 атм (сжатие решетки и схлопывание гелей)."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s9, 0.55, 4.68, 5.55, 1.40,
        "3. Знак кривизны мениска в нанопоре:",
        [
            "Выпуклая нанокапля (R > 0): избыточное сжатие внутри фазы (+2σ/R).",
            "Вогнутый мениск в смачиваемом капилляре (θ < 90°): ΔP_L = −2σ·cos θ / r_п < 0 (капиллярное всасывание)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    builder.add_figure(
        s9, os.path.join(FIG_DIR, "fig_09_laplace_pressure_meniscus.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 6. Гиперболический рост капиллярного давления Лапласа ΔP_L(R) при R → 2 нм"
    )
    builder.add_takeaway_banner(
        s9, "Вывод: давление Лапласа масштабируется как 1/R, создавая сотни атмосфер в наночастицах и мезопорах.",
        y=6.22, h=0.58
    )
    builder.add_footer(s9)

    # =========================================================================
    # СЛАЙД 10: Уравнение Кельвина и созревание Оствальда
    # =========================================================================
    s10 = builder.new_slide()
    builder.add_header(
        s10,
        "Уравнение Кельвина и термодинамика созревания Оствальда",
        "Раздел 2. Сдвиг химического потенциала и деградация наноансамблей",
        problem_id="P3"
    )
    add_r3_card(
        builder, s10, 0.55, 1.62, 5.55, 1.45,
        "1. Сдвиг химического потенциала:",
        [
            "Лапласовское сжатие увеличивает химический потенциал малых частиц: Δμ = V_m·ΔP_L = ±2σ·V_m / r.",
            "Уравнение У. Томсона (Кельвина): ln(P_r / P_∞) = ln(C_r / C_∞) = ±2σ·V_m / (r·R_g·T)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s10, 0.55, 3.18, 5.55, 1.40,
        "2. Механизм созревания Оствальда (1896):",
        [
            "Малые наночастицы (r₁) обладают повышенной растворимостью C(r₁) > C(r₂) и непрерывно растворяются.",
            "Диффузионный поток мономеров питает рост крупных частиц (r₂ ≫ r₁), снижая суммарную площадь границ."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s10, 0.55, 4.68, 5.55, 1.40,
        "3. Угроза для квантовых точек (КТ):",
        [
            "Размытие распределения КТ по размерам вызывает красный сдвиг и уширение пика фотолюминесценции.",
            "Снижение температуры расплава T_пл(r) наночастиц золота (с 1064 °C до < 400 °C при r ≈ 1.5 нм)."
        ],
        accent=ACCENT_ORANGE, font_size=11
    )
    builder.add_figure(
        s10, os.path.join(FIG_DIR, "fig_10_kelvin_ostwald_ripening.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 7. Экспоненциальные ветви закона Кельвина (а) и схема переноса массы при созревании Оствальда (б)"
    )
    builder.add_takeaway_banner(
        s10, "Вывод: экспоненциальный рост химпотенциала малых частиц является фундаментальной причиной их нестабильности.",
        y=6.22, h=0.58
    )
    builder.add_footer(s10)

    # =========================================================================
    # СЛАЙД 11: Капиллярная конденсация и гистерезис
    # =========================================================================
    s11 = builder.new_slide()
    builder.add_header(
        s11,
        "Капиллярная конденсация и петля сорбционного гистерезиса",
        "Раздел 2. Фазовые переходы газ — жидкость в мезопористых средах",
        problem_id="P2"
    )
    add_r3_card(
        builder, s11, 0.55, 1.62, 5.55, 1.45,
        "1. Конденсация при давлении ниже насыщения (P_r < P_0):",
        [
            "Над вогнутым мениском (r < 0) показатель экспоненты Кельвина отрицателен: P_r = P_0·exp(−2σV_m / rRT) < P_0.",
            "Пар спонтанно конденсируется в жидкость внутри мезопор (2–50 нм) задолго до достижения P_0."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s11, 0.55, 3.18, 5.55, 1.40,
        "2. Геометрическая причина петли гистерезиса:",
        [
            "При адсорбции газ сжижается на цилиндрической пленке стенок поры со средней кривизной 1/r_c.",
            "При десорбции испарение идет с вогнутого полусферического мениска устья с удвоенной кривизной 2/r_c."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s11, 0.55, 4.68, 5.55, 1.40,
        "3. Диагностика геометрии мезопор:",
        [
            "Удвоенная кривизна удерживает жидкость при меньшем давлении (P_дес < P_адс), формируя петлю типа IV.",
            "Форма петли гистерезиса однозначно различает цилиндрические каналы (SBA-15), щелевые и бутылкообразные поры."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s11, os.path.join(FIG_DIR, "fig_11_capillary_condensation.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 8. Изотерма сорбции IV типа с петлей капиллярного гистерезиса H1 для мезопористого кремнезема SBA-15"
    )
    builder.add_takeaway_banner(
        s11, "Вывод: капиллярный гистерезис связывает давление конденсации с радиусом каналов, лежа в основе порометрии.",
        y=6.22, h=0.58
    )
    builder.add_footer(s11)

    # =========================================================================
    # СЛАЙД 12: Практика — Термошок КТ и порометрия BJH
    # =========================================================================
    s12 = builder.new_slide()
    builder.add_header(
        s12,
        "Инженерная практика: стабилизация КТ и порометрия BJH",
        "Раздел 2. Применение законов Лапласа и Кельвина в синтезе и диагностике",
        problem_id="P3"
    )
    add_r3_card(
        builder, s12, 0.55, 1.62, 5.55, 2.15,
        "Кейс 1. Кинетическая заморозка КТ (Hot-Injection):",
        [
            "Впрыск холодного прекурсора в растворитель при 300 °C вызывает мгновенную взрывную нуклеацию зародышей CdSe.",
            "Экстренный сброс температуры до 220 °C (термошок) и пассивация олеиновой кислотой (ПАВ) снижают σ и диффузию.",
            "Созревание Оствальда блокируется: ансамбль КТ сохраняет разброс размеров σ_r < 5% и узкий пик свечения."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    add_r3_card(
        builder, s12, 0.55, 3.92, 5.55, 2.15,
        "Кейс 2. Метод порометрии BJH (Баррета – Джойнера – Халенды):",
        [
            "По ветви десорбции азота при 77 К каждому шагу давления P/P₀ сопоставляется кельвиновский радиус мениска r_K.",
            "Истинный радиус мезопоры учитывает толщину полимолекулярной пленки на стенках: r_p = r_K(P/P₀) + t(P/P₀).",
            "Дифференциальная кривая dV/d log D сертифицирует распределение мезопор катализаторов и мембран SBA-15."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    builder.add_figure(
        s12, os.path.join(FIG_DIR, "fig_12_qd_quenching_bjh.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 9. Температурный профиль синтеза КТ с термошоком (а) и распределение мезопор по размерам BJH (б)"
    )
    builder.add_takeaway_banner(
        s12, "Инженерный итог Раздела 2: закон Кельвина позволяет замораживать деградацию КТ и паспортизовать нанопоры BJH.",
        y=6.22, h=0.58
    )
    builder.add_footer(s12)

    # =========================================================================
    # СЛАЙД 13: РАЗДЕЛ 3 — Разделитель (Layout S, #002C5F)
    # =========================================================================
    add_section_divider_l4(
        builder,
        sec_label="РАЗДЕЛ 3   •   ПРОБЛЕМЫ №4 и №5",
        title="Термодинамическая классификация и механизмы роста тонких плёнок",
        problem_stmt="Прецизионное выращивание гетероструктур требует контроля морфологии: конкуренция свободных поверхностных энергий и накапливаемой упругой деформации решетки определяет, сформируется ли гладкий 2D-слой или массив 3D-островков.",
        pills="Критерий Бауэра Δσ и деформация ε  →  FM-рост (2D)  →  VW-рост (3D)  →  SK-рост (2D→3D КТ)",
        takeaway="Управлять переходом между послойным 2D-ростом и самоорганизацией 3D квантовых точек.",
        problem_ids=["P4", "P5"]
    )

    # =========================================================================
    # СЛАЙД 14: Критерий Бауэра и упругая энергия рассогласования
    # =========================================================================
    s14 = builder.new_slide()
    builder.add_header(
        s14,
        "Критерий Бауэра и упругая энергия несоответствия решеток",
        "Раздел 3. Термодинамический фундамент гетероэпитаксиального роста",
        problem_id="P4"
    )
    add_r3_card(
        builder, s14, 0.55, 1.62, 5.55, 1.45,
        "1. Термодинамический критерий Э. Бауэра (1958):",
        [
            "Знак изменения поверхностной свободной энергии при покрытии подложки пленкой: Δσ = σ_f + σ_i − σ_s.",
            "Связь с параметром Гаркинса: Δσ = −S. При Δσ ≤ 0 выгодно смачивание (2D), при Δσ > 0 — 3D-островки."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s14, 0.55, 3.18, 5.55, 1.40,
        "2. Параметр рассогласования решеток и упругая энергия:",
        [
            "Относительное несоответствие периодов пленки и подложки: ε = (a_f − a_s) / a_s.",
            "Упругая энергия псевдоморфного слоя растет линейно с толщиной h и квадратично с деформацией: E_упр(h) = Y·ε²·h."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s14, 0.55, 4.68, 5.55, 1.40,
        "3. Три фундаментальных режима гетероэпитаксии:",
        [
            "FM (Франк – ван дер Мерве, 2D): Δσ ≤ 0 и ε ≈ 0;  VW (Фольмер – Вебер, 3D): Δσ > 0 с первого монослоя.",
            "SK (Странский – Крастанов, 2D → 3D): Δσ ≤ 0, но |ε| = 1–8% вызывает срыв в 3D-островки при h > h_c."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    builder.add_figure(
        s14, os.path.join(FIG_DIR, "fig_14_bauer_strain_tree.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 10. Дерево режимов роста по Бауэру (а) и линейное накопление упругой энергии E_упр(h) (б)"
    )
    builder.add_takeaway_banner(
        s14, "Вывод: конкуренция поверхностного выигрыша Δσ и упругой энергии E_упр(h) диктует сценарий роста пленки.",
        y=6.22, h=0.58
    )
    builder.add_footer(s14)

    # =========================================================================
    # СЛАЙД 15: Послойный 2D-рост Франка – ван дер Мерве (FM) и ДБЭО (RHEED)
    # =========================================================================
    s15 = builder.new_slide()
    builder.add_header(
        s15,
        "Послойный 2D-рост Франка — ван дер Мерве и контроль ДБЭО",
        "Раздел 3. Механизм послойного роста Франка — ван дер Мерве (FM-рост)",
        problem_id="P4"
    )
    add_r3_card(
        builder, s15, 0.55, 1.62, 5.55, 1.45,
        "1. Условия идеального 2D послойного роста:",
        [
            "Выполняется полное смачивание подложки (Δσ ≤ 0) при исчезающе малом рассогласовании решеток (ε → 0).",
            "Адатомы формируют двумерные зародыши высотой в 1 монослой (МС); новый слой не растет, пока не заполнен предыдущий."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    add_r3_card(
        builder, s15, 0.55, 3.18, 5.55, 1.40,
        "2. Мониторинг in situ методом ДБЭО (RHEED):",
        [
            "При молекулярно-лучевой эпитаксии (МЛЭ) скользящий пучок электронов отражается от растущей грани.",
            "Максимум интенсивности соответствует гладкой грани (θ = 1 МС), минимум — рассеянию при θ = 0.5 МС (1 период = 1 МС)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s15, 0.55, 4.68, 5.55, 1.40,
        "3. Эталонная система наноэлектроники:",
        [
            "Гетеропара Al_xGa_{1−x}As / GaAs (001) с рассогласованием решеток менее ε = 0.04%.",
            "Атомарно-гладкая граница формирует двумерный электронный газ (ДЭГ) для транзисторов с высокой подвижностью электронов (HEMT)."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    builder.add_figure(
        s15, os.path.join(FIG_DIR, "fig_15_fm_growth_rheed.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 11. Схема заполнения монослоя FM и осцилляции интенсивности зеркального рефлекса ДБЭО (RHEED)"
    )
    builder.add_takeaway_banner(
        s15, "Вывод: режим FM и счет периодов ДБЭО обеспечивают субмонослойную точность сборки гетероструктур HEMT.",
        y=6.22, h=0.58
    )
    builder.add_footer(s15)

    # =========================================================================
    # СЛАЙД 16: Островковый 3D-рост Фольмера – Вебера (VW)
    # =========================================================================
    s16 = builder.new_slide()
    builder.add_header(
        s16,
        "Островковый 3D-рост Фольмера — Вебера и порог перколяции",
        "Раздел 3. Механизм островкового роста Фольмера — Вебера (VW-рост)",
        problem_id="P4"
    )
    add_r3_card(
        builder, s16, 0.55, 1.62, 5.55, 1.45,
        "1. Термодинамическое условие несмачивания (Δσ > 0):",
        [
            "Энергия когезии атомов пленки превышает работу адгезии к подложке: σ_f + σ_i > σ_s (Wa < Wc).",
            "Адатомы собираются в трехмерные купола прямо на обнаженной подложке, минимизируя площадь контакта."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s16, 0.55, 3.18, 5.55, 1.40,
        "2. Три стадии эволюции и порог перколяции:",
        [
            "Нуклеация изолированных 3D-островков → их разрастание → коалесценция (слияние) с образованием границ зерен.",
            "До порога перколяции (h < 10–15 нм для Au, Ag на SiO₂) пленка остается диэлектрически разорванной (R_s → ∞)."
        ],
        accent=ACCENT_ORANGE, font_size=11
    )
    add_r3_card(
        builder, s16, 0.55, 4.68, 5.55, 1.40,
        "3. Инженерное управление режимом VW:",
        [
            "Для сплошных электродов Au на SiO₂ напыляют адгезионный подслой Ti или Cr (1–2 нм), меняющий знак Δσ на ≤ 0.",
            "В гетерогенном катализе (Pt, Pd на Al₂O₃) режим VW используют целенаправленно для синтеза 3D-нанокластеров."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    builder.add_figure(
        s16, os.path.join(FIG_DIR, "fig_16_vw_island_coalescence.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 12. Стадии коалесценции 3D-островков VW (а) и перколяционный скачок сопротивления R_s(h) (б)"
    )
    builder.add_takeaway_banner(
        s16, "Вывод: режим VW препятствует созданию ультратонких контактов, но идеален для синтеза каталитических нанокластеров.",
        y=6.22, h=0.58
    )
    builder.add_footer(s16)

    # =========================================================================
    # СЛАЙД 17: Послойно-островковый рост Странского – Крастанова (SK)
    # =========================================================================
    s17 = builder.new_slide()
    builder.add_header(
        s17,
        "Рост Странского — Крастанова: самоорганизация квантовых точек",
        "Раздел 3. Механизм Странского — Крастанова (SK-рост, 2D → 3D)",
        problem_id="P5"
    )
    add_r3_card(
        builder, s17, 0.55, 1.62, 5.55, 1.45,
        "1. Двухэтапный гибридный сценарий (2D → 3D):",
        [
            "При Δσ ≤ 0 и умеренном рассогласовании решеток (|ε| = 1–8%) рост начинается послойно: формируется смачивающий 2D-слой.",
            "По мере роста толщины h упругая энергия сжатия E_упр ∝ ε²h линейно возрастает."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s17, 0.55, 3.18, 5.55, 1.40,
        "2. Критическая толщина и упругая 3D-релаксация:",
        [
            "При достижении порога h_c плоский слой теряет устойчивость: выигрыш от упругой релаксации вершин перекрывает цену граней.",
            "Без дислокаций несоответствия спонтанно формируется плотный массив когерентных 3D-пирамид на смачивающем слое."
        ],
        accent=ACCENT_RED, font_size=11
    )
    add_r3_card(
        builder, s17, 0.55, 4.68, 5.55, 1.40,
        "3. Эталонная система InAs / GaAs (001):",
        [
            "Рассогласование решеток ε = +7.2% задает критическую толщину перехода ровно h_c ≈ 1.7 МС.",
            "За секунды без литографии вырастает массив КТ (d ≈ 15–20 нм, 10¹⁰–10¹¹ см⁻²) для лазеров 1.3–1.55 мкм."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s17, os.path.join(FIG_DIR, "fig_17_sk_quantum_dots.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 13. Стадии перехода 2D → 3D в системе InAs/GaAs (а) и энергетическая развилка при h_c = 1.7 МС (б)"
    )
    builder.add_takeaway_banner(
        s17, "Вывод: упругая релаксация по механизму SK — главный промышленный метод безлитографического синтеза КТ.",
        y=6.22, h=0.58
    )
    builder.add_footer(s17)

    # =========================================================================
    # СЛАЙД 18: Сравнительная инженерная матрица FM, VW, SK (Layout C)
    # =========================================================================
    s18 = builder.new_slide()
    builder.add_header(
        s18,
        "Сравнительная матрица трех механизмов роста тонких пленок",
        "Раздел 3. Обобщение и правила технологического выбора в гетероэпитаксии",
        problem_id="P5"
    )
    rows_s18 = [
        ["Инженерный критерий", "Франк – ван дер Мерве (FM, 2D)", "Фольмер – Вебер (VW, 3D)", "Странский – Крастанов (SK, 2D→3D)"],
        ["Баланс энергий Бауэра Δσ", "Δσ ≤ 0 (W_a ≥ W_c, смачивание)", "Δσ > 0 (W_a < W_c, несмачивание)", "Δσ ≤ 0 на старте (смачивание)"],
        ["Рассогласование решеток ε", "ε ≈ 0 (< 0.1%, изопериодные)", "Любое (часто металл на оксиде)", "Умеренное (|ε| ≈ 1% – 8%)"],
        ["Эволюция морфологии", "Гладкие 2D-монослои с 1-го МС", "Сразу 3D-островки → коалесценция", "2D смачивающий слой → 3D-пирамиды"],
        ["Критическая особенность", "Осцилляции ДБЭО (1 период = 1 МС)", "Порог перколяции h_перк > 10–15 нм", "Порог перехода h_c ≈ 1.7 МС (InAs)"],
        ["Эталонные материалы", "AlGaAs / GaAs(001), Si / Si", "Au, Ag, Cu на SiO₂ и стекле", "InAs / GaAs(001), Ge / Si(001)"],
        ["Применение в наноприборах", "ДЭГ в СВЧ-транзисторах HEMT", "Катализаторы Pt/Al₂O₃, плазмоника", "Лазеры и однофотонные источники на КТ"]
    ]
    tbl_shape = s18.shapes.add_table(len(rows_s18), 4, Inches(0.55), Inches(1.62), Inches(12.233), Inches(4.42))
    tbl = tbl_shape.table
    col_widths = [2.45, 3.26, 3.26, 3.26]
    for c_idx, cw in enumerate(col_widths):
        tbl.columns[c_idx].width = Inches(cw)

    for r_idx, r_data in enumerate(rows_s18):
        for c_idx, val in enumerate(r_data):
            cell = tbl.cell(r_idx, c_idx)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            cell.fill.solid()
            if r_idx == 0:
                cell.fill.fore_color.rgb = SUAI_NAVY if c_idx == 0 else (ACCENT_GREEN if c_idx == 1 else (ACCENT_RED if c_idx == 2 else SUAI_BLUE))
            else:
                cell.fill.fore_color.rgb = CARD_WHITE if r_idx % 2 == 1 else RGBColor(0xF1, 0xF5, 0xF9)

            p = cell.text_frame.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c_idx == 0 else PP_ALIGN.CENTER
            if r_idx == 0:
                p.text = val
                p.font.name = FONT_HEADING
                p.font.size = Pt(11.5)
                p.font.bold = True
                p.font.color.rgb = CARD_WHITE
            else:
                format_para_with_r3(p, val, font_size=10.5, color=TEXT_DARK, bold_prefix_color=SUAI_NAVY)
                if c_idx == 0:
                    for r in p.runs:
                        r.font.bold = True
                        r.font.color.rgb = SUAI_NAVY

    builder.add_takeaway_banner(
        s18, "Инженерный итог Раздела 3: выбор подложки, буферного слоя и деформации ε позволяет переключать архитектуру нанопленки.",
        y=6.22, h=0.58
    )
    builder.add_footer(s18)

    # =========================================================================
    # СЛАЙД 19: РАЗДЕЛ 4 — Разделитель (Layout S, #002C5F)
    # =========================================================================
    add_section_divider_l4(
        builder,
        sec_label="РАЗДЕЛ 4   •   ПРОБЛЕМА №6",
        title="Адсорбция газов на наноматериалах: изотермы Ленгмюра и БЭТ",
        problem_stmt="Наноматериалы обладают колоссальной удельной площадью поверхности (до 1000 м²/г), на которой доминирует газообмен. Надежное проектирование наноустройств требует разграничения физисорбции и хемосорбции, а также точной метрологии площади по изотермам БЭТ.",
        pills="Физисорбция vs Хемосорбция  →  Модель Ленгмюра  →  Теория БЭТ  →  Золотой стандарт N₂ (77 К)",
        takeaway="Определять истинную площадь сложных наноструктур и управлять откликом газовых наносенсоров.",
        problem_ids=["P6"]
    )

    # =========================================================================
    # СЛАЙД 20: Физисорбция и хемосорбция (кривые Леннард-Джонса)
    # =========================================================================
    s20 = builder.new_slide()
    builder.add_header(
        s20,
        "Физисорбция и хемосорбция: силы Ван-дер-Ваальса против химической связи",
        "Раздел 4. Физико-химические основы сорбционных процессов",
        problem_id="P6"
    )
    add_r3_card(
        builder, s20, 0.55, 1.62, 5.55, 2.15,
        "1. Физическая адсорбция (физисорбция):",
        [
            "Природа сил: универсальные дисперсионные силы Ван-дер-Ваальса без перекрытия электронных оболочек (z₀ ≈ 0.35 нм).",
            "Энергетика: малая теплота ΔH ≈ 10–40 кДж/моль (сопоставима с теплотой конденсации пара E_L), барьер активации отсутствует.",
            "Свойства: полностью обратима, неспецифична и способна формировать полимолекулярные слои (основа порометрии БЭТ)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s20, 0.55, 3.92, 5.55, 2.15,
        "2. Химическая адсорбция (хемосорбция):",
        [
            "Природа сил: перенос электронов и образование прочной ковалентной или ионной связи с центром поверхности (z₀ ≈ 0.16 нм).",
            "Энергетика: высокая теплота реакции ΔH ≈ 80–400 кДж/моль; переход из прекурсора требует преодоления барьера E_акт.",
            "Свойства: избирательна и строго ограничена одним монослоем из-за насыщения валентностей (основа газовых сенсоров)."
        ],
        accent=ACCENT_RED, font_size=11
    )
    builder.add_figure(
        s20, os.path.join(FIG_DIR, "fig_20_adsorption_potentials.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 14. Одномерные потенциальные кривые Леннард-Джонса U(z) для физисорбции и активированной хемосорбции"
    )
    builder.add_takeaway_banner(
        s20, "Вывод: физисорбция обратима и полимолекулярна (метрология площади), а хемосорбция монослойна и селективна (сенсорика).",
        y=6.22, h=0.58
    )
    builder.add_footer(s20)

    # =========================================================================
    # СЛАЙД 21: Изотерма мономолекулярной адсорбции Ленгмюра
    # =========================================================================
    s21 = builder.new_slide()
    builder.add_header(
        s21,
        "Изотерма Ленгмюра: динамическое равновесие заполнения монослоя",
        "Раздел 4. Мономолекулярная адсорбция и хеморезистивные сенсоры",
        problem_id="P6"
    )
    add_r3_card(
        builder, s21, 0.55, 1.62, 5.55, 1.45,
        "1. Три постулата модели И. Ленгмюра (1916):",
        [
            "Поверхность содержит фиксированное число дискретных, энергетически эквивалентных центров адсорбции.",
            "Каждый центр удерживает ровно одну молекулу (емкость строго 1 монослой); латеральное взаимодействие отсутствует."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s21, 0.55, 3.18, 5.55, 1.40,
        "2. Кинетический вывод и предельные режимы:",
        [
            "Равенство скоростей v_адс = k_a·P(1 − θ) и v_дес = k_d·θ дает изотерму: θ = KP / (1 + KP), где K = k_a / k_d.",
            "Малые давления (KP ≪ 1): линейный закон Генри θ ≈ KP. Высокие давления (KP ≫ 1): плато насыщения θ → 1."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s21, 0.55, 4.68, 5.55, 1.40,
        "3. Линеаризация и принцип работы наносенсоров:",
        [
            "В координатах P/a = 1/(a_m·K) + P/a_m наклон прямой дает емкость монослоя a_m, а отсечка — константу равновесия K.",
            "Отклик проводимости пленок SnO₂ и ZnO на газы CO и NO₂ прямо пропорционален ленгмюровскому заполнению θ(P)."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s21, os.path.join(FIG_DIR, "fig_21_langmuir_isotherm.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 15. Семейство изотерм Ленгмюра θ(P) (а) и линейная анаморфоза P/a от P для расчета емкости монослоя (б)"
    )
    builder.add_takeaway_banner(
        s21, "Вывод: изотерма Ленгмюра связывает парциальное давление газа со степенью заполнения монослоя и сигналом наносенсора.",
        y=6.22, h=0.58
    )
    builder.add_footer(s21)

    # =========================================================================
    # СЛАЙД 22: Теория полимолекулярной адсорбции БЭТ
    # =========================================================================
    s22 = builder.new_slide()
    builder.add_header(
        s22,
        "Теория БЭТ: полимолекулярная конденсация на неоднородных центрах",
        "Раздел 4. Полимолекулярная сорбция Брунауэра — Эммета — Теллера",
        problem_id="P6"
    )
    add_r3_card(
        builder, s22, 0.55, 1.62, 5.55, 1.45,
        "1. Физические постулаты БЭТ (1938):",
        [
            "При низкотемпературной физисорбции молекулы образуют второй, третий и последующие слои до завершения первого.",
            "Теплота сорбции первого слоя равна E₁, а во всех вышележащих слоях равна теплоте конденсации чистого пара: E₂ = E₃ = E_L."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s22, 0.55, 3.18, 5.55, 1.45,
        "2. Линейное уравнение изотермы БЭТ:",
        [
            "Статистический баланс всех слоев дает линейную форму: P / [V(P₀ − P)] = 1/(V_m·C) + [(C − 1)/(V_m·C)]·(P/P₀).",
            "Здесь V_m — объем плотного монослоя, а константа C ≈ exp[(E₁ − E_L)/RT] характеризует силу притяжения к подложке."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s22, 0.55, 4.72, 5.55, 1.36,
        "3. Рабочее окно линейности (P/P₀ = 0.05 – 0.35):",
        [
            "Ниже 0.05 сказывается энергетическая неоднородность дефектов, выше 0.35 начинается капиллярная конденсация в порах.",
            "В окне 0.05–0.35 график дает строгую прямую линию y = A + B·(P/P₀), из которой находят V_m = 1 / (A + B)."
        ],
        accent=ACCENT_GREEN, font_size=11
    )
    builder.add_figure(
        s22, os.path.join(FIG_DIR, "fig_22_bet_multilayer_linear.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 16. Полимолекулярные изотермы БЭТ при различных константах C (а) и линейный график в окне 0.05–0.35 (б)"
    )
    builder.add_takeaway_banner(
        s22, "Вывод: теория БЭТ снимает монослойное ограничение Ленгмюра, позволяя точно извлекать емкость монослоя V_m.",
        y=6.22, h=0.58
    )
    builder.add_footer(s22)

    # =========================================================================
    # СЛАЙД 23: Метрология удельной поверхности БЭТ (N2, 77 K) и ИЮПАК
    # =========================================================================
    s23 = builder.new_slide()
    builder.add_header(
        s23,
        "Метрология наноматериалов: расчет S_уд по стандарту БЭТ (N₂, 77 K)",
        "Раздел 4. Практика применения адсорбционного анализа и классификация ИЮПАК",
        problem_id="P6"
    )
    add_r3_card(
        builder, s23, 0.55, 1.62, 5.55, 1.45,
        "1. Протокол золотого стандарта (Азот, T = 77.3 К):",
        [
            "Вакуумная дегазация навески массой m → охлаждение в жидком азоте (77.3 К) → съемка точек в окне P/P₀ = 0.05–0.35.",
            "Из наклона B и отсечки A прямой БЭТ вычисляют объем монослоя: V_m = 1 / (A + B) [см³/г при НТУ]."
        ],
        accent=SUAI_NAVY, font_size=11
    )
    add_r3_card(
        builder, s23, 0.55, 3.18, 5.55, 1.45,
        "2. Расчет удельной площади поверхности (S_уд):",
        [
            "Посадочная площадка молекулы азота равна σ₀ = 0.162 нм² = 16.2 Å²; молярный объем газа V₀ = 22414 см³/моль.",
            "Формула сертификации: S_уд = (V_m·N_A·σ₀) / (V₀·m) ≈ 4.35·V_m [м²/г] (графен — до 2630 м²/г, SBA-15 — до 1000 м²/г)."
        ],
        accent=SUAI_BLUE, font_size=11
    )
    add_r3_card(
        builder, s23, 0.55, 4.72, 5.55, 1.36,
        "3. Шесть типов изотерм по классификации ИЮПАК (IUPAC):",
        [
            "Тип I — микропоры цеолитов (< 2 нм); Тип II — непористые нанопорошки; Тип IV — мезопоры (2–50 нм) с петлей гистерезиса.",
            "Типы III и V — слабое притяжение (C ≤ 2); Тип VI — послойная ступенчатая адсорбция на атомарно-гладком графене."
        ],
        accent=ACCENT_PURPLE, font_size=11
    )
    builder.add_figure(
        s23, os.path.join(FIG_DIR, "fig_23_iupac_isotherms.png"),
        x=6.25, y=1.58, w=6.50, h=4.50,
        caption="Рис. 17. Матрица 6 канонических типов изотерм адсорбции по классификации ИЮПАК (IUPAC)"
    )
    builder.add_takeaway_banner(
        s23, "Инженерный итог Раздела 4: метод БЭТ по сорбции N₂ при 77 К — мировой эталон паспортизации площади наноматериалов.",
        y=6.22, h=0.58
    )
    builder.add_footer(s23)

    # =========================================================================
    # СЛАЙД 24: Итоговая инженерная матрица решений и анонс Лекции №5
    # =========================================================================
    s24 = builder.new_slide()
    builder.add_header(
        s24,
        "Инженерная матрица решений: от натяжения связей к нанотехнологиям",
        "Заключение и интеграция | Преодоление 6 барьеров и мост к Разделу 2 курса"
    )
    summary_items = [
        ("P1", "Барьер 1 (Отслаивание и капли)", "Формула Дюпре – Юнга W_a = σ_l(1+cos θ), параметр Гаркинса S ≥ 0 и O₂-плазменная активация (θ: 65° → 15°).", SUAI_BLUE),
        ("P2", "Барьер 2 (Схлопывание нанопор)", "Закон Лапласа ΔP = 2σ/R (~720 атм при 2 нм), капиллярная конденсация и распределение мезопор методом BJH.", ACCENT_ORANGE),
        ("P3", "Барьер 3 (Созревание Оствальда)", "Уравнение Кельвина для химпотенциала малых КТ, термошок горячего впрыска (300 → 220 °C) и пассивация ПАВ.", ACCENT_RED),
        ("P4", "Барьер 4 (Разрыв тонких пленок)", "Критерий Бауэра Δσ ≤ 0 для 2D-роста FM (контроль ДБЭО / RHEED) и адгезионный подслой Ti/Cr для подавления VW.", ACCENT_GREEN),
        ("P5", "Барьер 5 (Предел литографии КТ)", "Самоорганизация когерентных 3D КТ InAs/GaAs по механизму Странского – Крастанова (SK) при h_c = 1.7 МС.", ACCENT_PURPLE),
        ("P6", "Барьер 6 (Метрология площади S_уд)", "Изотерма Ленгмюра для наносенсоров и полимолекулярный стандарт БЭТ (N₂, 77 К) в окне P/P₀ = 0.05–0.35.", SUAI_NAVY),
    ]
    for idx, (pid, btitle, bsol, bcol) in enumerate(summary_items):
        row = idx // 2
        col = idx % 2
        cx = 0.55 + col * 6.18
        cy = 1.60 + row * 1.16
        cw, ch = 6.05, 1.06
        c_sh = s24.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(cy), Inches(cw), Inches(ch))
        c_sh.fill.solid()
        c_sh.fill.fore_color.rgb = CARD_WHITE
        c_sh.line.color.rgb = BORDER_GRAY
        c_sh.adjustments[0] = 0.04
        draw_l4_problem_icon(s24, cx + 0.10, cy + 0.14, 0.50, pid, bcol)

        tb_b = s24.shapes.add_textbox(Inches(cx + 0.68), Inches(cy + 0.06), Inches(cw - 0.76), Inches(ch - 0.12))
        tf_b = tb_b.text_frame
        tf_b.word_wrap = True
        tf_b.margin_left = tf_b.margin_right = tf_b.margin_top = tf_b.margin_bottom = 0
        pb0 = tf_b.paragraphs[0]
        pb0.space_after = Pt(2)
        format_para_with_r3(pb0, btitle + ":", font_size=11, color=bcol, bold_prefix_color=bcol)
        pb1 = tf_b.add_paragraph()
        format_para_with_r3(pb1, bsol, font_size=10, color=TEXT_DARK)

    # Мост к следующей лекции (y = 5.14..6.06)
    next_card = s24.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.55), Inches(5.14), Inches(12.233), Inches(0.92))
    next_card.fill.solid()
    next_card.fill.fore_color.rgb = RGBColor(0xEE, 0xF5, 0xFC)
    next_card.line.color.rgb = SUAI_BLUE
    next_card.line.width = Pt(1.5)
    next_card.adjustments[0] = 0.04

    tb_nx = s24.shapes.add_textbox(Inches(0.75), Inches(5.20), Inches(11.833), Inches(0.80))
    tf_nx = tb_nx.text_frame
    tf_nx.word_wrap = True
    pn0 = tf_nx.paragraphs[0]
    pn0.space_after = Pt(2)
    format_para_with_r3(pn0, "Анонс Лекции №5 (Раздел 2 «Структура и дефекты наноматериалов»):", font_size=11.5, color=SUAI_NAVY, bold_prefix_color=SUAI_NAVY)
    pn1 = tf_nx.add_paragraph()
    format_para_with_r3(
        pn1,
        "Что происходит при превышении второй критической толщины пленки: точечные и линейные дефекты, дислокации несоответствия, источники Франка – Рида и аномальный предел текучести Холла – Петча.",
        font_size=10.5, color=TEXT_DARK
    )

    builder.add_takeaway_banner(
        s24, "Генеральный вывод: поверхностная энергия в наномасштабе — главный инструмент направленной самоорганизации материи.",
        y=6.22, h=0.58
    )
    builder.add_footer(s24)

    # Встраивание 4-компонентных заметок докладчика (Speaker Notes) во все 24 слайда
    notes_map = parse_speech_notes(SPEECH_MD_PATH)
    for idx, slide in enumerate(builder.prs.slides, start=1):
        note_txt = notes_map.get(idx, f"1. Физический тезис: Слайд {idx}.\n2. Визуальные акценты.\n3. Инженерный контекст.\n4. Смысловой переход.")
        notes_slide = slide.notes_slide
        notes_slide.notes_text_frame.text = note_txt

    builder.save(OUT_PPTX)
    shutil.copyfile(OUT_PPTX, OUT_PPTX_ALT)
    print(f"Presentation saved to:\n  {OUT_PPTX}\n  {OUT_PPTX_ALT}")


if __name__ == "__main__":
    build_deck()
