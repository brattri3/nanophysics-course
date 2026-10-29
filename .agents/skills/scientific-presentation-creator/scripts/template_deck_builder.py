"""
Базовый модульный конструктор академических презентаций (16:9) на базе python-pptx.
Стандарт дизайн-кода ГУАП (SUAI Design Code) для курса «Физические основы нанотехнологий».
Поддерживает Layout T (Титул), Layout P (Проблемный обзор), Layout S (Разделитель),
Layout C (Сравнительная матрица), Layout A (Двухколоночный) и Layout B (Полноширинный).
"""

import os
from typing import List, Dict, Optional, Tuple, Any

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml


# ==============================================================================
# 1. Фирменная палитра темы ГУАП (SUAI Theme Palette)
# ==============================================================================

SUAI_PALETTE = {
    # Корпоративные цвета
    "DEEP_NAVY": RGBColor(0, 44, 95),      # #002C5F (dk2) — основной темный, титулы, разделители
    "BLUE": RGBColor(0, 90, 170),          # #005AAA (accent1) — первичный акцент, подзаголовки, рамки
    "RED": RGBColor(231, 15, 71),          # #E70F47 (accent2) — сигнальный красный, Агрегация
    "CYAN": RGBColor(0, 190, 243),         # #00BEF3 (accent3) — небесно-голубой, Сепарация
    "PURPLE": RGBColor(146, 105, 201),     # #9269C9 (accent4) — фиолетовый, Транспорт/нанофлюидика
    "ORANGE": RGBColor(255, 100, 24),      # #FF6418 (accent5) — оранжевый, Хранение/старение
    "GREEN": RGBColor(0, 154, 73),         # #009A49 (accent6) — изумрудно-зеленый, Технологичность
    # Нейтральные тона
    "CHARCOAL": RGBColor(36, 40, 52),      # #242834 (dk1) — высококонтрастный текст
    "WHITE": RGBColor(255, 255, 255),      # #FFFFFF (lt1) — чистый белый фон
    "CARD_BG": RGBColor(244, 247, 250),    # #F4F7FA — заливка информационных карточек
    "CARD_BORDER": RGBColor(200, 215, 230),# #C8D7E6 — контур карточек
    "TAKEAWAY_BG": RGBColor(238, 244, 250),# #EEF4FA — пастельный серо-голубой фон вывода
    "MUTED_STEEL": RGBColor(90, 105, 120), # #5A6978 — примечания, трекеры, оси
}

# Обратная совместимость с предыдущими скриптами
COLOR_NAVY = SUAI_PALETTE["DEEP_NAVY"]
COLOR_BLUE = SUAI_PALETTE["BLUE"]
COLOR_DARK = SUAI_PALETTE["CHARCOAL"]
COLOR_MUTED = SUAI_PALETTE["MUTED_STEEL"]
COLOR_CARD_BG = SUAI_PALETTE["CARD_BG"]
COLOR_CARD_BORDER = SUAI_PALETTE["CARD_BORDER"]
COLOR_BANNER_BG = SUAI_PALETTE["TAKEAWAY_BG"]
COLOR_WHITE = SUAI_PALETTE["WHITE"]
COLOR_PLACEHOLDER_BG = RGBColor(250, 250, 252)


# ==============================================================================
# 2. Таксономия 6 иконок-маркеров технологических проблем
# ==============================================================================

