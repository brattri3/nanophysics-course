"""
Базовый модульный конструктор академических презентаций (16:9) на базе python-pptx.
Позволяет быстро создать каркас лекции (слайды-заготовки) и наполнить их контентом и графикой.
"""

import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


# Академическая цветовая палитра
COLOR_NAVY = RGBColor(0, 51, 102)
COLOR_BLUE = RGBColor(0, 102, 204)
COLOR_DARK = RGBColor(34, 34, 34)
COLOR_MUTED = RGBColor(90, 105, 120)
COLOR_CARD_BG = RGBColor(244, 247, 250)
COLOR_CARD_BORDER = RGBColor(200, 215, 230)
COLOR_BANNER_BG = RGBColor(232, 242, 252)
COLOR_PLACEHOLDER_BG = RGBColor(250, 250, 252)
COLOR_WHITE = RGBColor(255, 255, 255)


def create_base_presentation() -> Presentation:
    """Создает пустую широкоформатную презентацию 16:9."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    return prs


def add_header(slide, title_text: str, subtitle_text: str = ""):
    """Добавляет стандартную шапку слайда с заголовком и акцентной линией."""
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.24), Inches(12.333), Inches(0.85))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.02)
    tf.margin_bottom = Inches(0.02)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.text = title_text
    p.font.name = "Arial"
    p.font.size = Pt(19.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY
    p.space_after = Pt(2)

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        p2.text = subtitle_text
        p2.font.name = "Arial"
        p2.font.size = Pt(12)
        p2.font.italic = True
        p2.font.color.rgb = COLOR_MUTED

    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.5), Inches(1.12), Inches(12.333), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = COLOR_BLUE
    line.line.fill.background()


def add_takeaway_banner(slide, takeaway_text: str):
    """Добавляет нижнюю плашку с ключевым выводом слайда."""
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.5), Inches(6.65), Inches(12.333), Inches(0.55)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = COLOR_BANNER_BG
    box.line.color.rgb = COLOR_BLUE
    box.line.width = Pt(1.2)

    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    p.text = f"Ключевой вывод: {takeaway_text}"
    p.font.name = "Arial"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = COLOR_NAVY


def add_content_card(slide, left: float, top: float, width: float, height: float,
                     heading: str, bullets: list[str]):
    """Добавляет карточку с заголовком и маркированным списком."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = COLOR_CARD_BG
    card.line.color.rgb = COLOR_CARD_BORDER
    card.line.width = Pt(1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.14)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    p0.text = heading
    p0.font.name = "Arial"
    p0.font.size = Pt(14)
    p0.font.bold = True
    p0.font.color.rgb = COLOR_NAVY
    p0.space_after = Pt(6)

    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.text = f"• {b}"
        p.font.name = "Arial"
        p.font.size = Pt(12)
        p.font.color.rgb = COLOR_DARK
        p.space_after = Pt(4)


def add_figure_or_placeholder(slide, left: float, top: float, width: float, height: float,
                              image_path: str = "", placeholder_desc: str = "Схема / График"):
    """Вставляет изображение с сохранением пропорций или рисует рамку-заготовку."""
    if image_path and os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(left), Inches(top), width=Inches(width))
    else:
        ph = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        ph.fill.solid()
        ph.fill.fore_color.rgb = COLOR_PLACEHOLDER_BG
        ph.line.color.rgb = COLOR_BLUE
        ph.line.width = Pt(1.5)
        tf = ph.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"[ЗАГОТОВКА ИЛЛЮСТРАЦИИ]\n\n{placeholder_desc}"
        p.font.name = "Arial"
        p.font.size = Pt(14)
        p.font.italic = True
        p.font.color.rgb = COLOR_MUTED


def set_speaker_notes(slide, notes_text: str):
    """Записывает методический текст в заметки докладчика."""
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text
