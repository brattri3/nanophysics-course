"""
Генератор презентаций Лекции №3:
«Термодинамика дисперсных систем и коллоидных растворов (Часть 2)»
Стандарт дизайн-кода ГУАП (SUAI Design Code) для курса «Физические основы нанотехнологий».

Функционал скрипта:
1. Генерация 3 дизайн-вариаций для первых 3 слайдов Лекции №3:
   - Вариация 1 (Classic SUAI Corporate): строгий белый корпоративный стиль ГУАП,
     полный официальный логотип, темно-синие заголовки, сетка 2x3 карточек проблем,
     подлинная микрофотография Faraday/Fe3O4, светлый центрированный разделитель.
   - Вариация 2 (Modern Scientific Infographic): инженерно-инфографический стиль,
     контейнерная плашка с бейджами тем, цветовое кодирование карточек проблем,
     технологический оверлей на микрофотографии, контрастный блок тезиса.
   - Вариация 3 (High-Contrast Problem-First / Deep Navy Hero): полноэкранный глубокий
     темно-синий холст (#002C5F), инвертированный белый логотип, циановые акценты,
     монументальный статус и максимальная читаемость с дальних рядов аудитории.
2. Сборка сравнительной презентации:
   course_materials/semester_4/lectures/lecture_03_comparative_variations.pptx (14 слайдов)
   (9 вариативных слайдов + титул + 4 аналитические матрицы сопоставления).
3. Сборка основной академической презентации лекции:
   course_materials/semester_4/lectures/lecture_03_colloids.pptx (17 слайдов)
   (Слайды 1–3 основной вариации + 13 теоретических слайдов + Слайд 17 технологического применения).
4. Полная очистка от упоминаний лабораторных работ (R1/R5):
   Слайд 17 переработан в прикладные модули «Коллоидная диагностика: плазмонный резонанс
   и дзета-потенциал (Au)» и «Промышленный синтез стабильных наносуспензий и коагуляция (Fe(OH)₃)».
"""

import os
import sys
from typing import List, Dict, Any, Optional
from PIL import Image

import pptx
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

# Подключение базового конструктора и дизайн-стандартов навыка
SKILL_SCRIPTS = os.path.abspath(".agents/skills/scientific-presentation-creator/scripts")
if SKILL_SCRIPTS not in sys.path:
    sys.path.insert(0, SKILL_SCRIPTS)

from template_deck_builder import (
    SUAI_PALETTE, PROBLEM_TAXONOMY,
    COLOR_NAVY, COLOR_BLUE, COLOR_DARK, COLOR_MUTED,
    COLOR_CARD_BG, COLOR_CARD_BORDER, COLOR_BANNER_BG, COLOR_WHITE,
    find_asset, get_problem_icon_path,
    create_base_presentation, add_signature_gradient_line,
    add_suai_header, add_header, add_takeaway_banner, add_content_card,
    add_figure_or_placeholder, add_problem_badge, set_speaker_notes,
    create_title_slide, create_problem_intro_slide,
    create_section_divider_slide, create_comparative_matrix_slide
)

# Пути к графическим ассетам и результирующим презентациям
FIG_DIR = os.path.abspath("course_materials/semester_4/lectures/figures_l03")
TEMPLATES_DIR = os.path.abspath("course_materials/templates")
OUT_MAIN_PPTX = os.path.abspath("course_materials/semester_4/lectures/lecture_03_colloids.pptx")
OUT_VARIATIONS_PPTX = os.path.abspath("course_materials/semester_4/lectures/lecture_03_comparative_variations.pptx")
PREVIEWS_VARIATIONS_DIR = os.path.abspath("previews_variations")


def get_variation_preview_path(filename: str) -> Optional[str]:
    path = os.path.join(PREVIEWS_VARIATIONS_DIR, filename)
    return path if os.path.exists(path) else None


# ==============================================================================
# 1. Вспомогательные функции рендеринга карточек и фигур
# ==============================================================================