PROBLEM_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "aggregation": {
        "title": "Агрегация / Слипание",
        "formula": "ΔGs = σ · S > 0",
        "description": "Ван-дер-ваальсово схлопывание незащищенных частиц в монолит",
        "color": SUAI_PALETTE["RED"],
        "hex": "E70F47",
        "file": "icon_aggregation.png",
        "tag": "[🔴🔗 АГРЕГАЦИЯ]",
    },
    "sedimentation": {
        "title": "Седиментация / Осадок",
        "formula": "v = 2 r² Δρ g / (9 η)",
        "description": "Гравитационное оседание агломератов по закону Стокса",
        "color": SUAI_PALETTE["DEEP_NAVY"],
        "hex": "002C5F",
        "file": "icon_sedimentation.png",
        "tag": "[⬇️⚗️ ОСАДОК]",
    },
    "storage": {
        "title": "Хранение / Старение",
        "formula": "Sr = S∞ exp(2σVm / rRT)",
        "description": "Созревание Оствальда и диффузионная коалесценция золей",
        "color": SUAI_PALETTE["ORANGE"],
        "hex": "FF6418",
        "file": "icon_storage.png",
        "tag": "[⏱️📦 ХРАНЕНИЕ]",
    },
    "transport": {
        "title": "Транспорт / Доставка",
        "formula": "ΔP = 8 η L Q / (π R⁴)",
        "description": "Сдвиговая коагуляция в потоке и сжатие ДЭС при высоком сдвиге",
        "color": SUAI_PALETTE["PURPLE"],
        "hex": "9269C9",
        "file": "icon_transport.png",
        "tag": "[🚚🚧 ТРАНСПОРТ]",
    },
    "separation": {
        "title": "Сепарация / Калибровка",
        "formula": "J = ΔP / [μ (Rm + Rp)]",
        "description": "Полидисперсность синтеза и забивание мембранных фильтров",
        "color": SUAI_PALETTE["CYAN"],
        "hex": "00BEF3",
        "file": "icon_separation.png",
        "tag": "[🔬🏁 СЕПАРАЦИЯ]",
    },
    "processability": {
        "title": "Технологичность",
        "formula": "σтг = σтж + σжг cos θ",
        "description": "Смачиваемость, реология и интеграция в композитную матрицу",
        "color": SUAI_PALETTE["GREEN"],
        "hex": "009A49",
        "file": "icon_processability.png",
        "tag": "[⚙️🏭 ТЕХНОЛОГИЧНОСТЬ]",
    },
}


# ==============================================================================
# 3. Вспомогательные функции поиска ассетов
# ==============================================================================

def find_asset(filename: str, candidates: Optional[List[str]] = None) -> Optional[str]:
    """Находит файл ассета (логотип, иконка, фотография) в стандартных каталогах проекта."""
    search_dirs = [
        "course_materials/templates",
        "course_materials/templates/icons",
        "course_materials/semester_4/lectures/figures_l03/icons",
        "course_materials/semester_4/lectures/figures_l03",
        ".agents/teamwork/explorer_survey_skill",
        ".agents/teamwork/explorer_survey_skill/icons",
        ".agents/skills/scientific-presentation-creator/assets",
        ".",
    ]
    if candidates:
        search_dirs = candidates + search_dirs

    for directory in search_dirs:
        full_path = os.path.join(directory, filename)
        if os.path.exists(full_path):
            return os.path.abspath(full_path)
    return None


def get_problem_icon_path(problem_id: str) -> Optional[str]:
    """Возвращает абсолютный путь к иконке технологической проблемы."""
    prob_meta = PROBLEM_TAXONOMY.get(problem_id.lower())
    if not prob_meta:
        return None
    filename = prob_meta["file"]
    # Пробуем прямое имя и псевдоним для технологичности
    path = find_asset(filename)
    if not path and problem_id.lower() == "processability":
        path = find_asset("icon_technology.png")
    return path


# ==============================================================================
# 4. Базовый холст и фирменные элементы верстки ГУАП
# ==============================================================================

def create_base_presentation() -> Presentation:
    """Создает пустую презентацию широкоформатного стандарта 16:9 (13.333" × 7.500")."""
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.500)
    return prs


def add_signature_gradient_line(slide, left: float = 0.60, top: float = 1.06,
                                width: float = 12.133, height: float = 0.02):
    """
    Добавляет фирменную трехточечную градиентную разделительную линию ГУАП:
    #005AAA (0%) -> #00BEF3 (54%) -> #E70F47 (100%).
    """
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    line.line.fill.background()  # Убираем стандартную рамку фигуры
    spPr = line._element.spPr
    for child in list(spPr):
        if child.tag.endswith("solidFill") or child.tag.endswith("gradFill"):
            spPr.remove(child)

    grad_xml = (
        '<a:gradFill xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" flip="none" rotWithShape="1">'
        '  <a:gsLst>'
        '    <a:gs pos="0">'
        '      <a:srgbClr val="005AAA"/>'
        '    </a:gs>'
        '    <a:gs pos="54000">'
        '      <a:srgbClr val="00BEF3"/>'
        '    </a:gs>'
        '    <a:gs pos="100000">'
        '      <a:srgbClr val="E70F47"/>'
        '    </a:gs>'
        '  </a:gsLst>'
        '  <a:lin ang="0" scaled="1"/>'
        '</a:gradFill>'
    )
    spPr.append(parse_xml(grad_xml))
    return line


