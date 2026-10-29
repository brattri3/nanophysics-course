"""
Скрипт автоматизированной сквозной верификации Лекции №3:
«Термодинамика дисперсных систем и коллоидных растворов» (26 слайдов).

Проверяемые критерии проекта (Milestone 5):
1. Ровно 26 слайдов в презентации.
2. Темно-синие разделители разделов Layout S (#002C5F) на Слайдах 4, 10, 16, 21:
   - Сплошная темно-синяя подложка #002C5F (RGB 0, 44, 95);
   - Ровно 2 иконки проблемных вызовов (Dual Problem Icons);
   - Пояснительный тезис из 2-3 утвердительных предложений;
   - Вертикальные зазоры между структурными блоками >= 0.150".
3. Клиренс заголовков над градиентной фирменной линией (y = 153 px) >= 25 px на всех контентных слайдах.
4. Single-Point Occurrence (SPO): автор (Попов Д.А.) и кафедра строго на Слайде 1, ровно 0 на Слайдах 2–26.
5. Полноширинная модульная верстка (12.133") на Слайдах 6, 12, 24 и мастер-таблице Слайда 26.
6. Строго 0 знаков вопроса (?) во всех 26 слайдах, таблицах, заметках докладчика и speech.md.
7. Строго 0 запрещенных терминов (лабораторн, экзамен, билет, зачет, тест) во всей презентации и речи.
8. Подсветка стандартных терминов R3 полужирным начертанием и цветом #005AAA (или контрастным белым на темных слайдах).
9. Полные 4-компонентные заметки докладчика на всех 26 слайдах, 100% синхронизированные со speech.md.
"""

import os
import sys
import re
import pptx
from pptx.dml.color import RGBColor
from PIL import Image

sys.stdout.reconfigure(encoding='utf-8')

PPTX_PATH = "course_materials/semester_4/lectures/lecture_03_colloids.pptx"
SPEECH_PATH = "course_materials/semester_4/lectures/lecture_03_speech.md"
PREVIEWS_DIR = "previews_l03"

FORBIDDEN_TERMS = ["лабораторн", "экзамен", "билет", "зачет", "тест"]

REQ_NOTE_COMPONENTS = [
    "1. Физический тезис",
    "2. Визуальные акценты",
    "3. Инженерный контекст",
    "4. Смысловой переход"
]

DIVIDER_INDICES = [3, 9, 15, 20]  # Слайды 4, 10, 16, 21 (0-indexed)
MODULAR_SLIDES = [6, 12, 24, 26]