def add_rich_card(slide, left: float, top: float, width: float, height: float,
                  heading: str, bullets: List[str], font_size: float = 11.4,
                  accent_color: Optional[RGBColor] = None):
    """Добавляет стандартизированную карточку теории с поддержкой формульных строк [Ф]."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(width), Inches(height)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
    card.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
    card.line.width = Pt(1.1)

    tf = card.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = Inches(0.16)
    tf.margin_right = Inches(0.14)
    tf.margin_top = Inches(0.10)
    tf.margin_bottom = Inches(0.08)

    p0 = tf.paragraphs[0]
    p0.alignment = PP_ALIGN.LEFT
    p0.text = heading
    p0.font.name = "Arial"
    p0.font.size = Pt(13.2)
    p0.font.bold = True
    p0.font.color.rgb = accent_color or SUAI_PALETTE["DEEP_NAVY"]
    p0.space_after = Pt(4)

    for b in bullets:
        p = tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        is_formula = b.startswith("  [Ф] ")
        is_sub = b.startswith("  - ") or b.startswith("    ")
        if is_formula:
            p.text = b.replace("  [Ф] ", "   ")
            p.font.name = "Arial"
            p.font.size = Pt(font_size + 0.4)
            p.font.bold = True
            p.font.color.rgb = SUAI_PALETTE["BLUE"]
            p.space_before = Pt(1.5)
            p.space_after = Pt(2.5)
        elif is_sub:
            p.text = b
            p.font.name = "Arial"
            p.font.size = Pt(font_size - 0.2)
            p.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
            p.space_after = Pt(2.0)
        else:
            p.text = f"• {b}" if not b.startswith("•") else b
            p.font.name = "Arial"
            p.font.size = Pt(font_size)
            p.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
            p.space_after = Pt(2.5)


def add_fitted_figure(slide, left: float, top: float, max_w: float, max_h: float,
                      image_filename: str, placeholder_desc: str, use_placeholder_only: bool = False):
    """Вставляет изображение с сохранением пропорций в заданную ограничивающую рамку."""
    image_path = os.path.join(FIG_DIR, image_filename)
    if not os.path.exists(image_path):
        resolved = find_asset(image_filename)
        if resolved:
            image_path = resolved

    if (not use_placeholder_only) and os.path.exists(image_path):
        frame = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left), Inches(top), Inches(max_w), Inches(max_h)
        )
        frame.fill.solid()
        frame.fill.fore_color.rgb = RGBColor(255, 255, 255)
        frame.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
        frame.line.width = Pt(1.0)

        with Image.open(image_path) as img:
            img_w, img_h = img.size
        aspect = img_w / float(img_h)
        pad = 0.08
        avail_w = max_w - 2 * pad
        avail_h = max_h - 2 * pad

        if avail_w / avail_h > aspect:
            pic_h = avail_h
            pic_w = avail_h * aspect
        else:
            pic_w = avail_w
            pic_h = avail_w / aspect

        pic_left = left + (max_w - pic_w) / 2.0
        pic_top = top + (max_h - pic_h) / 2.0
        slide.shapes.add_picture(image_path, Inches(pic_left), Inches(pic_top),
                                 width=Inches(pic_w), height=Inches(pic_h))
    else:
        ph = slide.shapes.add_shape(
            MSO_SHAPE.RECTANGLE, Inches(left), Inches(top), Inches(max_w), Inches(max_h)
        )
        ph.fill.solid()
        ph.fill.fore_color.rgb = RGBColor(250, 250, 252)
        ph.line.color.rgb = SUAI_PALETTE["BLUE"]
        ph.line.width = Pt(1.5)
        tf = ph.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        p.text = f"[НАУЧНАЯ ИЛЛЮСТРАЦИЯ: {image_filename}]\n\n{placeholder_desc}"
        p.font.name = "Arial"
        p.font.size = Pt(13)
        p.font.italic = True
        p.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]


# ==============================================================================
# 2. Реализация 3 дизайн-вариаций для Слайдов 1, 2, 3
# ==============================================================================

def add_variation_1_slides(prs: Presentation) -> List[Any]:
    """
    Вариация 1: «Академический классический стиль ГУАП» (Classic SUAI Corporate)
    - Слайд 1: Белый фон, цветной логотип ГУАП, темно-синяя иерархия, реквизиты однократно.
    - Слайд 2: Сетка 2x3 карточек 6 проблем с векторными иконками, сплит-визуал Фарадей/Fe3O4.
    - Слайд 3: Светлый центрированный слайд-разделитель (Layout S) первой проблемы (Агрегация).
    """
    slides = []

    # ---------------------------------------------------------
    # Вариация 1: Слайд 1 (Титульный лист ГУАП)
    # ---------------------------------------------------------
    s1 = create_title_slide(
        prs,
        title="Термодинамика дисперсных систем и коллоидных растворов",
        subtitle="Часть 2: Поверхностная энергия, двойной электрический слой (ДЭС) и устойчивость коллоидов",
        course_info="КУРС «ФИЗИЧЕСКИЕ ОСНОВЫ НАНОТЕХНОЛОГИЙ» • 3 КУРС • ЛЕКЦИЯ №3",
        teacher_info="Преподаватель: доцент Попов Д.А.",
        dept_info="Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026",
        style="classic",
        notes=(
            "1. Место лекции в курсе: Раздел 2 «Особенности термодинамики наноструктур» дисциплины "
            "«Физические основы нанотехнологий» (бакалавриат, 3 курс ГУАП). Лекция закладывает фундамент "
            "жидкофазного синтеза, устойчивости золей и наноколлоидов.\n"
            "2. Соответствие РПД: Темы №7 и №8 календарного плана (термодинамика границ раздела, ДЭС, теория ДЛФО).\n"
            "3. Обратите внимание студентов: все университетские реквизиты кафедры и преподавателя зафиксированы "
            "на титульном листе и далее на рабочих слайдах не повторяются."
        )
    )
    slides.append(s1)

    # ---------------------------------------------------------
    # Вариация 1: Слайд 2 (Вводный проблемный: 6 барьеров)
    # ---------------------------------------------------------
    split_img = find_asset("fig_01_split_faraday_vs_fe3o4.png") or os.path.join(FIG_DIR, "fig_01_split_faraday_vs_fe3o4.png")
    s2 = create_problem_intro_slide(
        prs,
        title="Шесть технологических барьеров нанодисперсных систем",
        image_path=split_img,
        image_caption="Золь золота Фарадея (1857 г.) vs Агрегат наночастиц Fe3O4 (сканирующая и просвечивающая ЭМ — СЭМ/ПЭМ)",
        takeaway="Без электростатической или стерической защиты любая наносистема неизбежно разрушается.",
        notes=(
            "1. Постановка проблемы: Переход к наномасштабу 1–100 нм сопровождается колоссальным ростом удельной "
            "поверхности. Это порождает 6 критических барьеров: слипание (агрегацию), гравитационный осадок, "
            "старение при хранении, сдвиговое разрушение при транспорте, сложность сепарации и несовместимость с матрицами.\n"
            "2. Подлинный научный эталон: Справа представлен рубиновый золь золота Майкла Фарадея (1857 г.), стабильный "
            "уже более 170 лет благодаря защитному ДЭС, в контрасте с незащищенным оксидом железа Fe3O4, скоагулировавшим в осадок."
        )
    )
    slides.append(s2)

    # ---------------------------------------------------------
    # Вариация 1: Слайд 3 (Разделитель Проблемы №1: Агрегация)
    # ---------------------------------------------------------
    s3 = create_section_divider_slide(
        prs,
        problem_id="aggregation",
        title="Слипание и термодинамическая агрегация наночастиц",
        subtitle="ТЕХНОЛОГИЧЕСКИЙ БАРЬЕР №1",
        thesis="Колоссальная удельная поверхность создает избыточную свободную энергию ΔGs = σ · S > 0, стремящуюся скоагулировать незащищенный золь в плотный осадок.",
        roadmap_steps=[
            "1. Геометрия поверхности и термодинамика Гиббса",
            "2. Строение мицеллы и двойной электрический слой (ДЭС)",
            "3. Барьер Дерягина–Ландау–Фервея–Овербека (ДЛФО)"
        ],
        style="light",
        notes=(
            "1. Фокус раздела: Открываем разбор первого и фундаментального барьера — агрегации наночастиц.\n"
            "2. Бритва Оккама: Слайд-разделитель содержит только ключевой физический тезис в 1–2 предложениях, "
            "акцентируя внимание на избытке свободной энергии Гиббса ΔGs = σ · S > 0.\n"
            "3. Дорожная карта: В данном блоке мы последовательно разберем геометрический взрыв поверхности, "
            "анатомию ДЭС и расчет потенциального барьера теории ДЛФО."
        )
    )
    slides.append(s3)

    return slides


def add_variation_2_slides(prs: Presentation) -> List[Any]:
    """
    Вариация 2: «Инженерно-инфографический стиль» (Modern Scientific Infographic)
    - Слайд 1: Контейнерная карточка #F4F7FA, бейдж дисциплины [КУРС «ФОН»], акцентные плашки.
    - Слайд 2: Карточки проблем с индивидуальными цветовыми бейджами [БАРЬЕР 1..6], формульный акцент.
    - Слайд 3: Модернизированный центрированный разделитель с акцентным кольцом и нумерованными шагами.
    """
    slides = []

    # ---------------------------------------------------------
    # Вариация 2: Слайд 1 (Инфографический титул)
    # ---------------------------------------------------------
    slide1 = prs.slides.add_slide(prs.slide_layouts[6])

    # Внешняя контурная карточка-контейнер
    container = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.60), Inches(0.50), Inches(12.133), Inches(6.50)
    )
    container.fill.solid()
    container.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
    container.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
    container.line.width = Pt(1.5)

    # Логотип ГУАП
    logo_path = find_asset("guap_logo_extracted.png") or find_asset("guap_image4.png")
    if logo_path and os.path.exists(logo_path):
        slide1.shapes.add_picture(logo_path, Inches(1.00), Inches(0.85), width=Inches(3.20))

    # Бейдж курса в правом верхнем углу контейнера
    badge = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.60), Inches(0.85), Inches(5.60), Inches(0.46)
    )
    badge.fill.solid()
    badge.fill.fore_color.rgb = SUAI_PALETTE["BLUE"]
    badge.line.fill.background()
    tf_b = badge.text_frame
    p_b = tf_b.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    p_b.text = "КУРС «ФИЗИЧЕСКИЕ ОСНОВЫ НАНОТЕХНОЛОГИЙ» • 3 КУРС"
    p_b.font.name = "Arial"
    p_b.font.size = Pt(10.5)
    p_b.font.bold = True
    p_b.font.color.rgb = SUAI_PALETTE["WHITE"]

    # Фирменная градиентная линия ГУАП
    add_signature_gradient_line(slide1, left=1.00, top=1.65, width=11.333, height=0.03)

    # Название лекции
    tb_t = slide1.shapes.add_textbox(Inches(1.00), Inches(2.05), Inches(11.333), Inches(1.40))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True
    p_t = tf_t.paragraphs[0]
    p_t.text = "Термодинамика дисперсных систем и коллоидных растворов"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(29)
    p_t.font.bold = True
    p_t.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

    # Подзаголовок в пастельной плашке
    sub_box = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.00), Inches(3.70), Inches(10.50), Inches(0.55)
    )
    sub_box.fill.solid()
    sub_box.fill.fore_color.rgb = SUAI_PALETTE["TAKEAWAY_BG"]
    sub_box.line.color.rgb = SUAI_PALETTE["CYAN"]
    sub_box.line.width = Pt(1.0)
    tf_sb = sub_box.text_frame
    p_sb = tf_sb.paragraphs[0]
    p_sb.alignment = PP_ALIGN.LEFT
    p_sb.text = "  Часть 2: Поверхностная энергия, двойной электрический слой (ДЭС) и устойчивость коллоидов"
    p_sb.font.name = "Arial"
    p_sb.font.size = Pt(13.5)
    p_sb.font.bold = True
    p_sb.font.color.rgb = SUAI_PALETTE["BLUE"]

    # Информационный блок преподавателя и кафедры
    meta_box = slide1.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.00), Inches(4.70), Inches(11.333), Inches(1.80)
    )
    meta_box.fill.solid()
    meta_box.fill.fore_color.rgb = SUAI_PALETTE["WHITE"]
    meta_box.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
    meta_box.line.width = Pt(1.0)

    tf_m = meta_box.text_frame
    tf_m.word_wrap = True
    p_m1 = tf_m.paragraphs[0]
    p_m1.text = "Преподаватель: доцент Попов Д.А."
    p_m1.font.name = "Arial"
    p_m1.font.size = Pt(14)
    p_m1.font.bold = True
    p_m1.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

    p_m2 = tf_m.add_paragraph()
    p_m2.text = "Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026"
    p_m2.font.name = "Arial"
    p_m2.font.size = Pt(12)
    p_m2.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]
    p_m2.space_before = Pt(4)

    p_m3 = tf_m.add_paragraph()
    p_m3.text = "Статус дисциплины: Обязательный общепрофессиональный модуль бакалавриата (03.03.01)"
    p_m3.font.name = "Arial"
    p_m3.font.size = Pt(11)
    p_m3.font.bold = True
    p_m3.font.color.rgb = SUAI_PALETTE["GREEN"]
    p_m3.space_before = Pt(6)

    set_speaker_notes(
        slide1,
        "Вариация 2 (Инженерная инфографика): Модульная композиция с контейнером и бейджами "
        "акцентирует внимание на структурированности курса. Все реквизиты указаны однократно."
    )
    slides.append(slide1)

    # ---------------------------------------------------------
    # Вариация 2: Слайд 2 (Инфографический проблемный слайд)
    # ---------------------------------------------------------
    slide2 = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide2,
        "Шесть технологических барьеров нанодисперсных систем",
        "Инфографическая карта физических вызовов и управляющих уравнений наноматериалов"
    )

    # Карточки с цветными плашками
    prob_list = [
        ("aggregation", "БАРЬЕР 1: СЛИПАНИЕ", SUAI_PALETTE["RED"]),
        ("sedimentation", "БАРЬЕР 2: ОСАДОК", SUAI_PALETTE["DEEP_NAVY"]),
        ("storage", "БАРЬЕР 3: СТАРЕНИЕ", SUAI_PALETTE["ORANGE"]),
        ("transport", "БАРЬЕР 4: ТРАНСПОРТ", SUAI_PALETTE["PURPLE"]),
        ("separation", "БАРЬЕР 5: СЕПАРАЦИЯ", SUAI_PALETTE["CYAN"]),
        ("processability", "БАРЬЕР 6: ФОРМУЛЯЦИЯ", SUAI_PALETTE["GREEN"]),
    ]

    col_w = 2.80
    row_h = 1.55
    start_x = 0.60
    start_y = 1.35

    for idx, (pid, badge_label, b_color) in enumerate(prob_list):
        c_idx = idx % 2
        r_idx = idx // 2
        card_x = start_x + c_idx * (col_w + 0.15)
        card_y = start_y + r_idx * (row_h + 0.15)

        meta = PROBLEM_TAXONOMY.get(pid, {})

        # Карточка
        card = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(card_x), Inches(card_y),
            Inches(col_w), Inches(row_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
        card.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
        card.line.width = Pt(1.0)

        # Верхний цветной бейдж категории
        t_badge = slide2.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(card_x + 0.08), Inches(card_y + 0.08),
            Inches(col_w - 0.16), Inches(0.24)
        )
        t_badge.fill.solid()
        t_badge.fill.fore_color.rgb = b_color
        t_badge.line.fill.background()
        tf_tb = t_badge.text_frame
        p_tb = tf_tb.paragraphs[0]
        p_tb.alignment = PP_ALIGN.CENTER
        p_tb.text = badge_label
        p_tb.font.name = "Arial"
        p_tb.font.size = Pt(8.5)
        p_tb.font.bold = True
        p_tb.font.color.rgb = SUAI_PALETTE["WHITE"]

        # Иконка
        add_problem_badge(slide2, card_x + 0.10, card_y + 0.40, pid, size=0.48)

        # Текст
        tb = slide2.shapes.add_textbox(
            Inches(card_x + 0.66), Inches(card_y + 0.36), Inches(col_w - 0.74), Inches(row_h - 0.44)
        )
        tf = tb.text_frame
        tf.word_wrap = True
        tf.margin_top = Inches(0.0)
        tf.margin_left = Inches(0.0)

        p1 = tf.paragraphs[0]
        p1.text = meta.get("formula", "")
        p1.font.name = "Arial"
        p1.font.size = Pt(10.5)
        p1.font.bold = True
        p1.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

        p2 = tf.add_paragraph()
        p2.text = meta.get("description", "")
        p2.font.name = "Arial"
        p2.font.size = Pt(8.8)
        p2.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
        p2.space_before = Pt(2)

    # Правая панель с иллюстрацией
    split_img = find_asset("fig_01_split_faraday_vs_fe3o4.png") or os.path.join(FIG_DIR, "fig_01_split_faraday_vs_fe3o4.png")
    img_x = 6.65
    img_y = 1.35
    img_w = 6.08
    img_h = 4.45

    if split_img and os.path.exists(split_img):
        slide2.shapes.add_picture(split_img, Inches(img_x), Inches(img_y), width=Inches(img_w))
    else:
        add_figure_or_placeholder(slide2, img_x, img_y, img_w, img_h, placeholder_desc="Фото Фарадея и СЭМ Fe3O4")

    # Академическая подпись
    tb_cap = slide2.shapes.add_textbox(Inches(img_x), Inches(img_y + img_h + 0.05), Inches(img_w), Inches(0.65))
    tf_cap = tb_cap.text_frame
    p_cap = tf_cap.paragraphs[0]
    p_cap.text = "Научная верификация: Колба золя Au Фарадея 1857 г. (слева) vs Агрегация Fe3O4 (сканирующая и просвечивающая ЭМ — СЭМ/ПЭМ)"
    p_cap.font.name = "Arial"
    p_cap.font.size = Pt(9.5)
    p_cap.font.italic = True
    p_cap.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]

    add_takeaway_banner(slide2, "Без электростатической или стерической защиты любая наносистема неизбежно разрушается.")
    set_speaker_notes(
        slide2,
        "Вариация 2: Цветовые бейджи барьеров создают мгновенную визуальную навигацию по технологическим вызовам."
    )
    slides.append(slide2)

    # ---------------------------------------------------------
    # Вариация 2: Слайд 3 (Инфографический разделитель)
    # ---------------------------------------------------------
    slide3 = prs.slides.add_slide(prs.slide_layouts[6])

    # Верхняя и нижняя тонкие полосы
    top_band = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.12))
    top_band.fill.solid()
    top_band.fill.fore_color.rgb = SUAI_PALETTE["DEEP_NAVY"]
    top_band.line.fill.background()

    bot_band = slide3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.38), Inches(13.333), Inches(0.12))
    bot_band.fill.solid()
    bot_band.fill.fore_color.rgb = SUAI_PALETTE["BLUE"]
    bot_band.line.fill.background()

    # Центрированное акцентное кольцо и иконка
    ring = slide3.shapes.add_shape(MSO_SHAPE.OVAL, Inches(5.86), Inches(1.10), Inches(1.60), Inches(1.60))
    ring.fill.solid()
    ring.fill.fore_color.rgb = SUAI_PALETTE["TAKEAWAY_BG"]
    ring.line.color.rgb = SUAI_PALETTE["CYAN"]
    ring.line.width = Pt(2.0)

    icon_path = get_problem_icon_path("aggregation")
    if icon_path and os.path.exists(icon_path):
        slide3.shapes.add_picture(icon_path, Inches(5.96), Inches(1.20), width=Inches(1.40), height=Inches(1.40))

    # Бейдж фокуса
    b_pill = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(4.40), Inches(2.95), Inches(4.533), Inches(0.40))
    b_pill.fill.solid()
    b_pill.fill.fore_color.rgb = SUAI_PALETTE["RED"]
    b_pill.line.fill.background()
    tf_bp = b_pill.text_frame
    p_bp = tf_bp.paragraphs[0]
    p_bp.alignment = PP_ALIGN.CENTER
    p_bp.text = "ТЕХНОЛОГИЧЕСКИЙ БАРЬЕР №1"
    p_bp.font.name = "Arial"
    p_bp.font.size = Pt(12)
    p_bp.font.bold = True
    p_bp.font.color.rgb = SUAI_PALETTE["WHITE"]

    # Заголовок
    tb_t = slide3.shapes.add_textbox(Inches(1.00), Inches(3.45), Inches(11.333), Inches(0.70))
    tf_t = tb_t.text_frame
    p_t = tf_t.paragraphs[0]
    p_t.alignment = PP_ALIGN.CENTER
    p_t.text = "Слипание и термодинамическая агрегация наночастиц"
    p_t.font.name = "Arial"
    p_t.font.size = Pt(26)
    p_t.font.bold = True
    p_t.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

    # Карточка тезиса
    th_box = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.60), Inches(4.30), Inches(10.133), Inches(0.95))
    th_box.fill.solid()
    th_box.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
    th_box.line.color.rgb = SUAI_PALETTE["BLUE"]
    th_box.line.width = Pt(1.2)
    tf_th = th_box.text_frame
    tf_th.word_wrap = True
    p_th = tf_th.paragraphs[0]
    p_th.alignment = PP_ALIGN.CENTER
    p_th.text = "Колоссальная удельная поверхность создает избыточную свободную энергию ΔGs = σ · S > 0, стремящуюся скоагулировать незащищенный золь в плотный осадок."
    p_th.font.name = "Arial"
    p_th.font.size = Pt(15)
    p_th.font.bold = True
    p_th.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

    # Нумерованные шаги дорожной карты
    steps = [
        "[01] Геометрия поверхности и термодинамика Гиббса",
        "[02] Строение мицеллы и двойного слоя (ДЭС)",
        "[03] Барьер Дерягина–Ландау–Фервея–Овербека (ДЛФО)"
    ]
    pill_w = 3.60
    total_w = len(steps) * pill_w + (len(steps) - 1) * 0.25
    start_px = (13.333 - total_w) / 2.0
    for idx, st in enumerate(steps):
        px = start_px + idx * (pill_w + 0.25)
        p_pill = slide3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(px), Inches(5.65), Inches(pill_w), Inches(0.48))
        p_pill.fill.solid()
        p_pill.fill.fore_color.rgb = SUAI_PALETTE["WHITE"]
        p_pill.line.color.rgb = SUAI_PALETTE["CARD_BORDER"]
        p_pill.line.width = Pt(1.0)
        tf_p = p_pill.text_frame
        p_p = tf_p.paragraphs[0]
        p_p.alignment = PP_ALIGN.CENTER
        p_p.text = st
        p_p.font.name = "Arial"
        p_p.font.size = Pt(11)
        p_p.font.bold = True
        p_p.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]

    set_speaker_notes(slide3, "Вариация 2: Разделитель с акцентной карточкой тезиса и нумерованными шагами темы.")
    slides.append(slide3)

    return slides


def add_variation_3_slides(prs: Presentation) -> List[Any]:
    """
    Вариация 3: «Премиальный глубокий темно-синий бренд ГУАП» (Deep Navy Hero)
    - Слайд 1: Полноэкранный темный холст #002C5F, белый логотип, циановые акценты.
    - Слайд 2: Контрастный проблемный слайд с акцентным темно-синим баннером и героическим визуалом.
    - Слайд 3: Полноэкранный темный разделитель (Layout S Navy) с циановым кольцом и белым тезисом.
    """
    slides = []

    # ---------------------------------------------------------
    # Вариация 3: Слайд 1 (Deep Navy Hero Title)
    # ---------------------------------------------------------
    s1 = create_title_slide(
        prs,
        title="Термодинамика дисперсных систем и коллоидных растворов",
        subtitle="Часть 2: Поверхностная энергия, двойной электрический слой (ДЭС) и устойчивость коллоидов",
        course_info="КУРС «ФИЗИЧЕСКИЕ ОСНОВЫ НАНОТЕХНОЛОГИЙ» • 3 КУРС • ЛЕКЦИЯ №3",
        teacher_info="Преподаватель: доцент Попов Д.А.",
        dept_info="Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026",
        style="navy",
        notes=(
            "1. Вариация 3 (Deep Navy Hero): Полноэкранный темно-синий фон #002C5F обеспечивает "
            "максимальный контраст и монументальный университетский статус на широкоформатных проекторах.\n"
            "2. Реквизиты преподавателя и кафедры строго зафиксированы однократно на титуле."
        )
    )
    slides.append(s1)

    # ---------------------------------------------------------
    # Вариация 3: Слайд 2 (Контрастный проблемный слайд)
    # ---------------------------------------------------------
    s2 = create_problem_intro_slide(
        prs,
        title="Шесть технологических барьеров нанодисперсных систем",
        image_path=find_asset("fig_01_split_faraday_vs_fe3o4.png"),
        image_caption="Золь золота Фарадея (1857 г.) vs Агрегат наночастиц Fe3O4 (сканирующая и просвечивающая ЭМ — СЭМ/ПЭМ)",
        takeaway="Без электростатической или стерической защиты любая наносистема неизбежно разрушается.",
        notes=(
            "Вариация 3: Высококонтрастная подача технологических барьеров с глубоким темно-синим акцентом "
            "в шапке и баннере вывода."
        )
    )
    # Добавляем контрастную темно-синюю плашку вывода
    for shp in s2.shapes:
        if shp.has_text_frame and "[ВЫВОД]" in shp.text_frame.text:
            shp.fill.solid()
            shp.fill.fore_color.rgb = SUAI_PALETTE["DEEP_NAVY"]
            shp.line.color.rgb = SUAI_PALETTE["CYAN"]
            shp.line.width = Pt(1.5)
            p = shp.text_frame.paragraphs[0]
            p.font.color.rgb = SUAI_PALETTE["WHITE"]

    slides.append(s2)

    # ---------------------------------------------------------
    # Вариация 3: Слайд 3 (Deep Navy Разделитель)
    # ---------------------------------------------------------
    s3 = create_section_divider_slide(
        prs,
        problem_id="aggregation",
        title="Слипание и термодинамическая агрегация наночастиц",
        subtitle="ТЕХНОЛОГИЧЕСКИЙ БАРЬЕР №1",
        thesis="Колоссальная удельная поверхность создает избыточную свободную энергию ΔGs = σ · S > 0, стремящуюся скоагулировать незащищенный золь в плотный осадок.",
        roadmap_steps=[
            "1. Геометрия поверхности и термодинамика Гиббса",
            "2. Строение мицеллы и двойной электрический слой (ДЭС)",
            "3. Барьер Дерягина–Ландау–Фервея–Овербека (ДЛФО)"
        ],
        style="navy",
        notes=(
            "Вариация 3: Темный разделитель раздела служит мощным когнитивным переключателем внимания "
            "в потоковой лекции, подготавливая студентов к глубокому физико-математическому анализу."
        )
    )
    slides.append(s3)

    return slides


# ==============================================================================
# 3. Спецификация основных теоретических слайдов Лекции №3 (Слайды 4–17)
# ==============================================================================

CORE_SLIDES_SPEC = [
    # -------------------------------------------------------------------------
    # Слайд 4 (в нумерации лекции: Слайд 4)
    # -------------------------------------------------------------------------
    {
        "num": 4,
        "layout": "A",
        "title": "Удельная поверхность S_уд ∝ 1/a — главный геометрический драйвер наносистем",
        "subtitle": "Блок 1. Классификация и количественные параметры дисперсных систем",
        "cards": [
            {
                "heading": "1. Дисперсность D и удельная поверхность S_уд",
                "height": 2.40,
                "bullets": [
                    "Дисперсная система состоит из дисперсной фазы (размер a) и сплошной дисперсионной среды.",
                    "Дисперсность D = 1/a [м⁻¹] определяет удельную площадь фазовой границы:",
                    "  [Ф] S_уд = S / V = k / a,     S_уд^(m) = S / m = k / (ρ · a)"
                ]
            },
            {
                "heading": "2. Правило «6 – 4 – 2» для фактора формы k",
                "height": 2.50,
                "bullets": [
                    "Фактор формы k строго зависит от размерности наноструктуры:",
                    "  - k = 6 — 3D-наночастицы (сфера, куб); k = 4 — 1D-нити; k = 2 — 2D-пленки.",
                    "  [Ф] Избыточная свободная энергия границы:  ΔG_s = σ · S ∝ 1 / a"
                ]
            }
        ],
        "fig": "fig_02_specific_surface.png",
        "fig_desc": "График роста удельной поверхности S_уд(a) и доли поверхностных атомов",
        "takeaway": "При дроблении вещества от 1 см до наночастиц 10 нм площадь поверхности и поверхностная энергия Гиббса возрастают в 1 000 000 раз.",
        "notes": (
            "1. Геометрический взрыв поверхности: При дроблении макроскопического кубика золота 1 см³ до наночастиц 10 нм суммарная площадь поверхности возрастает с 6 см² до 600 м².\n"
            "2. Фактор формы k: Из размерных соображений отношение S/V равно 6/a для 3D-кубика и сферы, 4/d для длинного 1D-цилиндра и 2/h для тонкой 2D-пленки.\n"
            "3. Поверхностные атомы: При диаметре менее 2–3 нм свыше 50–70% всех атомов находятся на межфазной границе, определяя уникальную реакционную способность наноматериалов."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 5
    # -------------------------------------------------------------------------
    {
        "num": 5,
        "layout": "A",
        "title": "Классификация дисперсных систем: размер, агрегатное состояние и лиофильность",
        "subtitle": "Блок 1. Систематика коллоидных и нанодисперсных материалов",
        "cards": [
            {
                "heading": "1. Классификация по размеру дисперсной фазы",
                "height": 2.40,
                "bullets": [
                    "Нанодисперсные (коллоидные) системы занимают фундаментальный диапазон 1–100 нм.",
                    "Грубодисперсные (a > 10 мкм) быстро седиментируют; истинные растворы (a < 1 нм) однофазны.",
                    "  [Ф] a = 1–100 нм (10⁻⁹–10⁻⁷ м): нанозоли, квантовые точки, мицеллы"
                ]
            },
            {
                "heading": "2. Лиофильные vs Лиофобные системы (критерий Ребиндера)",
                "height": 2.50,
                "bullets": [
                    "Лиофильные (поверхностно-активные вещества (ПАВ), биополимеры): σ ≈ 0, термодинамически устойчивы (ΔG_обр < 0).",
                    "Лиофобные нанозоли (Au, Ag, Fe(OH)₃): высокое натяжение σ ≫ 0, термодинамически нестабильны:",
                    "  [Ф] ΔG_обр = σ · S > 0   (существуют исключительно благодаря ДЭС)"
                ]
            }
        ],
        "fig": "fig_03_classification_matrix.png",
        "fig_desc": "Матрица 3x3 классов дисперсных систем по агрегатному состоянию ДФ и ДС",
        "takeaway": "Неорганические нанозоли (Au, Ag, Fe(OH)₃) являются лиофобными системами (ΔG > 0) и требуют электростатического барьера ДЭС для предотвращения коагуляции.",
        "notes": (
            "1. Диапазон коллоидов: Фундаментальный размерный интервал 1–100 нм объединяет классическую коллоидную химию и современную нанофизику.\n"
            "2. Критерий Ребиндера: Лиофильные системы самопроизвольно диспергируют за счет теплового движения, если поверхностное натяжение ничтожно мало (σ < σ_кр). Лиофобные системы требуют затраты работы и термодинамически метастабильны.\n"
            "3. Матрица дисперсности: Рассмотрены системы с твердой, жидкой и газовой дисперсной фазой и средой, включая твердые пористые матрицы."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 6
    # -------------------------------------------------------------------------
    {
        "num": 6,
        "layout": "B",
        "title": "От золя к гелю, ксерогелю и аэрогелю: эволюция связности наносистемы",
        "subtitle": "Блок 1. Золь-гель переход и капиллярная инженерия нанопористых материалов",
        "top_cards": [
            {
                "left": 0.5, "width": 6.0, "height": 1.42,
                "heading": "1. Золь (свободнодисперсный) → Гель (связнодисперсный)",
                "bullets": [
                    "Золь: изолированные наночастицы совершают броуновское движение в растворе.",
                    "Гель: агрегация и сшивка формируют единый перколяционный 3D-каркас с запертой средой."
                ]
            },
            {
                "left": 6.8, "width": 6.033, "height": 1.42,
                "heading": "2. Капиллярный коллапс Лапласа vs Сверхкритическая сушка",
                "bullets": [
                    "Сушка испарением: капиллярное давление P_L = 2σ/r (до сотен МПа) сминает каркас в ксерогель.",
                    "Сверхкритическая сушка (T > T_c, P > P_c): σ = 0 исключает мениски → пористый аэрогель (>95% пор)."
                ]
            }
        ],
        "fig": "fig_04_sol_gel_xerogel.png",
        "fig_desc": "Полноширинная 4-панельная схема Золь -> Гель -> Ксерогель и Аэрогель",
        "takeaway": "Управление капиллярным давлением Лапласа при сушке геля определяет переход либо в уплотненный ксерогель, либо в ультрапористый аэрогель.",
        "notes": (
            "1. Переход золь–гель: Свободнодисперсный золь при достижении порога перколяции формирует непрерывную пространственную сетку — гель.\n"
            "2. Капиллярный коллапс Лапласа: При обычной сушке в нанопорах радиусом r ≈ 2–5 нм мениски жидкости создают огромное капиллярное разрежение P_L = 2σ/r (до 200–500 МПа), разрушающее поры и приводящее к образованию плотного ксерогеля.\n"
            "3. Сверхкритическая сушка: Перевод растворителя в сверхкритическое состояние устраняет фазовую границу жидкость–пар (σ = 0). Отсутствие менисков позволяет сохранить исходный объем пор до 95–99% в аэрогеле."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 7
    # -------------------------------------------------------------------------
    {
        "num": 7,
        "layout": "A",
        "title": "Цеолиты — регулярные микропористые кристаллы и молекулярные сита",
        "subtitle": "Блок 1. Кристаллические связнодисперсные системы с калиброванными наноканалами",
        "cards": [
            {
                "heading": "1. Кристаллическая природа микропористых цеолитов",
                "height": 2.40,
                "bullets": [
                    "Каркас из тетраэдров [SiO₄]⁴⁻ и [AlO₄]⁵⁻ образует регулярную 3D-систему субнанометровых каналов.",
                    "Изоморфное замещение Si⁴⁺ → Al³⁺ сообщает каркасу отрицательный заряд, удерживающий катионы (Na⁺, Ca²⁺).",
                    "  [Ф] d_окна = 0.3 – 1.0 нм   (строго монодисперсные субнанометровые поры)"
                ]
            },
            {
                "heading": "2. Молекулярные сита и матричные нанореакторы",
                "height": 2.50,
                "bullets": [
                    "Молекулярные сита: точная кинетическая сепарация молекул по их критическому диаметру.",
                    "Гетерогенный нанокатализ: высокая плотность активных кислотных центров в объеме пор.",
                    "Матричный синтез (нанореакторы): пространственно ограниченный рост квантовых точек строго заданного размера."
                ]
            }
        ],
        "fig": "fig_05_zeolites.png",
        "fig_desc": "Схема селективного окна цеолита и график монодисперсного распределения пор",
        "takeaway": "Цеолиты сочетают удельную площадь до 1000 м²/г с кристаллографической монодисперсностью входных окон (0.3–1.0 нм), функционируя как сита и нанореакторы.",
        "notes": (
            "1. Строение цеолитов: В отличие от аморфного силикагеля с широким распределением пор по размерам (2–50 нм), цеолит — это кристалл. Диаметр входных окон жестко зафиксирован параметрами кристаллической решетки алюмосиликата.\n"
            "2. Молекулярные сита: Если диаметр окна составляет 0.45 нм, линейный н-алкан (диаметр 0.43 нм) диффундирует внутрь каналов, а разветвленный изоалкан (0.56 нм) не может войти в пору.\n"
            "3. Цеолиты как нанореакторы: Полости цеолитов служат шаблонами для синтеза изолированных квантовых точек и субнанометровых металлических кластеров с жестким пространственным ограничением роста."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 8
    # -------------------------------------------------------------------------
    {
        "num": 8,
        "layout": "A",
        "title": "Строение коллоидной мицеллы и правило Панета–Фаянса–Пескова",
        "subtitle": "Блок 2. Строение мицеллы неорганических веществ и двойной электрический слой",
        "cards": [
            {
                "heading": "1. Правило Панета–Фаянса: селективный заряд ядра",
                "height": 2.25,
                "bullets": [
                    "Кристаллическое ядро избирательно адсорбирует из раствора только «РОДНЫЕ» ионы (потенциалопределяющие ионы — ПОИ):",
                    "  - те ионы, которые входят в состав самой решетки ядра;",
                    "  - и при этом находятся в растворе в ИЗБЫТКЕ!",
                    "Именно знак заряда ПОИ определяет знак заряда всей гранулы."
                ]
            },
            {
                "heading": "2. Алгоритм сборки мицеллы за 4 шага (Навык №1)",
                "height": 2.65,
                "bullets": [
                    "Шаг 1 (Агрегат): нерастворимое кристаллическое ядро [M]_m (заряд 0).",
                    "Шаг 2 (Ядро): сажаем n родных ионов из избытка → [M]_m · n ПОИ⁺.",
                    "Шаг 3 (Гранула): добавляем (n−x) противоионов (ПИ) плотного слоя в скобки { ... }^(x+) — гранула ЗАРЯЖЕНА!",
                    "Шаг 4 (Мицелла): пишем x противоионов диффузного слоя за скобкой:",
                    "  [Ф] { [M]_m · n ПОИ⁺ · (n − x) ПИ⁻ }^(x+) · x ПИ⁻   (заряд = 0!)"
                ]
            }
        ],
        "fig": "fig_06_micelle_anatomy.png",
        "fig_desc": "Концентрическая диаграмма анатомии коллоидной мицеллы",
        "takeaway": "Гранула (коллоидная частица внутри плоскости скольжения) обладает нескомпенсированным зарядом ±x, но вся мицелла в целом строго электронейтральна!",
        "notes": (
            "1. Аналогия «Знаменитость в толпе фанатов»: Агрегат [M]_m — сцена; ПОИ — рок-звезда на сцене, задающая тон (заряд); плотный слой (n−x) — охрана вплотную к сцене (вместе со звездой это Гранула в фигурных скобках); диффузный слой x — фанаты на площади вокруг.\n"
            "2. Главная ловушка на зачете: «Какой заряд у мицеллы?» Правильный ответ: НУЛЕВОЙ! Заряжена только ГРАНУЛА (то, что внутри фигурных скобок), а вся мицелла электронейтральна."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 9
    # -------------------------------------------------------------------------
    {
        "num": 9,
        "layout": "A",
        "title": "Формулы мицелл: перезарядка золя AgI и гидрозоль Fe(OH)₃",
        "subtitle": "Блок 2. Практика составления мицеллярных формул неорганических гидрозолей",
        "cards": [
            {
                "heading": "1. Золь AgI: как избыток реагента меняет знак частицы",
                "height": 2.35,
                "bullets": [
                    "Реакция: AgNO₃ + KI → AgI↓ + KNO₃. В решетку AgI входят Ag⁺ и I⁻.",
                    "А) В избытке KI (лишние ионы I⁻ → ПОИ = I⁻, гранула «−»):",
                    "  [Ф] { [AgI]_m · n I⁻ · (n − x) K⁺ }^(x−) · x K⁺",
                    "Б) В избытке AgNO₃ (лишние ионы Ag⁺ → ПОИ = Ag⁺, гранула «+»):",
                    "  [Ф] { [AgI]_m · n Ag⁺ · (n − x) NO₃⁻ }^(x+) · x NO₃⁻"
                ]
            },
            {
                "heading": "2. Классический золь Fe(OH)₃ при гидролизе в кипящей воде",
                "height": 2.55,
                "bullets": [
                    "Гидролиз при 100 °C:  FeCl₃ + 3 H₂O → Fe(OH)₃↓ + 3 HCl.",
                    "Стабилизатор FeOCl диссоциирует:  FeOCl ⇄ FeO⁺ (ПОИ) + Cl⁻ (ПИ).",
                    "Катион FeO⁺ родной ядру → гранула Fe(OH)₃ заряжена ПОЛОЖИТЕЛЬНО:",
                    "  [Ф] { [Fe(OH)₃]_m · n FeO⁺ · (n − x) Cl⁻ }^(x+) · x Cl⁻"
                ]
            }
        ],
        "fig": "fig_07_agi_feoh3_micelles.png",
        "fig_desc": "Двухпанельная схема мицелл отрицательного золя AgI и положительного золя Fe(OH)3",
        "takeaway": "Гранула гидрозоля Fe(OH)₃ заряжена ПОЛОЖИТЕЛЬНО за счет адсорбции катионов FeO⁺, поэтому коагуляцию этого золя вызывают АНИОНЫ электролита!",
        "notes": (
            "1. Отработка Навыка №1: На примере AgI видно, что одно и то же вещество может быть и отрицательным золем (в избытке KI), и положительным (в избытке AgNO₃).\n"
            "2. Разбор золя Fe(OH)₃ (карточка 2): Классическая учебная задача! Осадок Fe(OH)₃, стабилизатор FeOCl, потенциалопределяющий ион — катион оксожелеза FeO⁺ (или Fe³⁺), противоионы — хлориды Cl⁻.\n"
            "3. Ключ к задачам на коагуляцию: Раз гранула заряжена плюсом (x+), то осаждать (коагулировать) ее будут отрицательные ионы (анионы) добавляемых солей!"
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 10
    # -------------------------------------------------------------------------
    {
        "num": 10,
        "layout": "A",
        "title": "Физические модели ДЭС: от конденсатора Гельмгольца к теории Гуи–Чепмена",
        "subtitle": "Блок 2. Эволюция представлений о строении двойного электрического слоя",
        "cards": [
            {
                "heading": "1. Модель Гельмгольца (1879) — «плоский конденсатор»",
                "height": 2.35,
                "bullets": [
                    "Противоионы притянуты к стенке в одну шеренгу на расстоянии радиуса иона d.",
                    "Потенциал φ(x) падает внутри зазора d строго по прямой линии:",
                    "  [Ф] φ(x) = φ₀ · (1 − x / d),     C_H = ε · ε₀ / d = const",
                    "Минус модели: забыта температура T! Не может объяснить электрофорез."
                ]
            },
            {
                "heading": "2. Модель Гуи–Чепмена (1910) — «диффузное облако»",
                "height": 2.55,
                "bullets": [
                    "Конкуренция двух сил: кулоновское притяжение к стенке (z·e·φ) против теплового броуновского разбрасывания ионов (k_B T).",
                    "Концентрация ионов вокруг частицы подчиняется закону Больцмана:",
                    "  [Ф] n(x) = n₀ · exp( − z · e · φ(x) / [k_B · T] )",
                    "Вместо плоской шеренги образуется протяженная ионная атмосфера."
                ]
            }
        ],
        "fig": "fig_08_helmholtz_vs_gouy.png",
        "fig_desc": "Сравнение расположения ионов и профилей потенциала в моделях Гельмгольца и Гуи–Чепмена",
        "takeaway": "Модель Гуи–Чепмена ввела в электростатику поверхности температуру T: тепловое движение размывает слой противоионов в диффузную ионную атмосферу.",
        "notes": (
            "1. Аналогия с атмосферой Земли: Гравитация тянет воздух к земле, а тепловое движение k_B T разбрасывает молекулы вверх — получается воздушная атмосфера. Точно так же вокруг наночастицы кулоновское притяжение и тепловой хаос создают диффузную ионную атмосферу Гуи–Чепмена!\n"
            "2. На графике внизу: Синий пунктир — резкий линейный обрыв потенциала в плоском конденсаторе Гельмгольца; красная кривая — плавная экспонента Гуи–Чепмена."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 11
    # -------------------------------------------------------------------------
    {
        "num": 11,
        "layout": "A",
        "title": "Закон спада потенциала и дебаевская толщина ДЭС λ_D = κ⁻¹",
        "subtitle": "Блок 2. Как концентрация и заряд соли сжимают защитную ионную «шубу»",
        "cards": [
            {
                "heading": "1. Экспоненциальный спад потенциала в диффузном слое",
                "height": 2.35,
                "bullets": [
                    "Из уравнения Пуассона–Больцмана следует: потенциал вглубь раствора затухает по экспоненте:",
                    "  [Ф] φ(x) = φ₀ · exp( −x / λ_D ) = φ₀ · exp( −κ · x )",
                    "Толщина ДЭС (длина Дебая λ_D = κ⁻¹) — это расстояние, на котором потенциал частицы падает в e ≈ 2.72 раза."
                ]
            },
            {
                "heading": "2. Главный рычаг управления: закон сжатия ДЭС",
                "height": 2.55,
                "bullets": [
                    "Толщина ионной «шубы» λ_D обратно пропорциональна заряду иона z и корню из концентрации электролита c:",
                    "  [Ф] λ_D ∝ 1 / (z · √c)   [в воде: λ_D ≈ 0.304 / (z·√c) нм]",
                    "Рост концентрации соли c в 100 раз сжимает толщину ДЭС ровно в 10 раз (с 30.4 нм до 3.04 нм)!"
                ]
            }
        ],
        "fig": "fig_09_debye_screening.png",
        "fig_desc": "Аналитические профили потенциала φ(x) при разной ионной силе и распределение ионов",
        "takeaway": "Толщина диффузного слоя λ_D обратно пропорциональна валентности противоиона z и корню из концентрации √c: добавление соли резко сжимает ДЭС.",
        "notes": (
            "1. Никакой лишней громоздкости: Нам важен физический закон λ_D ∝ 1 / (z·√c).\n"
            "2. Аналогия с зимним пуховиком в вакуумном пакете: В чистой воде (c = 10⁻⁴ М, синяя кривая) ионная шуба вокруг наночастицы пушистая (λ_D = 30.4 нм). Капнули соли до 10⁻² М (красная кривая) — шуба сдулась в 10 раз до 3 нм, и частицы оголились для слипания!"
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 12
    # -------------------------------------------------------------------------
    {
        "num": 12,
        "layout": "A",
        "title": "Объединенная модель ДЭС О. Штерна (1924): плотный и диффузный слои",
        "subtitle": "Блок 2. Современная физическая теория двойного электрического слоя",
        "cards": [
            {
                "heading": "1. Синтез двух моделей: плоскость Штерна x = δ",
                "height": 2.40,
                "bullets": [
                    "Ионы — не математические точки! Они имеют реальный радиус δ ≈ 0.3–0.5 нм.",
                    "Штерн разделил ДЭС на две последовательные зоны:",
                    "  - Плотный слой Штерна (0 ≤ x ≤ δ): прямая линия φ₀ → φ_δ;",
                    "  - Диффузный слой Гуи (x > δ): экспонента φ(x) = φ_δ · exp(−κ(x − δ))."
                ]
            },
            {
                "heading": "2. Специфическая адсорбция и перезарядка наночастицы",
                "height": 2.50,
                "bullets": [
                    "Два слоя работают как два последовательных конденсатора:",
                    "  [Ф] 1 / C_ДЭС = 1 / C_плотного + 1 / C_диффузного",
                    "Химическое прилипание многозарядных противоионов (Al³⁺, Th⁴⁺) в плотном слое может поменять знак потенциала φ_δ (кривая 3):",
                    "  [Ф] φ₀ > 0,   но   φ_δ < 0   (перезарядка поверхности!)"
                ]
            }
        ],
        "fig": "fig_10_stern_model.png",
        "fig_desc": "Аналитический график потенциала в модели Штерна для трех режимов адсорбции",
        "takeaway": "Модель Штерна разделяет падение потенциала на адсорбционный скачок (φ₀ → φ_δ) и диффузный хвост, объясняя феномен перезарядки наночастиц.",
        "notes": (
            "1. Суть модели Штерна: Ионы не могут подойти к стенке ближе своего радиуса δ (серая полоса на графике). Внутри δ — плоский конденсатор Гельмгольца, снаружи — диффузное облако Гуи.\n"
            "2. Феномен перезарядки (красная кривая 3): Если в раствор с положительными частицами (φ₀ = +80 мВ) добавить многозарядные анионы, они набьются в слой Штерна сверх меры и поменяют знак потенциала снаружи на минус (φ_δ = −32 мВ)!"
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 13
    # -------------------------------------------------------------------------
    {
        "num": 13,
        "layout": "A",
        "title": "Плоскость скольжения и электрокинетический дзета-потенциал (ζ)",
        "subtitle": "Блок 3. Дзета-потенциал и диагностика стабильности наноколлоидов (Навык №2)",
        "cards": [
            {
                "heading": "1. Плоскость скольжения и смысл ζ-потенциала",
                "height": 2.35,
                "bullets": [
                    "При движении наночастицы плотный слой и тонкая гидратная оболочка воды движутся вместе с ядром (это наша гранула).",
                    "Плоскость скольжения (x = x_s) — граница отрыва подвижной жидкости.",
                    "Дзета-потенциал (ζ) — потенциал ДЭС ровно на плоскости скольжения:",
                    "  [Ф] ζ = φ(x_s),     причем всегда   |ζ| ≤ |φ_δ| < |φ₀|"
                ]
            },
            {
                "heading": "2. Правило «Магические 30 мВ» (Навык диагностики №2)",
                "height": 2.55,
                "bullets": [
                    "|ζ| > 30 мВ — СТАБИЛЬНЫЙ ЗОЛЬ! Частицы сильно отталкиваются (у цитратного золя золота ζ ≈ −40 мВ).",
                    "15 < |ζ| < 30 мВ — пограничная зона, начало медленного слипания.",
                    "|ζ| < 15 мВ — БЫСТРАЯ КОАГУЛЯЦИЯ и выпадение осадка.",
                    "  [Ф] ζ = 0 мВ — изоэлектрическая точка (ИЭТ, мгновенная агрегация)"
                ]
            }
        ],
        "fig": "fig_11_zeta_potential.png",
        "fig_desc": "График падения дзета-потенциала ζ на плоскости скольжения при сжатии ДЭС",
        "takeaway": "Индифферентный электролит не меняет потенциал ядра φ₀, но из-за сжатия экспоненты φ(x) резко снижает ζ-потенциал на плоскости скольжения до критического (< 15 мВ).",
        "notes": (
            "1. Как померить потенциал наночастицы: Вольтметром ткнуть нельзя, но можно включить поле и померить скорость движения гранулы — она зависит от потенциала на линии отрыва жидкости (ζ-потенциала).\n"
            "2. Навык №2 («Магические 30 мВ»): Смотрим на модуль |ζ|. Если |ζ| > 30 мВ (+35 или −40 мВ) — золь живет месяцами. Если добавили соль (переход от зеленой кривой 1 к красной 3 на графике), экспонента прижалась к стенке, ζ упал ниже 15 мВ — золь гибнет!"
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 14
    # -------------------------------------------------------------------------
    {
        "num": 14,
        "layout": "A",
        "title": "Четыре электрокинетических явления: связь движения и электрического поля",
        "subtitle": "Блок 3. Открытие Ф.Ф. Рейсса (1809) и нанотехнологические применения",
        "cards": [
            {
                "heading": "1. Прямые явления: Поле E → Движение",
                "height": 2.40,
                "bullets": [
                    "1) Электрофорез: заряженные наночастицы (гранулы) плывут в неподвижной жидкости к электроду.",
                    "  - Применение: измерение ζ-потенциала, осаждение нанопокрытий (EPD).",
                    "2) Электроосмос: жидкость течет сквозь неподвижный пористый каркас или капилляр под действием поля E.",
                    "  - Применение: микронасосы без движущихся частей в чипах Lab-on-a-Chip."
                ]
            },
            {
                "heading": "2. Обратные явления: Движение → Генерация ЭДС (Δφ)",
                "height": 2.50,
                "bullets": [
                    "3) Потенциал седиментации: оседающие под действием гравитации заряженные частицы создают разность потенциалов между верхом и дном.",
                    "4) Потенциал течения: продавливание жидкости давлением ΔP сквозь пористую мембрану сносит ионы ДЭС и генерирует напряжение:",
                    "  [Ф] Δφ_теч  ∝  (ζ / η) · ΔP"
                ]
            }
        ],
        "fig": "fig_12_electrokinetic_phenomena.png",
        "fig_desc": "Четырехпанельная схема (2x2) электрофореза, электроосмоса, потенциалов седиментации и течения",
        "takeaway": "Все 4 электрокинетических явления обусловлены механическим сдвигом диффузного слоя по плоскости скольжения и прямо пропорциональны ζ-потенциалу.",
        "notes": (
            "1. Простая симметрия 2×2 без зубрежки: В верхнем ряду мы подключаем батарейку E — двигаются либо частицы (электрофорез), либо вода в порах (электроосмос). В нижнем ряду мы двигаем систему механически (гравитацией или насосом ΔP) — и на вольтметре возникает ЭДС!\n"
            "2. Исторический приоритет: Оба прямых явления открыл в Москве профессор Ф.Ф. Рейсс в 1809 году."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 15
    # -------------------------------------------------------------------------
    {
        "num": 15,
        "layout": "A",
        "title": "Как из скорости электрофореза найти ζ-потенциал: роль размера κr",
        "subtitle": "Блок 3. Влияние отношения радиуса наночастицы к толщине ионной шубы (κr = r / λ_D)",
        "cards": [
            {
                "heading": "1. Электрофоретическая подвижность и формула Генри",
                "height": 2.35,
                "bullets": [
                    "В электрическом поле E сила Кулона уравновешивается трением Стокса, и частица плывет с постоянной подвижностью u_e = v / E:",
                    "  [Ф] u_e = v / E = [ (2 · ε · ε₀ · ζ) / (3 · η) ] · f(κr)",
                    "Коэффициент Генри f(κr) зависит от отношения радиуса частицы r к толщине ее ионной шубы λ_D (где κr = r / λ_D)."
                ]
            },
            {
                "heading": "2. Переходная размерная область теории Генри (κr ~ 1–5)",
                "height": 2.55,
                "bullets": [
                    "Малая частица в толстой шубе (r ≪ λ_D, предел Хюккеля): f = 1.0.",
                    "Крупная частица в тонкой шубе (r ≫ λ_D, предел Смолуховского): f = 1.5 (скорость в 1.5 раза выше при том же ζ!).",
                    "Водные нанозоли (r ~ 10 нм, λ_D ~ 4 нм ⇒ κr ≈ 2.5) лежат ровно посередине склона — нужна полная формула Генри!"
                ]
            }
        ],
        "fig": "fig_13_henry_function.png",
        "fig_desc": "Аналитический график функции Генри f(κr) от 1.0 до 1.5",
        "takeaway": "Для наночастиц в водных золях (r ~ 5–20 нм, λ_D ~ 3–10 нм) параметр κr ~ 1–5 лежит в переходной зоне, поэтому для точного расчета ζ необходима формула Генри!",
        "notes": (
            "1. Физический смысл без перегрузки: Когда прибор померил скорость наночастицы v, как пересчитать ее в милливольты ζ? Все зависит от того, кто больше — сама частица r или ее шуба λ_D.\n"
            "2. На графике справа: Между левой полкой Хюккеля (1.0) и правой полкой Смолуховского (1.5) разница в полтора раза! Наночастицы золота и железа (r ~ 10 нм) живут прямо на переходном склоне (оранжевая точка)."
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 16
    # -------------------------------------------------------------------------
    {
        "num": 16,
        "layout": "A",
        "title": "Седиментационная устойчивость и закон Лапласа–Перрена",
        "subtitle": "Блок 4. Баланс броуновской диффузии и гравитационного оседания Стокса (r ≤ 10 нм)",
        "cards": [
            {
                "heading": "1. Два вида устойчивости коллоидов (Н.П. Песков)",
                "height": 2.30,
                "bullets": [
                    "Седиментационная: частицы не оседают на дно под силой тяжести.",
                    "Агрегативная: частицы не слипаются при столкновениях (сохраняют r).",
                    "Скорость оседания одиночного шарика в жидкости (закон Стокса):",
                    "  [Ф] v_сед = [ 2 · r² · (ρ − ρ₀) · g ] / (9 · η)  ∝  r²"
                ]
            },
            {
                "heading": "2. Дуэль гравитации и теплового движения (закон Перрена)",
                "height": 2.60,
                "bullets": [
                    "Оседанию вниз мешает тепловое броуновское движение (k_B T), подбрасывающее наночастицы вверх.",
                    "Характерная высота столба золя h_e обратно пропорциональна КУБУ радиуса частицы:",
                    "  [Ф] h_e = (3 · k_B · T) / (4 · π · r³ · Δρ · g)  ∝  1 / r³",
                    "Вывод: пока частицы малы (r < 10 нм), они не осядут никогда!"
                ]
            }
        ],
        "fig": "fig_14_sedimentation_perren.png",
        "fig_desc": "Аналитические профили концентрации наночастиц золота n(h)/n0 по высоте кюветы",
        "takeaway": "За счет зависимости h_e ∝ r⁻³ наночастицы золота (r ≤ 10 нм) седиментационно абсолютно устойчивы, пока не произойдет их агрегация!",
        "notes": (
            "1. Загадка коллоидного золота: Золото почти в 20 раз тяжелее воды, но рубиновый гидрозоль (r = 5 нм, синяя кривая) абсолютно однороден по высоте пробирки!\n"
            "2. Сила куба радиуса (1/r³): Стоит частицам потерять заряд и слипнуться всего в 3 раза по радиусу (с 5 до 16 нм, красная кривая), как куб радиуса r³ вырастает в 3.2³ ≈ 33 раза! Тепловое движение проигрывает, и золото камнем падает на дно. Значит, главное — не дать частицам слипнуться!"
        )
    },
    # -------------------------------------------------------------------------
    # Слайд 17 (Технологическое применение: очищено от упоминаний ЛР)
    # -------------------------------------------------------------------------
    {
        "num": 17,
        "layout": "A",
        "title": "Технологическое применение: коллоидная диагностика и промышленный синтез",
        "subtitle": "Сквозное резюме темы «Термодинамика дисперсных систем и коллоидных растворов»",
        "cards": [
            {
                "heading": "Прикладной модуль №1: Диагностика нанозолей (Au)",
                "height": 2.45,
                "bullets": [
                    "Цитратный синтез и плазмонный резонанс: монодисперсные наночастицы Au (d ≈ 15–20 нм) стабилизированы адсорбцией цитрат-ионов.",
                    "Электрокинетический мониторинг: дзета-потенциал (ζ ≈ −40 мВ) формирует защитный барьер; сжатие ДЭС электролитом вызывает оптический сдвиг 520 → 650 нм.",
                    "Диагностические методы: измерение подвижности в электрофорезе и динамическое рассеяние света (ДРС) для контроля агрегации."
                ]
            },
            {
                "heading": "Прикладной модуль №2: Промышленный синтез (Fe(OH)₃)",
                "height": 2.50,
                "bullets": [
                    "Конденсационный гидролиз прекурсоров: синтез золя Fe(OH)₃ со стабилизатором FeOCl (катионы FeO⁺ сообщают грануле положительный заряд).",
                    "Технологический барьер коагуляции: нейтрализация заряда гранулы анионами по закону шестой степени Дерягина–Ландау (правило Шульце–Гарди: 1 : 1/64 : 1/729).",
                    "Промышленное применение: прецизионный коагуляционный контроль в водоочистке, мембранной сепарации и производстве нанокомпозитов."
                ]
            }
        ],
        "fig": "fig_17_colloid_applications.png",
        "fig_desc": "Сводная инфографика прикладных модулей коллоидной диагностики и промышленного синтеза наносистем",
        "takeaway": "Коллоидная диагностика и промышленный синтез опираются на фундаментальные законы ДЭС и теории ДЛФО: от плазмонной стабильности золота до коагуляционного барьера z⁻⁶.",
        "notes": (
            "1. Прикладной модуль №1 (коллоидная диагностика): Синтез золя золота по методу Туркевича дает отрицательно заряженную гранулу (ζ ≈ −40 мВ). Высокий электростатический барьер обеспечивает устойчивость. При добавлении солей сжатие ДЭС вызывает агрегацию и спектральный сдвиг плазмонного пика 520 → 650 нм (золь синеет).\n"
            "2. Прикладной модуль №2 (промышленный контроль коагуляции): Синтез гидрозоля Fe(OH)₃ формирует положительно заряженную гранулу с ПОИ FeO⁺. Коагуляция инициируется анионами-противоионами, а пороги коагуляции подчиняются закону шестой степени Дерягина–Ландау (1 : 1/64 : 1/729 для z = 1, 2, 3).\n"
            "3. Анонс Лекции №4: В следующей лекции мы перейдем к термодинамике адсорбции на твердых поверхностях (изотермы Ленгмюра и БЭТ), краевому углу смачивания и атомным механизмам роста тонких пленок."
        )
    }
]


# ==============================================================================
# 4. Сборщик презентации сравнительных вариаций (14 слайдов)
# ==============================================================================

def build_comparative_deck(output_path: str = OUT_VARIATIONS_PPTX):
    """
    Формирует сравнительную презентацию lecture_03_comparative_variations.pptx:
    - Слайд 1: Титульный лист сравнительного обзора
    - Слайды 2–4: Вариация 1 (Classic SUAI Corporate: Титул, Проблемы, Разделитель)
    - Слайды 5–7: Вариация 2 (Modern Scientific Infographic: Титул, Проблемы, Разделитель)
    - Слайды 8–10: Вариация 3 (Deep Navy Hero: Титул, Проблемы, Разделитель)
    - Слайд 11: Сравнительная матрица Слайда 1 (Титульные листы T1 vs T2 vs T3)
    - Слайд 12: Сравнительная матрица Слайда 2 (Проблемный вводный P1 vs P2 vs P3)
    - Слайд 13: Сравнительная матрица Слайда 3 (Разделитель первой проблемы S1 vs S2 vs S3)
    - Слайд 14: Итоговая матрица рекомендаций и стандарты курса ГУАП
    """
    prs = create_base_presentation()

    # Слайд 1: Титульный лист сравнительного деки
    create_title_slide(
        prs,
        title="Сравнительный анализ дизайн-вариаций оформления первых трех слайдов",
        subtitle="Курс «Физические основы нанотехнологий» • Лекция №3 • ГУАП",
        course_info="СРАВНИТЕЛЬНАЯ ЭКСПЕРТИЗА МАКЕТОВ • СЕМЕСТР 4 • ВЕХА M4",
        teacher_info="Разработчик курса: доцент Попов Д.А.",
        dept_info="Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026",
        style="classic",
        notes="Презентация предназначена для экспертного сопоставления трех альтернативных стилистических вариаций первых трех слайдов Лекции №3."
    )

    # Добавляем последовательно 3 вариации по 3 слайда (Слайды 2–10)
    add_variation_1_slides(prs)
    add_variation_2_slides(prs)
    add_variation_3_slides(prs)

    # ---------------------------------------------------------
    # Слайд 11: Сравнительная матрица для Слайда 1 (Титул)
    # ---------------------------------------------------------
    create_comparative_matrix_slide(
        prs,
        title="Сравнительный анализ: Слайд 1 (Титульный лист университета)",
        subtitle="Сопоставление вариаций T1 (Classic), T2 (Modern Infographic) и T3 (Deep Navy Hero)",
        variations=[
            {
                "name": "Вариант T1: Classic SUAI",
                "preview_path": get_variation_preview_path("slide_02_preview.png"),
                "badge": "Корпоративный стандарт",
                "badge_color": SUAI_PALETTE["BLUE"],
                "criteria": [
                    "Бренд ГУАП: белый фон, оригинальный логотип",
                    "Типографика: строгий Arial Bold, иерархия Navy",
                    "Реквизиты: лектор, кафедра и курс указаны строго 1 раз",
                    "Эргономика: оптимально для светлых аудиторий",
                ],
            },
            {
                "name": "Вариант T2: Modern Infographic",
                "preview_path": get_variation_preview_path("slide_05_preview.png"),
                "badge": "Инженерный модуль",
                "badge_color": SUAI_PALETTE["GREEN"],
                "criteria": [
                    "Бренд ГУАП: контейнерная плашка #F4F7FA",
                    "Инфографика: акцентные бейджи курса и статуса",
                    "Реквизиты: выделенная карточка лектора",
                    "Эргономика: высокий визуальный интерес студентов",
                ],
            },
            {
                "name": "Вариант T3: Deep Navy Hero",
                "preview_path": get_variation_preview_path("slide_08_preview.png"),
                "badge": "Премиальный темный",
                "badge_color": SUAI_PALETTE["DEEP_NAVY"],
                "criteria": [
                    "Бренд ГУАП: глубокий Navy #002C5F, белый логотип",
                    "Контраст: циановые акценты #00BEF3 на темном",
                    "Реквизиты: контрастное серебряное начертание",
                    "Эргономика: максимальная видимость в поточных залах",
                ],
            },
        ],
        takeaway="Все 3 вариации строго соблюдают правило Single-Point Occurrence и брендбук ГУАП.",
        notes="Сравнение показывает, что вариант T1 обеспечивает максимальную академическую строгость, а T3 — наивысший контраст."
    )

    # ---------------------------------------------------------
    # Слайд 12: Сравнительная матрица для Слайда 2 (Проблемы)
    # ---------------------------------------------------------
    create_comparative_matrix_slide(
        prs,
        title="Сравнительный анализ: Слайд 2 (Шесть технологических барьеров)",
        subtitle="Сопоставление подходов к сетке 2x3 карточек, иконкам и аутентичному визуалу",
        variations=[
            {
                "name": "Вариант P1: Classic Grid",
                "preview_path": get_variation_preview_path("slide_03_preview.png"),
                "badge": "Равномерная сетка",
                "badge_color": SUAI_PALETTE["BLUE"],
                "criteria": [
                    "Карточки: единые плашки #F4F7FA с тонкими рамками",
                    "Иконки: 6 круглых 300 DPI маркеров проблем",
                    "Визуал: 16:9 сплит Faraday vs Fe3O4 справа",
                    "Лаконичность: 2-3 фразы, отсутствие Q&A формата",
                ],
            },
            {
                "name": "Вариант P2: Badge Infographic",
                "preview_path": get_variation_preview_path("slide_06_preview.png"),
                "badge": "Цветовое кодирование",
                "badge_color": SUAI_PALETTE["ORANGE"],
                "criteria": [
                    "Карточки: верхний цветной бейдж категории",
                    "Иконки: контрастный акцент на ключевой формуле",
                    "Визуал: академический оверлей верификации",
                    "Лаконичность: структурированная инженерная подача",
                ],
            },
            {
                "name": "Вариант P3: High-Contrast Hero",
                "preview_path": get_variation_preview_path("slide_09_preview.png"),
                "badge": "Высокий контраст",
                "badge_color": SUAI_PALETTE["DEEP_NAVY"],
                "criteria": [
                    "Карточки: Navy заголовки, четкий фокус на ΔGs",
                    "Иконки: глубокий темный баннер вывода",
                    "Визуал: акцент на парадоксе Фарадей/Fe3O4",
                    "Лаконичность: максимальная разгрузка от текста",
                ],
            },
        ],
        takeaway="Каждая вариация полностью исключает риторические вопросы и опирается на реальные научные данные.",
        notes="Вариация P2 дает максимальную скорость считывания формул благодаря индивидуальным цветным бейджам."
    )

    # ---------------------------------------------------------
    # Слайд 13: Сравнительная матрица для Слайда 3 (Разделитель)
    # ---------------------------------------------------------
    create_comparative_matrix_slide(
        prs,
        title="Сравнительный анализ: Слайд 3 (Открытие первой проблемы: Агрегация)",
        subtitle="Сопоставление центрированных макетов Layout S по фокусировке внимания",
        variations=[
            {
                "name": "Вариант S1: Classic Light",
                "preview_path": get_variation_preview_path("slide_04_preview.png"),
                "badge": "Светлый центрированный",
                "badge_color": SUAI_PALETTE["BLUE"],
                "criteria": [
                    "Иконка: крупный маркер 1.4x1.4 дюйма по центру",
                    "Тезис: строго 1–2 предложения (Бритва Оккама)",
                    "Дорожная карта: 3 светлых навигационных пилла",
                    "Эргономика: естественный переход от белых слайдов",
                ],
            },
            {
                "name": "Вариант S2: Modern Infographic",
                "preview_path": get_variation_preview_path("slide_07_preview.png"),
                "badge": "Акцентная плашка",
                "badge_color": SUAI_PALETTE["CYAN"],
                "criteria": [
                    "Иконка: двойное кольцо с циановым контуром",
                    "Тезис: выделенная контурная плашка в центре",
                    "Дорожная карта: нумерованные блоки [01]..[03]",
                    "Эргономика: динамичная инженерная визуализация",
                ],
            },
            {
                "name": "Вариант S3: Deep Navy Anchor",
                "preview_path": get_variation_preview_path("slide_10_preview.png"),
                "badge": "Темный когнитивный якорь",
                "badge_color": SUAI_PALETTE["DEEP_NAVY"],
                "criteria": [
                    "Иконка: светящийся циановый обод на Navy фоне",
                    "Тезис: чистый белый и светло-циановый текст",
                    "Дорожная карта: темные пиллы с яркими рамками",
                    "Эргономика: 100% переключение внимания аудитории",
                ],
            },
        ],
        takeaway="Слайд-разделитель Layout S задает монументальный ритм лекции и предотвращает рассеивание внимания.",
        notes="Темный вариант S3 идеален при переходе к сложным теоретическим разделам (ДЛФО, ДЭС)."
    )

    # ---------------------------------------------------------
    # Слайд 14: Итоговая сводная матрица рекомендаций курса
    # ---------------------------------------------------------
    slide14 = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide14,
        "Итоговая матрица соответствия стандартам и рекомендации для курса ГУАП",
        "Комплексная оценка вариаций по требованиям R1–R5 и условиям лекционных аудиторий"
    )

    col_w = 3.85
    start_x = 0.60
    gap = 0.29
    top_y = 1.35
    card_h = 5.05

    rec_data = [
        {
            "title": "Рекомендация: Базовый лекционный поток",
            "choice": "Вариация 1 (Classic SUAI)",
            "score": "Соответствие: 100% (R1–R5)",
            "color": SUAI_PALETTE["BLUE"],
            "points": [
                "Идеально для аудиторий с естественным светом (31-04а)",
                "Максимальная академическая строгость по ГОСТ",
                "Официальный векторный логотип ГУАП на белом фоне",
                "Гармонично сочетается со всеми 14 теоретическими слайдами",
                "Рекомендован как основной стандарт по умолчанию"
            ]
        },
        {
            "title": "Рекомендация: Инженерные практикумы",
            "choice": "Вариация 2 (Modern Infographic)",
            "score": "Соответствие: 100% (R1–R5)",
            "color": SUAI_PALETTE["GREEN"],
            "points": [
                "Цветные бейджи мгновенно разделяют 6 проблем",
                "Оптимально для семинаров и разбора задач на коагуляцию",
                "Высокая наглядность связки «проблема → формула»",
                "Усиленный акцент на прикладных модулях наноинженерии",
                "Рекомендован для междисциплинарных модулей"
            ]
        },
        {
            "title": "Рекомендация: Потоковые аудитории и конференции",
            "choice": "Вариация 3 (Deep Navy Hero)",
            "score": "Соответствие: 100% (R1–R5)",
            "color": SUAI_PALETTE["DEEP_NAVY"],
            "points": [
                "Максимальный проекционный контраст на больших экранах",
                "Слайд-разделитель служит мощным якорем внимания",
                "Премиальный университетский статус дисциплины",
                "Отличная читаемость белого текста с задних рядов",
                "Рекомендован для титула и ключевых узловых слайдов"
            ]
        }
    ]

    for idx, r in enumerate(rec_data):
        cx = start_x + idx * (col_w + gap)
        card = slide14.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE, Inches(cx), Inches(top_y), Inches(col_w), Inches(card_h)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
        card.line.color.rgb = r["color"]
        card.line.width = Pt(1.5)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.16)

        p0 = tf.paragraphs[0]
        p0.text = r["title"]
        p0.font.name = "Arial"
        p0.font.size = Pt(11)
        p0.font.bold = True
        p0.font.color.rgb = SUAI_PALETTE["MUTED_STEEL"]

        p1 = tf.add_paragraph()
        p1.text = r["choice"]
        p1.font.name = "Arial"
        p1.font.size = Pt(14)
        p1.font.bold = True
        p1.font.color.rgb = r["color"]
        p1.space_before = Pt(4)

        p2 = tf.add_paragraph()
        p2.text = r["score"]
        p2.font.name = "Arial"
        p2.font.size = Pt(10.5)
        p2.font.bold = True
        p2.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
        p2.space_before = Pt(3)
        p2.space_after = Pt(8)

        for pt in r["points"]:
            p = tf.add_paragraph()
            p.text = f"✓ {pt}"
            p.font.name = "Arial"
            p.font.size = Pt(10.5)
            p.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
            p.space_after = Pt(4)

    add_takeaway_banner(
        slide14,
        "ИТОГ: Вариация 1 интегрирована в основной дек курса; все 3 вариации доступны в сравнительной презентации."
    )
    set_speaker_notes(
        slide14,
        "Сводная рекомендация подтверждает полную валидацию всех требований технического задания R1–R5."
    )

    highlight_r3_abbreviations_in_deck(prs)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[SUCCESS] Сравнительная презентация успешно собрана: {output_path} ({len(prs.slides)} слайдов)")
    return prs


def highlight_r3_abbreviations_in_deck(prs: Presentation):
    """
    Автоматически выделяет полужирным шрифтом и фирменным цветом ГУАП
    ключевые терминологические аббревиатуры R3 в текстовых блоках слайдов и ячейках таблиц.
    """
    import re
    r3_terms = [
        "ДФ", "ДС", "ДЭС", "ДЛФО", "ПАВ", "ПОИ", "ПИ", "ККМ", "ИЭТ", "ПЭГ", "ПВП",
        "СЭМ", "ПЭМ", "АСМ", "ЛПР", "КТ", "ЭФО", "ДРС", "ЭЛС", "ζ-потенциал"
    ]
    pattern = re.compile(r"(\b(?:" + "|".join(r3_terms) + r")\b)")

    def process_tf(tf):
        for p in tf.paragraphs:
            full_text = p.text
            full_text = full_text.replace("\x0b", " ").replace("_x000B_", " ").replace("\r", "")
            if not pattern.search(full_text):
                continue
            fname = p.font.name or (p.runs[0].font.name if p.runs else "Arial") or "Arial"
            fsize = p.font.size or (p.runs[0].font.size if p.runs else Pt(11.4)) or Pt(11.4)
            fbold = p.font.bold if p.font.bold is not None else (p.runs[0].font.bold if p.runs else False)
            fitalic = p.font.italic if p.font.italic is not None else (p.runs[0].font.italic if p.runs else False)
            fcolor = None
            try:
                if p.font.color and p.font.color.type is not None:
                    fcolor = p.font.color.rgb
            except Exception:
                pass
            if fcolor is None and p.runs:
                try:
                    if p.runs[0].font.color and p.runs[0].font.color.type is not None:
                        fcolor = p.runs[0].font.color.rgb
                except Exception:
                    pass
            if fcolor is None:
                fcolor = SUAI_PALETTE["CHARCOAL"]

            parts = pattern.split(full_text)
            p.text = ""
            for part in parts:
                if not part:
                    continue
                r = p.add_run()
                r.text = part
                r.font.name = fname
                r.font.size = fsize
                r.font.italic = fitalic
                if pattern.fullmatch(part):
                    r.font.bold = True
                    if fcolor in (RGBColor(255, 255, 255), RGBColor(0xDC, 0xEB, 0xFA)):
                        r.font.color.rgb = fcolor
                    else:
                        r.font.color.rgb = SUAI_PALETTE["BLUE"]
                else:
                    r.font.bold = fbold
                    r.font.color.rgb = fcolor

    for slide in prs.slides:
        for shape in slide.shapes:
            if shape.has_text_frame:
                process_tf(shape.text_frame)
            elif shape.has_table:
                for row in shape.table.rows:
                    for cell in row.cells:
                        process_tf(cell.text_frame)


def add_styled_table(
    slide,
    left: float,
    top: float,
    width: float,
    height: float,
    headers: List[str],
    rows: List[List[str]],
    col_widths: Optional[List[float]] = None,
    header_bg: Optional[RGBColor] = None,
    font_size: float = 9.2,
    accent_first_col: bool = False
) -> Any:
    """Создает стандартизированную аналитическую таблицу ГУАП с автопереносом и форматированием."""
    table_shape = slide.shapes.add_table(
        len(rows) + 1, len(headers), Inches(left), Inches(top), Inches(width), Inches(height)
    )
    table = table_shape.table

    if col_widths and len(col_widths) == len(headers):
        for c_idx, cw in enumerate(col_widths):
            table.columns[c_idx].width = Inches(cw)

    h_bg = header_bg or SUAI_PALETTE["DEEP_NAVY"]

    # Шапка таблицы
    for c_idx, h_text in enumerate(headers):
        cell = table.cell(0, c_idx)
        cell.fill.solid()
        cell.fill.fore_color.rgb = h_bg
        cell.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf = cell.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.08)
        tf.margin_right = Inches(0.08)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)
        lines = str(h_text).split("\n")
        for l_idx, line in enumerate(lines):
            p = tf.paragraphs[0] if l_idx == 0 else tf.add_paragraph()
            p.alignment = PP_ALIGN.CENTER
            p.text = line
            p.font.name = "Arial"
            p.font.size = Pt(font_size + 1.0)
            p.font.bold = True
            p.font.color.rgb = SUAI_PALETTE["WHITE"]

    # Строки данных
    for r_idx, row_data in enumerate(rows):
        is_even = (r_idx % 2 == 0)
        row_bg = RGBColor(255, 255, 255) if is_even else RGBColor(244, 247, 250)
        for c_idx, cell_text in enumerate(row_data):
            cell = table.cell(r_idx + 1, c_idx)
            cell.fill.solid()
            if accent_first_col and c_idx == 0:
                cell.fill.fore_color.rgb = RGBColor(238, 244, 250)
            else:
                cell.fill.fore_color.rgb = row_bg
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            tf.margin_left = Inches(0.08)
            tf.margin_right = Inches(0.08)
            tf.margin_top = Inches(0.06)
            tf.margin_bottom = Inches(0.06)
            lines = str(cell_text).split("\n")
            for l_idx, line in enumerate(lines):
                p = tf.paragraphs[0] if l_idx == 0 else tf.add_paragraph()
                p.alignment = PP_ALIGN.LEFT if (c_idx > 0 or not accent_first_col) else PP_ALIGN.CENTER
                p.text = line
                p.font.name = "Arial"
                p.font.size = Pt(font_size)
                if accent_first_col and c_idx == 0:
                    p.font.bold = True
                    p.font.color.rgb = SUAI_PALETTE["DEEP_NAVY"]
                else:
                    p.font.color.rgb = SUAI_PALETTE["CHARCOAL"]

    return table_shape


def create_layout_a_slide(
    prs: Presentation,
    title: str,
    subtitle: str,
    cards: List[Dict[str, Any]],
    fig_filename: str,
    fig_desc: str,
    takeaway: str,
    notes: str = "",
    use_placeholders_only: bool = False
) -> Any:
    """Создает двухколоночный аналитический слайд Layout A (карточки теории слева + фигура справа)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(slide, title, subtitle)

    curr_top = 1.25
    for card in cards:
        h = card.get("height", 2.45)
        add_rich_card(slide, 0.60, curr_top, 5.35, h, card["heading"], card["bullets"], font_size=11.2)
        curr_top += h + 0.12

    add_fitted_figure(slide, 6.20, 1.25, 6.533, 5.15, fig_filename, fig_desc, use_placeholder_only=use_placeholders_only)
    add_takeaway_banner(slide, takeaway)
    if notes:
        set_speaker_notes(slide, notes)
    return slide


