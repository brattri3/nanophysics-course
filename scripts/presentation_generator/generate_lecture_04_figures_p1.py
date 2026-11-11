"""
Генерация иллюстраций (Часть 1: Слайды 2–12) для Лекции №4:
«Поверхностные явления и механизмы роста плёнок».
Строго по аналитическим формулам, из геометрических примитивов и с включением
подлинных открытых микрофотографий АСМ/ПЭМ/СЭМ и макрофото (300 DPI).
"""
import os
import subprocess
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge
from PIL import Image

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Segoe UI']
plt.rcParams['axes.edgecolor'] = '#334455'
plt.rcParams['axes.linewidth'] = 1.1

OUT_DIR = os.path.abspath("course_materials/semester_4/lectures/figures_l04")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = '#002C5F'
BLUE = '#005AAA'
CYAN = '#00A8E8'
RED = '#C0392B'
GREEN = '#1B7837'
ORANGE = '#D97706'
PURPLE = '#6D28D9'
DARK = '#1E293B'
MUTED = '#52606D'
CARD_BG = '#F4F7FA'
BBOX = dict(boxstyle='round,pad=0.26', fc='white', ec='#CBD5E1', alpha=0.96)

REAL_ASSETS = {
    "real_afm_quantum_dots.png": "https://upload.wikimedia.org/wikipedia/commons/c/cf/AFM_image_of_111_dots_window_05_micron.png",
    "real_tem_mesoporous_silica.jpg": "https://upload.wikimedia.org/wikipedia/commons/6/6d/Mesoporous_Silica_Nanoparticle.jpg",
    "real_lotus_droplet.jpg": "https://upload.wikimedia.org/wikipedia/commons/d/d8/Lotus-Effekt_%28Droplet_on_Leaf%29_%C2%A9_W._Barthlott%2C_Lotus-Salvinia.de.jpg",
    "real_contact_angle_goniometer.jpg": "https://upload.wikimedia.org/wikipedia/commons/0/02/Typical-droplet-acquisition-data-to-obtain-the-contact-angle----by-image-analysis-and-optimization-of-the-Laplace-equati.jpg",
}


def ensure_real_assets():
    """Скачивает подлинные открытые научные микрофотографии (Wikimedia Commons CC BY / CC BY-SA) при их отсутствии."""
    for fname, url in REAL_ASSETS.items():
        dest = os.path.join(OUT_DIR, fname)
        if os.path.exists(dest) and os.path.getsize(dest) > 5000:
            continue
        try:
            subprocess.run(
                ["curl.exe", "-s", "-L", "-A", "Mozilla/5.0", url, "-o", dest],
                check=True, timeout=45
            )
            if fname == "real_lotus_droplet.jpg" and os.path.exists(dest):
                with Image.open(dest) as im:
                    im.thumbnail((1200, 900), Image.Resampling.LANCZOS)
                    im.save(dest, quality=88, optimize=True)
        except Exception as exc:
            print(f"[WARN] Could not download {fname}: {exc}")


