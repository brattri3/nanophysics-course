#!/usr/bin/env python3
"""
generate_problem_icons.py
=========================
Генератор сквозной системы минималистичных векторных иконок-маркеров 6 фундаментальных
технологических проблем наноматериалов для курса «Физические основы нанотехнологий» (ГУАП).

Фирменная палитра ГУАП (SUAI Theme Palette):
- Агрегация / Слипание:       #E70F47 (SUAI Crimson, Accent 2)
- Седиментация / Осадок:      #002C5F (SUAI Deep Navy, dk2)
- Хранение / Старение:        #FF6418 (SUAI Orange, Accent 5)
- Транспорт / Доставка:       #9269C9 (SUAI Purple, Accent 4)
- Сепарация / Разделение:     #00BEF3 (SUAI Cyan, Accent 3)
- Технологичность / Процесс:  #009A49 (SUAI Emerald Green, Accent 6)

Выходные форматы:
- 600 x 600 px (300 DPI)
- Прозрачный фон вокруг круглой плашки (#F4F7FA)
- Субпиксельное сглаживание методом 4x-суперсемплинга (Lanczos)
- Сохранение в course_materials/templates/icons/ и figures_l03/icons/
"""

import os
import math
import shutil
from PIL import Image, ImageDraw

# Константы палитры ГУАП
SUAI_CRIMSON = "#E70F47"
SUAI_NAVY    = "#002C5F"
SUAI_ORANGE  = "#FF6418"
SUAI_PURPLE  = "#9269C9"
SUAI_CYAN    = "#00BEF3"
SUAI_GREEN   = "#009A49"
SUAI_CHARCOAL= "#242834"
SUAI_CARD_BG = "#F4F7FA"

def render_badge(draw, size, scale, border_color):
    """Отрисовка круглой фоновой плашки с фирменной окантовкой."""
    center = size / 2
    radius = (size / 2) - (18 * scale)
    lw = 8 * scale
    draw.ellipse(
        [center - radius, center - radius, center + radius, center + radius],
        fill=SUAI_CARD_BG,
        outline=border_color,
        width=lw
    )
    return center, radius

def draw_arrow(draw, start, end, color, width, head_size):
    """Отрисовка направляющего вектора/стрелки с пропорциональным наконечником."""
    draw.line([start, end], fill=color, width=width)
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    length = math.hypot(dx, dy)
    if length == 0:
        return
    ux, uy = dx / length, dy / length
    perp_x, perp_y = -uy, ux
    p1 = (end[0] - ux * head_size + perp_x * (head_size * 0.6),
          end[1] - uy * head_size + perp_y * (head_size * 0.6))
    p2 = (end[0] - ux * head_size - perp_x * (head_size * 0.6),
          end[1] - uy * head_size - perp_y * (head_size * 0.6))
    draw.polygon([end, p1, p2], fill=color)