def add_suai_header(slide, title_text: str, subtitle_text: str = "",
                    logo_path: Optional[str] = None):
    """
    Добавляет мастер-шапку контентного слайда по стандарту ГУАП:
    - Заголовок слайда (Arial Bold 19–21 pt, SUAI Deep Navy #002C5F).
    - Компактный официальный логотип ГУАП в правом верхнем углу (11.62", 0.42").
    - Трехточечная градиентная линия (#005AAA -> #00BEF3 -> #E70F47) на top = 1.06".
    """
    # 1. Текстовое поле заголовка
    tb = slide.shapes.add_textbox(Inches(0.60), Inches(0.34), Inches(10.85), Inches(0.68))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_top = Inches(0.0)
    tf.margin_bottom = Inches(0.0)
    tf.margin_left = Inches(0.0)
    tf.margin_right = Inches(0.0)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT
    p.text = title_text
    p.font.name = "Arial"
    # Подбор кегля для предотвращения пересечения с линией 1.06"
    p.font.size = Pt(18.5) if len(title_text) > 55 else Pt(21)
    p.font.bold = True
    p.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]
    p.space_after = Pt(1)

    if subtitle_text:
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        p2.text = subtitle_text
        p2.font.name = "Arial"
        p2.font.size = Pt(11.5)
        p2.font.italic = True
        p2.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]

    # 2. Компактный логотип ГУАП
    resolved_logo = logo_path or find_asset("guap_image4.png")
    if resolved_logo and os.path.exists(resolved_logo):
        slide.shapes.add_picture(
            resolved_logo, Inches(11.62), Inches(0.42), width=Inches(1.11), height=Inches(0.34)
        )

    # 3. Фирменная градиентная линия
    add_signature_gradient_line(slide, left=0.60, top=1.06, width=12.133, height=0.02)


def add_header(slide, title_text: str, subtitle_text: str = ""):
    """Обертка для обратной совместимости: формирует мастер-шапку ГУАП."""
    add_suai_header(slide, title_text, subtitle_text)


def add_takeaway_banner(slide, takeaway_text: str):
    """
    Добавляет нижнюю плашку ключевого вывода слайда (Takeaway Banner):
    - Положение: left = 0.60", top = 6.65", width = 12.133", height = 0.55".
    - Фон: пастельный серо-голубой #EEF4FA, рамка 1.2 pt цвета #005AAA.
    - Шрифт: Arial Bold 12.5–13.0 pt Deep Navy.
    """
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(6.65), Inches(12.133), Inches(0.55)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = SUAI_PALETTE["TAKEAWAY_BG"]
    box.line.color.rgb = SUAI_PALETTE["BLUE"]
    box.line.width = Pt(1.2)

    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Inches(0.20)
    tf.margin_right = Inches(0.20)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    prefix = "[ВЫВОД] " if not takeaway_text.startswith(("[", "Ключевой", "Вывод")) else ""
    p.text = f"{prefix}{takeaway_text}"
    p.font.name = "Arial"
    p.font.size = Pt(12.5)
    p.font.bold = True
    p.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]


def add_content_card(slide, left: float, top: float, width: float, height: float,
                     heading: str, bullets: List[str], accent_color: Optional[RGBColor] = None):
    """
    Добавляет стандартизированную аналитическую карточку:
    - Фон #F4F7FA, субтильный контур #C8D7E6 (1.0 pt).
    - Заголовок 13–14 pt Bold Navy, буллиты 11.4–12.5 pt Charcoal.
    """
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
    card.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
    card.line.width = Pt(1.0)

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
    p0.font.size = Pt(13.5)
    p0.font.bold = True
    p0.font.color.rgb = accent_color or SUAI_PALETTE["DEEP_NAVY"]
    p0.space_after = Pt(5)

    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.text = f"• {b}"
        p.font.name = "Arial"
        p.font.size = Pt(12.0)
        p.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
        p.space_after = Pt(3)


def add_figure_or_placeholder(slide, left: float, top: float, width: float, height: float,
                              image_path: str = "", placeholder_desc: str = "Схема / График"):
    """Вставляет изображение с сохранением пропорций или рисует рамку-заготовку."""
    if image_path and os.path.exists(image_path):
        slide.shapes.add_picture(image_path, Inches(left), Inches(top), width=Inches(width))
    else:
        ph = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
        )
        ph.fill.solid()
        ph.fill.fore_color.rgb = COLOR_PLACEHOLDER_BG
        ph.line.color.rgb = SUAI_PALETTE["BLUE"]
        ph.line.width = Pt(1.2)
        tf = ph.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"[НАУЧНАЯ ИЛЛЮСТРАЦИЯ / ГРАФИК]\n\n{placeholder_desc}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.italic = True
        p.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]


