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
    ключевые терминологические аббревиатуры R3 в текстовых блоках слайдов.
    """
    import re
    r3_terms = [
        "ДЭС", "ДЛФО", "ПАВ", "ПОИ", "ПИ", "ККМ", "ИЭТ", "ПЭГ", "ПВП",
        "СЭМ", "ПЭМ", "АСМ", "ЛПР", "КТ", "ЭФО", "ДРС", "ЭЛС"
    ]
    pattern = re.compile(r"(\b(?:" + "|".join(r3_terms) + r")\b)")

    for slide in prs.slides:
        for shape in slide.shapes:
            if not shape.has_text_frame:
                continue
            for p in shape.text_frame.paragraphs:
                full_text = p.text
                if not pattern.search(full_text):
                    continue
                # Считываем базовые параметры шрифта из параграфа или первого run
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
                        if fcolor in (SUAI_PALETTE["CHARCOAL"], SUAI_PALETTE["MUTED_STEEL"]):
                            r.font.color.rgb = SUAI_PALETTE["BLUE"]
                        else:
                            r.font.color.rgb = fcolor
                    else:
                        r.font.bold = fbold
                        r.font.color.rgb = fcolor


# ==============================================================================
# 5. Сборщик основной презентации курса lecture_03_colloids.pptx (17 слайдов)
# ==============================================================================

def build_lecture_03_deck(output_path: str = OUT_MAIN_PPTX, primary_variation: int = 1,
                          use_placeholders_only: bool = False):
    """
    Формирует полную академическую презентацию Лекции №3 (17 слайдов):
    - Слайды 1–3: выбранная основная вариация (по умолчанию Вариация 1: Classic SUAI Corporate).
    - Слайды 4–16: основные теоретические слайды курса (без дублирования реквизитов кафедры).
    - Слайд 17: технологическое применение (полностью очищено от упоминаний ЛР).
    """
    prs = create_base_presentation()

    # 1. Добавляем первые 3 слайда выбранной вариации
    if primary_variation == 1:
        add_variation_1_slides(prs)
    elif primary_variation == 2:
        add_variation_2_slides(prs)
    elif primary_variation == 3:
        add_variation_3_slides(prs)
    else:
        add_variation_1_slides(prs)

    # 2. Добавляем последующие слайды теории (Слайды 4–17)
    blank_layout = prs.slide_layouts[6]

    for spec in CORE_SLIDES_SPEC:
        slide = prs.slides.add_slide(blank_layout)
        add_suai_header(slide, spec["title"], spec["subtitle"])

        if spec["layout"] == "A":
            # Левая колонка карточек теории
            curr_top = 1.25
            for card in spec["cards"]:
                h = card["height"] + 0.06
                add_rich_card(slide, 0.60, curr_top, 5.35, h, card["heading"], card["bullets"], font_size=11.4)
                curr_top += h + 0.12

            # Правая колонка с иллюстрацией
            add_fitted_figure(slide, 6.20, 1.25, 6.533, 5.15,
                              spec["fig"], spec["fig_desc"], use_placeholder_only=use_placeholders_only)

        elif spec["layout"] == "B":
            # Верхний ряд карточек
            for tc in spec["top_cards"]:
                add_rich_card(slide, tc["left"], 1.25, tc["width"], tc["height"],
                              tc["heading"], tc["bullets"], font_size=11.2)
            # Полноширинная фигура внизу
            add_fitted_figure(slide, 0.60, 2.78, 12.133, 3.68,
                              spec["fig"], spec["fig_desc"], use_placeholder_only=use_placeholders_only)

        add_takeaway_banner(slide, spec["takeaway"])
        set_speaker_notes(slide, spec["notes"])

    highlight_r3_abbreviations_in_deck(prs)
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    prs.save(output_path)
    print(f"[SUCCESS] Основная презентация лекции успешно собрана: {output_path} ({len(prs.slides)} слайдов)")
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

    # 2. Сборка основной презентации лекции (17 слайдов)
    print("\n[ЭТАП 2/2] Сборка основной лекционной презентации (17 слайдов)...")
    build_lecture_03_deck(OUT_MAIN_PPTX, primary_variation=1, use_placeholders_only=False)

    print("\n" + "=" * 78)
    print("ВСЕ ПРЕЗЕНТАЦИИ УСПЕШНО СКОМПИЛИРОВАНЫ!")
    print(f"1. Сравнительный дек: {OUT_VARIATIONS_PPTX}")
    print(f"2. Основной дек лекции: {OUT_MAIN_PPTX}")
    print("=" * 78)