def generate_aggregation(scale=4) -> Image.Image:
    """1. Агрегация / Слипание (#E70F47 Crimson): две сближающиеся наносферы с векторами притяжения."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_CRIMSON)
    
    r_core = 70 * scale
    offset = 110 * scale
    
    # Ионные диффузные оболочки (ореол ДЭС)
    draw.ellipse([center - offset - r_core - 15*scale, center - r_core - 15*scale,
                  center - offset + r_core + 15*scale, center + r_core + 15*scale],
                 fill=None, outline=SUAI_CRIMSON, width=3*scale)
    draw.ellipse([center + offset - r_core - 15*scale, center - r_core - 15*scale,
                  center + offset + r_core + 15*scale, center + r_core + 15*scale],
                 fill=None, outline=SUAI_CRIMSON, width=3*scale)

    # Ядра наночастиц
    draw.ellipse([center - offset - r_core, center - r_core,
                  center - offset + r_core, center + r_core],
                 fill=SUAI_CRIMSON)
    draw.ellipse([center + offset - r_core, center - r_core,
                  center + offset + r_core, center + r_core],
                 fill=SUAI_CRIMSON)

    # Силы Ван-дер-Ваальсова взаимного притяжения (внутренние векторы)
    y_arr = center
    draw_arrow(draw, (center - offset + r_core + 15*scale, y_arr),
                     (center - 10*scale, y_arr), SUAI_CHARCOAL, 8*scale, 24*scale)
    draw_arrow(draw, (center + offset - r_core - 15*scale, y_arr),
                     (center + 10*scale, y_arr), SUAI_CHARCOAL, 8*scale, 24*scale)
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_sedimentation(scale=4) -> Image.Image:
    """2. Седиментация / Осадок (#002C5F Deep Navy): частицы, оседающие по закону Стокса на дно."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_NAVY)
    
    # Линия дна кюветы
    y_base = center + 140 * scale
    draw.line([(center - 150*scale, y_base), (center + 150*scale, y_base)],
              fill=SUAI_CHARCOAL, width=10*scale)
    
    # Плотный слой осажденных наночастиц
    r_s = 24 * scale
    xs = [-120, -75, -30, 15, 60, 105, -95, -50, -5, 40, 85]
    ys = [y_base - r_s, y_base - r_s, y_base - r_s, y_base - r_s, y_base - r_s, y_base - r_s,
          y_base - 2.5*r_s, y_base - 2.5*r_s, y_base - 2.5*r_s, y_base - 2.5*r_s, y_base - 2.5*r_s]
    for x, y in zip(xs, ys):
        draw.ellipse([center + x*scale - r_s, y - r_s, center + x*scale + r_s, y + r_s],
                     fill=SUAI_NAVY)

    # Оседающая частица
    r_fall = 38 * scale
    y_fall = center - 85 * scale
    draw.ellipse([center - r_fall, y_fall - r_fall, center + r_fall, y_fall + r_fall],
                 fill=SUAI_NAVY)
    
    # Вектор скорости седиментации v_сед / g
    draw_arrow(draw, (center, y_fall + r_fall + 10*scale),
                     (center, y_base - 3.8*r_s), SUAI_NAVY, 10*scale, 28*scale)
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_storage(scale=4) -> Image.Image:
    """3. Хранение / Старение (#FF6418 Orange): защитный щит и таймер долговечности против созревания Оствальда."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_ORANGE)
    
    # Контур защитного щита стабильности
    pts = [
        (center, center - 150*scale),
        (center + 125*scale, center - 90*scale),
        (center + 105*scale, center + 45*scale),
        (center, center + 155*scale),
        (center - 105*scale, center + 45*scale),
        (center - 125*scale, center - 90*scale),
    ]
    draw.polygon(pts, fill=None, outline=SUAI_ORANGE, width=12*scale)
    
    # Циферблат таймера / времени жизни
    r_clock = 55 * scale
    y_clock = center + 5 * scale
    draw.ellipse([center - r_clock, y_clock - r_clock, center + r_clock, y_clock + r_clock],
                 fill="#FFFFFF", outline=SUAI_ORANGE, width=7*scale)
    # Стрелки часов (10:10)
    draw.line([(center, y_clock), (center - 25*scale, y_clock - 25*scale)],
              fill=SUAI_CHARCOAL, width=7*scale)
    draw.line([(center, y_clock), (center + 30*scale, y_clock - 20*scale)],
              fill=SUAI_CHARCOAL, width=6*scale)
    draw.ellipse([center - 6*scale, y_clock - 6*scale, center + 6*scale, y_clock + 6*scale],
                 fill=SUAI_ORANGE)
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_transport(scale=4) -> Image.Image:
    """4. Транспорт / Доставка (#9269C9 Purple): микрофлюидный канал, линии тока и перенос частиц."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_PURPLE)
    
    # Стенки микрофлюидного капилляра
    y_top = center - 100 * scale
    y_bot = center + 100 * scale
    draw.line([(center - 150*scale, y_top), (center + 150*scale, y_top)],
              fill=SUAI_CHARCOAL, width=10*scale)
    draw.line([(center - 150*scale, y_bot), (center + 150*scale, y_bot)],
              fill=SUAI_CHARCOAL, width=10*scale)
    
    # Направляющий гидродинамический вектор потока
    draw_arrow(draw, (center - 130*scale, center), (center + 130*scale, center),
               SUAI_PURPLE, 12*scale, 32*scale)
    
    # Частицы в потоке
    r_part = 18 * scale
    positions = [
        (center - 70*scale, center - 50*scale),
        (center + 20*scale, center - 45*scale),
        (center - 30*scale, center + 50*scale),
        (center + 60*scale, center + 45*scale),
    ]
    for px, py in positions:
        draw.ellipse([px - r_part, py - r_part, px + r_part, py + r_part],
                     fill=SUAI_PURPLE)
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_separation(scale=4) -> Image.Image:
    """5. Сепарация / Разделение (#00BEF3 Cyan): мембранный фильтр, отсечение агрегатов и проход монодисперсных частиц."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_CYAN)
    
    # Калиброванная пористая мембрана (перфорированная линия)
    y_mem = center
    x_start = center - 145 * scale
    x_end = center + 145 * scale
    seg = 20 * scale
    gap = 14 * scale
    cur_x = x_start
    while cur_x < x_end:
        draw.line([(cur_x, y_mem), (min(cur_x + seg, x_end), y_mem)],
                  fill=SUAI_CHARCOAL, width=9*scale)
        cur_x += seg + gap
        
    # Крупные полидисперсные агрегаты над мембраной (задержанные)
    r_coarse = 38 * scale
    draw.ellipse([center - 65*scale - r_coarse, center - 75*scale - r_coarse,
                  center - 65*scale + r_coarse, center - 75*scale + r_coarse],
                 fill=SUAI_CYAN)
    draw.ellipse([center + 65*scale - r_coarse, center - 75*scale - r_coarse,
                  center + 65*scale + r_coarse, center - 75*scale + r_coarse],
                 fill=SUAI_CYAN)
    draw.ellipse([center - 30*scale - 20*scale, center - 55*scale - 20*scale,
                  center - 30*scale + 20*scale, center - 55*scale + 20*scale],
                 fill=SUAI_CYAN)
    
    # Монодисперсные наночастицы под мембраной (откалиброванные)
    r_fine = 16 * scale
    below_pts = [
        (center - 80*scale, center + 65*scale),
        (center, center + 85*scale),
        (center + 80*scale, center + 65*scale),
    ]
    for bx, by in below_pts:
        draw.ellipse([bx - r_fine, by - r_fine, bx + r_fine, by + r_fine],
                     fill=SUAI_CYAN)
        draw.line([(bx, by + r_fine + 4*scale), (bx, by + r_fine + 16*scale)],
                  fill=SUAI_CYAN, width=4*scale)
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_processability(scale=4) -> Image.Image:
    """6. Технологичность / Процесс (#009A49 Green): зубчатое колесо и смачивающая капля формуляции."""
    size = 600 * scale
    im = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(im)
    center, _ = render_badge(draw, size, scale, SUAI_GREEN)
    
    # Механическая шестерня
    n_teeth = 8
    r_outer = 125 * scale
    r_inner = 95 * scale
    r_hub = 45 * scale
    
    gear_pts = []
    for i in range(n_teeth):
        a_mid = i * (2 * math.pi / n_teeth)
        a_half_tooth = 0.16
        
        p1 = (center + r_outer * math.cos(a_mid - a_half_tooth),
              center + r_outer * math.sin(a_mid - a_half_tooth))
        p2 = (center + r_outer * math.cos(a_mid + a_half_tooth),
              center + r_outer * math.sin(a_mid + a_half_tooth))
        p3 = (center + r_inner * math.cos(a_mid + a_half_tooth + 0.08),
              center + r_inner * math.sin(a_mid + a_half_tooth + 0.08))
        p4 = (center + r_inner * math.cos(a_mid + 2*math.pi/n_teeth - a_half_tooth - 0.08),
              center + r_inner * math.sin(a_mid + 2*math.pi/n_teeth - a_half_tooth - 0.08))
        gear_pts.extend([p1, p2, p3, p4])
        
    draw.polygon(gear_pts, fill=SUAI_GREEN)
    
    # Внутренняя ступица
    draw.ellipse([center - r_hub, center - r_hub, center + r_hub, center + r_hub],
                 fill=SUAI_CARD_BG, outline=SUAI_GREEN, width=6*scale)
    
    # Капля коллоидного раствора / мениск смачивания
    r_drop = 22 * scale
    y_drop = center + 6 * scale
    draw.ellipse([center - r_drop, y_drop - r_drop, center + r_drop, y_drop + r_drop],
                 fill=SUAI_GREEN)
    draw.polygon([(center, y_drop - 32*scale),
                  (center - r_drop + 3*scale, y_drop - 6*scale),
                  (center + r_drop - 3*scale, y_drop - 6*scale)], fill=SUAI_GREEN)
    draw.ellipse([center - 10*scale, y_drop - 10*scale, center - 2*scale, y_drop - 2*scale],
                 fill="#FFFFFF")
    return im.resize((600, 600), Image.Resampling.LANCZOS)

def generate_all_icons(target_dirs):
    """Генерация комплекта всех 6 иконок в указанные каталоги."""
    generators = {
        "icon_aggregation.png": generate_aggregation,
        "icon_sedimentation.png": generate_sedimentation,
        "icon_storage.png": generate_storage,
        "icon_transport.png": generate_transport,
        "icon_separation.png": generate_separation,
        "icon_processability.png": generate_processability,
    }
    
    rendered_images = {}
    print("Рендеринг векторных пиктограмм в разрешении 600x600 px (300 DPI)...")
    for name, gen_fn in generators.items():
        img = gen_fn(scale=4)
        rendered_images[name] = img
        print(f"  [OK] Срендерена {name}")

    for target_dir in target_dirs:
        os.makedirs(target_dir, exist_ok=True)
        print(f"\nСохранение иконок в каталог: {target_dir}")
        for name, img in rendered_images.items():
            out_path = os.path.join(target_dir, name)
            img.save(out_path, "PNG", dpi=(300, 300))
            print(f"  -> {name} ({os.path.getsize(out_path)} байт)")
        
        # Создаем алиас icon_technology.png для обратной совместимости
        tech_path = os.path.join(target_dir, "icon_technology.png")
        proc_path = os.path.join(target_dir, "icon_processability.png")
        shutil.copy2(proc_path, tech_path)
        print(f"  -> icon_technology.png (алиас для {os.path.basename(proc_path)})")

if __name__ == "__main__":
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    templates_icons_dir = os.path.join(base_dir, "course_materials", "templates", "icons")
    lectures_icons_dir = os.path.join(base_dir, "course_materials", "semester_4", "lectures", "figures_l03", "icons")
    
    generate_all_icons([templates_icons_dir, lectures_icons_dir])
    print("\n[УСПЕХ] Все 6 иконок проблем успешно сгенерированы в 300 DPI и размещены.")