# ------------------------------------------------------------------------------
# Конкретные генераторы слайдов для мастер-архитектуры (26 слайдов)
# ------------------------------------------------------------------------------

def create_roadmap_slide(prs: Presentation, notes: str = "") -> Any:
    """Слайд 3: Инженерный маршрут преодоления барьеров нанодисперсности."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Инженерный маршрут преодоления барьеров нанодисперсности",
        "Четыре сквозных проблемных раздела: от геометрии поверхности к барьеру ДЛФО"
    )

    bullets = [
        "Раздел 1. Слипание и капиллярный коллапс: термодинамика Гиббса ΔG > 0, скачок S_уд = 3/r, давление Лапласа P_L ~ 200 МПа, аэрогели и цеолиты.",
        "Раздел 2. Потеря заряда и разрушение оболочки: строение мицеллы, правила Панета–Фаянса, экранирование ДЭС длиной Дебая λ_D ~ 1/(z√c).",
        "Раздел 3. Слепой контроль и микрофлюидика: плоскость скольжения, дзета-потенциал |ζ| ≥ 30 мВ, эффект Рейсса, безнасосный чип Lab-on-a-Chip.",
        "Раздел 4. Седиментация и солевой шок: баланс Перрена, потенциальный барьер ДЛФО U_max, закон Шульце–Гарди 1/z⁶, стерическая защита ПАВ."
    ]
    add_rich_card(slide, 0.60, 1.25, 4.80, 5.15, "Последовательность инженерных задач курса", bullets, font_size=10.4)
    add_fitted_figure(slide, 5.60, 1.25, 7.133, 5.15, "fig_01_roadmap.png", "4-блочная карта лекции")
    add_takeaway_banner(
        slide,
        "Управление устойчивостью коллоидов опирается на сквозную цепочку: термодинамика поверхности → заряд ДЭС → электрокинетический потенциал → барьер ДЛФО."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_06_modular(prs: Presentation, notes: str = "") -> Any:
    """Слайд 6: Полноширинный модульный слайд определений и матрицы 9 классов (без картинок)."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Термодинамика границы раздела: свободная энергия Гиббса и критерий Ребиндера",
        "Раздел 1. Фундаментальные понятия, условия агрегации и классификационная матрица"
    )

    c1_bullets = [
        "Дисперсная фаза (ДФ): раздробленное вещество, образующее гетерогенную границу раздела.",
        "Дисперсионная среда (ДС): непрерывная среда, в которой распределена фаза.",
        "Межфазная граница характеризуется удельной свободной поверхностной энергией σ [Дж/м²]."
    ]
    add_rich_card(slide, 0.60, 1.25, 3.85, 2.25, "1. Фаза (ДФ) и среда (ДС)", c1_bullets, font_size=10.2)

    c2_bullets = [
        "  [Ф] ΔG_s = σ · ΔA > 0",
        "Термодинамический импульс стремится самопроизвольно сократить избыточную площадь поверхности: ΔA → min.",
        "Слипание (агрегация) частиц термодинамически выгодно при отсутствии энергетического барьера."
    ]
    add_rich_card(slide, 4.74, 1.25, 3.85, 2.25, "2. Избыточная энергия Гиббса ΔG", c2_bullets, font_size=10.2)

    c3_bullets = [
        "  [Ф] σ_кр ≈ α · (k_B T / r²)",
        "Лиофильные системы (σ < σ_кр, ΔG_обр < 0): самопроизвольно диспергируют, термодинамически устойчивы.",
        "Лиофобные золи (σ > σ_кр, ΔG_обр > 0): термодинамически нестабильны, требуют силового барьера."
    ]
    add_rich_card(slide, 8.88, 1.25, 3.85, 2.25, "3. Критерий Ребиндера σ_кр", c3_bullets, font_size=10.2)

    headers = ["ДФ \\ ДС", "ДС: Газ (Г)", "ДС: Жидкость (Ж)", "ДС: Твердое тело (Т)"]
    rows = [
        [
            "Газ (Г)",
            "Г / Г: Гомогенные смеси\n(молекулярный уровень, без границы)",
            "Г / Ж: Газовые эмульсии и пены\n(нанопены, флотация, микропузырьки)",
            "Г / Т: Пористые материалы\n(аэрогели SiO₂, цеолиты, нанопористый Si)"
        ],
        [
            "Жидкость (Ж)",
            "Ж / Г: Аэрозоли (туманы)\n(спреи, капельный CVD-аэрозоль)",
            "Ж / Ж: Эмульсии (прямые/обратные)\n(обратные мицеллы как нанореакторы)",
            "Ж / Т: Гели, студни, капилляры\n(нанопористые мембраны, гидрогели)"
        ],
        [
            "Твердое (Т)",
            "Т / Г: Аэрозоли (дымы, порошки)\n(нанопорошки ZnO, TiO₂, аэрогели)",
            "Т / Ж: Золи, гидрозоли, суспензии\n(золи Au, AgI, Fe(OH)₃, квантовые точки)",
            "Т / Т: Твердые золи и композиты\n(рубиновое стекло, нанокомпозиты, КТ)"
        ]
    ]
    add_styled_table(
        slide,
        left=0.60,
        top=3.65,
        width=12.133,
        height=2.80,
        headers=headers,
        rows=rows,
        col_widths=[1.85, 3.42, 3.42, 3.443],
        header_bg=SUAI_PALETTE["DEEP_NAVY"],
        font_size=9.2,
        accent_first_col=True
    )

    add_takeaway_banner(
        slide,
        "Неорганические нанозоли термодинамически лиофобны (ΔG > 0) и способны существовать только при наличии защитного силового барьера, препятствующего коагуляции."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_09_summary(prs: Presentation, notes: str = "") -> Any:
    """Слайд 9: Сводная инженерная таблица решений Раздела 1."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Инженерные методы управления свободной энергией и капиллярными силами",
        "Раздел 1. Сводная матрица технологических решений первого барьера нанодисперсности"
    )

    headers = [
        "Технологическая система",
        "Физический барьер и механизм",
        "Инженерный регламент управления",
        "Практический результат"
    ]
    rows = [
        [
            "Лиофобные гидрозоли\n(Au, Ag, оксиды Fe, Ti)",
            "Спонтанная агрегация:\nΔG_s = σ · ΔA > 0\n(ван-дер-ваальсово схлопывание)",
            "Формирование защитного ДЭС путем адсорбции потенциалопределяющих ионов (ПОИ) или введение поверхностно-активных веществ (ПАВ)",
            "Длительная кинетическая стабильность нанозолей (сохранение размерности 1–100 нм)"
        ],
        [
            "Нанопористые ксерогели\n(силикагель, оксидные сорбенты)",
            "Капиллярный коллапс пор:\nP_L = 2σ/r ~ 200 МПа\n(менисковое стягивание стенок)",
            "Конвективная сушка золь-гель каркаса с контролируемой усадкой нанопор",
            "Формирование механически прочных гранул сорбентов с остаточной пористостью 10–30%"
        ],
        [
            "Ультрапористые аэрогели\n(монолиты аэрогеля SiO₂)",
            "Разрушение ажурного каркаса\nкапиллярным натяжением при испарении",
            "Сверхкритическая сушка флюидом CO₂ при T > T_c, P > P_c и полном устранении натяжения (σ = 0)",
            "Сохранение исходного 3D-каркаса с пористостью свыше 95% и рекордно низкой теплопроводностью"
        ],
        [
            "Цеолитные нанореакторы\n(кристаллические алюмосиликаты)",
            "Полидисперсность и вторичная агрегация при синтезе нанокластеров",
            "Инкапсуляция прекурсоров в жесткие кристаллографические окна и полости 0.3–1.0 нм",
            "Прецизионный синтез калиброванных квантовых точек (КТ) с монодисперсным спектром"
        ]
    ]
    add_styled_table(
        slide,
        left=0.60,
        top=1.25,
        width=12.133,
        height=5.20,
        headers=headers,
        rows=rows,
        col_widths=[2.60, 3.10, 3.40, 3.033],
        header_bg=SUAI_PALETTE["DEEP_NAVY"],
        font_size=9.8,
        accent_first_col=True
    )

    add_takeaway_banner(
        slide,
        "Контроль поверхностной энергии через выбор растворителя, введение ПАВ и устранение капиллярных менисков позволяет направленно управлять морфологией нанопродуктов."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_12_builder(prs: Presentation, notes: str = "") -> Any:
    """Слайд 12: Четырехшаговый алгоритм составления формул мицелл гидрозолей."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Четырехшаговый алгоритм составления формул мицелл гидрозолей",
        "Раздел 2. Пошаговая сборка формул и феномен перезарядки золей"
    )

    steps = [
        ("Шаг 1: Агрегат", "Нерастворимый остов [M]_m\n(электронейтрален, q = 0)", SUAI_PALETTE["DEEP_NAVY"]),
        ("Шаг 2: Ядро", "Адсорбция n родных ПОИ из избытка:\n[M]_m · n ПОИ± (заряд ±n)", SUAI_PALETTE["BLUE"]),
        ("Шаг 3: Гранула", "Связывание (n-x) ПИ в плотный слой:\n{[M]_m · n ПОИ± · (n-x) ПИ∓}±x", SUAI_PALETTE["RED"]),
        ("Шаг 4: Мицелла", "Диффузный слой x ПИ за скобкой:\n{Гранула}±x · x ПИ∓ (заряд 0)", SUAI_PALETTE["GREEN"]),
    ]
    step_w = 2.85
    step_gap = 0.244
    for i, (stitle, sbody, scol) in enumerate(steps):
        sx = 0.60 + i * (step_w + step_gap)
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(sx), Inches(1.25), Inches(step_w), Inches(2.15))
        card.fill.solid()
        card.fill.fore_color.rgb = SUAI_PALETTE["CARD_BG"]
        card.line.color.rgb = scol
        card.line.width = Pt(1.5)
        tf = card.text_frame
        tf.word_wrap = True
        p0 = tf.paragraphs[0]
        p0.text = stitle
        p0.font.name = "Arial"
        p0.font.size = Pt(12)
        p0.font.bold = True
        p0.font.color.rgb = scol
        p1 = tf.add_paragraph()
        p1.text = sbody
        p1.font.name = "Arial"
        p1.font.size = Pt(10)
        p1.font.color.rgb = SUAI_PALETTE["CHARCOAL"]
        p1.space_before = Pt(4)

    card_l_bullets = [
        "Избыток KI (I⁻ — ПОИ, K⁺ — ПИ):",
        "  [Ф] {[AgI]_m · n I⁻ · (n-x) K⁺}ˣ⁻ · x K⁺   (гранула отрицательна)",
        "Избыток AgNO₃ (Ag⁺ — ПОИ, NO₃⁻ — ПИ):",
        "  [Ф] {[AgI]_m · n Ag⁺ · (n-x) NO₃⁻}ˣ⁺ · x NO₃⁻   (гранула положительна)"
    ]
    add_rich_card(slide, 0.60, 3.65, 5.90, 2.75, "1. Перезарядка золя иодида серебра (AgI)", card_l_bullets, font_size=10.0)

    card_r_bullets = [
        "Гидролиз FeCl₃ в кипящей воде со стабилизатором FeOCl ⇄ FeO⁺ + Cl⁻:",
        "  - Катион оксожелеза FeO⁺ адсорбируется как ПОИ:",
        "  [Ф] {[Fe(OH)₃]_m · n FeO⁺ · (n-x) Cl⁻}ˣ⁺ · x Cl⁻",
        "  - Гранула заряжена строго положительно, анионы Cl⁻ в диффузном слое."
    ]
    add_rich_card(slide, 6.83, 3.65, 5.90, 2.75, "2. Гидрозоль гидроксида железа (Fe(OH)₃)", card_r_bullets, font_size=10.0)

    add_takeaway_banner(
        slide,
        "Знак заряда коллоидной гранулы однозначно определяется знаком потенциалопределяющего иона, находящегося в избытке при проведении химической реакции синтеза."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_15_regulations(prs: Presentation, notes: str = "") -> Any:
    """Слайд 15: Технологический регламент стабилизации гидрозолей при жидкофазном синтезе."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Технологический регламент стабилизации гидрозолей при жидкофазном синтезе",
        "Раздел 2. Сводная матрица физико-химических параметров устойчивости ДЭС"
    )
    headers = ["Параметр синтеза", "Физический механизм влияния на ДЭС", "Технологическое ограничение", "Инженерное решение"]
    rows = [
        [
            "Ионная сила раствора I\nи дебаевская длина λ_D",
            "Компрессия диффузного слоя по закону экранирования:\nλ_D = [εε₀ k_B T / (2 e² N_A I)]¹/² ∝ 1/√(I)",
            "Критическая дебаевская толщина λ_D < 10 нм провоцирует коагуляцию;\nдопустимый предел ионной силы I ≤ 10⁻³ моль/л",
            "Синтез нанозолей в разбавленных средах с непрерывным кондуктометрическим контролем электропроводности"
        ],
        [
            "Неиндифферентные\nэлектролиты (избыток ПОИ)",
            "Избирательная хемосорбция родных ионов на агрегате по правилу Панета–Фаянса–Пескова, рост потенциала φ₀",
            "Недостаток ПОИ не создает защитного барьера;\nизбыток ПОИ свыше 15–20% сжимает диффузный слой",
            "Строго дозированный стехиометрический избыток стабилизатора 5–15% моль по отношению к прекурсору"
        ],
        [
            "Индифферентные\nэлектролиты и валентность z",
            "Ионы не входят в решетку агрегата; увеличивают ионную силу ∝ z², вызывая компрессию диффузного слоя (λ_D ∝ 1/(z√c))",
            "Многозарядные примесные катионы и анионы (Al³⁺, Fe³⁺, SO₄²⁻) вызывают солевой шок при микроконцентрациях",
            "Применение деионизованной воды высокой очистки (сопротивление 18.2 МОм·см) и ультрачистых реактивов"
        ],
        [
            "Специфическая адсорбция\nи перезарядка поверхности",
            "Внедрение поливалентных противоионов в плотный слой Штерна с инверсией знака потенциала φ_δ",
            "Прохождение через изоэлектрическую точку (ИЭТ, φ_δ = 0) с мгновенным выпадением гидрозоля в осадок",
            "Быстрый ввод раствора перезаряжающего электролита (Al³⁺, Th⁴⁺) при интенсивном гидродинамическом перемешивании"
        ]
    ]
    add_styled_table(
        slide, left=0.60, top=1.25, width=12.133, height=5.20,
        headers=headers, rows=rows, col_widths=[2.40, 3.40, 3.10, 3.233],
        header_bg=SUAI_PALETTE["DEEP_NAVY"], font_size=8.8, accent_first_col=True
    )
    add_takeaway_banner(
        slide,
        "Для предотвращения спонтанной коагуляции технологический регламент требует поддержания ионной силы раствора ниже критической и строгого дозирования избытка ПОИ."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_24_coagulation_modular(prs: Presentation, notes: str = "") -> Any:
    """Слайд 24: Порог коагуляции, закон 1/z⁶ Шульце–Гарди и кинетика Смолуховского."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Порог коагуляции, закон 1/z⁶ Шульце–Гарди и кинетика Смолуховского",
        "Раздел 4. Критические концентрации коагуляции и каскадное действие многозарядных ионов"
    )
    c1_bullets = [
        "Минимальная концентрация электролита, вызывающая исчезновение барьера U_max ≤ 0.",
        "Формула расчета порога в растворе:",
        "  [Ф] γ_кр = (C_эл · V_эл) / (V_золя + V_эл) · 1000  (ммоль/л)",
        "Разграничение зон скрытой, медленной и быстрой коагуляции."
    ]
    add_rich_card(slide, 0.60, 1.25, 3.85, 4.95, "1. Порог коагуляции γ_кр", c1_bullets, font_size=10.0)

    c2_bullets = [
        "Теория Дерягина–Ландау: сжатие барьера ДЭС до нуля:",
        "  [Ф] γ_кр = C · (εε₀)³ (k_B T)⁵ / (A_H² e⁶) · (1 / z⁶)",
        "Коагулирующим действием обладает противоион.",
        "Каскадный ряд порогов коагуляции:",
        "  [Ф] 1 : 1/64 : 1/729  для  Na⁺ : Ca²⁺ : Al³⁺",
        "Трехвалентные ионы в 729 раз активнее одновалентных."
    ]
    add_rich_card(slide, 4.74, 1.25, 3.85, 4.95, "2. Закон 1/z⁶ Шульце–Гарди", c2_bullets, font_size=10.0)

    c3_bullets = [
        "Быстрая коагуляция: каждое тепловое столкновение эффективно:",
        "  [Ф] 1 / ν(t) = 1 / ν₀ + k_d · t",
        "Диффузионная константа скорости:",
        "  [Ф] k_d = 4 k_B T / (3 η) ≈ 6.1 · 10⁻¹⁸ м³/с",
        "Время половинной коагуляции τ₁/₂ = 1 / (k_d · ν₀) зависит только от исходной концентрации частиц."
    ]
    add_rich_card(slide, 8.88, 1.25, 3.85, 4.95, "3. Кинетика Смолуховского", c3_bullets, font_size=10.0)

    add_takeaway_banner(
        slide,
        "Критическая концентрация коагуляции падает обратно пропорционально шестой степени заряда противоиона (z⁻⁶), делая трехвалентные ионы в 700 раз активнее одновалентных."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


def create_slide_26_master_matrix(prs: Presentation, notes: str = "") -> Any:
    """Слайд 26: Инженерная матрица выбора стратегии стабилизации наносистем."""
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    add_suai_header(
        slide,
        "Инженерная матрица выбора стратегии стабилизации наносистем",
        "Раздел 4. Сводное технологическое руководство преодоления барьеров нанодисперсности"
    )
    headers = ["Технологический вызов", "Физический барьер", "Оптимальная стратегия", "Промышленный регламент"]
    rows = [
        ["1. Агрегация нанозолей (Au, Ag)", "ΔG_s > 0, ван-дер-ваальсово схлопывание", "Электростатическая стабилизация ДЭС", "Поддержание |ζ| ≥ 30 мВ и низкой ионной силы среды"],
        ["2. Седиментация и оседание", "Гравитационный осадок по Стоксу (v ∝ r²)", "Суб-10 нм масштаб и броуновский баланс", "Синтез наночастиц r ≤ 10 нм по барометрическому закону Перрена"],
        ["3. Созревание при хранении", "Оствальдов перенос массы (Кельвин–Томсон)", "Стерическая защита полимерами (ПЭГ, ПВП)", "Создание упругих полимерных оболочек, экранирующих наночастицы"],
        ["4. Сдвиговая деградация в потоке", "Динамический срыв ионной атмосферы", "Ковалентная модификация поверхности", "Плотная прививка длинноцепочечных лигандов к ядру частицы"],
        ["5. Капиллярный коллапс нанопор", "Лапласово давление P_L = 2σ/r ~ 200 МПа", "Сверхкритическая сушка флюидом", "Полное устранение межфазного натяжения (σ = 0) при T > T_c, P > P_c"],
        ["6. Полидисперсность синтеза", "Неконтролируемая кинетика кристаллизации", "Матричные нанореакторы (цеолиты)", "Синтез в калиброванных субнанометровых порах 0.3–1.0 нм"]
    ]
    add_styled_table(
        slide, left=0.60, top=1.25, width=12.133, height=5.20,
        headers=headers, rows=rows, col_widths=[2.50, 3.00, 3.20, 3.433],
        header_bg=SUAI_PALETTE["DEEP_NAVY"], font_size=9.2, accent_first_col=True
    )
    add_takeaway_banner(
        slide,
        "Выбор между электростатической, стерической и структурно-механической защитой определяется химической природой среды, солевым фоном и температурным режимом эксплуатации."
    )
    if notes:
        set_speaker_notes(slide, notes)
    return slide


# ==============================================================================
# 5. Сборщик полной 26-слайдовой презентации лекции
# ==============================================================================

def build_lecture_03_deck(output_path: str = OUT_MAIN_PPTX, primary_variation: int = 1,
                          use_placeholders_only: bool = False):
    """
    Формирует полную академическую презентацию Лекции №3 (ровно 26 слайдов, 4 проблемных раздела):
    - Вводный блок (Слайды 1–3): Титул, Проблемный Visual-First обзор, Инженерный маршрут.
    - Раздел 1 (Слайды 4–9): Слипание и капиллярный коллапс нанопор.
    - Раздел 2 (Слайды 10–15): Потеря заряда и разрушение защитной оболочки наночастицы.
    - Раздел 3 (Слайды 16–20): Слепой контроль стабильности и безнасосный транспорт на чипе.
    - Раздел 4 (Слайды 21–26): Расслоение при хранении, солевой шок и рецептуры «вечных» коллоидов.
    """
    prs = create_base_presentation()

    # --------------------------------------------------------------------------
    # ВВОДНЫЙ БЛОК (СЛАЙДЫ 1–3)
    # --------------------------------------------------------------------------
    # Слайд 1 (Титульный лист ГУАП)
    create_title_slide(
        prs,
        title="Термодинамика дисперсных систем и коллоидных растворов",
        subtitle="Поверхностная энергия, капиллярные явления, двойной электрический слой (ДЭС) и барьеры устойчивости",
        course_info="КУРС «ФИЗИЧЕСКИЕ ОСНОВЫ НАНОТЕХНОЛОГИЙ» • 3 КУРС • ЛЕКЦИЯ №3 ИЗ 8",
        teacher_info="Преподаватель: доцент Попов Д.А.",
        dept_info="Кафедра №3 «Физики и нанотехнологий» ГУАП | Санкт-Петербург, 2026",
        style="classic",
        notes=(
            "1. Физический тезис: Раздел 2 «Особенности термодинамики наноструктур» дисциплины «Физические основы нанотехнологий» (бакалавриат, 3 курс ГУАП). Лекция закладывает фундамент жидкофазного синтеза, агрегативной устойчивости наносистем, термодинамики границ раздела, формирования двойного электрического слоя и физико-химических методов коллоидной диагностики.\n"
            "2. Визуальные акценты: Титульный лист оформлен по академическому дизайн-коду ГУАП: контрастный темно-синий колорит, официальное наименование курса, темы лекции, реквизиты кафедры и преподавателя.\n"
            "3. Инженерный контекст: Все университетские реквизиты кафедры и преподавателя зафиксированы на титульном листе и далее на рабочих слайдах не повторяются (Single-Point Occurrence). Темы №7 и №8 календарного плана соответствуют РПД.\n"
            "4. Смысловой переход: Переходим к анализу фундаментального противоречия между длительной стабильностью коллоидов и самопроизвольной агрегацией наночастиц."
        )
    )

    # Слайд 2 (Вводный проблемный — Visual-First)
    split_img = find_asset("fig_01_split_faraday_vs_fe3o4.png") or os.path.join(FIG_DIR, "fig_01_split_faraday_vs_fe3o4.png")
    create_problem_intro_slide(
        prs,
        title="Шесть технологических вызовов нанодисперсных систем",
        image_path=split_img,
        image_caption="Золь золота Фарадея 1857 г. (The Royal Institution) vs ПЭМ слипшихся наночастиц Fe3O4",
        takeaway="Без электростатического или стерического барьера любая нанодисперсная система неизбежно теряет агрегативную устойчивость и выпадает в осадок.",
        notes=(
            "1. Физический тезис: Переход к наномасштабу 1–100 нм сопровождается взрывным ростом свободной поверхностной энергии, порождающим шесть фундаментальных технологических проблем: агрегацию (слипание), гравитационное оседание, деградацию при хранении, разрушение при гидродинамическом транспорте, трудности сепарации и несовместимость при формуляции материалов.\n"
            "2. Визуальные акценты: На слайде сопоставлены два противоположных состояния материи: подлинный рубиновый золь золота Майкла Фарадея 1857 года, сохраняющий устойчивость свыше 170 лет, и ПЭМ-микрофотография агрегатов оксида железа Fe3O4, скоагулировавших в плотный осадок при отсутствии защитного экрана.\n"
            "3. Инженерный контекст: Без искусственно созданного электростатического или стерического барьера любая дисперсная наносистема неизбежно теряет агрегативную устойчивость и переходит в монолит.\n"
            "4. Смысловой переход: Для преодоления каждого из шести барьеров сформирован последовательный четырехэтапный инженерный маршрут лекции."
        )
    )

    # Слайд 3 (Инженерный маршрут лекции)
    create_roadmap_slide(
        prs,
        notes=(
            "1. Физический тезис: Программа лекции представляет собой сквозную цепочку физико-химических инструментов: от геометрии наноповерхности к строению двойного электрического слоя, расчету электрокинетического дзета-потенциала и проектированию барьера теории Дерягина–Ландау–Фервея–Овербека (ДЛФО).\n"
            "2. Визуальные акценты: Обратите внимание на четыре тематических блока дорожной карты: Раздел 1 анализирует скачок удельной поверхности и капиллярные силы Лапласа; Раздел 2 раскрывает электростатическую броню мицеллы; Раздел 3 рассматривает плоскость скольжения и микрофлюидику; Раздел 4 дает расчет критических порогов коагуляции и стерической защиты поверхностно-активными веществами (ПАВ).\n"
            "3. Инженерный контекст: Освоение этой сквозной методологии необходимо для проектирования устойчивых коллоидных растворов в микроэлектронике, биомедицине и катализе.\n"
            "4. Смысловой переход: Приступаем к Разделу 1, посвященному термодинамическому драйверу наномасштаба и капиллярным силам в нанопорах."
        )
    )

    # --------------------------------------------------------------------------
    # РАЗДЕЛ 1: САМОПРОИЗВОЛЬНОЕ СЛИПАНИЕ И КАПИЛЛЯРНЫЙ КОЛЛАПС (СЛАЙДЫ 4–9)
    # --------------------------------------------------------------------------
    # Слайд 4 (Разделитель Раздела 1, Layout S #002C5F)
    create_section_divider_slide(
        prs,
        problem_ids=["aggregation", "separation"],
        title="Самопроизвольное слипание наночастиц и капиллярный коллапс нанопор",
        subtitle="ПРОБЛЕМНЫЙ РАЗДЕЛ 1: ТЕХНОЛОГИЧЕСКИЙ ВЫЗОВ №1",
        thesis=(
            "Колоссальная удельная площадь поверхности наноматериалов порождает избыточную энергию Гиббса ΔG = σ·ΔA > 0, "
            "стремящуюся скоагулировать частицы. При сушке нанопористых гелей капиллярное давление Лапласа достигает "
            "сотен МПа, разрушая каркас в ксерогель. Сохранение наноструктур требует термодинамического "
            "контроля натяжения σ и сверхкритической сушки."
        ),
        roadmap_steps=[
            "1. Геометрия наномасштаба и S_уд = 3/r",
            "2. Термодинамика Гиббса и критерий Ребиндера",
            "3. Давление Лапласа и аэрогель SiO2",
            "4. Кристаллические цеолиты"
        ],
        style="navy",
        notes=(
            "1. Физический тезис: Раздел 1 посвящен анализу самопроизвольного слипания частиц под действием избыточной энергии Гиббса и механического сжатия нанопор капиллярным давлением Лапласа.\n"
            "2. Визуальные акценты: Слайд-разделитель выполнен в корпоративном стиле ГУАП Layout S с акцентными иконками агрегации и сепарации, фиксируя ключевой технологический вызов наноиндустрии.\n"
            "3. Инженерный контекст: Управление поверхностной энергией и капиллярными силами определяет выход годных наноструктурированных аэрогелей, мембран и стабильных суспензий.\n"
            "4. Смысловой переход: Количественный масштаб проблемы раскрывается через закон гиперболического роста удельной поверхности при уменьшении радиуса частиц."
        )
    )

    # Слайд 5 (Layout A: Скачок S_уд и эффект Тиндаля)
    s5_cards = [
        {
            "heading": "1. Дисперсность D и скачок удельной поверхности",
            "height": 2.45,
            "bullets": [
                "Дисперсная система состоит из дисперсной фазы (размер a) и сплошной дисперсионной среды.",
                "Дисперсность D = 1/a [м⁻¹] определяет удельную площадь фазовой границы:",
                "  [Ф] S_уд = S / V = 6 / a = 3 / r,   S_уд^(m) = k / (ρ · a)",
                "Фактор формы k строго зависит от размерности: k = 6 (сфера, 3D), k = 4 (нить, 1D), k = 2 (пленка, 2D)."
            ]
        },
        {
            "heading": "2. Конус Фарадея–Тиндаля и доля поверхностных атомов",
            "height": 2.45,
            "bullets": [
                "Рассеяние света на частицах 1–100 нм формирует видимый световой конус в нанозоле в отличие от истинного раствора.",
                "При диаметре частицы менее 3 нм свыше 50% всех атомов выходят на межфазную границу:",
                "  [Ф] Доля поверхностных атомов: N_s / N_tot = 1 - (1 - 2 d_at / d)³",
                "Выход атомов на поверхность определяет экстремальную химическую и каталитическую активность наноматериалов."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Удельная поверхность и эффект Фарадея–Тиндаля наномасштаба 1–100 нм",
        subtitle="Раздел 1. Геометрический фактор и оптическая идентификация коллоидной фазы",
        cards=s5_cards,
        fig_filename="fig_02_specific_surface.png",
        fig_desc="Эффект Фарадея–Тиндаля, удельная поверхность S_уд(a) и доля поверхностных атомов",
        takeaway="При уменьшении размера частиц от 1 см до 10 нм удельная площадь поверхности возрастает в миллион раз, а свыше 50% атомов выходят на межфазную границу.",
        notes=(
            "1. Физический тезис: При дроблении вещества до коллоидного диапазона 1–100 нм удельная площадь поверхности возрастает обратно пропорционально линейному размеру S_уд = k/a = 3/r, а оптическое рассеяние света на частицах формирует характерный конус Фарадея–Тиндаля.\n"
            "2. Визуальные акценты: На верхней панели представлено реальное оптическое явление: лазерный луч невидим в истинном молекулярном растворе, но ярко визуализируется в коллоидном золе за счет дифракционного рассеяния. На нижних графиках показан гиперболический рост S_уд и выход свыше 50% атомов на поверхность при диаметре частиц менее 3 нм.\n"
            "3. Инженерный контекст: Оптический экспресс-контроль конуса Тиндаля служит первичным индикатором коллоидной дисперсности в производственных процессах жидкофазного синтеза.\n"
            "4. Смысловой переход: Колоссальная площадь фазовой границы порождает избыточную свободную энергию, классификация которой требует введения строгих термодинамических критериев."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 6 (Layout B Pure Modular: Определения, Гиббс, Ребиндер, Матрица 9 классов)
    create_slide_06_modular(
        prs,
        notes=(
            "1. Физический тезис: Дисперсная система состоит из дисперсной фазы (ДФ) и дисперсионной среды (ДС). Не скомпенсированные межмолекулярные силы на границе создают избыточную энергию Гиббса ΔG = σ·ΔA > 0, стремящуюся скоагулировать частицы.\n"
            "2. Визуальные акценты: Верхний модульный ярус раскрывает определения ДФ и ДС, термодинамический смысл энергии Гиббса и критерий Ребиндера σ_кр. Нижняя матрица систематизирует 9 классов систем по агрегатному состоянию фаз (Т/Ж, Т/Г, Т/Т, Ж/Т, Г/Т).\n"
            "3. Инженерный контекст: Неорганические нанозоли термодинамически лиофобны (ΔG > 0) и способны длительно существовать только при наличии защитного силового барьера (электростатического или стерического).\n"
            "4. Смысловой переход: При сближении и агрегации наночастиц в объеме жидкости происходит золь–гель переход с образованием пространственной трехмерной сетки."
        )
    )

    # Слайд 7 (Layout A: Золь-гель переход, давление Лапласа и аэрогель)
    s7_cards = [
        {
            "heading": "1. Золь–гель технология и перколяция каркаса",
            "height": 2.45,
            "bullets": [
                "Золь–гель технология: синтез наноматериалов через переход от свободнодисперсного золя к связнодисперсному гелю.",
                "Достижение порога перколяции формирует единый пространственный 3D-каркас с запертой жидкой дисперсионной средой.",
                "Связнодисперсный гель удерживает форму и сопротивляется сдвигу при сохранении наноразмерных каналов."
            ]
        },
        {
            "heading": "2. Капиллярное давление Лапласа P_L и аэрогели",
            "height": 2.45,
            "bullets": [
                "При испарении растворителя капиллярные мениски создают гигантское стягивающее давление:",
                "  [Ф] P_L = (2 σ cos θ) / r_пор ~ 200 МПа  (при r = 1–2 нм)",
                "Обычная сушка сминает нанокаркас в плотный ксерогель с остаточной пористостью 10–30%.",
                "Сверхкритическая сушка (σ = 0) устраняет фазовую границу жидкость–пар, сохраняя ультрапористый аэрогель (>95% пор)."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Золь–гель переход, капиллярное давление Лапласа и сверхкритическая сушка",
        subtitle="Раздел 1. Фазовый переход связности и предотвращение коллапса нанопор",
        cards=s7_cards,
        fig_filename="fig_04_sol_gel_xerogel.png",
        fig_desc="Полноширинная схема перехода Золь -> Гель -> Ксерогель и Аэрогель",
        takeaway="Устранение межфазного натяжения (σ = 0) при сверхкритической сушке исключает капиллярный коллапс Лапласа и сохраняет ажурный 3D-каркас аэрогеля с пористостью свыше 95%.",
        notes=(
            "1. Физический тезис: Золь–гель технология основана на формировании непрерывного перколяционного каркаса геля. При обычной конвективной сушке капиллярное давление Лапласа P_L = 2σ/r достигает 70–200 МПа и сминает нанопоры в плотный ксерогель, тогда как сверхкритическая сушка исключает капиллярный коллапс.\n"
            "2. Визуальные акценты: На четырехпанельной схеме показана последовательность трансформации структуры: свободнодисперсный золь → перколяционный гель → капиллярная усадка в ксерогель (пористость 10–30%) против сверхкритической сушки флюидом СО2 при σ = 0, сохраняющей каркас аэрогеля с пористостью свыше 95%.\n"
            "3. Инженерный контекст: Диоксидкремниевые аэрогели обладают рекордно низкой теплопроводностью (0.013 Вт/(м·К)) и плотностью, находя широкое применение в теплоизоляции космических аппаратов и катализе.\n"
            "4. Смысловой переход: В отличие от хаотической аморфной сетки аэрогелей, строго монодисперсную пористость обеспечивают кристаллические цеолиты."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 8 (Layout A: Кристаллические цеолиты и квантовые точки)
    s8_cards = [
        {
            "heading": "1. Алюмосиликатный каркас и калиброванные поры",
            "height": 2.45,
            "bullets": [
                "Цеолиты: кристаллические связнодисперсные алюмосиликаты на основе тетраэдров [SiO4]4- и [AlO4]5-.",
                "Отрицательный каркас компенсируется подвижными катионами (Na+, Ca2+), определяющими сорбционные свойства.",
                "Диаметр входных окон строго калиброван кристаллической решеткой в диапазоне 0.3–1.0 нм."
            ]
        },
        {
            "heading": "2. Молекулярные сита и синтез квантовых точек",
            "height": 2.45,
            "bullets": [
                "Молекулярные сита: селективное разделение молекул по размеру и конфигурации (н-бутан 0.43 нм vs изобутан 0.50 нм).",
                "Полости цеолитов выступают как матричный нанореактор для прецизионного синтеза монодисперсных квантовых точек (КТ).",
                "Жесткие границы кристаллической поры физически ограничивают рост нанокристалла, обеспечивая квантово-размерный эффект."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Кристаллические цеолиты: субнанометровые окна и матричные нанореакторы",
        subtitle="Раздел 1. Кристаллические связнодисперсные системы с монодисперсными нанопорами",
        cards=s8_cards,
        fig_filename="fig_05_zeolites.png",
        fig_desc="Структура микропор цеолита, молекулярно-ситовой эффект и квантовые точки",
        takeaway="Атомно-монодисперсные входные окна цеолитов (0.3–1.0 нм) совмещают функции молекулярных сит и матричных нанореакторов для прецизионного синтеза квантовых точек.",
        notes=(
            "1. Физический тезис: Кристаллические цеолиты на основе тетраэдров [SiO4]4- и [AlO4]5- обладают субнанометровыми окнами 0.3–1.0 нм, калиброванными с точностью до долей ангстрема.\n"
            "2. Визуальные акценты: На иллюстрации представлены СЭМ-микрофотография кристаллов цеолита и атомная схема полостей. Продемонстрирован молекулярно-ситовой эффект разделения изомеров углеводородов и механизм матричного синтеза полупроводниковых квантовых точек (КТ).\n"
            "3. Инженерный контекст: Жесткие кристаллические нанореакторы исключают полидисперсность и агрегацию при синтезе квантовых точек, задавая монодисперсное распределение спектров фотолюминесценции.\n"
            "4. Смысловой переход: Сведем рассмотренные инженерные методы управления поверхностной энергией и капиллярным давлением в единую сводную матрицу Раздела 1."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 9 (Layout B Table: Сводная таблица решений Раздела 1)
    create_slide_09_summary(
        prs,
        notes=(
            "1. Физический тезис: Инженерный контроль свободной энергии Гиббса и давления Лапласа осуществляется тремя взаимодополняющими стратегиями: снижением поверхностного натяжения σ, устранением капиллярных менисков жидкости и пространственной геометрической локализацией наночастиц.\n"
            "2. Визуальные акценты: Таблица систематизирует четыре класса технологических решений: лиофобные гидрозоли (стабилизация ДЭС и ПАВ), нанопористые ксерогели (капиллярное формование сорбентов), ультрапористые аэрогели (сверхкритическая сушка при σ = 0) и цеолитные нанореакторы (матричная локализация квантовых точек).\n"
            "3. Инженерный контекст: Представленный сводный регламент служит практическим руководством для выбора технологии синтеза и сушки нанопористых и дисперсных материалов.\n"
            "4. Смысловой переход: Для сохранения свободнодисперсных золей в жидкой фазе требуется создать защитный ионный экран на межфазной границе, переходя к Разделу 2."
        )
    )

    # --------------------------------------------------------------------------
    # РАЗДЕЛ 2: ПОТЕРЯ ЗАРЯДА И РАЗРУШЕНИЕ ОБОЛОЧКИ (СЛАЙДЫ 10–15)
    # --------------------------------------------------------------------------
    # Слайд 10 (Разделитель Раздела 2, Layout S #002C5F)
    create_section_divider_slide(
        prs,
        problem_ids=["aggregation", "processability"],
        title="Потеря заряда и разрушение защитной оболочки наночастицы",
        subtitle="ПРОБЛЕМНЫЙ РАЗДЕЛ 2: ТЕХНОЛОГИЧЕСКИЙ ВЫЗОВ №2",
        thesis=(
            "Лиофобные наночастицы в жидкости удерживаются от термодинамического схлопывания электростатической защитой — "
            "двойным электрическим слоем (ДЭС). Избирательная адсорбция ионов на ядре формирует заряженную гранулу, "
            "экранированную диффузным слоем противоионов. Добавление электролитов сжимает дебаевскую толщину оболочки λ_D, "
            "приводя к потере заряда и мгновенной агрегации."
        ),
        roadmap_steps=[
            "1. Анатомия мицеллы и правило Панета–Фаянса",
            "2. 4-шаговый конструктор формул AgI и Fe(OH)3",
            "3. Модели ДЭС: Гельмгольц, Гуи, Штерн",
            "4. Длина Дебая λ_D и перезарядка"
        ],
        style="navy",
        notes=(
            "1. Физический тезис: Раздел 2 исследует электростатическую защиту лиофобных наночастиц от спонтанного слипания путем формирования двойного электрического слоя (ДЭС). Избирательная адсорбция ионов на ядре формирует заряженную гранулу, экранированную диффузной ионной шубой.\n"
            "2. Визуальные акценты: Слайд-разделитель выполнен в корпоративном темно-синем стиле ГУАП Layout S (#002C5F) с центральными векторными иконками агрегации и технологичности, фокусируя внимание на технологическом вызове №2.\n"
            "3. Инженерный контекст: Введение электролитов и рост ионной силы вызывают сжатие дебаевской толщины оболочки λ_D, приводя к потере заряда гранулы и необратимой коагуляции золей в технологических процессах.\n"
            "4. Смысловой переход: Для понимания механизма электростатической защиты детально исследуем пространственную анатомию коллоидной мицеллы и правило избирательной адсорбции."
        )
    )

    # Слайд 11 (Layout A: Анатомия мицеллы и Панет–Фаянс)
    s11_cards = [
        {
            "heading": "1. Концентрическая архитектура коллоидной мицеллы",
            "height": 2.45,
            "bullets": [
                "Коллоидная мицелла гидрозоля состоит из нейтрального кристаллического агрегата [M]_m и двойного электрического слоя (ДЭС).",
                "Потенциалопределяющие ионы (ПОИ) хемосорбируются на поверхности агрегата, образуя заряженное ядро.",
                "Противоионы (ПИ) распределяются между адсорбционным плотным слоем Штерна и диффузным слоем Гуи–Чепмена."
            ]
        },
        {
            "heading": "2. Правило избирательной адсорбции Панета–Фаянса–Пескова",
            "height": 2.45,
            "bullets": [
                "На кристаллическом агрегате преимущественно адсорбируются ионы, входящие в состав его кристаллической решетки.",
                "  [Ф] Обобщенная формула мицеллы:",
                "  [Ф] { [M]_m · n ПОИ± · (n-x) ПИ∓ }±x · x ПИ∓",
                "Гранула мицеллы в фигурных скобках несет заряд ±x, тогда как вся мицелла строго электронейтральна."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Анатомия коллоидной мицеллы и правило избирательной адсорбции",
        subtitle="Раздел 2. Формирование межфазного заряда гранулы и ионной оболочки",
        cards=s11_cards,
        fig_filename="fig_06_micelle_anatomy.png",
        fig_desc="Анатомия коллоидной мицеллы, агрегат, ПОИ, ПИ и гранула",
        takeaway="Гранула мицеллы несет нескомпенсированный электрический заряд и перемещается во внешнем поле, тогда как вся коллоидная мицелла строго электронейтральна.",
        notes=(
            "1. Физический тезис: Коллоидная мицелла гидрозоля представляет собой концентрическую электростатическую структуру, состоящую из нерастворимого кристаллического агрегата, заряженного ядра с потенциалопределяющими ионами (ПОИ) и двойного электрического слоя (ДЭС) противоионов (ПИ).\n"
            "2. Визуальные акценты: На диаграмме анатомии мицеллы наглядно разграничены четыре концентрические зоны: кристаллический агрегат [M]_m, адсорбционный монослой ПОИ, плотный слой Штерна с противоионами (образующие заряженную гранулу) и внешняя диффузная атмосфера противоионов.\n"
            "3. Инженерный контекст: Правило Панета–Фаянса–Пескова устанавливает, что заряд наночастицы определяется ионом решетки, находящимся в стехиометрическом избытке, позволяя инженеру программировать знак гранулы при химическом синтезе нанозолей.\n"
            "4. Смысловой переход: Перейдем от качественной схемы к строгому четырехшаговому алгоритму конструирования формул гидрозолей и феномену перезарядки."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 12 (Layout B Pure Modular: Конструктор мицелл)
    create_slide_12_builder(
        prs,
        notes=(
            "1. Физический тезис: Четырехшаговый алгоритм сборки формулы мицеллы отражает строгую физико-химическую иерархию: нейтральный агрегат → заряженное ядро → электрокинетическая гранула → электронейтральная мицелла. Знак заряда гранулы полностью контролируется выбором реагента в избытке.\n"
            "2. Визуальные акценты: Верхняя модульная цепочка наглядно демонстрирует переход от шага 1 к шагу 4. Нижние карточки сопоставляют перезарядку золя иодида серебра (отрицательная гранула при избытке KI против положительной при избытке AgNO3) и гидрозоль гидроксида железа с ионами FeO+.\n"
            "3. Инженерный контекст: Ошибка в дозировании прекурсора на стадии синтеза меняет знак заряда гранулы на противоположный, что приводит к несовместимости компонентов и мгновенному осаждению наносуспензии.\n"
            "4. Смысловой переход: Пространственное распределение противоионов между гранулой и диффузным слоем описывается классическими электростатическими моделями ДЭС."
        )
    )

    # Слайд 13 (Layout A: Модели Гельмгольца и Гуи-Чепмена)
    s13_cards = [
        {
            "heading": "1. Модель плоского конденсатора Гельмгольца (1879)",
            "height": 2.45,
            "bullets": [
                "Предположение: жесткая мономолекулярная плоскость противоионов на расстоянии молекулярного радиуса d.",
                "  [Ф] Линейный спад потенциала: φ(x) = φ₀ · (1 - x / d)",
                "Недостаток модели: полное игнорирование теплового броуновского движения и диффузии противоионов вглубь раствора."
            ]
        },
        {
            "heading": "2. Диффузная атмосфера Гуи–Чепмена (1910)",
            "height": 2.45,
            "bullets": [
                "Равновесие электростатического притяжения и тепловой диффузии по распределению Больцмана:",
                "  [Ф] n_i(x) = n_i₀ · exp(- z_i e φ(x) / k_B T)",
                "Экспоненциальный профиль потенциала: φ(x) = φ₀ · exp(- κ x).",
                "Толщина диффузной атмосферы описывается дебаевской длиной экранирования λ_D = κ⁻¹."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Классические модели ДЭС: теории Гельмгольца и Гуи–Чепмена",
        subtitle="Раздел 2. Эволюция представлений о пространственном распределении противоионов",
        cards=s13_cards,
        fig_filename="fig_08_helmholtz_vs_gouy.png",
        fig_desc="Профили потенциала Гельмгольца vs Гуи-Чепмена",
        takeaway="Тепловое броуновское движение противодействует электростатическому осаждению противоионов на стенку, формируя экспоненциально спадающую диффузную атмосферу.",
        notes=(
            "1. Физический тезис: Распределение электрического потенциала в двойном электрическом слое (ДЭС) определяется конкуренцией кулоновского притяжения и тепловой диффузии. Модель плоского конденсатора Гельмгольца задает линейный спад потенциала, а модель Гуи–Чепмена описывает диффузную атмосферу распределением Больцмана.\n"
            "2. Визуальные акценты: На верхней панели сопоставлены жесткая мономолекулярная стенка Гельмгольца и тепловое облако ионов Гуи–Чепмена. На нижнем графике показан резкий линейный спад φ(x) плоского конденсатора в сравнении с плавной экспонентой Пуассона–Больцмана с дебаевской длиной экранирования λ_D.\n"
            "3. Инженерный контекст: Модель Гельмгольца применима только при экстремально высоких концентрациях солей, тогда как в разбавленных нанозолях доминирует диффузная атмосфера Гуи–Чепмена, определяющая дальнодействующее электростатическое отталкивание частиц.\n"
            "4. Смысловой переход: Реальный ДЭС совмещает плотный слой у границы раздела и диффузный хвост в объеме жидкости, что объединено в модели Отто Штерна."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 14 (Layout A: Модель Штерна и дебаевский радиус)
    s14_cards = [
        {
            "heading": "1. Объединенная модель Отто Штерна (1924)",
            "height": 2.45,
            "bullets": [
                "ДЭС делится на плотный слой Штерна (толщина δ) и диффузный слой Гуи–Чепмена.",
                "  [Ф] Последовательное соединение емкостей: 1 / C = 1 / C_пл + 1 / C_диф",
                "В слое Штерна потенциал падает линейно от φ₀ до φ_δ, а далее спадает экспоненциально в диффузной области."
            ]
        },
        {
            "heading": "2. Дебаевская длина λ_D и феномен перезарядки",
            "height": 2.45,
            "bullets": [
                "  [Ф] Длина экранирования Дебая: λ_D = κ⁻¹ ∝ 1 / (z · √c)",
                "Рост ионной силы c сжимает защитную шубу ДЭС до единиц нанометров, провоцируя агрегацию.",
                "Специфическая хемосорбция многозарядных ионов (Al³⁺, Th⁴⁺) в слое Штерна способна инвертировать знак потенциала φ_δ."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Объединенная модель Штерна, длина Дебая λ_D и феномен перезарядки",
        subtitle="Раздел 2. Компрессия диффузного слоя электролитами и специфическая адсорбция",
        cards=s14_cards,
        fig_filename="fig_10_stern_model.png",
        fig_desc="Профиль потенциала модели Штерна и закон экранирования Дебая",
        takeaway="Толщина защитной ионной шубы λ_D сжимается обратно пропорционально корню из концентрации соли и валентности иона, а специфическая адсорбция способна инвертировать знак потенциала.",
        notes=(
            "1. Физический тезис: Объединенная модель Штерна делит ДЭС на плотный слой толщиной δ (конечный размер гидратированных ионов) и внешнюю диффузную атмосферу. Дебаевская длина экранирования λ_D обратно пропорциональна валентности z и квадратному корню из концентрации электролита c.\n"
            "2. Визуальные акценты: График модели Штерна демонстрирует излом потенциала на границе x = δ: линейное падение от φ0 до φδ с последующим экспоненциальным затуханием. Показаны три физических режима: базовый спад, специфическая адсорбция и перезарядка поверхности многозарядными катионами Al3+ и Th4+ с инверсией знака φδ.\n"
            "3. Инженерный контекст: Специфическая хемосорбция многозарядных ионов позволяет искусственно инвертировать знак заряда наночастиц без изменения состава кристаллического ядра, обеспечивая стабильность нанозолей в агрессивных электролитах.\n"
            "4. Смысловой переход: Количественные закономерности сжатия и перезарядки ДЭС формируют основу промышленного регламента жидкофазного синтеза коллоидов."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 15 (Layout B Table: Регламент Раздела 2)
    create_slide_15_regulations(
        prs,
        notes=(
            "1. Физический тезис: Технологический регламент устойчивости коллоидов при жидкофазном синтезе требует поддержания критической дебаевской длины экранирования λ_D ≥ 10 нм и строгого разграничения действия индифферентных и неиндифферентных электролитов на двойной электрический слой (ДЭС).\n"
            "2. Визуальные акценты: Полноширинная модульная матрица систематизирует четыре ключевых технологических параметра: ионную силу раствора I, стехиометрический избыток неиндифферентных ПОИ, концентрацию индифферентных электролитов и температурно-кондуктометрический режим.\n"
            "3. Инженерный контекст: Неиндифферентные электролиты достраивают кристаллическую решетку ядра и увеличивают термодинамический потенциал φ0, тогда как индифферентные электролиты лишь сжимают диффузный слой, провоцируя солевой шок при превышении допустимой ионной силы.\n"
            "4. Смысловой переход: Завершив анализ строения ДЭС, перейдем к Разделу 3, где исследуем электрокинетические явления и методику измерения дзета-потенциала на плоскости скольжения."
        )
    )

    # --------------------------------------------------------------------------
    # РАЗДЕЛ 3: СЛЕПОЙ КОНТРОЛЬ И МИКРОФЛЮИДИКА (СЛАЙДЫ 16–20)
    # --------------------------------------------------------------------------
    # Слайд 16 (Разделитель Раздела 3, Layout S #002C5F)
    create_section_divider_slide(
        prs,
        problem_ids=["transport", "processability"],
        title="Слепой контроль стабильности и безнасосный транспорт на чипе",
        subtitle="ПРОБЛЕМНЫЙ РАЗДЕЛ 3: ТЕХНОЛОГИЧЕСКИЙ ВЫЗОВ №3",
        thesis=(
            "Потенциал наночастицы невозможно измерить контактным вольтметром: границей отрыва подвижной жидкости выступает "
            "плоскость скольжения, определяющая дзета-потенциал ζ. Потенциал скольжения управляет четырьмя электрокинетическими "
            "явлениями Рейсса, позволяя реализовать безнасосный электроосмотический транспорт в чипах Lab-on-a-Chip и "
            "электрофоретическое осаждение нанопокрытий. Диагностический критерий «30 мВ» обеспечивает оперативный контроль "
            "стабильности суспензий методами ДРС и ЭЛС."
        ),
        roadmap_steps=[
            "1. Плоскость скольжения, ζ-потенциал и правило 30 мВ",
            "2. 4 явления Рейсса (матрица 2×2)",
            "3. Подвижность u_e и функция Генри f(κr)",
            "4. Чипы Lab-on-a-Chip и контроль ДРС/ЭЛС"
        ],
        style="navy",
        notes=(
            "1. Физический тезис: Потенциал поверхности наночастицы недоступен для прямых вольтметрических измерений: единственным экспериментально определяемым параметром границы фаз выступает электрокинетический дзета-потенциал, возникающий на гидродинамической плоскости скольжения.\n"
            "2. Визуальные акценты: Слайд-разделитель выполнен в темно-синем корпоративном стиле ГУАП Layout S (#002C5F) с центральными векторными иконками транспорта жидкостей и технологичности процессов, открывая третий технологический вызов.\n"
            "3. Инженерный контекст: Электрокинетический потенциал управляет безнасосным транспортом жидкостей в микрофлюидных аналитических лабораториях на чипе Lab-on-a-Chip и процессами электрофоретического осаждения нанопокрытий, а критерий «30 мВ» обеспечивает экспресс-диагностику агрегативной устойчивости суспензий.\n"
            "4. Смысловой переход: Для практического применения электрокинетики определим точное физическое положение плоскости скольжения и диагностический критерий устойчивости."
        )
    )

    # Слайд 17 (Layout A: Дзета-потенциал и правило 30 мВ)
    s17_cards = [
        {
            "heading": "1. Плоскость скольжения x_s и дзета-потенциал (ζ)",
            "height": 2.45,
            "bullets": [
                "При движении частицы в жидкости гидратная оболочка частично увлекается за ней.",
                "Плоскость гидродинамического сдвига x_s отсекает неподвижный слой жидкости от подвижного объема.",
                "  [Ф] Электрокинетический дзета-потенциал (ζ-потенциал): ζ = φ(x_s)",
                "Потенциал ζ строго меньше потенциала поверхности: |ζ| < |φ_δ| < |φ₀|."
            ]
        },
        {
            "heading": "2. Диагностический критерий стабильности «30 мВ»",
            "height": 2.45,
            "bullets": [
                "  [Ф] |ζ| ≥ 30 мВ — длительная агрегативная устойчивость нанозоля.",
                "  [Ф] 15 мВ < |ζ| < 30 мВ — зона коагуляционного риска и медленной агрегации.",
                "  [Ф] |ζ| ≤ 15 мВ — зона потери барьера и быстрой коагуляции.",
                "  [Ф] ζ = 0 мВ — изоэлектрическая точка (ИЭТ), мгновенное выпадение осадка.",
                "Контроль ζ методами лазерного рассеяния света (ДРС и ЭЛС)."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Плоскость скольжения, дзета-потенциал (ζ) и критерий устойчивости «30 мВ»",
        subtitle="Раздел 3. Электрокинетический потенциал как оперативный индикатор стабильности",
        cards=s17_cards,
        fig_filename="fig_11_zeta_potential.png",
        fig_desc="Схема плоскости скольжения и зон устойчивости дзета-потенциала",
        takeaway="Пороговое значение |ζ| ≥ 30 мВ служит общепринятым критерием длительной агрегативной устойчивости коллоидных суспензий в промышленности.",
        notes=(
            "1. Физический тезис: При относительном движении фаз плоскость гидродинамического сдвига xs отсекает неподвижный гидратный слой от объема жидкости, определяя электрокинетический дзета-потенциал ζ = φ(xs), величина которого строго подчиняется иерархии |ζ| < |φδ| < |φ0|.\n"
            "2. Визуальные акценты: На графике наглядно показано положение плоскости скольжения xs за плотным слоем Штерна, а также три диагностические зоны стабильности: зеленая область устойчивости (|ζ| ≥ 30 мВ), оранжевая зона риска (15–30 мВ) и красная зона быстрой коагуляции с изоэлектрической точкой ИЭТ (ζ = 0).\n"
            "3. Инженерный контекст: Измерение дзета-потенциала методами лазерного рассеяния света ДРС и ЭЛС служит промышленным стандартом входного контроля дисперсий в наноиндустрии и фармацевтике.\n"
            "4. Смысловой переход: Тангенциальный сдвиг слоев ДЭС по плоскости скольжения лежит в основе четырех классических явлений Рейсса."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 18 (Layout A: Четыре явления Рейсса)
    s18_cards = [
        {
            "heading": "1. Прямые электрокинетические явления (E → движение)",
            "height": 2.45,
            "bullets": [
                "Электрофорез: направленное перемещение заряженных наночастиц в неподвижной жидкости под действием внешнего поля E.",
                "Электроосмос: движение полярной жидкости через неподвижную пористую диафрагму или капилляр при наложении поля E.",
                "  [Ф] Скорость электроосмоса: v_эо = - (ε ε₀ ζ / η) · E"
            ]
        },
        {
            "heading": "2. Обратные электрокинетические явления (движение → E)",
            "height": 2.45,
            "bullets": [
                "Потенциал седиментации (эффект Дорна): возникновение разности потенциалов при гравитационном оседании заряженных наночастиц.",
                "Потенциал течения (эффект Квинке): появление электрического поля при прокачивании жидкости через пористую мембрану давлением ΔP:",
                "  [Ф] Потенциал течения: Δφ_теч = (ε ε₀ ζ / (η · κ_уд)) · ΔP"
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Четыре электрокинетических явления Рейсса: движение и электрическое поле",
        subtitle="Раздел 3. Прямые и обратные электрокинетические эффекты на границе фаз",
        cards=s18_cards,
        fig_filename="fig_12_electrokinetic_phenomena.png",
        fig_desc="Инфографика 4 электрокинетических явлений Рейсса",
        takeaway="Все 4 явления вызваны взаимным сдвигом заряженных слоев ДЭС по плоскости скольжения и прямо пропорциональны электрокинетическому дзета-потенциалу.",
        notes=(
            "1. Физический тезис: Электрокинетические явления вызваны тангенциальным сдвигом подвижной части ДЭС относительно дисперсной фазы по плоскости скольжения и разделяются на прямые (электрическое поле порождает движение) и обратные (механическое движение генерирует разность потенциалов).\n"
            "2. Визуальные акценты: Четырехпанельная схема сопоставляет прямые явления — электрофорез (движение частиц в жидкости) и электроосмос (поток жидкости в поре со скоростью vэо = -(εε0ζ/η)E) — с обратными явлениями: потенциалом седиментации Дорна и потенциалом течения Квинке (Δφтеч = (εε0ζ/(η·κуд))·ΔP).\n"
            "3. Инженерный контекст: Прямые эффекты используются для транспортировки жидких сред и осаждения покрытий, а обратные служат высокоточными бесконтактными методами определения дзета-потенциала нанопористых диафрагм и мембранных фильтров.\n"
            "4. Смысловой переход: Для количественного пересчета экспериментальной подвижности наночастиц в дзета-потенциал необходимо учитывать размерное соотношение частицы и ДЭС по теории Генри."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 19 (Layout A: Функция Генри)
    s19_cards = [
        {
            "heading": "1. Электрофоретическая подвижность u_e и уравнение Генри",
            "height": 2.45,
            "bullets": [
                "Электрофоретическая подвижность: u_e = v / E [(м/с)/(В/м)].",
                "  [Ф] Обобщенное уравнение Д. Генри (1931):",
                "  [Ф] u_e = [ (2 ε ε₀ ζ) / (3 η) ] · f(κ r)",
                "Безразмерный аргумент κr = r / λ_D определяет отношение радиуса частицы к толщине диффузного слоя ДЭС."
            ]
        },
        {
            "heading": "2. Предельные режимы: Хюккель vs Смолуховский",
            "height": 2.45,
            "bullets": [
                "Предел Хюккеля (κr ≪ 1, толстый ДЭС, неполярные среды): f(κr) = 1.0.",
                "Предел Смолуховского (κr ≫ 1, тонкий ДЭС, электролиты): f(κr) = 1.5.",
                "Большинство наноколлоидов (r ≈ 5–20 нм, λ_D ≈ 3–10 нм) попадают в переходную область κr ≈ 1–5, требующую полного расчета по функции Генри."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Электрофоретическая подвижность и уравнение Генри f(κr)",
        subtitle="Раздел 3. Теоретический расчет дзета-потенциала в переходной нанометровой области",
        cards=s19_cards,
        fig_filename="fig_13_henry_function.png",
        fig_desc="Аналитическая кривая функции Генри с пределами Хюккеля и Смолуховского",
        takeaway="Большинство водных нанозолей (r ~ 5–20 нм, λ_D ~ 3–10 нм) попадают в переходную область κr ~ 1–5, где расчет дзета-потенциала требует полной формулы Генри.",
        notes=(
            "1. Физический тезис: Электрофоретическая подвижность ue = v/E связана с дзета-потенциалом обобщенным уравнением Генри ue = (2εε0ζ/(3η))·f(κr), где безразмерный параметр κr = r/λD задает отношение радиуса наночастицы к толщине диффузной атмосферы экранирования.\n"
            "2. Визуальные акценты: Аналитическая кривая демонстрирует монотонный переход функции f(κr) от предела Хюккеля (f = 1.0 при κr ≪ 1, малые частицы в органических растворителях) к пределу Смолуховского (f = 1.5 при κr ≫ 1, крупные частицы в проводящих водных средах).\n"
            "3. Инженерный контекст: Большинство наноколлоидов с радиусом 5–20 нм попадают в переходный диапазон κr ≈ 1–5, где пренебрежение размерной поправкой Генри приводит к ошибке определения дзета-потенциала до 33%, искажая оценку устойчивости золя.\n"
            "4. Смысловой переход: Перейдем к анализу практических применений электрокинетики в микрофлюидных устройствах и технологиях осаждения функциональных нанопленок."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 20 (Layout A: Микрофлюидика и ЭФО)
    s20_cards = [
        {
            "heading": "1. Безнасосная микрофлюидика на чипе (Lab-on-a-Chip)",
            "height": 2.45,
            "bullets": [
                "Электроосмотический поток в микроканалах чипа создает плоский профиль скоростей без параболической дисперсии Пуазейля.",
                "Отсутствие механических подвижных элементов обеспечивает надежность микронасосов в химических биосенсорах.",
                "Управление напряжением E позволяет с нанолитровой точностью дозировать потоки реактивов."
            ]
        },
        {
            "heading": "2. Электрофоретическое осаждение нанопокрытий (ЭФО)",
            "height": 2.45,
            "bullets": [
                "Направленный перенос заряженных наночастиц на электрод с формированием плотных равномерных нанопленок.",
                "  [Ф] Масса осадка (закон Хэмакера): m = ∫ η_e C u_e E A dt",
                "Промышленный контроль синтезированных партий методами лазерного рассеяния света (ДРС и ЭЛС) исключает брак."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Микрофлюидика на чипе и электрофоретическое осаждение нанопокрытий",
        subtitle="Раздел 3. Промышленные применения электрокинетических явлений в наноиндустрии",
        cards=s20_cards,
        fig_filename="fig_17_colloid_applications.png",
        fig_desc="Прикладные модули микрофлюидики, электрофоретического осаждения и контроля партий",
        takeaway="Электроосмос позволяет создавать микронасосы без механических подвижных элементов, а электрофорез обеспечивает прецизионное нанесение равномерных наноструктурированных слоев.",
        notes=(
            "1. Физический тезис: Безнасосный электроосмотический поток в микроканалах формирует плоский поршневой профиль скоростей Plug Flow, исключающий гидродинамическую дисперсию Пуазейля, а электрофорез обеспечивает направленное осаждение наночастиц на подложку по кинетическому закону Хэмакера.\n"
            "2. Визуальные акценты: На схеме представлены прикладные инженерные модули: микрофлюидный чип Lab-on-a-Chip с безнасосной подачей реагентов, электрофоретическое осаждение (ЭФО) монолитных нанопленок на электрод под действием внешнего поля и схема оптического контроля партий золей методами ДРС и ЭЛС.\n"
            "3. Инженерный контекст: Электроосмотические микронасосы без механических клапанов незаменимы в портативных биосенсорах и ДНК-анализаторах, а метод ЭФО позволяет с высокой однородностью наносить нанопокрытия на проводящие подложки сложной геометрии.\n"
            "4. Смысловой переход: Завершив анализ электрокинетических явлений, перейдем к Разделу 4, посвященному седиментационной устойчивости, теории ДЛФО и стерической защите наноколлоидов."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # --------------------------------------------------------------------------
    # РАЗДЕЛ 4: СЕДИМЕНТАЦИЯ, БАРЬЕР ДЛФО И РЕЦЕПТУРЫ (СЛАЙДЫ 21–26)
    # --------------------------------------------------------------------------
    # Слайд 21 (Разделитель Раздела 4, Layout S #002C5F)
    create_section_divider_slide(
        prs,
        problem_ids=["sedimentation", "storage"],
        title="Расслоение при хранении, солевой шок и рецептуры «вечных» коллоидов",
        subtitle="ПРОБЛЕМНЫЙ РАЗДЕЛ 4: ТЕХНОЛОГИЧЕСКИЙ ВЫЗОВ №4",
        thesis=(
            "Седиментация частиц под действием гравитации подавляется тепловым броуновским движением лишь при радиусе r ≤ 10 нм по закону Перрена. "
            "Агрегативная стабильность определяется балансом сил ван-дер-ваальсова притяжения и кулоновского отталкивания ДЭС по теории ДЛФО с потенциальным барьером U_max ≥ 15 k_B T. "
            "Солевой шок подчиняется закону шестой степени Шульце–Гарди 1/z⁶, а долговременная устойчивость в концентрированных средах достигается стерической защитой ПАВ и полимерами."
        ),
        roadmap_steps=[
            "1. Седиментация Перрена и феррофлюид",
            "2. Барьер теории ДЛФО U_max",
            "3. Закон Шульце–Гарди 1/z⁶",
            "4. Стерическая стабилизация ПАВ"
        ],
        style="navy",
        notes=(
            "1. Физический тезис: Раздел 4 посвящен анализу седиментационно-диффузионного равновесия Перрена, термодинамического барьера устойчивости ДЛФО, каскадного закона солевой коагуляции и стерической защиты коллоидов полимерными щетками.\n"
            "2. Визуальные акценты: Слайд-разделитель выполнен в корпоративном темно-синем стиле ГУАП Layout S (#002C5F) с центральными векторными иконками седиментации и хранения, четко обозначая переход к завершающему проблемному блоку.\n"
            "3. Инженерный контекст: В реальных условиях наночастицы испытывают конкуренцию гравитационного осаждения и броуновской диффузии, а добавление электролитов нейтрализует электростатический барьер ДЭС по закону шестой степени, требуя применения стерической стабилизации.\n"
            "4. Смысловой переход: Начнем анализ с седиментационно-диффузионного равновесия Перрена и вывода критического радиуса наночастиц."
        )
    )

    # Слайд 22 (Layout A: Седиментация Стокса и Перрен)
    s22_cards = [
        {
            "heading": "1. Скорость гравитационного осаждения Стокса",
            "height": 2.45,
            "bullets": [
                "  [Ф] Скорость оседания шарообразной частицы: v_сед = 2 r² Δρ g / (9 η)",
                "Квадратичная зависимость от радиуса: для микрочастиц (r = 1 мкм) осаждение происходит за минуты.",
                "Для наночастиц (r = 5 нм) скорость осаждения составляет доли миллиметра в год."
            ]
        },
        {
            "heading": "2. Барометрическое равновесие Лапласа–Перрена",
            "height": 2.45,
            "bullets": [
                "Броуновская диффузия противодействует гравитационному осаждению:",
                "  [Ф] Распределение концентрации по высоте: n(h) = n₀ · exp(- h / h_e)",
                "  [Ф] Высота эффективного столба: h_e = (3 k_B T) / (4 π r³ Δρ g) ∝ 1 / r³",
                "При радиусе r ≤ 10 нм высота h_e превышает сотни метров: коллоид абсолютно седиментационно устойчив (феррофлюид)."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Седиментационная устойчивость: баланс Стокса и диффузии Перрена",
        subtitle="Раздел 4. Гравитационное расслоение и барометрическое распределение наночастиц",
        cards=s22_cards,
        fig_filename="fig_14_sedimentation_perren.png",
        fig_desc="Баланс седиментации Стокса и диффузии Перрена, феррожидкость",
        takeaway="За счет кубической зависимости высоты столба he ∝ r⁻³ наночастицы с радиусом r ≤ 10 нм обладают абсолютной седиментационной стабильностью при условии отсутствия агрегации.",
        notes=(
            "1. Физический тезис: В гравитационном поле Земли взвешенные наночастицы подчиняются седиментационно-диффузионному равновесию Жана Перрена, где квадратичная скорость осаждения Стокса v_сед = 2 r² (ρ - ρ0) g / (9 η) уравновешивается броуновской диффузией.\n"
            "2. Визуальные акценты: На графиках сопоставлены квадратичный рост скорости оседания v_сед ∝ r² и кубический рост высоты эквивалентной атмосферы he ∝ 1/r³, достигающей сотен метров для частиц радиусом 5–10 нм, что подтверждается устойчивостью феррофлюида во внешнем магнитном поле.\n"
            "3. Инженерный контекст: За счет кубической зависимости высоты столба наночастицы с радиусом r ≤ 10 нм обладают абсолютной седиментационной стабильностью при условии отсутствия агрегации.\n"
            "4. Смысловой переход: Теоретическое описание силового барьера против агрегации дает теория ДЛФО."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 23 (Layout A: Теория ДЛФО)
    s23_cards = [
        {
            "heading": "1. Конкуренция притяжения и отталкивания в теории ДЛФО",
            "height": 2.45,
            "bullets": [
                "Суммарная потенциальная энергия взаимодействия двух частиц:",
                "  [Ф] U_total(h) = U_vdw(h) + U_el(h)",
                "Молекулярное притяжение Ван-дер-Ваальса: U_vdw(h) = - (A_H · r) / (12 h) (степенной спад).",
                "Электростатическое отталкивание перекрывающихся ДЭС: U_el(h) ∝ r ψ₀² · exp(- κ h) (экспоненциальный спад)."
            ]
        },
        {
            "heading": "2. Потенциальный барьер U_max и минимумы энергии",
            "height": 2.45,
            "bullets": [
                "  [Ф] Критерий агрегативной стабильности: U_max ≥ 15–20 k_B T",
                "Первичный минимум (h → 0): глубокая яма, необратимая коагуляция в монолит.",
                "Вторичный минимум (h ~ λ_D): неглубокая яма (1–3 k_B T), обратимая коагуляция с возможностью легкой пептизации."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Теория устойчивости ДЛФО: баланс сил притяжения и отталкивания",
        subtitle="Раздел 4. Потенциальный барьер U_max, первичный и вторичный минимумы",
        cards=s23_cards,
        fig_filename="fig_15_dlvo_potential.png",
        fig_desc="Аналитическая кривая энергии взаимодействия ДЛФО с барьером U_max",
        takeaway="Для предотвращения коагуляции наночастиц потенциальный барьер отталкивания ДЛФО должен превышать энергию тепловых столкновений (U_max ≥ 15–20 k_B T).",
        notes=(
            "1. Физический тезис: Фундаментом коллоидной физики выступает теория Дерягина–Ландау–Фервея–Овербека (ДЛФО), постулирующая аддитивность сил межмолекулярного ван-дер-ваальсова притяжения U_vdw ∝ -A_H / h и электростатического кулоновского отталкивания ДЭС U_el ∝ exp(-κ h).\n"
            "2. Визуальные акценты: На суммарной кривой взаимодействия формируется энергетический профиль с потенциальным барьером U_max: для агрегативной устойчивости высота барьера должна превышать 15–20 k_B T, предотвращая попадание частиц в глубокий первичный потенциальный минимум.\n"
            "3. Инженерный контекст: Введение электролита увеличивает коэффициент экранирования κ, вызывая крутое затухание экспоненты отталкивания и делая возможным самопроизвольное преодоление барьера и коагуляцию.\n"
            "4. Смысловой переход: Исследуем порог исчезновения барьера ДЛФО и выведем закон Дерягина–Ландау."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 24 (Layout B Pure Modular: Шульце-Гарди и Смолуховский)
    create_slide_24_coagulation_modular(
        prs,
        notes=(
            "1. Физический тезис: Критическая концентрация электролита, при которой потенциальный барьер ДЛФО снижается до нуля (U = 0 и dU/dh = 0), называется порогом коагуляции γ_кр и обратно пропорциональна шестой степени заряда коагулирующего противоиона (γ_кр ∝ 1/z⁶).\n"
            "2. Визуальные акценты: На модульном полноширинном слайде сопоставлены три блока: порог коагуляции, каскадный ряд Шульце–Гарди (1 : 1/64 : 1/729 для одно-, двух- и трехзарядных противоионов) и диффузионная кинетика быстрой коагуляции Смолуховского.\n"
            "3. Инженерный контекст: Закон шестой степени объясняет солевой шок: для коагуляции положительного золя Fe(OH)3 трехзарядным анионом требуется концентрация в 729 раз меньшая, чем для однозарядного хлорид-иона.\n"
            "4. Смысловой переход: Для защиты коллоидов в средах с высокой концентрацией солей применяется стерическая стабилизация."
        )
    )

    # Слайд 25 (Layout A: Стерическая стабилизация ПАВ)
    s25_cards = [
        {
            "heading": "1. Стерическая стабилизация полимерами и ПАВ",
            "height": 2.45,
            "bullets": [
                "Адсорбция длинноцепочечных молекул (ПЭГ, ПВП) формирует упругую полимерную щетку на поверхности ядра.",
                "При сближении частиц перекрытие полимерных цепей уменьшает конформационную энтропию:",
                "  [Ф] ΔG_стерич = ΔH_смеш - T ΔS_упруг > 0",
                "Стерическая защита не зависит от концентрации электролитов и предотвращает коагуляцию в физиологических средах."
            ]
        },
        {
            "heading": "2. Мицеллообразование (ККМ) и эффект Ребиндера",
            "height": 2.45,
            "bullets": [
                "Поверхностно-активные вещества (ПАВ) при критической концентрации мицеллообразования (ККМ) образуют прямые и обратные мицеллы.",
                "Эффект Ребиндера: адсорбционное понижение поверхностной энергии твердого тела при диспергировании в присутствии ПАВ:",
                "  [Ф] Δσ = - ∫ Γ dμ < 0",
                "Облегчает механическое измельчение и предотвращает слипание свежеобразованных наноструктур."
            ]
        }
    ]
    create_layout_a_slide(
        prs,
        title="Стерическая стабилизация наносистем полимерами (ПЭГ, ПВП) и ПАВ",
        subtitle="Раздел 4. Полимерные щетки, адсорбционные слои ПАВ и эффект Ребиндера",
        cards=s25_cards,
        fig_filename="fig_16_schultze_hardy_coagulation.png",
        fig_desc="Сжатие барьера ДЛФО и стерическая стабилизация полимерами",
        takeaway="Стерическая стабилизация полимерами не зависит от ионной силы электролита и обеспечивает агрегативную устойчивость коллоидов в физиологических и агрессивных средах.",
        notes=(
            "1. Физический тезис: В средах с высокой ионной силой электростатический барьер ДЭС подавляется, и универсальным решением выступает стерическая стабилизация полимерами (ПЭГ, ПВП) и поверхностно-активными веществами (ПАВ), создающими упругое отталкивание ΔG_стерич = ΔH_смеш - T ΔS_упруг > 0.\n"
            "2. Визуальные акценты: На иллюстрации показаны перекрытие полимерных щеток при сближении частиц, снижение конформационной энтропии цепей, мицеллообразование ПАВ при ККМ и адсорбционное снижение поверхностного натяжения по эффекту Ребиндера Δσ = - ∫ Γ dμ < 0.\n"
            "3. Инженерный контекст: Пэгилирование наночастиц является золотым стандартом наномедицины, обеспечивая сохранение агрегативной устойчивости коллоидов в кровотоке и предотвращая солевую коагуляцию.\n"
            "4. Смысловой переход: Обобщим все изученные стратегии стабилизации в итоговой инженерной матрице лекции."
        ),
        use_placeholders_only=use_placeholders_only
    )

    # Слайд 26 (Layout B Table: Итоговая инженерная матрица)
    create_slide_26_master_matrix(
        prs,
        notes=(
            "1. Физический тезис: Итоговая инженерная матрица управления устойчивостью связывает шесть технологических вызовов нанодисперсности с освоенными физико-химическими инструментами преодоления термодинамических и кинетических барьеров.\n"
            "2. Визуальные акценты: Полноширинная таблица сопоставляет вызовы (агрегация, седиментация, старение, сдвиг, капиллярный коллапс, полидисперсность), физические барьеры, оптимальные стратегии и промышленные регламенты.\n"
            "3. Инженерный контекст: Выбор между электростатической, стерической и структурно-механической защитой определяется химической природой среды, солевым фоном и температурным режимом эксплуатации.\n"
            "4. Смысловой переход: Освоенная система физических принципов и расчетных соотношений составляет теоретическую и практическую базу для проектирования устойчивых нанотехнологических процессов."
        )
    )

    # Автоматическое терминологическое форматирование стандарта R3
    highlight_r3_abbreviations_in_deck(prs)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[SUCCESS] Основная презентация лекции успешно собрана: {output_path} (ровно {len(prs.slides)} слайдов)")
    return prs


# ==============================================================================
# 6. Точка входа в скрипт
# ==============================================================================

if __name__ == "__main__":
    print("=" * 78)
    print("ГЕНЕРАТОР ПРЕЗЕНТАЦИЙ ЛЕКЦИИ №3 (ГУАП, КУРС «ФОН», СЕМЕСТР 4)")
    print("=" * 78)

    # 1. Сборка сравнительной презентации вариаций (14 слайдов)
    print("\n[ЭТАП 1/2] Сборка презентации сравнительных дизайн-вариаций...")
    build_comparative_deck(OUT_VARIATIONS_PPTX)

    # 2. Сборка основной презентации лекции (26 слайдов)
    print("\n[ЭТАП 2/2] Сборка основной лекционной презентации (26 слайдов)...")
    build_lecture_03_deck(OUT_MAIN_PPTX, primary_variation=1, use_placeholders_only=False)

    print("\n" + "=" * 78)
    print("ВСЕ ПРЕЗЕНТАЦИИ УСПЕШНО СКОМПИЛИРОВАНЫ!")
    print(f"1. Сравнительный дек: {OUT_VARIATIONS_PPTX}")
    print(f"2. Основной дек лекции: {OUT_MAIN_PPTX}")
    print("=" * 78)
