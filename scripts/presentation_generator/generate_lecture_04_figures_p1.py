"""
Генерация иллюстраций (Часть 1: Слайды 2–12) для Лекции №4:
«Поверхностные явления и механизмы роста плёнок».
Строго по аналитическим формулам и из геометрических примитивов (300 DPI).
"""
import os
import urllib.request
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Wedge, Polygon
from PIL import Image

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']
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
BBOX = dict(boxstyle='round,pad=0.28', fc='white', ec='#CBD5E1', alpha=0.95)


def fig_02_problem_cases():
    """Слайд 2: Сопоставление деградации (3D-островки/деветтинг) и сплошной эпитаксиальной наноструктуры + реальная СЭМ/оптика."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.2, 5.4), dpi=300)

    # Верхняя панель: Деветтинг и распад пленки Au/SiO2 на 3D-островки (Фольмер-Вебер, Δσ > 0)
    np.random.seed(42)
    x_grid, y_grid = np.meshgrid(np.linspace(0, 500, 300), np.linspace(0, 220, 140))
    sem_bad = 0.18 + 0.04 * np.random.randn(*x_grid.shape)
    centers = [(65, 60, 28), (150, 140, 34), (240, 75, 42), (340, 150, 31),
               (425, 80, 36), (110, 175, 22), (290, 170, 25), (445, 165, 24), (195, 45, 26)]
    for cx, cy, r in centers:
        dist2 = (x_grid - cx)**2 + (y_grid - cy)**2
        island = np.exp(-dist2 / (2 * (r * 0.55)**2))
        rim = 0.25 * np.exp(-((np.sqrt(dist2) - r * 0.75) / 6.0)**2)
        sem_bad += 0.72 * island + rim
    ax1.imshow(np.clip(sem_bad, 0, 1), cmap='gray', extent=[0, 500, 0, 220], origin='lower', aspect='auto')
    ax1.set_title("АВАРИЙНЫЙ РЕЖИМ: распад пленки Au/SiO₂ на 3D-островки (Δσ > 0, θ = 118°)",
                  fontsize=8.8, fontweight='bold', color=RED, pad=5)
    ax1.text(15, 185, "Разрыв проводящего канала (R → ∞)\nОбнаженная подложка SiO₂",
             fontsize=7.8, fontweight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.25', fc='#991B1B', ec='white', alpha=0.88))
    # Масштабная линейка 100 нм
    ax1.plot([370, 470], [22, 22], color='white', lw=3.5)
    ax1.text(420, 32, "100 нм (СЭМ)", color='white', fontsize=7.5, fontweight='bold', ha='center')
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Нижняя панель: Атомарно-гладкая сверхрешетка AlGaAs/GaAs и массив КТ InAs/GaAs
    sem_good = 0.22 + 0.025 * np.random.randn(*x_grid.shape)
    for y_layer in [35, 70, 105, 140, 175]:
        sem_good += 0.48 * np.exp(-((y_grid - y_layer) / 5.5)**2)
    for qx in np.linspace(55, 445, 7):
        qd = 0.55 * np.exp(-((x_grid - qx)**2 / (2 * 14**2) + (y_grid - 183)**2 / (2 * 7**2))) * (y_grid >= 175)
        sem_good += qd
    ax2.imshow(np.clip(sem_good, 0, 1), cmap='bone', extent=[0, 500, 0, 220], origin='lower', aspect='auto')
    ax2.set_title("ЦЕЛЕВОЙ РЕЖИМ: послойный FM-рост и когерентные КТ InAs/GaAs (Δσ ≤ 0)",
                  fontsize=8.8, fontweight='bold', color=GREEN, pad=5)
    ax2.text(15, 182, "Когерентные 3D КТ InAs (h > 1.7 МС)",
             fontsize=7.6, fontweight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.22', fc=BLUE, ec='white', alpha=0.88))
    ax2.text(15, 78, "Атомарно-гладкие 2D-слои AlGaAs/GaAs (ДЭГ)",
             fontsize=7.6, fontweight='bold', color='white',
             bbox=dict(boxstyle='round,pad=0.22', fc=GREEN, ec='white', alpha=0.88))
    ax2.plot([370, 470], [22, 22], color='white', lw=3.5)
    ax2.text(420, 32, "20 нм (ПЭМ)", color='white', fontsize=7.5, fontweight='bold', ha='center')
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.suptitle("Критический выбор нанотехнологии: деградация поверхности vs управляемая сборка",
                 fontsize=9.5, fontweight='bold', color=NAVY, y=0.99)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_02_problem_cases.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_03_roadmap():
    """Слайд 3: Горизонтальная структурно-логическая блок-схема 4 разделов лекции."""
    fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=300)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    blocks = [
        (0.3, 3.5, 4.3, 2.3, NAVY, "РАЗДЕЛ 1. Смачивание и адгезия",
         "• Поверхностная энергия σ (Дж/м²)\n• Когезия Wc = 2σ и адгезия Дюпре Wa\n• Закон Юнга: cos θ = (σs − σsl)/σl\n• Критерий Гаркинса S = Wa − Wc ≥ 0"),
        (5.4, 3.5, 4.3, 2.3, BLUE, "РАЗДЕЛ 2. Кривизна и капиллярность",
         "• Скачок Лапласа ΔP = 2σ/R (~720 атм)\n• Уравнение Кельвина Pr/P∞ = exp(±2σVm/rRT)\n• Созревание Оствальда в КТ (термошок)\n• Капиллярная конденсация и поры BJH"),
        (0.3, 0.4, 4.3, 2.3, GREEN, "РАЗДЕЛ 3. Механизмы гетероэпитаксии",
         "• Критерий Бауэра Δσ = σf + σi − σs\n• Упругая энергия несоответствия E ∝ ε²h\n• FM (2D, ДЭГ), VW (3D), SK (2D→3D, КТ)\n• Осцилляции ДБЭО (RHEED) и hc = 1.7 МС"),
        (5.4, 0.4, 4.3, 2.3, PURPLE, "РАЗДЕЛ 4. Адсорбция и метрология БЭТ",
         "• Физисорбция (Ван-дер-Ваальс) vs Хемосорбция\n• Монослой Ленгмюра θ = KP/(1+KP) (сенсоры)\n• Полимолекулярная теория БЭТ (P/P0 = 0.05–0.35)\n• Эталон N2 (77 К) и 6 изотерм ИЮПАК (IUPAC)")
    ]

    for x, y, w, h, col, title, body in blocks:
        card = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12", fc=CARD_BG, ec=col, lw=2.0)
        ax.add_patch(card)
        hdr = FancyBboxPatch((x, y + h - 0.52), w, 0.52, boxstyle="round,pad=0.06", fc=col, ec=col, lw=1.0)
        ax.add_patch(hdr)
        ax.text(x + w/2, y + h - 0.26, title, color='white', fontsize=8.5, fontweight='bold', ha='center', va='center')
        ax.text(x + 0.18, y + h - 0.72, body, color=DARK, fontsize=7.8, va='top', ha='left', linespacing=1.35)

    # Стрелки связи между разделами
    ax.annotate("", xy=(5.35, 4.65), xytext=(4.65, 4.65), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.8))
    ax.annotate("", xy=(2.45, 2.75), xytext=(7.55, 3.45), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2, ls='--'))
    ax.annotate("", xy=(5.35, 1.55), xytext=(4.65, 1.55), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.8))

    ax.text(5.0, 6.22, "Сквозная физико-инженерная логика управления поверхностью (σ → R → ε → Sуд)",
            fontsize=9.8, fontweight='bold', color=NAVY, ha='center')
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_03_roadmap.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_05_surface_energy_dupre():
    """Слайд 5: Координационный дефицит на поверхности (Zs < Zb) и схема работ когезии Wc = 2σ и адгезии Дюпре Wa."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 4.9), dpi=300)

    # Левая панель: Кристаллическая решетка и нескомпенсированная сила
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 6.2)
    ax1.axhspan(0, 3.8, color='#E2E8F0', alpha=0.7)
    ax1.axhspan(3.8, 6.2, color='#F8FAFC', alpha=0.9)
    ax1.axhline(3.8, color=BLUE, lw=2.2, ls='--')
    ax1.text(3.0, 5.75, "Газ / Вакуум (отсутствие соседей сверху)", fontsize=8.0, color=MUTED, ha='center', fontweight='bold')

    for ix in range(1, 6):
        for iy in range(1, 4):
            y_pos = iy * 1.1 + 0.3
            is_surf = (iy == 3)
            col = RED if (ix == 3 and is_surf) else (ORANGE if is_surf else BLUE)
            c = Circle((ix, y_pos), 0.28, fc=col, ec='white', lw=1.2, zorder=5)
            ax1.add_patch(c)

    # Векторы сил для объемного атома (3, 1.4) и поверхностного (3, 3.6)
    for dx, dy in [(-0.7, 0), (0.7, 0), (0, -0.7), (0, 0.7)]:
        ax1.annotate("", xy=(3 + dx, 1.4 + dy), xytext=(3, 1.4),
                     arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))
    ax1.text(3.0, 0.35, "Объем (Zb = 12): ∑F = 0", fontsize=8.0, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    for dx, dy in [(-0.75, 0), (0.75, 0), (-0.55, -0.65), (0.55, -0.65), (0, -0.95)]:
        ax1.annotate("", xy=(3 + dx, 3.6 + dy), xytext=(3, 3.6),
                     arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax1.text(3.0, 4.65, "Поверхность (Zs < Zb):\nF_внутр ≠ 0 → σ = (∂G/∂A)",
             fontsize=8.2, fontweight='bold', color=RED, ha='center', bbox=BBOX)
    ax1.set_title("а) Микроскопическая природа σ", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Правая панель: Когезия Wc vs Адгезия Дюпре Wa
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 6.2)
    # Верх: Когезия
    ax2.add_patch(Rectangle((0.4, 4.2), 1.8, 1.2, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.text(1.3, 4.8, "Фаза А\n(единая)", color='white', fontsize=7.8, fontweight='bold', ha='center', va='center')
    ax2.annotate("", xy=(3.4, 4.8), xytext=(2.4, 4.8), arrowprops=dict(arrowstyle="->", color=NAVY, lw=2.2))
    ax2.text(2.9, 5.15, "+Wc", fontsize=8.2, fontweight='bold', color=NAVY, ha='center')
    ax2.add_patch(Rectangle((3.6, 4.95), 1.9, 0.55, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.add_patch(Rectangle((3.6, 3.95), 1.9, 0.55, fc=BLUE, ec=NAVY, alpha=0.85))
    ax2.text(4.55, 4.72, " +σ_l (1 м²) ", color=RED, fontsize=7.5, fontweight='bold', ha='center')
    ax2.text(3.0, 3.45, "Когезия: Wc = 2σ_l (разрыв однородной фазы)", fontsize=8.0, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    # Низ: Адгезия Дюпре
    ax2.add_patch(Rectangle((0.4, 1.65), 1.8, 0.65, fc=CYAN, ec=BLUE, alpha=0.85))
    ax2.add_patch(Rectangle((0.4, 1.0), 1.8, 0.65, fc='#64748B', ec=DARK, alpha=0.9))
    ax2.text(1.3, 1.97, "Пленка (l)", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax2.text(1.3, 1.32, "Подложка (s)", color='white', fontsize=7.2, fontweight='bold', ha='center', va='center')
    ax2.annotate("", xy=(3.4, 1.65), xytext=(2.4, 1.65), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.2))
    ax2.text(2.9, 2.0, "+Wa", fontsize=8.2, fontweight='bold', color=GREEN, ha='center')
    ax2.add_patch(Rectangle((3.6, 1.9), 1.9, 0.55, fc=CYAN, ec=BLUE, alpha=0.85))
    ax2.add_patch(Rectangle((3.6, 0.9), 1.9, 0.55, fc='#64748B', ec=DARK, alpha=0.9))
    ax2.text(4.55, 1.68, "+σ_s + σ_l − σ_sl", color=GREEN, fontsize=7.5, fontweight='bold', ha='center')
    ax2.text(3.0, 0.35, "Адгезия Дюпре: Wa = σ_s + σ_l − σ_sl", fontsize=8.0, fontweight='bold', color=GREEN, ha='center', bbox=BBOX)
    ax2.set_title("б) Работы когезии и адгезии Дюпре", fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_05_surface_energy_dupre.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_06_young_harkins_droplet():
    """Слайд 6: Баланс векторов Юнга на трехфазной линии и аналитический график параметра растекания Гаркинса S(θ)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Геометрия капли на подложке и векторы Юнга
    ax1.set_xlim(-2.2, 2.8)
    ax1.set_ylim(-0.7, 2.6)
    ax1.add_patch(Rectangle((-2.2, -0.7), 5.0, 0.7, fc='#CBD5E1', ec=DARK, lw=1.5))
    ax1.text(0.3, -0.35, "Твердая подложка (Surface, σ_s)", fontsize=8.2, fontweight='bold', color=DARK, ha='center')

    theta_deg = 52.0
    theta_rad = np.radians(theta_deg)
    R_drop = 1.65
    yc = -R_drop * np.cos(theta_rad)
    xc = R_drop * np.sin(theta_rad)
    angles = np.linspace(np.pi/2 - theta_rad, np.pi/2 + theta_rad, 200)
    x_drop = -xc + R_drop * np.cos(angles)
    y_drop = yc + R_drop * np.sin(angles)
    ax1.fill_between(x_drop, 0, y_drop, color='#38BDF8', alpha=0.55, edgecolor=BLUE, lw=2.0)
    ax1.text(-xc, 0.42, "Жидкая фаза\n(Наночернила)", fontsize=8.0, fontweight='bold', color=NAVY, ha='center')

    # Трехфазная точка O = (0, 0)
    ax1.scatter([0], [0], color=RED, s=55, zorder=8)
    # Вектор σ_s (вправо)
    ax1.annotate("", xy=(1.75, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=GREEN, lw=2.5))
    ax1.text(1.45, 0.16, "σ_s", fontsize=9.5, fontweight='bold', color=GREEN)
    # Вектор σ_sl (влево)
    ax1.annotate("", xy=(-1.1, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.5))
    ax1.text(-0.95, 0.16, "σ_sl", fontsize=9.5, fontweight='bold', color=ORANGE)
    # Вектор σ_l (по касательной под углом θ)
    dx_l = 1.45 * np.cos(theta_rad)
    dy_l = 1.45 * np.sin(theta_rad)
    ax1.annotate("", xy=(dx_l, dy_l), xytext=(0, 0), arrowprops=dict(arrowstyle="->", color=RED, lw=2.5))
    ax1.text(dx_l + 0.08, dy_l + 0.05, "σ_l", fontsize=9.5, fontweight='bold', color=RED)
    # Проекция σ_l cos θ
    ax1.plot([dx_l, dx_l], [0, dy_l], color=RED, ls=':', lw=1.4)
    arc = Wedge((0, 0), 0.55, 0, theta_deg, width=0.04, fc=RED, ec=RED)
    ax1.add_patch(arc)
    ax1.text(0.68, 0.25, f"θ = {theta_deg:.0f}°", fontsize=8.5, fontweight='bold', color=RED)

    ax1.text(0.3, 2.1, "Закон Юнга: σ_s = σ_sl + σ_l·cos θ\nФормула Дюпре–Юнга: Wa = σ_l(1 + cos θ)",
             fontsize=8.0, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)
    ax1.set_title("а) Механическое равновесие капли", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Правая панель: Аналитические кривые Wa/σ_l и S/σ_l от θ
    th = np.linspace(0, 180, 400)
    th_r = np.radians(th)
    wa_norm = 1.0 + np.cos(th_r)      # Wa / σ_l = 1 + cos θ
    s_norm = np.cos(th_r) - 1.0       # S / σ_l = (Wa - Wc)/σ_l = cos θ - 1

    ax2.axvspan(0, 90, color='#E0F2FE', alpha=0.55, label='Смачивание (θ < 90°, Wa > Wc/2)')
    ax2.axvspan(90, 180, color='#FEE2E2', alpha=0.55, label='Несмачивание (θ > 90°, Wa < Wc/2)')
    ax2.axhline(0, color=DARK, lw=1.0)
    ax2.axvline(90, color=MUTED, ls='--', lw=1.3)

    ax2.plot(th, wa_norm, color=BLUE, lw=2.5, label='Адгезия Wa / σ_l = 1 + cos θ')
    ax2.plot(th, s_norm, color=RED, lw=2.5, ls='-.', label='Параметр Гаркинса S / σ_l = cos θ − 1')

    ax2.scatter([0, 90, 180], [2.0, 1.0, 0.0], color=BLUE, s=45, zorder=6)
    ax2.scatter([0, 90, 180], [0.0, -1.0, -2.0], color=RED, s=45, zorder=6)
    ax2.annotate("Полное растекание\n(θ = 0°, S ≥ 0, Wa ≥ Wc)", xy=(0, 0), xytext=(22, -0.55),
                 fontsize=7.5, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.4))

    ax2.set_xlim(0, 180)
    ax2.set_ylim(-2.2, 2.3)
    ax2.set_xticks([0, 45, 90, 135, 180])
    ax2.set_xlabel("Краевой угол смачивания θ, град", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Нормированная энергия (в ед. σ_l)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.set_title("б) Зависимость Wa и S Гаркинса от угла θ", fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=7.0, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_06_young_harkins_droplet.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_07_wetting_engineering_lotus():
    """Слайд 7: O2-плазменная гидрофилизация для печати Ag-наночернил vs режим Касси–Бакстера (эффект лотоса θ* > 150°)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: O2-плазма снижает θ с 85° до 12°
    ax1.set_xlim(-2.2, 2.2)
    ax1.set_ylim(-0.6, 2.2)
    ax1.add_patch(Rectangle((-2.2, -0.6), 4.4, 0.6, fc='#FDE68A', ec=ORANGE, lw=1.5))
    ax1.text(0, -0.32, "Полиимидная подложка после O₂-плазмы (−OH, −COOH)", fontsize=7.5, fontweight='bold', color=DARK, ha='center')

    # До плазмы (пунктир, θ = 85°)
    th1 = np.radians(82)
    R1 = 1.15
    ang1 = np.linspace(np.pi/2 - th1, np.pi/2 + th1, 150)
    ax1.plot(R1 * np.cos(ang1), -R1 * np.cos(th1) + R1 * np.sin(ang1), color=RED, ls='--', lw=2.0, label='До плазмы: θ = 85° (разрыв дорожки)')

    # После плазмы (сплошная пленка Ag, θ = 12°)
    x_ag = np.linspace(-1.85, 1.85, 200)
    y_ag = 0.28 * (1 - (x_ag / 1.85)**2)
    ax1.fill_between(x_ag, 0, y_ag, color='#38BDF8', alpha=0.75, edgecolor=BLUE, lw=2.2, label='После O₂-плазмы: θ = 12° (S → 0)')
    for gx in np.linspace(-1.6, 1.6, 9):
        ax1.text(gx, 0.04, "OH", fontsize=6.5, fontweight='bold', color=GREEN, ha='center')

    ax1.text(0, 1.55, "Прививка полярных групп ↑σ_s:\ncos θ ↑ → θ: 85° → 12°\nСплошная дорожка наночернил Ag",
             fontsize=7.8, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)
    ax1.set_title("а) Плазменная активация (Печатная электроника)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower center', bbox_to_anchor=(0.5, 0.36), fontsize=7.0)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Правая панель: Режим Касси-Бакстера (Супергидрофобность)
    theta_young = 108.0  # гидрофобный фторполимер/воск
    fs = np.linspace(0.02, 1.0, 300)
    cos_cb = fs * (np.cos(np.radians(theta_young)) + 1.0) - 1.0
    theta_cb = np.degrees(np.arccos(np.clip(cos_cb, -1.0, 1.0)))

    ax2.axhspan(150, 180, color='#DCFCE7', alpha=0.65, label='Супергидрофобная зона (θ* > 150°, эффект лотоса)')
    ax2.axhline(150, color=GREEN, ls='--', lw=1.5)
    ax2.plot(fs, theta_cb, color=NAVY, lw=2.6, label='Уравнение Касси–Бакстера:\ncos θ* = f_s(cos θ + 1) − 1')

    fs_op = 0.08
    th_op = float(np.degrees(np.arccos(fs_op * (np.cos(np.radians(theta_young)) + 1.0) - 1.0)))
    ax2.scatter([fs_op], [th_op], color=RED, s=65, zorder=6)
    ax2.annotate(f"Наностолбики (f_s = 0.08):\nθ* = {th_op:.1f}° (воздушные карманы 92%)",
                 xy=(fs_op, th_op), xytext=(0.24, 162),
                 fontsize=7.6, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax2.set_xlim(0, 1.0)
    ax2.set_ylim(100, 180)
    ax2.set_xlabel("Доля твердого контакта выступов f_s", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Кажущийся краевой угол θ*, град", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.set_title("б) Закон Касси–Бакстера (Супергидрофобность)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='lower left', fontsize=7.2, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_07_wetting_engineering_lotus.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_09_laplace_pressure_meniscus():
    """Слайд 9: Аналитическая кривая давления Лапласа ΔP_L(R) = 2σ/R для воды (72.8 МПа при R = 2 нм) и схема менисков."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    sigma = 72.8e-3  # Н/м (вода при 20 °C)
    R_nm = np.linspace(1.0, 50.0, 500)
    dP_MPa = (2.0 * sigma / (R_nm * 1e-9)) / 1e6  # МПа

    ax.plot(R_nm, dP_MPa, color=BLUE, lw=2.8, label='Закон Лапласа: ΔP_L(R) = 2σ / R (вода, σ = 72.8 мН/м)')
    ax.fill_between(R_nm, 0, dP_MPa, color='#DBEAFE', alpha=0.45)

    # Реперная точка R = 2 нм -> 72.8 МПа (~720 атм)
    r_ref = 2.0
    p_ref = (2.0 * sigma / (r_ref * 1e-9)) / 1e6
    ax.scatter([r_ref], [p_ref], color=RED, s=75, zorder=7)
    ax.annotate(f"Реперная точка наномасштаба:\nR = {r_ref:.0f} нм → ΔP_L = {p_ref:.1f} МПа (≈ 720 атм!)",
                xy=(r_ref, p_ref), xytext=(8.5, 92.0),
                fontsize=8.5, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))

    # Вторая точка R = 10 нм -> 14.56 МПа
    r_10 = 10.0
    p_10 = (2.0 * sigma / (r_10 * 1e-9)) / 1e6
    ax.scatter([r_10], [p_10], color=NAVY, s=55, zorder=7)
    ax.annotate(f"R = 10 нм: ΔP_L = {p_10:.1f} МПа (≈ 144 атм)",
                xy=(r_10, p_10), xytext=(16.0, 32.0),
                fontsize=8.0, fontweight='bold', color=NAVY, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    ax.text(28.0, 62.0,
            "Знак кривизны мениска:\n"
            "• Выпуклая нанокапля (R > 0):\n  ΔP_L > 0 (сжатие ядра до сотен атм)\n"
            "• Вогнутый мениск в поре (R < 0, θ < 90°):\n  ΔP_L = −2σ·cos θ / r_п < 0\n  (разрежение → капиллярное всасывание)",
            fontsize=7.8, color=DARK, bbox=dict(boxstyle='round,pad=0.35', fc='#F8FAFC', ec=BLUE, lw=1.3))

    ax.set_xlim(1.0, 50.0)
    ax.set_ylim(0, 150.0)
    ax.set_xlabel("Радиус кривизны поверхности R, нм", fontsize=9.5, fontweight='bold', color=NAVY)
    ax.set_ylabel("Капиллярное давление Лапласа |ΔP_L|, МПа", fontsize=9.5, fontweight='bold', color=NAVY)
    ax.set_title("Масштабирование капиллярного давления Лапласа ΔP_L = 2σ/R в наномасштабе",
                 fontsize=9.8, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=8.2, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_09_laplace_pressure_meniscus.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_10_kelvin_ostwald_ripening():
    """Слайд 10: Аналитические ветви уравнения Кельвина P(r)/P∞ и схема созревания Оствальда (r1 -> r2)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Точный график уравнения Кельвина (вода при 293 К, l_K = 2σVm/RT ≈ 1.076 нм)
    l_K = 1.076  # нм
    r = np.linspace(0.8, 20.0, 400)
    p_convex = np.exp(+l_K / r)   # Выпуклая нанокапля / наночастица (Оствальд-Фрейндлих)
    p_concave = np.exp(-l_K / r)  # Вогнутый мениск в нанопоре (конденсация)

    ax1.axhline(1.0, color=DARK, ls='--', lw=1.3, label='Плоская поверхность (r → ∞, P/P∞ = 1)')
    ax1.plot(r, p_convex, color=RED, lw=2.6, label='Выпуклая наночастица (r > 0): exp(+2σVm/rRT)')
    ax1.plot(r, p_concave, color=BLUE, lw=2.6, label='Вогнутый мениск поры (r < 0): exp(−2σVm/rRT)')
    ax1.fill_between(r, 1.0, p_convex, color='#FEE2E2', alpha=0.45)
    ax1.fill_between(r, p_concave, 1.0, color='#DBEAFE', alpha=0.45)

    r_pt = 1.5
    p_pt = float(np.exp(l_K / r_pt))
    ax1.scatter([r_pt], [p_pt], color=RED, s=55, zorder=6)
    ax1.annotate(f"r = {r_pt} нм:\nP/P∞ = {p_pt:.2f} (+105%!)",
                 xy=(r_pt, p_pt), xytext=(4.5, 2.45),
                 fontsize=7.8, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    r_c = 1.5
    p_c = float(np.exp(-l_K / r_c))
    ax1.scatter([r_c], [p_c], color=BLUE, s=55, zorder=6)
    ax1.annotate(f"Нанопора r = {r_c} нм:\nКонденсация при P/P∞ = {p_c:.2f}",
                 xy=(r_c, p_c), xytext=(4.5, 0.25),
                 fontsize=7.8, fontweight='bold', color=BLUE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax1.set_xlim(0.8, 20.0)
    ax1.set_ylim(0.0, 3.3)
    ax1.set_xlabel("Радиус кривизны частицы / поры r, нм", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Отношение давлений (растворимостей) P(r) / P∞", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.set_title("а) Закон Кельвина (Оствальда–Фрейндлиха)", fontsize=9.0, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper right', fontsize=6.8, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Схема созревания Оствальда
    ax2.set_xlim(0, 6)
    ax2.set_ylim(0, 6)
    ax2.add_patch(FancyBboxPatch((0.2, 0.2), 5.6, 5.6, boxstyle="round,pad=0.1", fc='#F8FAFC', ec='#CBD5E1', lw=1.5))

    # Малая растворяющаяся частица r1
    c_small_old = Circle((1.4, 3.3), 0.72, fc='none', ec=RED, ls='--', lw=1.8)
    c_small = Circle((1.4, 3.3), 0.42, fc=RED, ec='white', lw=1.5, alpha=0.9)
    ax2.add_patch(c_small_old)
    ax2.add_patch(c_small)
    ax2.text(1.4, 3.3, "r₁", color='white', fontsize=9.0, fontweight='bold', ha='center', va='center')
    ax2.text(1.4, 4.45, "Малая КТ (r₁ = 1.5 нм)\nμ(r₁) > μ_р-ра → РАСТВОРЕНИЕ", fontsize=7.5, fontweight='bold', color=RED, ha='center', bbox=BBOX)

    # Крупная растущая частица r2
    c_big_new = Circle((4.4, 3.3), 1.25, fc='#BFDBFE', ec=BLUE, ls='--', lw=1.8, alpha=0.5)
    c_big = Circle((4.4, 3.3), 0.98, fc=BLUE, ec='white', lw=1.8, alpha=0.9)
    ax2.add_patch(c_big_new)
    ax2.add_patch(c_big)
    ax2.text(4.4, 3.3, "r₂ ≫ r₁", color='white', fontsize=9.5, fontweight='bold', ha='center', va='center')
    ax2.text(4.4, 5.05, "Крупная КТ (r₂ = 6.0 нм)\nμ(r₂) < μ_р-ра → РОСТ", fontsize=7.5, fontweight='bold', color=BLUE, ha='center', bbox=BBOX)

    # Стрелки диффузионного потока мономеров J
    for y_arr in [2.9, 3.3, 3.7]:
        ax2.annotate("", xy=(3.15, y_arr), xytext=(2.2, y_arr),
                     arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2.2))
    ax2.text(2.68, 2.25, "Диффузионный поток\nмономеров J (∇μ)", fontsize=7.8, fontweight='bold', color=ORANGE, ha='center')

    ax2.text(3.0, 0.85, "Следствие: размытие размеров Δr ↑,\nкрасный сдвиг спектра и потеря монодисперсности КТ",
             fontsize=7.6, fontweight='bold', color=DARK, ha='center', bbox=BBOX)
    ax2.set_title("б) Механизм созревания Оствальда", fontsize=9.0, fontweight='bold', color=NAVY)
    ax2.set_xticks([])
    ax2.set_yticks([])

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_10_kelvin_ostwald_ripening.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_11_capillary_condensation():
    """Слайд 11: Изотерма IV типа с петлей капиллярного гистерезиса H1 (SBA-15) и геометрия кривизны 1/r vs 2/r."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    x = np.linspace(0.01, 0.99, 500)
    # Базовая полимолекулярная сорбция + капиллярный скачок
    base = 140 * (18 * x) / ((1 - 0.35 * x) * (1 + 17 * x))
    v_ads = base + 380 / (1 + np.exp(-(x - 0.72) / 0.022))
    v_des = base + 380 / (1 + np.exp(-(x - 0.56) / 0.018))

    ax.plot(x, v_ads, color=BLUE, lw=2.8, label='Ветвь адсорбции (цилиндрическая пленка, кривизна 1/r_c)')
    ax.plot(x, v_des, color=RED, lw=2.8, ls='--', label='Ветвь десорбции (полусферический мениск, кривизна 2/r_c)')
    ax.fill_between(x, v_ads, v_des, where=(v_des > v_ads), color='#FDE68A', alpha=0.55,
                    label='Петля капиллярного гистерезиса (ИЮПАК тип IV, H1)')

    # Точки конденсации и испарения
    x_cond, y_cond = 0.72, float(140 * (18 * 0.72) / ((1 - 0.35 * 0.72) * (1 + 17 * 0.72)) + 190)
    x_evap, y_evap = 0.56, float(140 * (18 * 0.56) / ((1 - 0.35 * 0.56) * (1 + 17 * 0.56)) + 190)
    ax.scatter([x_cond], [y_cond], color=BLUE, s=65, zorder=7)
    ax.scatter([x_evap], [y_evap], color=RED, s=65, zorder=7)

    ax.annotate("Конденсация с цилиндра:\nln(P_а/P₀) = −σVm / (r_c RT)",
                xy=(x_cond, y_cond), xytext=(0.48, 225),
                fontsize=8.0, fontweight='bold', color=BLUE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.6))

    ax.annotate("Испарение с полусферы:\nln(P_д/P₀) = −2σVm / (r_c RT)\n(кривизна в 2 раза выше → P_д < P_а)",
                xy=(x_evap, y_evap), xytext=(0.06, 395),
                fontsize=8.0, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0, 620)
    ax.set_xlabel("Относительное давление пара P / P₀", fontsize=9.5, fontweight='bold', color=NAVY)
    ax.set_ylabel("Объем сорбированного азота V, см³/г (НТУ)", fontsize=9.5, fontweight='bold', color=NAVY)
    ax.set_title("Капиллярная конденсация и петля гистерезиса в мезопористом кремнеземе SBA-15",
                 fontsize=9.5, fontweight='bold', color=NAVY)
    ax.legend(loc='lower right', fontsize=7.6, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_11_capillary_condensation.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_12_qd_quenching_bjh():
    """Слайд 12: Подавление созревания Оствальда термошоком (300 -> 220 °C) при синтезе КТ и распределение пор по размерам BJH."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Профиль термошока LaMer / Hot-Injection
    t = np.linspace(0, 12, 400)
    T_quench = np.where(t < 2.0, 300.0, 220.0 + 80.0 * np.exp(-(t - 2.0) / 0.45))
    T_no_quench = np.where(t < 2.0, 300.0, 295.0 - 1.5 * (t - 2.0))

    ax1.plot(t, T_no_quench, color=RED, ls='--', lw=2.2, label='Без закалки (300 °C): созревание Оствальда (σ_r > 22%)')
    ax1.plot(t, T_quench, color=GREEN, lw=2.8, label='Термошок (300 → 220 °C) + ПАВ: монодисперсные КТ (σ_r < 5%)')
    ax1.axvspan(1.8, 2.6, color='#FEF3C7', alpha=0.75, label='Впрыск прекурсора (взрывная нуклеация)')
    ax1.scatter([2.0], [300.0], color=ORANGE, s=65, zorder=7)
    ax1.annotate("Точка горячего впрыска\n(T = 300 °C)", xy=(2.0, 300.0), xytext=(3.6, 304.0),
                 fontsize=7.8, fontweight='bold', color=ORANGE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))
    ax1.annotate("Кинетическая заморозка\nи пассивация олеиновой кислотой", xy=(4.0, 221.0), xytext=(3.5, 248.0),
                 fontsize=7.8, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    ax1.set_xlim(0, 12)
    ax1.set_ylim(200, 325)
    ax1.set_xlabel("Время синтеза квантовых точек CdSe t, мин", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Температура реактора T, °C", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_title("а) Подавление созревания Оствальда (Термошок)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower left', fontsize=6.8, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Кривая распределения мезопор по размерам методом BJH (r_p = r_K + t)
    D_nm = np.linspace(2.0, 20.0, 400)
    psd_sba = 1.85 * np.exp(-((D_nm - 8.2) / 0.95)**2)
    psd_gel = 0.65 * np.exp(-((D_nm - 11.5) / 3.8)**2)

    ax2.plot(D_nm, psd_sba, color=BLUE, lw=2.8, label='Упорядоченный кремнезем SBA-15 (D_пик = 8.2 нм)')
    ax2.fill_between(D_nm, 0, psd_sba, color='#DBEAFE', alpha=0.55)
    ax2.plot(D_nm, psd_gel, color=MUTED, ls='-.', lw=2.0, label='Аморфный силикагель (широкое распределение пор)')

    ax2.scatter([8.2], [1.85], color=RED, s=60, zorder=7)
    ax2.annotate("Узкий пик мезопор SBA-15:\nD_п = 2(r_K + t) = 8.2 ± 0.6 нм",
                 xy=(8.2, 1.85), xytext=(10.2, 1.48),
                 fontsize=7.8, fontweight='bold', color=BLUE, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax2.set_xlim(2.0, 20.0)
    ax2.set_ylim(0, 2.15)
    ax2.set_xlabel("Диаметр пор D_п = 2(r_K + t), нм", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Дифференциальный объем dV / d log D, см³/г", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_title("б) Порометрия BJH (Баррета–Джойнера–Халенды)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=6.8, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
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
    print("Part 1 figures (Slides 2-12) generated successfully.")