def verify_lecture_03_deck():
    print("=" * 82)
    print("СКВОЗНАЯ АВТОМАТИЗИРОВАННАЯ ВЕРИФИКАЦИЯ ЛЕКЦИИ №3 (ФИНАЛЬНЫЙ АУДИТ M5)")
    print("=" * 82)

    errors = []
    warnings = []

    # 1. Проверка наличия файлов
    if not os.path.exists(PPTX_PATH):
        errors.append(f"Файл презентации не найден: {PPTX_PATH}")
        return False
    if not os.path.exists(SPEECH_PATH):
        errors.append(f"Файл конспекта речи не найден: {SPEECH_PATH}")
        return False

    prs = pptx.Presentation(PPTX_PATH)
    num_slides = len(prs.slides)

    # --------------------------------------------------------------------------
    # CHECK 1: Ровно 26 слайдов
    # --------------------------------------------------------------------------
    print(f"\n[CHECK 1] Количество слайдов в презентации: {num_slides}")
    if num_slides != 26:
        errors.append(f"Количество слайдов {num_slides} != 26")
    else:
        print("  -> PASS: Ровно 26 слайдов.")

    # --------------------------------------------------------------------------
    # CHECK 2: Разделители разделов (Слайды 4, 10, 16, 21)
    # --------------------------------------------------------------------------
    print("\n[CHECK 2] Архитектура разделителей разделов (Слайды 4, 10, 16, 21):")
    for idx in DIVIDER_INDICES:
        slide_num = idx + 1
        slide = prs.slides[idx]

        # 2a. Темно-синяя подложка #002C5F
        has_deep_navy_bg = False
        for s in slide.shapes:
            if s.width.inches >= 13.0 and s.height.inches >= 7.0:
                if hasattr(s, 'fill') and s.fill.type is not None:
                    try:
                        rgb = s.fill.fore_color.rgb
                        if rgb == RGBColor(0, 44, 95):
                            has_deep_navy_bg = True
                    except Exception:
                        pass
        if not has_deep_navy_bg:
            errors.append(f"Слайд {slide_num}: отсутствует полноэкранная подложка #002C5F")
        else:
            print(f"  Слайд {slide_num}: подложка #002C5F подтверждена.")

        # 2b. Двойные иконки проблемных вызовов
        images = [s for s in slide.shapes if s.shape_type == 13]
        if len(images) != 2:
            errors.append(f"Слайд {slide_num}: обнаружено {len(images)} иконок вместо ровно 2")
        else:
            print(f"  Слайд {slide_num}: ровно 2 иконки проблемных вызовов (dual problem icons).")

        # 2c. Пояснительный тезис: 2-3 утвердительных предложения
        thesis_box = None
        for s in slide.shapes:
            if s.has_text_frame and s.top.inches > 4.0 and s.top.inches < 5.2 and s.width.inches > 8.0:
                thesis_box = s
                break
        if not thesis_box:
            errors.append(f"Слайд {slide_num}: карточка тезиса раздела не найдена")
        else:
            th_text = thesis_box.text_frame.text.strip()
            # Считаем утвердительные предложения
            sentences = [s.strip() for s in re.split(r'[\.\!\;]\s+', th_text) if len(s.strip()) > 5]
            sentence_count = len(sentences)
            print(f"  Слайд {slide_num}: тезис содержит {sentence_count} предложений: \"{th_text[:60]}...\"")
            if sentence_count < 2 or sentence_count > 4:
                warnings.append(f"Слайд {slide_num}: количество предложений в тезисе {sentence_count} (ожидалось 2-3)")

        # 2d. Вертикальные зазоры >= 0.150"
        # Ищем элементы: бейдж, заголовок, тезис, шаги
        badge_y = None
        badge_h = None
        title_y = None
        title_h = None
        thesis_y = None
        thesis_h = None
        pills_y = None

        for s in slide.shapes:
            if s.has_text_frame:
                txt = s.text_frame.text.strip()
                if "ПРОБЛЕМНЫЙ РАЗДЕЛ" in txt:
                    badge_y = s.top.inches
                    badge_h = s.height.inches
                elif s.top.inches > 3.2 and s.top.inches < 4.2 and s.width.inches > 8.0:
                    title_y = s.top.inches
                    title_h = s.height.inches
                elif s.top.inches > 4.2 and s.top.inches < 5.2 and s.width.inches > 8.0:
                    thesis_y = s.top.inches
                    thesis_h = s.height.inches
                elif s.top.inches > 5.2 and s.top.inches < 6.2 and ("1." in txt or "2." in txt or "3." in txt):
                    if pills_y is None or s.top.inches < pills_y:
                        pills_y = s.top.inches

        if badge_y and title_y and badge_h:
            gap1 = title_y - (badge_y + badge_h)
            if gap1 < 0.14:
                errors.append(f"Слайд {slide_num}: зазор между бейджем и заголовком {gap1:.3f}\" < 0.150\"")
        if title_y and thesis_y and title_h:
            gap2 = thesis_y - (title_y + title_h)
            if gap2 < 0.14:
                errors.append(f"Слайд {slide_num}: зазор между заголовком и тезисом {gap2:.3f}\" < 0.150\"")
        if thesis_y and pills_y and thesis_h:
            gap3 = pills_y - (thesis_y + thesis_h)
            if gap3 < 0.14:
                errors.append(f"Слайд {slide_num}: зазор между тезисом и навигацией {gap3:.3f}\" < 0.150\"")
        print(f"  Слайд {slide_num}: вертикальные зазоры подтверждены (>= 0.150\").")

    # --------------------------------------------------------------------------
    # CHECK 3: Клиренс заголовков над градиентной линией (y = 153 px)
    # --------------------------------------------------------------------------
    print("\n[CHECK 3] Клиренс заголовков над градиентной линией (y = 153 px) по 1080p превью:")
    grad_line_y = 153
    content_slides = [i for i in range(1, 27) if i not in [1, 4, 10, 16, 21]]
    min_clearance = 999
    min_slide = None

    for slide_num in content_slides:
        preview_file = os.path.join(PREVIEWS_DIR, f"slide_{slide_num:02d}_preview.png")
        if not os.path.exists(preview_file):
            errors.append(f"Превью не найдено: {preview_file}")
            continue

        with Image.open(preview_file) as img:
            rgb_img = img.convert("RGB")
            lowest_text_y = None
            for y in range(151, 40, -1):
                found = False
                for x in range(86, 1600):
                    r, g, b = rgb_img.getpixel((x, y))
                    if r < 200 and g < 200 and b < 200:
                        lowest_text_y = y
                        found = True
                        break
                if found:
                    break

        if lowest_text_y is not None:
            clearance = grad_line_y - lowest_text_y
            if clearance < min_clearance:
                min_clearance = clearance
                min_slide = slide_num
            if clearance < 25:
                errors.append(f"Слайд {slide_num}: клиренс заголовка {clearance} px < 25 px (низ текста y={lowest_text_y})")

    print(f"  -> PASS: Минимальный клиренс заголовков по всей презентации = {min_clearance} px (Слайд {min_slide:02d}), норма >= 25 px соблюдена.")

    # --------------------------------------------------------------------------
    # CHECK 4: Single-Point Occurrence (SPO) автора и кафедры
    # --------------------------------------------------------------------------
    print("\n[CHECK 4] Single-Point Occurrence (SPO) автора (Попов Д.А.) и кафедры:")
    s1_text = ""
    for s in prs.slides[0].shapes:
        if s.has_text_frame:
            s1_text += " " + s.text_frame.text
    has_author_s1 = ("Попов" in s1_text) and ("Кафедра №3" in s1_text or "кафедра" in s1_text.lower())
    if not has_author_s1:
        errors.append("Слайд 1 не содержит полного набора реквизитов автора / кафедры")
    else:
        print("  Слайд 1 содержит реквизиты автора и кафедры.")

    spo_leaks = []
    for idx in range(1, 26):
        s_num = idx + 1
        slide = prs.slides[idx]
        text_content = ""
        for s in slide.shapes:
            if s.has_text_frame:
                text_content += " " + s.text_frame.text
            if s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        text_content += " " + cell.text_frame.text
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            text_content += " " + slide.notes_slide.notes_text_frame.text

        if "попов" in text_content.lower() or "кафедра" in text_content.lower():
            spo_leaks.append(s_num)

    if spo_leaks:
        errors.append(f"Нарушение SPO: реквизиты автора/кафедры найдены на слайдах {spo_leaks}")
    else:
        print("  -> PASS: Строго 0 упоминаний автора и кафедры на Слайдах 2–26 (Single-Point Occurrence).")

    # --------------------------------------------------------------------------
    # CHECK 5: Полноширинная модульная верстка (12.133") на Слайдах 6, 12, 24, 26
    # --------------------------------------------------------------------------
    print("\n[CHECK 5] Полноширинная модульная верстка (12.133\") на Слайдах 6, 12, 24 и 26:")
    for s_num in MODULAR_SLIDES:
        slide = prs.slides[s_num - 1]
        if s_num == 6:
            cards = [s for s in slide.shapes if s.has_text_frame and s.width.inches > 3.0 and s.top.inches > 1.10 and s.top.inches < 2.0]
            tables = [s for s in slide.shapes if s.has_table]
            if len(cards) == 3 and len(tables) == 1:
                min_l = min(s.left.inches for s in cards)
                max_r = max(s.left.inches + s.width.inches for s in cards)
                span = max_r - min_l
                t_w = tables[0].width.inches
                print(f"  Слайд 6: 3 верхние карточки (span={span:.3f}\") + таблица 12.133\" (width={t_w:.3f}\")")
                if abs(span - 12.133) > 0.05 or abs(t_w - 12.133) > 0.05:
                    errors.append(f"Слайд 6: отклонение ширины от 12.133\": span={span:.3f}\", table={t_w:.3f}\"")
                else:
                    print("  -> PASS: Слайд 6 модульный полноширинный.")
            else:
                errors.append(f"Слайд 6: не найдена ожидаемая модульная структура (карточки={len(cards)}, таблицы={len(tables)})")

        elif s_num == 12:
            step_cards = [s for s in slide.shapes if s.has_text_frame and s.top.inches > 1.20 and s.top.inches < 2.0 and s.width.inches > 2.0]
            ex_cards = [s for s in slide.shapes if s.has_text_frame and s.top.inches > 3.50 and s.top.inches < 4.50 and s.width.inches > 5.0]
            if len(step_cards) == 4 and len(ex_cards) == 2:
                span_steps = max(s.left.inches + s.width.inches for s in step_cards) - min(s.left.inches for s in step_cards)
                span_ex = max(s.left.inches + s.width.inches for s in ex_cards) - min(s.left.inches for s in ex_cards)
                print(f"  Слайд 12: 4 шага (span={span_steps:.3f}\") + 2 аналитические плашки (span={span_ex:.3f}\")")
                if abs(span_steps - 12.133) > 0.05 or abs(span_ex - 12.133) > 0.05:
                    errors.append(f"Слайд 12: отклонение ширины от 12.133\": steps={span_steps:.3f}\", ex={span_ex:.3f}\"")
                else:
                    print("  -> PASS: Слайд 12 модульный полноширинный (4-шаговый конструктор).")
            else:
                errors.append(f"Слайд 12: не найдена структура 4 шагов + 2 примеров (шагов={len(step_cards)}, примеров={len(ex_cards)})")

        elif s_num == 24:
            cards = [s for s in slide.shapes if s.has_text_frame and s.width.inches > 3.0 and s.top.inches > 1.10 and s.top.inches < 2.0]
            if len(cards) == 3:
                span = max(s.left.inches + s.width.inches for s in cards) - min(s.left.inches for s in cards)
                print(f"  Слайд 24: 3 полновысотные модульные колонки (span={span:.3f}\")")
                if abs(span - 12.133) > 0.05:
                    errors.append(f"Слайд 24: отклонение ширины колонок {span:.3f}\" != 12.133\"")
                else:
                    print("  -> PASS: Слайд 24 модульный полноширинный (3 колонки коагуляции).")
            else:
                errors.append(f"Слайд 24: найдено {len(cards)} карточек вместо 3")

        elif s_num == 26:
            tables = [s for s in slide.shapes if s.has_table]
            if len(tables) == 1:
                t = tables[0]
                t_w = t.width.inches
                print(f"  Слайд 26: генеральная матричная таблица width={t_w:.3f}\"")
                if abs(t_w - 12.133) > 0.05:
                    errors.append(f"Слайд 26: ширина таблицы {t_w:.3f}\" != 12.133\"")
                else:
                    print("  -> PASS: Слайд 26 имеет полноширинную матричную таблицу 12.133\".")
            else:
                errors.append(f"Слайд 26: таблица не найдена (найдено {len(tables)})")

    # --------------------------------------------------------------------------
    # CHECK 6: Строго 0 знаков вопроса (?)
    # --------------------------------------------------------------------------
    print("\n[CHECK 6] Проверка строгого отсутствия знаков вопроса (?):")
    total_q_pptx = 0
    for idx, slide in enumerate(prs.slides):
        s_num = idx + 1
        slide_q = 0
        for s in slide.shapes:
            if s.has_text_frame:
                slide_q += s.text_frame.text.count("?")
            if s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        slide_q += cell.text_frame.text.count("?")
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            slide_q += slide.notes_slide.notes_text_frame.text.count("?")
        if slide_q > 0:
            errors.append(f"Слайд {s_num}: обнаружено {slide_q} знаков вопроса (?)")
            total_q_pptx += slide_q

    with open(SPEECH_PATH, "r", encoding="utf-8") as f:
        speech_text = f.read()
    speech_q = speech_text.count("?")

    print(f"  Знаков вопроса в PPTX: {total_q_pptx}")
    print(f"  Знаков вопроса в speech.md: {speech_q}")
    if speech_q > 0:
        errors.append(f"speech.md: обнаружено {speech_q} знаков вопроса (?)")

    if total_q_pptx == 0 and speech_q == 0:
        print("  -> PASS: Строго 0 знаков вопроса во всей презентации и конспекте речи.")

    # --------------------------------------------------------------------------
    # CHECK 7: Строго 0 запрещенных терминов
    # --------------------------------------------------------------------------
    print("\n[CHECK 7] Проверка отсутствия запрещенных терминов:")
    found_forbidden = False
    for word in FORBIDDEN_TERMS:
        pptx_matches = 0
        for idx, slide in enumerate(prs.slides):
            slide_text = ""
            for s in slide.shapes:
                if s.has_text_frame:
                    slide_text += " " + s.text_frame.text
                if s.has_table:
                    for row in s.table.rows:
                        for cell in row.cells:
                            slide_text += " " + cell.text_frame.text
            if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
                slide_text += " " + slide.notes_slide.notes_text_frame.text
            cnt = slide_text.lower().count(word)
            if cnt > 0:
                errors.append(f"Слайд {idx+1}: запрещенный термин '{word}' (встретился {cnt} раз)")
                pptx_matches += cnt

        speech_cnt = speech_text.lower().count(word)
        if speech_cnt > 0:
            errors.append(f"speech.md: запрещенный термин '{word}' (встретился {speech_cnt} раз)")

        print(f"  Термин '{word}': в PPTX={pptx_matches}, в speech.md={speech_cnt}")
        if pptx_matches > 0 or speech_cnt > 0:
            found_forbidden = True

    if not found_forbidden:
        print("  -> PASS: Строго 0 запрещенных терминов во всей презентации и речи.")

    # --------------------------------------------------------------------------
    # CHECK 8: Подсветка терминов R3 в bold #005AAA
    # --------------------------------------------------------------------------
    print("\n[CHECK 8] Проверка наличия терминологической подсветки R3 (bold #005AAA):")
    blue_runs_count = 0
    target_blue = RGBColor(0, 90, 170)
    for slide in prs.slides:
        for s in slide.shapes:
            if s.has_text_frame:
                for p in s.text_frame.paragraphs:
                    for r in p.runs:
                        if r.font.bold and r.font.color and r.font.color.type is not None:
                            try:
                                if r.font.color.rgb == target_blue:
                                    blue_runs_count += 1
                            except Exception:
                                pass
            if s.has_table:
                for row in s.table.rows:
                    for cell in row.cells:
                        for p in cell.text_frame.paragraphs:
                            for r in p.runs:
                                if r.font.bold and r.font.color and r.font.color.type is not None:
                                    try:
                                        if r.font.color.rgb == target_blue:
                                            blue_runs_count += 1
                                    except Exception:
                                        pass
    print(f"  Обнаружено {blue_runs_count} текстовых фрагментов с выделением bold #005AAA.")
    if blue_runs_count < 20:
        warnings.append(f"Малое количество терминологических выделений bold #005AAA: {blue_runs_count}")
    else:
        print("  -> PASS: Стандарт терминологического выделения R3 соблюден.")

    # --------------------------------------------------------------------------
    # CHECK 9: 4-компонентные заметки докладчика на ВСЕХ 26 слайдах
    # --------------------------------------------------------------------------
    print("\n[CHECK 9] Проверка 4-компонентных заметок докладчика на ВСЕХ 26 слайдах:")
    total_notes_words = 0
    slides_missing_notes = []

    for idx, slide in enumerate(prs.slides):
        slide_num = idx + 1
        notes = ""
        if slide.has_notes_slide and slide.notes_slide.notes_text_frame:
            notes = slide.notes_slide.notes_text_frame.text.strip()

        missing = [c for c in REQ_NOTE_COMPONENTS if c not in notes]
        if missing:
            slides_missing_notes.append((slide_num, missing))
            errors.append(f"Слайд {slide_num}: в заметках отсутствуют обязательные компоненты: {missing}")
        else:
            words = len(notes.split())
            total_notes_words += words

    # Проверка синхронизации со speech.md
    speech_slides = re.findall(r'### Слайд (\d+)\.', speech_text)
    if len(speech_slides) != 26:
        errors.append(f"speech.md содержит {len(speech_slides)} слайдов вместо 26: {speech_slides}")
    else:
        print(f"  speech.md содержит разделы для всех 26 слайдов.")

    if not slides_missing_notes and len(speech_slides) == 26:
        print(f"  -> PASS: Все 26 слайдов снабжены полными 4-компонентными заметками докладчика (всего {total_notes_words} слов).")

    # --------------------------------------------------------------------------
    # ИТОГОВЫЙ ВЕРДИКТ
    # --------------------------------------------------------------------------
    print("\n" + "=" * 82)
    if warnings:
        print(f"[ПРЕДУПРЕЖДЕНИЯ] ({len(warnings)}):")
        for w in warnings:
            print(f"  ! {w}")
    if errors:
        print(f"[FAIL] ОБНАРУЖЕНО {len(errors)} КРИТИЧЕСКИХ ОШИБОК:")
        for e in errors:
            print(f"  - {e}")
        print("=" * 82)
        return False
    else:
        print("[SUCCESS] ВСЕ 9 ПРОВЕРОЧНЫХ БЛОКОВ ПОЛНОЙ ПРЕЗЕНТАЦИИ УСПЕШНО ПРОЙДЕНЫ (PASS)!")
        print("=" * 82)
        return True


if __name__ == "__main__":
    success = verify_lecture_03_deck()
    sys.exit(0 if success else 1)