def fig_02_problem_cases():
    """Слайд 2: Подлинные экспериментальные микрофотографии АСМ, гониометрии и ПЭМ/СЭМ (Wikimedia CC BY-SA)."""
    ensure_real_assets()
    fig = plt.figure(figsize=(6.6, 5.2), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1.0, 1.12], width_ratios=[1.05, 1.0], hspace=0.28, wspace=0.18)

    ax_afm = fig.add_subplot(gs[0, 0])
    ax_drop = fig.add_subplot(gs[0, 1])
    ax_tem = fig.add_subplot(gs[1, :])

    # 1. Верх-лево: Подлинная АСМ-топография самоорганизованных 3D квантовых точек на террасах (окно 500 нм)
    afm_path = os.path.join(OUT_DIR, "real_afm_quantum_dots.png")
    if os.path.exists(afm_path):
        with Image.open(afm_path) as im:
            # Кадрируем рабочую область скана со шкалой 0..500 нм и градиентом высоты
            w, h = im.size
            crop_afm = im.crop((0, 0, w, int(h * 0.76)))
            ax_afm.imshow(crop_afm)
    ax_afm.set_title("а) АСМ: 3D-островки КТ (окно 500 нм)", fontsize=8.0, fontweight='bold', color=NAVY, pad=4)
    ax_afm.text(0.03, 0.92, "Самоорганизация SK\n(высота 0–2.2 нм)", transform=ax_afm.transAxes,
                fontsize=6.8, fontweight='bold', color='white', va='top',
                bbox=dict(boxstyle='round,pad=0.2', fc=NAVY, ec='white', alpha=0.88))
    ax_afm.set_xticks([])
    ax_afm.set_yticks([])

    # 2. Верх-право: Подлинная оптическая гониометрия сидячей капли (профиль Лапласа-Юнга)
    drop_path = os.path.join(OUT_DIR, "real_contact_angle_goniometer.jpg")
    if os.path.exists(drop_path):
        with Image.open(drop_path) as im:
            ax_drop.imshow(im)
    ax_drop.set_title("б) Гониометрия капли (угол θ)", fontsize=8.0, fontweight='bold', color=RED, pad=4)
    ax_drop.text(0.04, 0.92, "Несмачивание (θ > 90°)\nСтягивание дорожки", transform=ax_drop.transAxes,
                 fontsize=6.8, fontweight='bold', color='white', va='top',
                 bbox=dict(boxstyle='round,pad=0.2', fc='#991B1B', ec='white', alpha=0.88))
    ax_drop.set_xticks([])
    ax_drop.set_yticks([])

    # 3. Низ: Подлинные микрофотографии ПЭМ и СЭМ мезопористого диоксида кремния (масштабы 100 нм и 20 нм)
    tem_path = os.path.join(OUT_DIR, "real_tem_mesoporous_silica.jpg")
    if os.path.exists(tem_path):
        with Image.open(tem_path) as im:
            w, h = im.size
            # Верхняя полоса панелей (a, b) или нижняя полоса (c: ПЭМ, d: СЭМ S-5200 30kV)
            crop_tem = im.crop((0, int(h * 0.50), w, h))
            ax_tem.imshow(crop_tem)
    ax_tem.set_title("в) ПЭМ (слева) и СЭМ (справа): мезопористый SiO₂ (масштаб 100 нм, вставки 20 нм)",
                     fontsize=8.2, fontweight='bold', color=BLUE, pad=4)
    ax_tem.text(0.50, 0.16, "Каналы d ≈ 4–10 нм: ΔPL ≈ 73 МПа, конденсация Кельвина и эталон БЭТ / BJH",
                transform=ax_tem.transAxes, fontsize=6.6, fontweight='bold', color='white', ha='center',
                bbox=dict(boxstyle='round,pad=0.20', fc=BLUE, ec='white', alpha=0.90))
    ax_tem.set_xticks([])
    ax_tem.set_yticks([])

    fig.suptitle("Подлинные микрофотографии межфазных явлений (АСМ, гониометрия, ПЭМ/СЭМ — CC BY-SA)",
                 fontsize=8.6, fontweight='bold', color=NAVY, y=0.99)
    fig.savefig(os.path.join(OUT_DIR, "fig_02_problem_cases.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_03_roadmap():
    """Слайд 3: Горизонтальная структурно-логическая блок-схема 4 разделов лекции."""
    fig, ax = plt.subplots(figsize=(8.0, 5.1), dpi=300)
    ax.set_xlim(0, 10.6)
    ax.set_ylim(0, 6.6)
    ax.axis('off')

    blocks = [
        (0.25, 3.55, 4.65, 2.35, NAVY, "РАЗДЕЛ 1. Смачивание и адгезия",
         "• Поверхностная энергия σ (Дж/м²)\n"
         "• Когезия Wc = 2σ и адгезия Дюпре Wa\n"
         "• Закон Юнга: cos θ = (σs − σsl) / σl\n"
         "• Критерий Гаркинса: S = Wa − Wc ≥ 0"),
        (5.70, 3.55, 4.65, 2.35, BLUE, "РАЗДЕЛ 2. Кривизна и капиллярность",
         "• Скачок Лапласа ΔPL = 2σ/R (~720 атм)\n"
         "• Закон Кельвина: Pr/P∞ = exp(±2σVm/rRT)\n"
         "• Созревание Оствальда в КТ (термошок)\n"
         "• Капиллярная конденсация и поры BJH"),
        (0.25, 0.40, 4.65, 2.35, GREEN, "РАЗДЕЛ 3. Механизмы гетероэпитаксии",
         "• Критерий Бауэра: Δσ = σf + σi − σs\n"
         "• Упругая энергия деформации Eупр ∝ ε²h\n"
         "• Режимы FM (2D), VW (3D), SK (2D→3D КТ)\n"
         "• Осцилляции ДБЭО (RHEED), hc = 1.7 МС"),
        (5.70, 0.40, 4.65, 2.35, PURPLE, "РАЗДЕЛ 4. Адсорбция и метрология БЭТ",
         "• Физисорбция (Ван-дер-Ваальс) и хемосорбция\n"
         "• Изотерма Ленгмюра θ = KP/(1+KP) (сенсоры)\n"
         "• Полимолекулярная теория БЭТ (0.05–0.35)\n"
         "• Стандарт N₂ (77 К) и 6 изотерм ИЮПАК")
    ]

    for x, y, w, h, col, title, body in blocks:
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10", fc=CARD_BG, ec=col, lw=2.0)
        ax.add_patch(card)
        hdr = FancyBboxPatch((x, y + h - 0.50), w, 0.50, boxstyle="round,pad=0.05", fc=col, ec=col, lw=1.0)
        ax.add_patch(hdr)
        ax.text(x + w / 2, y + h - 0.25, title, color='white', fontsize=8.0, fontweight='bold', ha='center', va='center')
        ax.text(x + 0.16, y + h - 0.68, body, color=DARK, fontsize=7.5, va='top', ha='left', linespacing=1.35)

    # Стрелки связи между разделами
    ax.annotate("", xy=(5.60, 4.72), xytext=(5.00, 4.72), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.6))
    ax.annotate("", xy=(2.58, 2.85), xytext=(8.02, 3.45), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2, ls='--'))
    ax.annotate("", xy=(5.60, 1.58), xytext=(5.00, 1.58), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.6))

    ax.text(5.30, 6.28, "Сквозная физико-инженерная логика управления поверхностью (σ → R → ε → Sуд)",
            fontsize=9.4, fontweight='bold', color=NAVY, ha='center')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_03_roadmap.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_05_surface_energy_dupre():
    """Слайд 5: Координационный дефицит на поверхности (Zs < Zb) и схема работ когезии Wc = 2σ и адгезии Дюпре Wa."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.9), dpi=300, gridspec_kw={'wspace': 0.20})

    # Левая панель: Кристаллическая решетка и нескомпенсированная сила
    ax1.set_xlim(0.2, 5.8)
    ax1.set_ylim(0, 6.2)
    ax1.axhspan(0, 3.8, color='#E2E8F0', alpha=0.7)
    ax1.axhspan(3.8, 6.2, color='#F8FAFC', alpha=0.9)
    ax1.axhline(3.8, color=BLUE, lw=2.2, ls='--')
    ax1.text(3.0, 5.75, "Газ / Вакуум (нет соседей сверху)", fontsize=7.8, color=MUTED, ha='center', fontweight='bold')

    for ix in range(1, 6):
        for iy in range(1, 4):
            y_pos = iy * 1.1 + 0.3
            is_surf = (iy == 3)
            col = RED if (ix == 3 and is_surf) else (ORANGE if is_surf else BLUE)
            c = Circle((ix, y_pos), 0.27, fc=col, ec='white', lw=1.2, zorder=5)
            ax1.add_patch(c)

    for dx, dy in [(-0.68, 0), (0.68, 0), (0, -0.68), (0, 0.68)]:
        ax1.annotate("", xy=(3 + dx, 1.4 + dy), xytext=(3, 1.4),
                     arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))
    ax1.text(3.0, 0.35, "Объем (Zb = 12): ∑F = 0", fontsize=7.8, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    for dx, dy in [(-0.72, 0), (0.72, 0), (-0.52, -0.62), (0.52, -0.62), (0, -0.92)]:
        ax1.annotate("", xy=(3 + dx, 3.6 + dy), xytext=(3, 3.6),
                     arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax1.text(3.0, 4.68, "Поверхность (Zs < Zb):\nFвнутр ≠ 0 → σ = (∂G/∂A)",
             fontsize=7.8, fontweight='bold', color=RED, ha='center', bbox=BBOX)
    ax1.set_title("а) Микроскопическая природа σ", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Правая панель: Когезия Wc vs Адгезия Дюпре Wa
    ax2.set_xlim(0.0, 6.0)
    ax2.set_ylim(0, 6.2)
    # Верх: Когезия
    ax2.add_patch(Rectangle((0.35, 4.25), 1.75, 1.15, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.text(1.22, 4.82, "Фаза А\n(единая)", color='white', fontsize=7.6, fontweight='bold', ha='center', va='center')
    ax2.annotate("", xy=(3.35, 4.82), xytext=(2.25, 4.82), arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.2))
    ax2.text(2.80, 5.15, "+Wc", fontsize=8.0, fontweight='bold', color=NAVY, ha='center')
    ax2.add_patch(Rectangle((3.55, 4.98), 2.05, 0.52, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.add_patch(Rectangle((3.55, 4.00), 2.05, 0.52, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.text(4.58, 4.74, "+σl + σl (2 грани)", color=RED, fontsize=7.3, fontweight='bold', ha='center')
    ax2.text(3.0, 3.48, "Когезия: Wc = 2σl (разрыв фазы)", fontsize=7.6, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    # Низ: Адгезия Дюпре
    ax2.add_patch(Rectangle((0.35, 1.65), 1.75, 0.62, fc=CYAN, ec=BLUE, alpha=0.85))
    ax2.add_patch(Rectangle((0.35, 1.03), 1.75, 0.62, fc='#64748B', ec=DARK, alpha=0.9))
    ax2.text(1.22, 1.96, "Пленка (l)", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax2.text(1.22, 1.34, "Подложка (s)", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax2.annotate("", xy=(3.35, 1.65), xytext=(2.25, 1.65), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.2))
    ax2.text(2.80, 1.98, "+Wa", fontsize=8.0, fontweight='bold', color=GREEN, ha='center')
    ax2.add_patch(Rectangle((3.55, 1.92), 2.05, 0.52, fc=CYAN, ec=BLUE, alpha=0.85))
    ax2.add_patch(Rectangle((3.55, 0.92), 2.05, 0.52, fc='#64748B', ec=DARK, alpha=0.9))
    ax2.text(4.58, 1.68, "+σs + σl − σsl", color=GREEN, fontsize=7.3, fontweight='bold', ha='center')
    ax2.text(3.0, 0.38, "Адгезия Дюпре: Wa = σs + σl − σsl", fontsize=7.6, fontweight='bold', color=GREEN, ha='center', bbox=BBOX)
    ax2.set_title("б) Работы когезии и адгезии Дюпре", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.savefig(os.path.join(OUT_DIR, "fig_05_surface_energy_dupre.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_06_young_harkins_droplet():
    """Слайд 6: Баланс векторов Юнга на трехфазной линии и аналитический график параметра растекания Гаркинса S(θ)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.9), dpi=300, gridspec_kw={'wspace': 0.26})

    # Левая панель: Геометрия капли на подложке и векторы Юнга
    ax1.set_xlim(-2.2, 2.8)
    ax1.set_ylim(-0.7, 2.6)
    ax1.add_patch(Rectangle((-2.2, -0.7), 5.0, 0.7, fc='#CBD5E1', ec=DARK, lw=1.5))
    ax1.text(0.3, -0.35, "Твердая подложка (σs)", fontsize=8.0, fontweight='bold', color=DARK, ha='center')

    theta_deg = 52.0
    theta_rad = np.radians(theta_deg)
    R_drop = 1.65
    yc = -R_drop * np.cos(theta_rad)
    xc = R_drop * np.sin(theta_rad)
    angles = np.linspace(np.pi / 2 - theta_rad, np.pi / 2 + theta_rad, 200)
    x_drop = -xc + R_drop * np.cos(angles)
    y_drop = yc + R_drop * np.sin(angles)
    ax1.fill_between(x_drop, 0, y_drop, color='#38BDF8', alpha=0.55, edgecolor=BLUE, lw=2.0)
    ax1.text(-xc, 0.42, "Жидкая фаза\n(наночернила)", fontsize=7.8, fontweight='bold', color=NAVY, ha='center')

    ax1.scatter([0], [0], color=RED, s=55, zorder=8)
    ax1.annotate("", xy=(1.75, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    ax1.text(1.42, 0.16, "σs", fontsize=9.2, fontweight='bold', color=GREEN)
    ax1.annotate("", xy=(-1.1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5))
    ax1.text(-0.95, 0.16, "σsl", fontsize=9.2, fontweight='bold', color=ORANGE)
    dx_l = 1.45 * np.cos(theta_rad)
    dy_l = 1.45 * np.sin(theta_rad)
    ax1.annotate("", xy=(dx_l, dy_l), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))
    ax1.text(dx_l + 0.08, dy_l + 0.05, "σl", fontsize=9.2, fontweight='bold', color=RED)
    ax1.plot([dx_l, dx_l], [0, dy_l], color=RED, ls=':', lw=1.4)
    arc = Wedge((0, 0), 0.55, 0, theta_deg, width=0.04, fc=RED, ec=RED)
    ax1.add_patch(arc)
    ax1.text(0.66, 0.24, f"θ = {theta_deg:.0f}°", fontsize=8.2, fontweight='bold', color=RED)

    ax1.text(0.3, 2.08, "Закон Юнга: σs = σsl + σl·cos θ\nДюпре–Юнг: Wa = σl(1 + cos θ)",
             fontsize=7.6, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)
    ax1.set_title("а) Механическое равновесие капли", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Правая панель: Аналитические кривые Wa/σl и S/σl от θ
    th = np.linspace(0, 180, 400)
    th_r = np.radians(th)
    wa_norm = 1.0 + np.cos(th_r)
    s_norm = np.cos(th_r) - 1.0

    ax2.axvspan(0, 90, color='#E0F2FE', alpha=0.55, label='Смачивание (θ < 90°, Wa > Wc/2)')
    ax2.axvspan(90, 180, color='#FEE2E2', alpha=0.55, label='Несмачивание (θ > 90°, Wa < Wc/2)')
    ax2.axhline(0, color=DARK, lw=1.0)
    ax2.axvline(90, color=MUTED, ls='--', lw=1.3)

    ax2.plot(th, wa_norm, color=BLUE, lw=2.5, label='Адгезия Wa / σl = 1 + cos θ')
    ax2.plot(th, s_norm, color=RED, lw=2.5, ls='-.', label='Гаркинс S / σl = cos θ − 1')

    ax2.scatter([0, 90, 180], [2.0, 1.0, 0.0], color=BLUE, s=45, zorder=6)
    ax2.scatter([0, 90, 180], [0.0, -1.0, -2.0], color=RED, s=45, zorder=6)
    ax2.annotate("Полное растекание\n(θ = 0°, S ≥ 0, Wa ≥ Wc)", xy=(0, 0), xytext=(22, -0.58),
                 fontsize=7.3, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4))

    ax2.set_xlim(0, 180)
    ax2.set_ylim(-2.2, 2.35)
    ax2.set_xticks([0, 45, 90, 135, 180])
    ax2.set_xlabel("Краевой угол смачивания θ, град", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Нормированная энергия (в ед. σl)", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Зависимость Wa и S от угла θ", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_06_young_harkins_droplet.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_07_wetting_engineering_lotus():
    """Слайд 7: O2-плазма (θ: 65° -> 15°), подлинное макрофото эффекта лотоса (W. Barthlott) и закон Касси–Бакстера."""
    ensure_real_assets()
    fig = plt.figure(figsize=(7.6, 4.9), dpi=300)
    gs = fig.add_gridspec(2, 2, width_ratios=[1.0, 1.12], height_ratios=[1.0, 1.0], wspace=0.28, hspace=0.32)

    ax_pl = fig.add_subplot(gs[0, 0])
    ax_lotus = fig.add_subplot(gs[1, 0])
    ax_cb = fig.add_subplot(gs[:, 1])

    # 1. Верх-лево: O2-плазма снижает θ с 65° до 15° (строго по плану и речи лектора)
    ax_pl.set_xlim(-2.1, 2.1)
    ax_pl.set_ylim(-0.55, 1.95)
    ax_pl.add_patch(Rectangle((-2.0, -0.50), 4.0, 0.50, fc='#FDE68A', ec=ORANGE, lw=1.4))
    ax_pl.text(0, -0.26, "Полиимид + O₂-плазма (−OH, −COOH)", fontsize=6.8, fontweight='bold', color=DARK, ha='center', va='center')

    th1 = np.radians(65.0)
    R1 = 1.05
    ang1 = np.linspace(np.pi / 2 - th1, np.pi / 2 + th1, 150)
    ax_pl.plot(R1 * np.cos(ang1), -R1 * np.cos(th1) + R1 * np.sin(ang1), color=RED, ls='--', lw=2.0,
               label='До плазмы: θ ≈ 65° (разрыв)')

    x_ag = np.linspace(-1.75, 1.75, 200)
    y_ag = 0.24 * (1 - (x_ag / 1.75)**2)
    ax_pl.fill_between(x_ag, 0, y_ag, color='#38BDF8', alpha=0.75, edgecolor=BLUE, lw=2.0,
                       label='После O₂-плазмы: θ ≈ 15° (S → 0)')
    ax_pl.text(0, 1.42, "Рост энергии σs → растекание Ag-чернил",
               fontsize=6.9, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)
    ax_pl.set_title("а) Плазменная активация (65° → 15°)", fontsize=8.2, fontweight='bold', color=NAVY, pad=4)
    ax_pl.legend(loc='center', bbox_to_anchor=(0.5, 0.48), fontsize=6.3, framealpha=0.94)
    ax_pl.set_xticks([])
    ax_pl.set_yticks([])

    # 2. Низ-лево: Подлинное фото капли на листе лотоса (W. Barthlott, CC BY-SA)
    lotus_path = os.path.join(OUT_DIR, "real_lotus_droplet.jpg")
    if os.path.exists(lotus_path):
        with Image.open(lotus_path) as im:
            ax_lotus.imshow(im)
    ax_lotus.set_title("б) Эффект лотоса (фото W. Barthlott)", fontsize=8.2, fontweight='bold', color=GREEN, pad=4)
    ax_lotus.text(0.04, 0.14, "Супергидрофобная сфера: θ* > 160°", transform=ax_lotus.transAxes,
                  fontsize=6.8, fontweight='bold', color='white',
                  bbox=dict(boxstyle='round,pad=0.2', fc=GREEN, ec='white', alpha=0.88))
    ax_lotus.set_xticks([])
    ax_lotus.set_yticks([])

    # 3. Право: Аналитическая кривая Касси-Бакстера
    theta_young = 108.0
    fs = np.linspace(0.02, 1.0, 300)
    cos_cb = fs * (np.cos(np.radians(theta_young)) + 1.0) - 1.0
    theta_cb = np.degrees(np.arccos(np.clip(cos_cb, -1.0, 1.0)))

    ax_cb.axhspan(150, 180, color='#DCFCE7', alpha=0.65, label='Супергидрофобная зона (θ* > 150°)')
    ax_cb.axhline(150, color=GREEN, ls='--', lw=1.5)
    ax_cb.plot(fs, theta_cb, color=NAVY, lw=2.6, label='Касси–Бакстер:\ncos θ* = fs(cos θ + 1) − 1')

    fs_op = 0.08
    th_op = float(np.degrees(np.arccos(fs_op * (np.cos(np.radians(theta_young)) + 1.0) - 1.0)))
    ax_cb.scatter([fs_op], [th_op], color=RED, s=65, zorder=6)
    ax_cb.annotate(f"Наностолбики (fs = 0.08):\nθ* = {th_op:.1f}° (воздух 92%)",
                   xy=(fs_op, th_op), xytext=(0.24, 161.5),
                   fontsize=7.2, fontweight='bold', color=RED, bbox=BBOX,
                   arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax_cb.set_xlim(0, 1.0)
    ax_cb.set_ylim(100, 180)
    ax_cb.set_xlabel("Доля твердого контакта выступов fs", fontsize=8.4, fontweight='bold', color=NAVY)
    ax_cb.set_ylabel("Кажущийся краевой угол θ*, град", fontsize=8.4, fontweight='bold', color=NAVY)
    ax_cb.set_title("в) Закон Касси–Бакстера θ*(fs)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax_cb.legend(loc='lower left', fontsize=6.8, framealpha=0.95)
    ax_cb.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_07_wetting_engineering_lotus.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_09_laplace_pressure_meniscus():
    """Слайд 9: Аналитическая кривая давления Лапласа ΔPL(R) = 2σ/R для воды (72.8 МПа при R = 2 нм)."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    sigma = 72.8e-3
    R_nm = np.linspace(1.0, 50.0, 500)
    dP_MPa = (2.0 * sigma / (R_nm * 1e-9)) / 1e6

    ax.plot(R_nm, dP_MPa, color=BLUE, lw=2.8, label='Закон Лапласа: ΔPL(R) = 2σ / R (вода, σ = 72.8 мН/м)')
    ax.fill_between(R_nm, 0, dP_MPa, color='#DBEAFE', alpha=0.45)

    r_ref = 2.0
    p_ref = (2.0 * sigma / (r_ref * 1e-9)) / 1e6
    ax.scatter([r_ref], [p_ref], color=RED, s=75, zorder=7)
    ax.annotate(f"Реперная точка наномасштаба:\nR = {r_ref:.0f} нм → ΔPL = {p_ref:.1f} МПа (≈ 720 атм!)",
                xy=(r_ref, p_ref), xytext=(8.5, 92.0),
                fontsize=8.2, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))

    r_10 = 10.0
    p_10 = (2.0 * sigma / (r_10 * 1e-9)) / 1e6
    ax.scatter([r_10], [p_10], color=NAVY, s=55, zorder=7)
    ax.annotate(f"R = 10 нм: ΔPL = {p_10:.1f} МПа (≈ 144 атм)",
                xy=(r_10, p_10), xytext=(15.5, 31.0),
                fontsize=7.8, fontweight='bold', color=NAVY, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    ax.text(22.5, 58.0,
            "Знак кривизны мениска:\n"
            "• Выпуклая нанокапля (R > 0):\n  ΔPL > 0 (сжатие ядра до сотен атм)\n"
            "• Вогнутый мениск в поре (R < 0, θ < 90°):\n  ΔPL = −2σ·cos θ / rп < 0\n  (разрежение → капиллярное всасывание)",
            fontsize=7.5, color=DARK, bbox=dict(boxstyle='round,pad=0.32', fc='#F8FAFC', ec=BLUE, lw=1.3))

    ax.set_xlim(1.0, 50.0)
    ax.set_ylim(0, 150.0)
    ax.set_xlabel("Радиус кривизны поверхности R, нм", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_ylabel("Капиллярное давление Лапласа |ΔPL|, МПа", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_title("Масштабирование капиллярного давления Лапласа ΔPL = 2σ/R в наномасштабе",
                 fontsize=9.4, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=8.0, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_09_laplace_pressure_meniscus.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_10_kelvin_ostwald_ripening():
    """Слайд 10: Аналитические ветви уравнения Кельвина P(r)/P∞ и схема созревания Оствальда (r1 -> r2)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.6, 4.9), dpi=300, gridspec_kw={'wspace': 0.24})

    l_K = 1.076
    r = np.linspace(0.8, 20.0, 400)
    p_convex = np.exp(+l_K / r)
    p_concave = np.exp(-l_K / r)

    ax1.axhline(1.0, color=DARK, ls='--', lw=1.3, label='Плоская граница (r → ∞, P/P∞ = 1)')
    ax1.plot(r, p_convex, color=RED, lw=2.6, label='Выпуклая частица (r > 0): exp(+2σVm/rRT)')
    ax1.plot(r, p_concave, color=BLUE, lw=2.6, label='Вогнутый мениск (r < 0): exp(−2σVm/rRT)')
    ax1.fill_between(r, 1.0, p_convex, color='#FEE2E2', alpha=0.45)
    ax1.fill_between(r, p_concave, 1.0, color='#DBEAFE', alpha=0.45)

    r_pt = 1.5
    p_pt = float(np.exp(l_K / r_pt))
    ax1.scatter([r_pt], [p_pt], color=RED, s=55, zorder=6)
    ax1.annotate(f"r = {r_pt} нм:\nP/P∞ = {p_pt:.2f} (+105%!)",
                 xy=(r_pt, p_pt), xytext=(4.8, 2.38),
                 fontsize=7.5, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    r_c = 1.5
    p_c = float(np.exp(-l_K / r_c))
    ax1.scatter([r_c], [p_c], color=BLUE, s=55, zorder=6)
    ax1.annotate(f"Пора r = {r_c} нм:\nP/P∞ = {p_c:.2f}",
                 xy=(r_c, p_c), xytext=(4.8, 0.22),
                 fontsize=7.5, fontweight='bold', color=BLUE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax1.set_xlim(0.8, 20.0)
    ax1.set_ylim(0.0, 3.35)
    ax1.set_xlabel("Радиус кривизны частицы / поры r, нм", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Отношение давлений (растворимостей) P(r) / P∞", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_title("а) Закон Кельвина (Оствальда–Фрейндлиха)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper right', fontsize=6.4, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Схема созревания Оствальда (без наложений текста на окружности и рамку)
    ax2.set_xlim(0, 6.4)
    ax2.set_ylim(0, 6.4)
    ax2.add_patch(FancyBboxPatch((0.15, 0.15), 6.1, 6.1, boxstyle="round,pad=0.08", fc='#F8FAFC', ec='#CBD5E1', lw=1.4))

    c_small_old = Circle((1.45, 3.45), 0.68, fc='none', ec=RED, ls='--', lw=1.8)
    c_small = Circle((1.45, 3.45), 0.40, fc=RED, ec='white', lw=1.5, alpha=0.9)
    ax2.add_patch(c_small_old)
    ax2.add_patch(c_small)
    ax2.text(1.45, 3.45, "r₁", color='white', fontsize=8.8, fontweight='bold', ha='center', va='center')
    ax2.text(2.15, 4.65, "Малая КТ (r₁ = 1.5 нм)\nμ(r₁) > μр-ра → растворение",
             fontsize=6.5, fontweight='bold', color=RED, ha='center', bbox=BBOX)

    c_big_new = Circle((4.65, 3.45), 1.15, fc='#BFDBFE', ec=BLUE, ls='--', lw=1.8, alpha=0.5)
    c_big = Circle((4.65, 3.45), 0.90, fc=BLUE, ec='white', lw=1.8, alpha=0.9)
    ax2.add_patch(c_big_new)
    ax2.add_patch(c_big)
    ax2.text(4.65, 3.45, "r₂ ≫ r₁", color='white', fontsize=9.0, fontweight='bold', ha='center', va='center')
    ax2.text(4.50, 5.25, "Крупная КТ (r₂ = 6 нм)\nμ(r₂) < μр-ра → РОСТ",
             fontsize=6.8, fontweight='bold', color=BLUE, ha='center', bbox=BBOX)

    for y_arr in [3.10, 3.45, 3.80]:
        ax2.annotate("", xy=(3.35, y_arr), xytext=(2.25, y_arr),
                     arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2))
    ax2.text(2.80, 1.98, "Поток мономеров J (∇μ)", fontsize=7.0, fontweight='bold', color=ORANGE, ha='center', bbox=BBOX)

    ax2.text(3.20, 0.85, "Следствие созревания Оствальда:\nрост дисперсии Δr ↑ и уширение спектра КТ",
             fontsize=6.4, fontweight='bold', color=DARK, ha='center', bbox=BBOX)
    ax2.set_title("б) Механизм созревания Оствальда", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.savefig(os.path.join(OUT_DIR, "fig_10_kelvin_ostwald_ripening.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_11_capillary_condensation():
    """Слайд 11: Изотерма IV типа с петлей капиллярного гистерезиса H1 (SBA-15) и геометрия кривизны 1/r vs 2/r."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    x = np.linspace(0.01, 0.99, 500)
    base = 140 * (18 * x) / ((1 - 0.35 * x) * (1 + 17 * x))
    v_ads = base + 380 / (1 + np.exp(-(x - 0.72) / 0.022))
    v_des = base + 380 / (1 + np.exp(-(x - 0.56) / 0.018))

    ax.plot(x, v_ads, color=BLUE, lw=2.8, label='Ветвь адсорбции (цилиндрическая пленка, кривизна 1/rc)')
    ax.plot(x, v_des, color=RED, lw=2.8, ls='--', label='Ветвь десорбции (полусферический мениск, кривизна 2/rc)')
    ax.fill_between(x, v_ads, v_des, where=(v_des > v_ads), color='#FDE68A', alpha=0.55,
                    label='Петля капиллярного гистерезиса (ИЮПАК тип IV, H1)')

    x_cond, y_cond = 0.72, float(140 * (18 * 0.72) / ((1 - 0.35 * 0.72) * (1 + 17 * 0.72)) + 190)
    x_evap, y_evap = 0.56, float(140 * (18 * 0.56) / ((1 - 0.35 * 0.56) * (1 + 17 * 0.56)) + 190)
    ax.scatter([x_cond], [y_cond], color=BLUE, s=65, zorder=7)
    ax.scatter([x_evap], [y_evap], color=RED, s=65, zorder=7)

    # Размещаем подпись адсорбции справа-внизу от кривой без пересечения с петлей
    ax.annotate("Конденсация с цилиндра:\nln(Pа/P₀) = −σVm / (rc·RT)",
                xy=(x_cond, y_cond), xytext=(0.56, 120),
                fontsize=7.8, fontweight='bold', color=BLUE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6))

    ax.annotate("Испарение с полусферы:\nln(Pд/P₀) = −2σVm / (rc·RT)\n(кривизна вдвое выше → Pд < Pа)",
                xy=(x_evap, y_evap), xytext=(0.05, 395),
                fontsize=7.8, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0, 620)
    ax.set_xlabel("Относительное давление пара P / P₀", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_ylabel("Объем сорбированного азота V, см³/г (НТУ)", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_title("Капиллярная конденсация и петля гистерезиса в мезопористом кремнеземе SBA-15",
                 fontsize=9.2, fontweight='bold', color=NAVY)
    ax.legend(loc='lower right', fontsize=7.4, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_11_capillary_condensation.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_12_qd_quenching_bjh():
    """Слайд 12: Подавление созревания Оствальда термошоком (300 -> 220 °C) и распределение пор по размерам BJH."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.30})

    t = np.linspace(0, 12, 400)
    T_quench = np.where(t < 2.0, 300.0, 220.0 + 80.0 * np.exp(-(t - 2.0) / 0.45))
    T_no_quench = np.where(t < 2.0, 300.0, 295.0 - 1.5 * (t - 2.0))

    ax1.plot(t, T_no_quench, color=RED, ls='--', lw=2.2, label='Без закалки: созревание (σr > 20%)')
    ax1.plot(t, T_quench, color=GREEN, lw=2.8, label='Термошок (300→220 °C): σr < 5%')
    ax1.axvspan(1.8, 2.5, color='#FEF3C7', alpha=0.75, label='Горячий впрыск (нуклеация)')
    ax1.scatter([2.0], [300.0], color=ORANGE, s=60, zorder=7)
    ax1.annotate("Горячий впрыск\n(T = 300 °C)", xy=(2.0, 300.0), xytext=(3.6, 303.0),
                 fontsize=7.3, fontweight='bold', color=ORANGE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax1.annotate("Заморозка диффузии\nи пассивация ПАВ", xy=(3.8, 221.5), xytext=(3.8, 248.0),
                 fontsize=7.3, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    ax1.set_xlim(0, 12)
    ax1.set_ylim(200, 326)
    ax1.set_xlabel("Время синтеза КТ CdSe t, мин", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Температура реактора T, °C", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_title("а) Термошок при синтезе КТ", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower left', fontsize=6.4, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    D_nm = np.linspace(2.0, 20.0, 400)
    psd_sba = 1.85 * np.exp(-((D_nm - 8.2) / 0.95)**2)
    psd_gel = 0.65 * np.exp(-((D_nm - 11.5) / 3.8)**2)

    ax2.plot(D_nm, psd_sba, color=BLUE, lw=2.8, label='Кремнезем SBA-15 (Dпик = 8.2 нм)')
    ax2.fill_between(D_nm, 0, psd_sba, color='#DBEAFE', alpha=0.55)
    ax2.plot(D_nm, psd_gel, color=MUTED, ls='-.', lw=2.0, label='Аморфный силикагель (широкий спектр)')

    ax2.scatter([8.2], [1.85], color=RED, s=60, zorder=7)
    ax2.annotate("Пик мезопор SBA-15:\nDп = 2(rK + t) ≈ 8.2 нм",
                 xy=(8.2, 1.85), xytext=(9.6, 1.34),
                 fontsize=7.0, fontweight='bold', color=BLUE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax2.set_xlim(2.0, 20.0)
    ax2.set_ylim(0, 2.20)
    ax2.set_xlabel("Диаметр пор Dп = 2(rK + t), нм", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Дифференциальный объем dV / d log D, см³/г", fontsize=8.2, fontweight='bold', color=NAVY)
    ax2.set_title("б) Порометрия BJH (десорбция N₂)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=6.4, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_12_qd_quenching_bjh.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == "__main__":
    fig_02_problem_cases()
    fig_03_roadmap()
    fig_05_surface_energy_dupre()
    fig_06_young_harkins_droplet()
    fig_07_wetting_engineering_lotus()
    fig_09_laplace_pressure_meniscus()
    fig_10_kelvin_ostwald_ripening()
    fig_11_capillary_condensation()
    fig_12_qd_quenching_bjh()
    print("Part 1 figures (Slides 2-12) regenerated cleanly.")