def add_problem_badge(slide, left: float, top: float, problem_id: str,
                      size: float = 0.50) -> Optional[Any]:
    """Размещает иконку технологической проблемы или аккуратный векторный бейдж."""
    icon_path = get_problem_icon_path(problem_id)
    if icon_path and os.path.exists(icon_path):
        return slide.shapes.add_picture(
            icon_path, Inches(left), Inches(top), width=Inches(size), height=Inches(size)
        )
    # Векторная заглушка при отсутствии растрового файла иконки
    meta = PROBLEM_TAXONOMY.get(problem_id.lower(), {})
    color = meta.get("color", SUAI_PALETTE["BLUE"])
    circle = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, Inches(left), Inches(top), Inches(size), Inches(size)
    )
    circle.fill.solid()
    circle.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
    circle.line.color.rgb = color
    circle.line.width = Pt(1.5)
    return circle


def set_speaker_notes(slide, notes_text: str):
    """Записывает методический текст в заметки докладчика."""
    notes_slide = slide.notes_slide
    notes_slide.notes_text_frame.text = notes_text


# ==============================================================================
# 5. Каталог макетов слайдов (Layouts T, P, S, C)
# ==============================================================================

def create_title_slide(
    prs: Presentation,
    title: str = "Термодинамика дисперсных систем и коллоидных растворов",
    subtitle: str = "Часть 2: Поверхностная энергия, электростатическая стабилизация и теория ДЛФО",
    course_info: str = "КУРС «ФИЗИЧЕСКИЕ ОСНОВЫ НАНОТЕХНОЛОГИЙ» • 3 КУРС • ЛЕКЦИЯ №3",
    teacher_info: str = "Преподаватель: доцент Попов Д.А.",
    dept_info: str = "Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026",
    style: str = "classic",
    logo_path: Optional[str] = None,
    notes: str = "",
) -> Any:
    """
    Layout T: Титульный лист университета (Title Slide).
    Соблюдает правило Single-Point Occurrence: реквизиты курса, кафедры и преподавателя
    фиксируются строго на титуле и не повторяются на последующих слайдах.

    Поддерживаемые стили:
    - 'classic' (T1): Белый фон, цветной логотип ГУАП, акцентная линия #005AAA, Navy типографика.
    - 'split' (T2): Асимметричный сплит — левая плашка #F4F7FA, правая панель.
    - 'navy' (T3): Полноэкранный глубокий Navy фон #002C5F, белый логотип, белая/циановая типографика.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    is_navy = (style == "navy")

    if is_navy:
        # Темно-синяя фоновая подложка
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = SUAI_PALETTE["DEEP_NAVY"]
        bg.line.fill.background()
        logo_file = "guap_logo_white.png"
        text_title_color = SUAI_PALETTE["WHITE"]
        text_sub_color = SUAI_PALETTE["CYAN"]
        text_meta_color = RGBColor(180, 205, 230)
    else:
        logo_file = "guap_logo_extracted.png"
        text_title_color = SUAI_PALETTE["DEEP_NAVY"]
        text_sub_color = SUAI_PALETTE["BLUE"]
        text_meta_color = SUAI_PALETTE["MUTED_STEEL"]

    # 1. Официальный полноразмерный логотип ГУАП
    resolved_logo = logo_path or find_asset(logo_file)
    if not resolved_logo and is_navy:
        resolved_logo = find_asset("guap_image4.png")
    if not resolved_logo and not is_navy:
        resolved_logo = find_asset("guap_image4.png")

    if resolved_logo and os.path.exists(resolved_logo):
        slide.shapes.add_picture(
            resolved_logo, Inches(0.80), Inches(0.75), width=Inches(3.30)
        )

    # 2. Декоративная разделительная полоса
    line = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE, Inches(0.80), Inches(1.80), Inches(11.733), Inches(0.03)
    )
    line.fill.solid()
    line.fill.fore_color.rgb = SUAI_PALETTE["CYAN"] if is_navy else SUAI_PALETTE["BLUE"]
    line.line.fill.background()

    # 3. Навигационная строка курса
    tb_course = slide.shapes.add_textbox(Inches(0.80), Inches(2.15), Inches(11.733), Inches(0.40))
    tf_c = tb_course.text_frame
    tf_c.word_wrap = True
    p_c = tf_c.paragraphs[0]
    p_c.text = course_info
    p_c.font.name = "Arial"
    p_c.font.size = Pt(13)
    p_c.font.bold = True
    p_c.font.color.rgb = text_meta_color

    # 4. Основной заголовок темы лекции
    tb_title = slide.shapes.add_textbox(Inches(0.80), Inches(2.65), Inches(11.733), Inches(1.35))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = title
    p_t.font.name = "Arial"
    p_t.font.size = Pt(30)
    p_t.font.bold = True
    p_t.font.color.rgb = text_title_color

    # 5. Подзаголовок темы
    if subtitle:
        tb_sub = slide.shapes.add_textbox(Inches(0.80), Inches(4.15), Inches(11.733), Inches(0.70))
        tf_s = tb_sub.text_frame
        tf_s.word_wrap = True
        p_s = tf_s.paragraphs[0]
        p_s.text = subtitle
        p_s.font.name = "Arial"
        p_s.font.size = Pt(16)
        p_s.font.bold = True
        p_s.font.color.rgb = text_sub_color

    # 6. Карточка преподавателя и кафедры
    tb_meta = slide.shapes.add_textbox(Inches(0.80), Inches(5.60), Inches(11.733), Inches(0.80))
    tf_m = tb_meta.text_frame
    tf_m.word_wrap = True
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = teacher_info
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(13.5)
    p_m1.font.bold = True
    p_m1.font.color.rgb = text_title_color

    p_m2 = tf_m.add_paragraph()
    p_m2.text = dept_info
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = text_meta_color

    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_problem_intro_slide(
    prs: Presentation,
    title: str = "Шесть технологических барьеров нанодисперсных систем",
    problems: Optional[List[str]] = None,
    image_path: Optional[str] = None,
    image_caption: str = "Золь золота Фарадея (1857 г.) vs Агрегат наночастиц Fe3O4",
    takeaway: str = "Без электростатической или стерической защиты любая наносистема неизбежно разрушается.",
    notes: str = "",
) -> Any:
    """
    Layout P: Вводный проблемный слайд (Problem Intro).
    - Шапка с градиентной линией и логотипом ГУАП.
    - Левая половина: сетка 2×3 карточек 6 проблем наноматериалов с круглыми иконками-маркерами.
    - Правая половина: доминирующая подлинная научная микрофотография/фотоколба.
    - Нижний баннер ключевого вывода Takeaway.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(slide, title, "Фронтальные вызовы нанотехнологий при переходе к масштабу 1–100 нм")

    selected_problems = problems or [
        "aggregation", "sedimentation",
        "storage", "transport",
        "separation", "processability"
    ]

    # Левая колонка: сетка 2x3 карточек (left = 0.60", width = 5.75")
    col_w = 2.80
    row_h = 1.55
    start_x = 0.60
    start_y = 1.35

    for idx, pid in enumerate(selected_problems[:6]):
        c_idx = idx % 2
        r_idx = idx // 2
        card_x = start_x + c_idx * (col_w + 0.15)
        card_y = start_y + r_idx * (row_h + 0.15)

        meta = PROBLEM_TAXONOMY.get(pid, {})
        p_title = meta.get("title", pid.capitalize())
        p_formula = meta.get("formula", "")
        p_color = meta.get("color", SUAI_PALETTE["BLUE"])

        # Фон карточки
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(card_x), Inches(card_y),
            Inches(col_w), Inches(row_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
        card.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
        card.line.width = Pt(1.0)

        # Иконка проблемы
        add_problem_badge(slide, card_x + 0.12, card_y + 0.14, pid, size=0.46)

        # Текстовое описание внутри карточки
        tb = slide.shapes.add_textbox(
            Inches(card_x + 0.64), Inches(card_y + 0.10), Inches(col_w - 0.72), Inches(row_h - 0.20)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.margin_top = Inches(0.0)
        tf.margin_left = Inches(0.0)

        p1 = tf.paragraphs[0]
        p1.text = p_title
        p1.font.name = "Arial"
        p1.font.size = Pt(11)
        p1.font.bold = True
        p1.font.color.rgb = p_color

        p2 = tf.add_paragraph()
        p2.text = p_formula
        p2.font.name = "Arial"
        p2.font.size = Pt(10)
        p2.font.bold = True
        p2.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]
        p2.space_before = Pt(2)

        desc = meta.get("description", "")
        if desc:
            p3 = tf.add_paragraph()
            p3.text = desc
            p3.font.name = "Arial"
            p3.font.size = Pt(9)
            p3.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
            p3.space_before = Pt(2)

    # Правая колонка: подлинная научная иллюстрация (left = 6.65", width = 6.08", height = 5.05")
    resolved_img = image_path or find_asset("fig_01_faraday_vs_iron_oxide.jpg")
    img_x = 6.65
    img_y = 1.35
    img_w = 6.08
    img_h = 4.45

    if resolved_img and os.path.exists(resolved_img):
        slide.shapes.add_picture(
            resolved_img, Inches(img_x), Inches(img_y), width=Inches(img_w)
        )
    else:
        add_figure_or_placeholder(
            slide, img_x, img_y, img_w, img_h,
            placeholder_desc="Подлинная фотография: Колба Фарадея 1857 г. и СЭМ агрегации Fe3O4"
        )

    # Подпись к иллюстрации
    tb_cap = slide.shapes.add_textbox(
        Inches(img_x), Inches(img_y + img_h + 0.05), Inches(img_w), Inches(0.65)
    )
    tf_cap = tb_cap.text_frame
    tf_cap.word_wrap = True
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = f"Научная верификация: {image_caption}"
    p_cap.font.name = "Arial"
    p_cap.font.size = Pt(10)
    p_cap.font.italic = True
    p_cap.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]

    # Нижний баннер Takeaway
    add_takeaway_banner(slide, takeaway)

    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_section_divider_slide(
    prs: Presentation,
    problem_id: str = "aggregation",
    title: str = "Слипание и термодинамическая агрегация наночастиц",
    subtitle: str = "ТЕХНОЛОГИЧЕСКИЙ БАРЬЕР №1",
    thesis: str = "Колоссальная удельная поверхность создает избыточную свободную энергию ΔGs = σ · S > 0, стремящуюся скоагулировать незащищенный золь в плотный осадок.",
    roadmap_steps: Optional[List[str]] = None,
    style: str = "light",
    icon_path: Optional[str] = None,
    notes: str = "",
    problem_ids: Optional[List[str]] = None,
) -> Any:
    """
    Layout S: Слайд-разделитель / Открытие проблемы (Section Divider).
    - Центрированная композиция.
    - Крупные иконки-маркеры проблемы (1.40" × 1.40"), поддержка одиночной и парной иконок.
    - Надзаголовок проблемы, заголовок 24–28 pt Bold.
    - Физический тезис строго в 1–2 предложения (Pareto/Оккам).
    - Дорожная карта шагов решения в лекции.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    is_navy = (style == "navy")

    if is_navy:
        bg = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(7.500)
        )
        bg.fill.solid()
        bg.fill.fore_color.rgb = SUAI_PALETTE["DEEP_NAVY"]
        bg.line.fill.background()
        title_color = SUAI_PALETTE["WHITE"]
        thesis_color = RGBColor(220, 235, 250)
    else:
        title_color = SUAI_PALETTE["DEEP_NAVY"]
        thesis_color = SUAI_PALETTE["CHARCOAL"]

    meta = PROBLEM_TAXONOMY.get(problem_id.lower(), {})
    accent_color = meta.get("color", SUAI_PALETTE["RED"])
    if is_navy and accent_color == SUAI_PALETTE["DEEP_NAVY"]:
        accent_color = SUAI_PALETTE["CYAN"]

    # 1. Крупные иконки-маркеры по центру (1.40" x 1.40")
    pids = problem_ids if problem_ids else [problem_id]
    icon_w = 1.40
    gap = 0.25
    total_w = len(pids) * icon_w + (len(pids) - 1) * gap
    start_x = (13.333 - total_w) / 2.0
    for idx, pid in enumerate(pids):
        ix = start_x + idx * (icon_w + gap)
        resolved_icon = (icon_path if len(pids) == 1 else None) or get_problem_icon_path(pid)
        if resolved_icon and os.path.exists(resolved_icon):
            slide.shapes.add_picture(
                resolved_icon, Inches(ix), Inches(1.45), width=Inches(icon_w), height=Inches(icon_w)
            )
        else:
            circle = slide.shapes.add_shape(
                MSO_SHAPE.OVAL, Inches(ix), Inches(1.45), Inches(icon_w), Inches(icon_w)
            )
            circle.fill.solid()
            circle.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
            meta_i = PROBLEM_TAXONOMY.get(pid.lower(), {})
            col_i = meta_i.get("color", SUAI_PALETTE["RED"])
            if is_navy and col_i == SUAI_PALETTE["DEEP_NAVY"]:
                col_i = SUAI_PALETTE["CYAN"]
            circle.line.color.rgb = col_i
            circle.line.width = Pt(2.0)

    # 2. Надзаголовок проблемы
    tb_sub = slide.shapes.add_textbox(Inches(1.50), Inches(3.02), Inches(10.333), Inches(0.25))
    tf_s = tb_sub.text_frame
    tf_s.word_wrap = True
    tf_s.margin_left = Inches(0.0)
    tf_s.margin_right = Inches(0.0)
    tf_s.margin_top = Inches(0.0)
    tf_s.margin_bottom = Inches(0.0)
    p_s = tf_s.paragraphs[0]
    p_s.alignment = PP_ALIGN.CENTER
    p_s.text = subtitle
    p_s.font.name = "Arial"
    p_s.font.size = Pt(13)
    p_s.font.bold = True
    p_s.font.color.rgb = accent_color

    # 3. Основной заголовок раздела / проблемы
    tb_t = slide.shapes.add_textbox(Inches(1.00), Inches(3.42), Inches(11.333), Inches(0.88))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    tf_t.margin_left = Inches(0.0)
    tf_t.margin_right = Inches(0.0)
    tf_t.margin_top = Inches(0.0)
    tf_t.margin_bottom = Inches(0.0)
    p_t = tf_t.paragraphs[0]
    p_t.alignment = PP_ALIGN.CENTER
    p_t.text = title
    p_t.font.name = "Arial"
    p_t.font.size = Pt(24)
    p_t.font.bold = True
    p_t.font.color.rgb = title_color

    # 4. Физический тезис (1-2 предложения)
    tb_th = slide.shapes.add_textbox(Inches(1.10), Inches(4.46), Inches(11.133), Inches(0.90))
    tf_th = tb_th.text_frame
    tf_th.word_wrap = True
    tf_th.margin_left = Inches(0.0)
    tf_th.margin_right = Inches(0.0)
    tf_th.margin_top = Inches(0.0)
    tf_th.margin_bottom = Inches(0.0)
    p_th = tf_th.paragraphs[0]
    p_th.alignment = PP_ALIGN.CENTER
    p_th.text = thesis
    p_th.font.name = "Arial"
    p_th.font.size = Pt(13.0)
    p_th.font.color.rgb = thesis_color

    # 5. Дорожная карта шагов (Roadmap Pills)
    steps = roadmap_steps or [
        "1. Термодинамика Гиббса",
        "2. Строение ДЭС",
        "3. Электростатический барьер ДЛФО"
    ]
    num_steps = len(steps)
    if num_steps > 0:
        max_total_w = 12.133  # Стандартная ширина контента ГУАП (13.333 - 2 * 0.60)
        gap = 0.20 if num_steps >= 4 else 0.25
        if num_steps <= 3:
            pill_w = 3.20
            total_w = num_steps * pill_w + (num_steps - 1) * gap
        else:
            pill_w = (max_total_w - (num_steps - 1) * gap) / num_steps  # ~2.883" для 4 шагов
            total_w = max_total_w
        pill_start_x = (13.333 - total_w) / 2.0  # Ровно 0.60" для 4 шагов
        pill_y = 5.55

        for idx, step_text in enumerate(steps):
            px = pill_start_x + idx * (pill_w + gap)
            pill = slide.shapes.add_shape(
                MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(pill_y), Inches(pill_w), Inches(0.50)
            )
            pill.fill.solid()
            pill.fill.fore_color.rgb = RGBColor(15, 60, 115) if is_navy else SUAI_PALETTE["CARD_BG"]
            pill.line.color.rgb = SUAI_PALETTE["CYAN"] if is_navy else SUAI_PALETTE["BLUE"]
            pill.line.width = Pt(1.0)

            tf_p = pill.text_frame
            tf_p.word_wrap = True
            tf_p.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf_p.margin_left = Inches(0.06)
            tf_p.margin_right = Inches(0.06)
            tf_p.margin_top = Inches(0.02)
            tf_p.margin_bottom = Inches(0.02)
            p_p = tf_p.paragraphs[0]
            p_p.alignment = PP_ALIGN.CENTER
            p_p.text = step_text
            p_p.font.name = "Arial"
            p_p.font.size = Pt(10.5 if num_steps >= 4 else 11.5)
            p_p.font.bold = True
            p_p.font.color.rgb = SUAI_PALETTE["WHITE"] if is_navy else SUAI_PALETTE["DEEP_NAVY"]

    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_comparative_matrix_slide(
    prs: Presentation,
    title: str = "Сравнительный анализ дизайн-вариаций оформления",
    subtitle: str = "Сопоставление подходов по бренд-коду ГУАП, лаконичности Оккама и фокусу внимания",
    variations: Optional[List[Dict[str, Any]]] = None,
    takeaway: str = "Все 3 вариации соответствуют брендбуку ГУАП, предлагая различные уровни контраста и акцентов.",
    notes: str = "",
) -> Any:
    """
    Layout C: Сравнительная матрица вариаций (Comparative Matrix).
    - 3 колонки превью слайдов (width = 3.85" каждое).
    - Карточки критериев сравнения под каждым превью.
    - Баннер ключевого вывода Takeaway внизу.
    """
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(slide, title, subtitle)

    default_vars = [
        {
            "name": "Вариация 1: Academic Classic",
            "preview_path": None,
            "badge": "Корпоративный стандарт",
            "badge_color": SUAI_PALETTE["BLUE"],
            "criteria": [
                "Бренд ГУАП: белый фон, классический логотип",
                "Плотность: строгий лимит до 35 слов",
                "Фокус: высокая академическая строгость",
            ],
        },
        {
            "name": "Вариация 2: Tech Minimalist",
            "preview_path": None,
            "badge": "Инженерный акцент",
            "badge_color": SUAI_PALETTE["ORANGE"],
            "criteria": [
                "Бренд ГУАП: модульные карточки с рамкой",
                "Плотность: горизонтальные индикаторы",
                "Фокус: технологическая наглядность формул",
            ],
        },
        {
            "name": "Вариация 3: Deep Navy Prestige",
            "preview_path": None,
            "badge": "Премиальный темный",
            "badge_color": SUAI_PALETTE["DEEP_NAVY"],
            "criteria": [
                "Бренд ГУАП: полноэкранный глубокий Navy #002C5F",
                "Плотность: 2 емких предложения в центре",
                "Фокус: максимальный контраст с задних рядов",
            ],
        },
    ]

    selected_vars = variations or default_vars
    col_w = 3.85
    start_x = 0.60
    gap = 0.29
    top_y = 1.35
    thumb_h = 2.16
    card_h = 2.90

    for idx, var in enumerate(selected_vars[:3]):
        cx = start_x + idx * (col_w + gap)

        # 1. Рамка превью слайда (или реальный скриншот)
        preview_path = var.get("preview_path")
        if preview_path and os.path.exists(preview_path):
            slide.shapes.add_picture(
                preview_path, Inches(cx), Inches(top_y), width=Inches(col_w)
            )
        else:
            thumb = slide.shapes.add_shape(
                MSO_SHAPE.RECTANGLE, Inches(cx), Inches(top_y), Inches(col_w), Inches(thumb_h)
            )
            thumb.fill.solid()
            thumb.fill.fore_color.rgb = COLOR_PLACEHOLDER_BG
            thumb.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
            thumb.line.width = Pt(1.0)
            tf_th = thumb.text_frame
            tf_th.word_wrap = True
            p_th = tf_th.paragraphs[0]
            p_th.alignment = PP_ALIGN.CENTER
            p_th.text = f"[ПРЕВЬЮ СЛАЙДА]\n\n{var.get('name', f'Вариант {idx+1}')}"
            p_th.font.name = "Arial"
            p_th.font.size = Pt(11)
            p_th.font.italic = True
            p_th.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]

        # 2. Карточка критериев под превью
        card_y = top_y + thumb_h + 0.14
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(card_y), Inches(col_w), Inches(card_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
        card.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
        card.line.width = Pt(1.0)

        tf_c = card.text_frame
        tf_c.word_wrap = True
        tf_c.vertical_anchor = MSO_ANCHOR.TOP
        tf_c.margin_left = Inches(0.15)
        tf_c.margin_right = Inches(0.15)
        tf_c.margin_top = Inches(0.12)

        # Заголовок карточки
        p_c0 = tf_c.paragraphs[0]
        p_c0.text = var.get("name", f"Вариант {idx+1}")
        p_c0.font.name = "Arial"
        p_c0.font.size = Pt(12.5)
        p_c0.font.bold = True
        p_c0.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

        # Бейдж статуса
        badge_text = var.get("badge")
        if badge_text:
            p_badge = tf_c.add_paragraph()
            p_badge.text = f"● {badge_text}"
            p_badge.font.name = "Arial"
            p_badge.font.size = Pt(10.5)
            p_badge.font.bold = True
            p_badge.font.color.rgb = var.get("badge_color", SUAI_PALETTE["BLUE"])
            p_badge.space_after = Pt(4)

        # Пункты критериев
        criteria = var.get("criteria", [])
        for cr in criteria:
            p_cr = tf_c.add_paragraph()
            p_cr.text = f"• {cr}"
            p_cr.font.name = "Arial"
            p_cr.font.size = Pt(10.5)
            p_cr.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
            p_cr.space_after = Pt(2)

    # 3. Нижний баннер Takeaway
    add_takeaway_banner(slide, takeaway)

    if notes:
        set_speaker_notes(slide, notes)
    return slide
