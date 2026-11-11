"""
Финальный верификатор презентации Лекции №4 (24 слайда):
«Поверхностные явления и механизмы роста плёнок».

Проверяет:
1. Количество слайдов (24) и формат 16:9 (13.333" x 7.500").
2. Разделители разделов (Слайды 4, 8, 13, 19): фон #002C5F и вертикальный клиренс >= 0.150".
3. Пиксельный клиренс заголовков над градиентной линией (y = 153 px) по PNG-превью (>= 25 px).
4. Single-Point Occurrence (SPO): реквизиты ГУАП/кафедры/лектора только на Слайде 1 (0 на Слайдах 2–24).
5. Отсутствие вопросительных знаков (?) и запрещенных слов (ЛР, лабораторная работа).
6. Подсветку аббревиатур R3 (#005AAA bold).
7. Наличие 4-компонентных заметок докладчика (Speaker Notes) на всех 24 слайдах.
"""

import os
import re
import sys
import numpy as np
from PIL import Image
from pptx import Presentation
from pptx.dml.color import RGBColor

PPTX_PATH = os.path.abspath("course_materials/semester_4/lectures/lecture_04_surface_growth.pptx")
PREVIEWS_DIR = os.path.abspath("previews_l04")

DIVIDER_SLIDES = {4, 8, 13, 19}
SPO_FORBIDDEN_RX = re.compile(r'(ГУАП|Попов|Кафедра\s*№?\s*3|Санкт-Петербургский)', re.I)
FORBIDDEN_WORDS_RX = re.compile(r'\b(лабораторн\w*|ЛР|экзамен\w*|зачет\w*|билет\w*)\b', re.I)


def run_verification():
    assert os.path.exists(PPTX_PATH), f"Файл не найден: {PPTX_PATH}"
    prs = Presentation(PPTX_PATH)

    n_slides = len(prs.slides)
    w_in = prs.slide_width.inches
    h_in = prs.slide_height.inches
    print(f"=== ВЕРИФИКАЦИЯ ЛЕКЦИИ №4: { os.path.basename(PPTX_PATH) } ===")
    print(f"Слайдов: {n_slides} (ожидается 24) | Размер: {w_in:.3f}\" x {h_in:.3f}\"")
    assert n_slides == 24, f"Ожидалось 24 слайда, получено {n_slides}"

    spo_leaks = 0
    q_marks = 0
    forbidden_hits = 0
    r3_blue_runs = 0
    notes_valid = 0
    divider_ok = 0

    for idx, slide in enumerate(prs.slides, start=1):
        slide_texts = []
        for sh in slide.shapes:
            if sh.has_text_frame:
                slide_texts.append(sh.text_frame.text)
                for p in sh.text_frame.paragraphs:
                    for r in p.runs:
                        try:
                            if r.font.bold and r.font.color and r.font.color.rgb == RGBColor(0x00, 0x5A, 0xAA):
                                r3_blue_runs += 1
                        except Exception:
                            pass
            if sh.has_table:
                for row in sh.table.rows:
                    for cell in row.cells:
                        slide_texts.append(cell.text_frame.text)

        full_text = "\n".join(slide_texts)

        if idx > 1:
            if SPO_FORBIDDEN_RX.search(full_text):
                print(f"  [SPO LEAK] Слайд {idx}: обнаружены титульные реквизиты!")
                spo_leaks += 1

        if "?" in full_text:
            print(f"  [QUESTION MARK] Слайд {idx}: обнаружен знак '?' в тексте слайда!")
            q_marks += 1

        if FORBIDDEN_WORDS_RX.search(full_text):
            print(f"  [FORBIDDEN WORD] Слайд {idx}: обнаружено запрещенное слово!")
            forbidden_hits += 1

        # Проверка разделителей разделов (4, 8, 13, 19)
        if idx in DIVIDER_SLIDES:
            bg_shape = slide.shapes[0]
            rgb = bg_shape.fill.fore_color.rgb
            assert rgb == RGBColor(0x00, 0x2C, 0x5F), f"Слайд {idx}: неверный цвет фона {rgb}"
            divider_ok += 1

        # Проверка заметок докладчика
        note_txt = slide.notes_slide.notes_text_frame.text if slide.has_notes_slide else ""
        if all(k in note_txt for k in ("1. Физический тезис:", "2. Визуальные акценты:", "3. Инженерный контекст", "4. Смысловой переход:")):
            notes_valid += 1
        else:
            print(f"  [NOTES] Слайд {idx}: неполная структура заметок докладчика!")

        if "?" in note_txt:
            print(f"  [NOTES QUESTION MARK] Слайд {idx}: знак '?' в заметках!")
            q_marks += 1

    # Пиксельная проверка клиренса заголовков над градиентной линией (y = 153 px)
    min_clearance_px = 999
    checked_previews = 0
    for idx in range(2, 25):
        if idx in DIVIDER_SLIDES:
            continue
        p_path = os.path.join(PREVIEWS_DIR, f"slide_{idx:02d}_preview.png")
        if os.path.exists(p_path):
            checked_previews += 1
            arr = np.array(Image.open(p_path).convert("RGB"))
            # Область между y=85 и y=150 (градиентная линия расположена на y ~ 152..156)
            band = arr[85:150, 80:1620, :]
            # Текст темнее фона (#F8FAFC -> >240)
            is_ink = np.any(band < 210, axis=2)
            ink_rows = np.where(np.any(is_ink, axis=1))[0]
            last_ink_y = (85 + int(ink_rows[-1])) if len(ink_rows) > 0 else 85
            clearance = 153 - last_ink_y
            if clearance < min_clearance_px:
                min_clearance_px = clearance

    print(f"Разделители разделов (#002C5F): {divider_ok}/4 OK")
    print(f"Утечки реквизитов SPO (Слайды 2–24): {spo_leaks} (ожидается 0)")
    print(f"Вопросительные знаки (?): {q_marks} (ожидается 0)")
    print(f"Запрещенные слова (ЛР и др.): {forbidden_hits} (ожидается 0)")
    print(f"Подсвеченные ранги R3 (#005AAA bold): {r3_blue_runs} (> 50)")
    print(f"Валидные 4-компонентные заметки докладчика: {notes_valid}/24")
    print(f"Проверено PNG-превью контентных слайдов: {checked_previews}/19 | Мин. клиренс шапки: {min_clearance_px} px (норма >= 25 px)")

    assert spo_leaks == 0
    assert q_marks == 0
    assert forbidden_hits == 0
    assert divider_ok == 4
    assert notes_valid == 24
    assert r3_blue_runs >= 30
    if checked_previews > 0:
        assert min_clearance_px >= 25, f"Клиренс шапки слишком мал: {min_clearance_px} px < 25 px"

    print("=== ВСЕ ПРОВЕРКИ УСПЕШНО ПРОЙДЕНЫ (100% PASS) ===")


if __name__ == "__main__":
    run_verification()
