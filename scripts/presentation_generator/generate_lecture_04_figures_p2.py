"""
Генерация иллюстраций (Часть 2: Слайды 14–23) для Лекции №4:
«Поверхностные явления и механизмы роста плёнок».
Строго по аналитическим формулам и из геометрических примитивов (300 DPI) без наложений текста.
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Polygon
from scipy.optimize import brentq

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
BBOX = dict(boxstyle='round,pad=0.25', fc='white', ec='#CBD5E1', alpha=0.96)


def fig_14_bauer_strain_tree():
    """Слайд 14: Дерево критерия Бауэра Δσ и аналитический график накопления упругой энергии Eупр(h) ∝ ε²h."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.26})

    # Левая панель: Дерево выбора механизма гетероэпитаксии по Бауэру (1958)
    ax1.set_xlim(0, 6.6)
    ax1.set_ylim(0, 6.3)
    ax1.axis('off')

    root = FancyBboxPatch((0.35, 5.05), 5.9, 0.95, boxstyle="round,pad=0.08", fc=NAVY, ec=NAVY)
    ax1.add_patch(root)
    ax1.text(3.3, 5.52, "Критерий Э. Бауэра (1958):\nΔσ = σf + σi − σs   и   ε = (af − as) / as",
             color='white', fontsize=7.6, fontweight='bold', ha='center', va='center')

    b_left = FancyBboxPatch((0.20, 3.20), 2.85, 1.00, boxstyle="round,pad=0.08", fc='#E0F2FE', ec=BLUE, lw=1.6)
    ax1.add_patch(b_left)
    ax1.text(1.62, 3.70, "Смачивание:\nΔσ ≤ 0 (Wa ≥ Wc)", color=BLUE, fontsize=7.4, fontweight='bold', ha='center', va='center')

    b_right = FancyBboxPatch((3.55, 3.20), 2.85, 1.00, boxstyle="round,pad=0.08", fc='#FEE2E2', ec=RED, lw=1.6)
    ax1.add_patch(b_right)
    ax1.text(4.98, 3.70, "Несмачивание:\nΔσ > 0 (Wa < Wc)", color=RED, fontsize=7.4, fontweight='bold', ha='center', va='center')

    ax1.annotate("", xy=(1.62, 4.25), xytext=(2.60, 5.00), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2.0))
    ax1.annotate("", xy=(4.98, 4.25), xytext=(4.00, 5.00), arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))

    # Три терминальных режима с четкими интервалами без наложений
    fm_box = FancyBboxPatch((0.12, 0.35), 1.96, 2.00, boxstyle="round,pad=0.06", fc='#DCFCE7', ec=GREEN, lw=1.8)
    sk_box = FancyBboxPatch((2.32, 0.35), 1.96, 2.00, boxstyle="round,pad=0.06", fc='#FEF3C7', ec=ORANGE, lw=1.8)
    vw_box = FancyBboxPatch((4.52, 0.35), 1.96, 2.00, boxstyle="round,pad=0.06", fc='#FEE2E2', ec=RED, lw=1.8)
    ax1.add_patch(fm_box)
    ax1.add_patch(sk_box)
    ax1.add_patch(vw_box)

    ax1.text(1.10, 1.35, "1. FM-рост (2D)\nФранк–\nван дер Мерве\n|ε| ≤ 0.5%\nПослойный\nAlGaAs / GaAs",
             color=GREEN, fontsize=6.4, fontweight='bold', ha='center', va='center')
    ax1.text(3.30, 1.35, "3. SK-рост (КТ)\nСтранский–\nКрастанов\n|ε| = 2–7%\nСлой + 3D КТ\nInAs / GaAs",
             color=ORANGE, fontsize=6.4, fontweight='bold', ha='center', va='center')
    ax1.text(5.50, 1.35, "2. VW-рост (3D)\nФольмер–\nВебер\nЛюбое ε\n3D-островки\nAu, Ag / SiO₂",
             color=RED, fontsize=6.4, fontweight='bold', ha='center', va='center')

    ax1.annotate("", xy=(1.10, 2.42), xytext=(1.35, 3.16), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax1.annotate("", xy=(3.30, 2.42), xytext=(1.95, 3.16), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8))
    ax1.annotate("", xy=(5.50, 2.42), xytext=(4.98, 3.16), arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax1.set_title("а) Термодинамическое дерево Бауэра", fontsize=8.6, fontweight='bold', color=NAVY)

    # Правая панель: Аналитический график Eупр(h) = Y * ε² * h
    h_ml = np.linspace(0, 4.0, 300)
    e_inas = 0.1215 * h_ml
    e_sige = 0.1215 * (4.2 / 7.16)**2 * h_ml
    e_algaas = 0.1215 * (0.1 / 7.16)**2 * h_ml
    barrier = 0.2065

    ax2.axhspan(barrier, 0.50, color='#FEF3C7', alpha=0.55, label='Зона 3D-релаксации (КТ / дислокации)')
    ax2.axhline(barrier, color=RED, ls='--', lw=1.6, label='Порог устойчивости 2D-слоя')
    ax2.plot(h_ml, e_inas, color=RED, lw=2.6, label='InAs/GaAs (ε = +7.2%): hc = 1.7 МС')
    ax2.plot(h_ml, e_sige, color=ORANGE, lw=2.3, label='Ge/Si (ε = +4.2%): hc ≈ 4–5 МС')
    ax2.plot(h_ml, e_algaas, color=GREEN, lw=2.5, label='AlGaAs/GaAs (ε ≈ 0.04%): 2D FM-рост')

    ax2.scatter([1.7], [0.1215 * 1.7], color=RED, s=65, zorder=7)
    ax2.annotate("Порог SK: hc = 1.7 МС\n(переход 2D → 3D КТ)",
                 xy=(1.7, 0.1215 * 1.7), xytext=(1.72, 0.06),
                 fontsize=7.2, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax2.set_xlim(0, 4.0)
    ax2.set_ylim(0, 0.49)
    ax2.set_xlabel("Толщина эпитаксиальной пленки h, монослои (МС)", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Упругая энергия деформации Eупр ∝ ε²h, Дж/м²", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Накопление упругой энергии Eупр(h)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.3, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_14_bauer_strain_tree.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_15_fm_growth_rheed():
    """Слайд 15: Послойный 2D-рост Франка – ван дер Мерве (FM) и аналитические осцилляции ДБЭО (RHEED)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7.2, 5.1), dpi=300, gridspec_kw={'height_ratios': [1.0, 1.42], 'hspace': 0.22})

    ax1.set_xlim(0, 10.4)
    ax1.set_ylim(0, 2.55)
    ax1.axis('off')

    stages = [
        (0.25, "θ = 0.0 МС (Гладкая грань)\nМаксимум рефлекса I(t)", []),
        (3.80, "θ = 0.5 МС (2D-островки)\nРассеяние (Минимум I)", [1, 2, 4]),
        (7.35, "θ = 1.0 МС (Полный слой)\nНовый максимум I(t)", [0, 1, 2, 3, 4])
    ]
    for x0, title, top_row in stages:
        ax1.add_patch(Rectangle((x0, 0.18), 2.8, 0.44, fc='#64748B', ec=DARK))
        ax1.text(x0 + 1.40, 0.40, "Подложка GaAs (001)", color='white', fontsize=6.8, fontweight='bold', ha='center', va='center')
        for i in range(5):
            ax1.add_patch(Rectangle((x0 + 0.12 + i * 0.52, 0.65), 0.48, 0.34, fc=BLUE, ec='white', lw=0.8))
        for i in top_row:
            ax1.add_patch(Rectangle((x0 + 0.12 + i * 0.52, 1.02), 0.48, 0.34, fc=CYAN, ec=NAVY, lw=1.0))
        ax1.text(x0 + 1.40, 1.92, title, color=NAVY, fontsize=7.0, fontweight='bold', ha='center', va='center', bbox=BBOX)

    t_ml = np.linspace(0, 5.0, 600)
    I_rheed = np.where(
        t_ml < 0.2,
        1.0,
        0.58 + 0.42 * np.exp(-(t_ml - 0.2) / 6.5) * np.cos(2 * np.pi * (t_ml - 0.2))
    )

    ax2.plot(t_ml, I_rheed, color=BLUE, lw=2.6, label='Зеркальный рефлекс ДБЭО (RHEED)')
    ax2.axvline(0.2, color=RED, ls='--', lw=1.4, label='Старт МЛЭ (открытие заслонки)')

    max_t = np.array([1.2, 2.2, 3.2, 4.2])
    max_y = 0.58 + 0.42 * np.exp(-(max_t - 0.2) / 6.5)
    ax2.scatter(max_t, max_y, color=GREEN, s=55, zorder=7, label='Максимумы: полные слои (1..4 МС)')
    for idx, (tx, ty) in enumerate(zip(max_t, max_y), 1):
        ax2.text(tx, ty + 0.055, f"{idx} МС", fontsize=7.8, fontweight='bold', color=GREEN, ha='center')

    min_t = np.array([0.7, 1.7, 2.7, 3.7])
    min_y = 0.58 - 0.42 * np.exp(-(min_t - 0.2) / 6.5)
    ax2.scatter(min_t, min_y, color=ORANGE, s=45, zorder=7, label='Минимумы: заполнение θ = 0.5 МС')

    ax2.set_xlim(0, 5.0)
    ax2.set_ylim(-0.08, 1.18)
    ax2.set_xlabel("Время роста (в единицах монослоев, 1 период = 1 МС ≈ 0.283 нм)", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Интенсивность ДБЭО I(t), отн. ед.", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("Послойный 2D-рост Франка – ван дер Мерве и осцилляции ДБЭО (RHEED)",
                  fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='lower right', fontsize=6.4, framealpha=0.95, ncol=2)
    ax2.grid(True, ls=':', alpha=0.55)

    fig.savefig(os.path.join(OUT_DIR, "fig_15_fm_growth_rheed.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_16_vw_island_coalescence():
    """Слайд 16: 3 стадии островкового 3D-роста Фольмера – Вебера (VW) и порог перколяции проводимости."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.28})

    ax1.set_xlim(0, 6.2)
    ax1.set_ylim(0, 6.2)
    ax1.axis('off')

    levels = [
        (4.25, "I. 3D-нуклеация (h < 3 нм)\nИзолированные купола (Rs → ∞)", [(1.1, 0.45), (3.0, 0.52), (4.9, 0.48)], False),
        (2.25, "II. Разрастание и коалесценция\nСлияние островков (h ≈ 6–10 нм)", [(1.4, 0.88), (3.2, 0.95), (4.8, 0.85)], False),
        (0.25, "III. Поликристаллическая пленка\nМежзеренные границы (h > 15 нм)", [(1.2, 1.15), (2.7, 1.15), (4.1, 1.15), (5.2, 1.15)], True)
    ]

    for y0, label, domes, is_merged in levels:
        ax1.add_patch(Rectangle((0.3, y0), 5.6, 0.35, fc='#CBD5E1', ec=DARK))
        for cx, r in domes:
            ang = np.linspace(0, np.pi, 80)
            xd = np.clip(cx + r * np.cos(ang), 0.3, 5.9)
            yd = y0 + 0.35 + r * 0.65 * np.sin(ang)
            ax1.fill(xd, yd, color=ORANGE, alpha=0.88, edgecolor=RED, lw=1.4)
        if is_merged:
            for gx in [1.95, 3.4, 4.65]:
                ax1.plot([gx, gx], [y0 + 0.35, y0 + 0.98], color=RED, ls='--', lw=1.8)
            ax1.text(3.4, y0 + 1.12, "Границы зерен (рассеяние e⁻)", fontsize=6.8, fontweight='bold', color=RED, ha='center')
        ax1.text(3.1, y0 + 1.48, label, fontsize=7.2, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax1.set_title("а) Эволюция островков Фольмера–Вебера", fontsize=8.6, fontweight='bold', color=NAVY)

    h_nm = np.linspace(1.0, 22.0, 400)
    log_R_vw = 1.2 + 7.5 / (1.0 + np.exp((h_nm - 12.0) / 1.15))
    log_R_ti = 1.1 + 7.5 / (1.0 + np.exp((h_nm - 3.8) / 0.75))

    ax2.axvspan(1.0, 12.0, color='#FEE2E2', alpha=0.45, label='Диэлектрический разрыв Au/SiO₂')
    ax2.axvline(12.0, color=RED, ls='--', lw=1.6)
    ax2.plot(h_nm, log_R_vw, color=RED, lw=2.6, label='Au на SiO₂ (VW: перколяция 12 нм)')
    ax2.plot(h_nm, log_R_ti, color=GREEN, lw=2.6, label='Au с подслоем Ti: сплошность с 4 нм')

    ax2.scatter([12.0], [float(1.2 + 7.5 / 2.0)], color=RED, s=60, zorder=7)
    ax2.annotate("Порог перколяции:\nhперк ≈ 12 нм",
                 xy=(12.0, 4.95), xytext=(12.4, 5.8),
                 fontsize=6.8, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax2.annotate("Подслой Ti/Cr (↑σs):\nподавление деветтинга",
                 xy=(4.2, 3.8), xytext=(5.6, 2.2),
                 fontsize=7.2, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    ax2.set_xlim(1.0, 22.0)
    ax2.set_ylim(0.5, 10.4)
    ax2.set_xlabel("Номинальная толщина металлической пленки h, нм", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Логарифм сопротивления log₁₀(Rs, Ом/□)", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Порог перколяции и роль подслоя Ti/Cr", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=6.3, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_16_vw_island_coalescence.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_17_sk_quantum_dots():
    """Слайд 17: Механизм Странского – Крастанова (SK, 2D -> 3D) для InAs/GaAs (ε = +7.2%, hc = 1.7 МС)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.28})

    ax1.set_xlim(0, 6.2)
    ax1.set_ylim(0, 6.2)
    ax1.axis('off')

    ax1.add_patch(Rectangle((0.35, 4.30), 5.5, 0.44, fc='#64748B', ec=DARK))
    ax1.add_patch(Rectangle((0.35, 4.74), 5.5, 0.28, fc=BLUE, ec=NAVY))
    ax1.text(3.1, 5.50, "1. Смачивающий 2D-слой (h < 1.7 МС)\nУпругое сжатие InAs (ε = +7.2%)",
             fontsize=7.2, fontweight='bold', color=BLUE, ha='center', bbox=BBOX)

    ax1.add_patch(Rectangle((0.35, 2.30), 5.5, 0.44, fc='#64748B', ec=DARK))
    x_w = np.linspace(0.35, 5.85, 200)
    y_w = 2.74 + 0.32 + 0.08 * np.sin(2 * np.pi * (x_w - 0.35) / 1.6)
    ax1.fill_between(x_w, 2.74, y_w, color=ORANGE, alpha=0.85, edgecolor=RED, lw=1.4)
    ax1.text(3.1, 3.55, "2. Критическая толщина (hc = 1.7 МС)\nУпругая неустойчивость 2D-фронта",
             fontsize=7.2, fontweight='bold', color=ORANGE, ha='center', bbox=BBOX)

    ax1.add_patch(Rectangle((0.35, 0.25), 5.5, 0.44, fc='#64748B', ec=DARK))
    ax1.add_patch(Rectangle((0.35, 0.69), 5.5, 0.18, fc=BLUE, ec=NAVY))
    for qx in [1.35, 3.10, 4.85]:
        tri = Polygon([[qx - 0.65, 0.87], [qx + 0.65, 0.87], [qx, 1.54]], closed=True, fc=RED, ec=NAVY, lw=1.4)
        ax1.add_patch(tri)
    ax1.text(3.1, 1.92, "3. Когерентные 3D КТ InAs на смачивающем слое\nРелаксация вершин без дислокаций (3·10¹⁰ см⁻²)",
             fontsize=7.0, fontweight='bold', color=RED, ha='center', bbox=BBOX)

    ax1.set_title("а) Стадии перехода Странского–Крастанова", fontsize=8.4, fontweight='bold', color=NAVY)

    h = np.linspace(0.0, 3.5, 400)
    E_2d = 1.0 * h
    hc = 1.7
    E_sk_curve = 0.68 + 0.60 * h

    ax2.axvline(hc, color=RED, ls='--', lw=1.6)
    ax2.plot(h, E_2d, color=BLUE, lw=2.5, ls='--', label='Напряженный 2D-слой: E2D = Y·ε²·h')
    ax2.plot(h, E_sk_curve, color=RED, lw=2.6, label='3D-островки SK: E3D = ΔEгр + (1−γ)Yε²h')
    ax2.plot(h, np.minimum(E_2d, E_sk_curve), color=GREEN, lw=3.2, alpha=0.65, label='Равновесная траектория минимума ΔG')

    ax2.scatter([hc], [1.70], color=RED, s=70, zorder=8)
    ax2.annotate("Точка перехода SK:\nhc = 1.70 МС",
                 xy=(hc, 1.70), xytext=(0.20, 2.25),
                 fontsize=7.4, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))

    ax2.text(2.48, 1.15, "Выигрыш энергии\nпри 3D-релаксации\nвершин пирамид",
             fontsize=7.0, fontweight='bold', color=GREEN, ha='center', bbox=BBOX)

    ax2.set_xlim(0, 3.5)
    ax2.set_ylim(0, 3.85)
    ax2.set_xlabel("Количество осажденного InAs h, монослои (МС)", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Свободная энергия системы ΔG, отн. ед.", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Энергетический баланс SK-роста", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.3, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_17_sk_quantum_dots.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_20_adsorption_potentials():
    """Слайд 20: Потенциальные кривые Леннард-Джонса U(z) для физисорбции и активированной хемосорбции."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    z = np.linspace(0.09, 0.80, 600)
    z_p = 0.35
    D_p = 32.0
    u_phys = D_p * ((z_p / z)**12 - 2.0 * (z_p / z)**6)

    z_c = 0.16
    D_c = 225.0
    E_diss = 60.0
    u_chem = E_diss + D_c * (np.exp(-2 * 14.5 * (z - z_c)) - 2.0 * np.exp(-14.5 * (z - z_c)))

    z_cross = float(brentq(lambda zv: D_p * ((z_p / zv)**12 - 2.0 * (z_p / zv)**6) -
                           (E_diss + D_c * (np.exp(-2 * 14.5 * (zv - z_c)) - 2.0 * np.exp(-14.5 * (zv - z_c)))), 0.20, 0.32))
    E_act = float(D_p * ((z_p / z_cross)**12 - 2.0 * (z_p / z_cross)**6))

    ax.axhline(0, color=DARK, lw=1.2)
    ax.plot(z, u_phys, color=BLUE, lw=2.6, label='Физисорбция M + S (силы Ван-дер-Ваальса, без активации)')
    ax.plot(z, u_chem, color=RED, lw=2.6, label='Хемосорбция 2A + S (ковалентная связь, перенос заряда)')

    ax.scatter([z_p], [-D_p], color=BLUE, s=65, zorder=7)
    ax.scatter([z_c], [E_diss - D_c], color=RED, s=65, zorder=7)
    ax.scatter([z_cross], [E_act], color=ORANGE, s=70, zorder=8)

    ax.annotate(f"Яма физисорбции:\nz₀ ≈ {z_p:.2f} нм\nΔHфиз ≈ −{D_p:.0f} кДж/моль\n(полимолекулярная)",
                xy=(z_p, -D_p), xytext=(0.46, -92),
                fontsize=7.6, fontweight='bold', color=BLUE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax.annotate(f"Яма хемосорбции:\nz₀ ≈ {z_c:.2f} нм\nΔHхем ≈ {E_diss - D_c:.0f} кДж/моль\n(строго 1 монослой!)",
                xy=(z_c, E_diss - D_c), xytext=(0.26, -165),
                fontsize=7.6, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    # Размещаем выноску барьера активации на y = +18 кДж/моль (ниже красной асимптоты и легенды)
    ax.annotate(f"Барьер активации\nEакт = +{E_act:.0f} кДж/моль",
                xy=(z_cross, E_act), xytext=(0.42, 16),
                fontsize=7.6, fontweight='bold', color=ORANGE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))

    ax.set_xlim(0.08, 0.78)
    ax.set_ylim(-190, 112)
    ax.set_xlabel("Расстояние молекулы от поверхности твердого тела z, нм", fontsize=9.0, fontweight='bold', color=NAVY)
    ax.set_ylabel("Потенциальная энергия U(z), кДж/моль", fontsize=9.0, fontweight='bold', color=NAVY)
    ax.set_title("Потенциальные кривые Леннард-Джонса: физисорбция vs хемосорбция",
                 fontsize=9.4, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=7.4, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_20_adsorption_potentials.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_21_langmuir_isotherm():
    """Слайд 21: Изотерма мономолекулярной адсорбции Ленгмюра θ = KP/(1+KP) и линейная анаморфоза P/a от P."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.28})

    P = np.linspace(0, 10.0, 400)
    K_high, K_mid, K_low = 2.5, 0.8, 0.2
    th_high = (K_high * P) / (1.0 + K_high * P)
    th_mid = (K_mid * P) / (1.0 + K_mid * P)
    th_low = (K_low * P) / (1.0 + K_low * P)

    ax1.axhline(1.0, color=RED, ls='--', lw=1.5, label='Насыщение монослоя (θ → 1)')
    ax1.plot(P, th_high, color=BLUE, lw=2.6, label='Сильная сорбция (K = 2.5)')
    ax1.plot(P, th_mid, color=GREEN, lw=2.4, label='Средняя сорбция (K = 0.8)')
    ax1.plot(P, th_low, color=ORANGE, lw=2.2, ls='-.', label='Слабая сорбция (K = 0.2)')

    p_henry = np.linspace(0, 0.38, 50)
    ax1.plot(p_henry, K_high * p_henry, color=NAVY, ls=':', lw=2.0, label='Закон Генри: θ ≈ K·P')

    ax1.annotate("Область Генри (θ ≈ KP)",
                 xy=(0.25, float(K_high * 0.25 / (1 + K_high * 0.25))), xytext=(1.6, 0.42),
                 fontsize=7.2, fontweight='bold', color=NAVY, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    ax1.annotate("Плато насыщения (θ → 1)",
                 xy=(7.2, float(K_high * 7.2 / (1 + K_high * 7.2))), xytext=(3.6, 0.82),
                 fontsize=7.2, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))

    ax1.set_xlim(0, 10.0)
    ax1.set_ylim(0, 1.14)
    ax1.set_xlabel("Парциальное давление газа P, усл. ед.", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Степень заполнения монослоя θ = a / am", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_title("а) Изотерма И. Ленгмюра (1916)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower right', fontsize=6.3, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Линейная форма P/a = 1/(am*K) + P/am
    a_m = 4.0
    K_val = 0.8
    P_pts = np.array([0.5, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0])
    a_pts = a_m * (K_val * P_pts) / (1.0 + K_val * P_pts)
    y_lin_pts = P_pts / a_pts
    y_lin_curve = 1.0 / (a_m * K_val) + P / a_m

    ax2.plot(P, y_lin_curve, color=BLUE, lw=2.5, label='Прямая: P/a = 1/(am·K) + P/am')
    ax2.scatter(P_pts, y_lin_pts, color=RED, s=55, zorder=7, label='Экспериментальные точки')
    ax2.scatter([0], [1.0 / (a_m * K_val)], color=GREEN, s=65, zorder=8)

    ax2.annotate(f"Отсечка A = 1/(am·K) = {1.0/(a_m*K_val):.2f}",
                 xy=(0, 1.0 / (a_m * K_val)), xytext=(2.0, 0.22),
                 fontsize=7.2, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    # Размещаем блок тангенса наклона справа под прямой без наложения на точки и линию
    ax2.text(6.3, 1.02, f"Наклон: tan α = 1/am = {1.0/a_m:.2f}\n→ Емкость am = {a_m:.1f} ммоль/г",
             fontsize=7.2, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax2.set_xlim(0, 10.0)
    ax2.set_ylim(0, 3.05)
    ax2.set_xlabel("Парциальное давление газа P, усл. ед.", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Линеаризованный параметр P / a", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Линейная анаморфоза Ленгмюра", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_21_langmuir_isotherm.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_22_bet_multilayer_linear():
    """Слайд 22: Полимолекулярная теория БЭТ (1938) и линейный график в рабочем окне P/P0 = 0.05–0.35."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.8, 4.9), dpi=300, gridspec_kw={'wspace': 0.28})

    x = np.linspace(0.005, 0.88, 500)
    for C_val, col, lbl in [
        (120.0, BLUE, 'C = 120 (E₁ ≫ EL: четкая точка B)'),
        (25.0, GREEN, 'C = 25 (оксиды SiO₂, TiO₂)'),
        (1.5, ORANGE, 'C = 1.5 (E₁ ≈ EL: слабая связь)')
    ]:
        v_norm = (C_val * x) / ((1.0 - x) * (1.0 + (C_val - 1.0) * x))
        ax1.plot(x, v_norm, color=col, lw=2.5, label=lbl)

    ax1.axhline(1.0, color=RED, ls='--', lw=1.4, label='Емкость монослоя (V / Vm = 1)')
    ax1.axvspan(0.05, 0.35, color='#DBEAFE', alpha=0.55, label='Окно линейности БЭТ (0.05–0.35)')

    x_B = 1.0 / (np.sqrt(120.0) + 1.0)
    ax1.scatter([x_B], [1.0], color=RED, s=65, zorder=8)
    ax1.annotate("Точка B (V = Vm):\nзавершение 1-го слоя",
                 xy=(x_B, 1.0), xytext=(0.24, 3.15),
                 fontsize=7.3, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax1.set_xlim(0, 0.88)
    ax1.set_ylim(0, 5.5)
    ax1.set_xlabel("Относительное давление пара x = P / P₀", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Число статистических монослоев V / Vm", fontsize=8.4, fontweight='bold', color=NAVY)
    ax1.set_title("а) Полимолекулярная изотерма БЭТ (1938)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper left', fontsize=6.3, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    Vm = 180.0
    C_bet = 85.0
    A_int = 1.0 / (Vm * C_bet)
    B_slp = (C_bet - 1.0) / (Vm * C_bet)

    x_win = np.linspace(0.02, 0.40, 200)
    y_bet = (A_int + B_slp * x_win) * 1000.0
    x_exp = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
    y_exp = (A_int + B_slp * x_exp) * 1000.0

    ax2.axvspan(0.05, 0.35, color='#DCFCE7', alpha=0.55, label='Диапазон ИЮПАК (P/P₀ = 0.05–0.35)')
    ax2.plot(x_win, y_bet, color=NAVY, lw=2.5, label='Линейная регрессия БЭТ (R² = 0.9999)')
    ax2.scatter(x_exp, y_exp, color=RED, s=55, zorder=8, label='Точки сорбции N₂ при 77.3 К')

    S_ud = Vm * 4.3526
    # Размещаем расчетный блок в правом нижнем углу под прямой без пересечения с точками
    ax2.text(0.262, 0.34,
             f"Расчет из прямой БЭТ:\n"
             f"• Vm = 1/(A+B) = {Vm:.0f} см³/г\n"
             f"• Константа C = {C_bet:.0f}\n"
             f"• Sуд = 4.35·Vm = {S_ud:.0f} м²/г",
             fontsize=6.9, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax2.set_xlim(0.0, 0.40)
    ax2.set_ylim(0.0, 2.38)
    ax2.set_xlabel("Относительное давление P / P₀", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Координата БЭТ P / [V(P₀ − P)] × 10³, г/см³", fontsize=8.2, fontweight='bold', color=NAVY)
    ax2.set_title("б) Линейный график БЭТ для расчета Vm и Sуд", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.4, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.savefig(os.path.join(OUT_DIR, "fig_22_bet_multilayer_linear.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_23_iupac_isotherms():
    """Слайд 23: Матрица 2x3 всех 6 канонических типов изотерм адсорбции по классификации ИЮПАК (IUPAC)."""
    fig, axes = plt.subplots(2, 3, figsize=(7.6, 4.9), dpi=300)
    x = np.linspace(0.005, 0.98, 300)

    ax = axes[0, 0]
    y1 = 95.0 * (45 * x) / (1 + 45 * x)
    ax.plot(x, y1, color=BLUE, lw=2.4)
    ax.fill_between(x, 0, y1, color='#DBEAFE', alpha=0.45)
    ax.set_title("Тип I: Микропоры (< 2 нм)\nЦеолиты, активный уголь", fontsize=7.5, fontweight='bold', color=NAVY)

    ax = axes[0, 1]
    y2 = 22.0 * (35 * x) / ((1 - 0.82 * x) * (1 + 34 * x))
    ax.plot(x, y2, color=GREEN, lw=2.4)
    yb = float(22.0 * (35 * 0.15) / ((1 - 0.82 * 0.15) * (1 + 34 * 0.15)))
    ax.scatter([0.15], [yb], color=RED, s=38, zorder=6)
    ax.annotate("Точка B", xy=(0.15, yb), xytext=(0.35, 12),
                fontsize=6.8, fontweight='bold', color=RED,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
    ax.set_title("Тип II: Непористые порошки\nПолислойная сорбция БЭТ", fontsize=7.5, fontweight='bold', color=NAVY)

    ax = axes[0, 2]
    y3 = 12.0 * x / (1 - 0.86 * x)
    ax.plot(x, y3, color=ORANGE, lw=2.4)
    ax.set_title("Тип III: Слабая связь (C ≤ 2)\nВода на гидрофобном графите", fontsize=7.5, fontweight='bold', color=NAVY)

    ax = axes[1, 0]
    base4 = 25 * (25 * x) / (1 + 25 * x)
    y4_ads = base4 + 65 / (1 + np.exp(-(x - 0.68) / 0.03))
    y4_des = base4 + 65 / (1 + np.exp(-(x - 0.50) / 0.025))
    ax.plot(x, y4_ads, color=BLUE, lw=2.2, label='Адс.')
    ax.plot(x, y4_des, color=RED, lw=2.2, ls='--', label='Дес.')
    ax.fill_between(x, y4_ads, y4_des, color='#FEF3C7', alpha=0.7)
    ax.legend(loc='lower right', fontsize=6.2)
    ax.set_title("Тип IV: Мезопоры (2–50 нм)\nКремнезем SBA-15 (гистерезис)", fontsize=7.5, fontweight='bold', color=NAVY)

    ax = axes[1, 1]
    y5_ads = 90 / (1 + np.exp(-(x - 0.72) / 0.04))
    y5_des = 90 / (1 + np.exp(-(x - 0.54) / 0.035))
    ax.plot(x, y5_ads, color=PURPLE, lw=2.2)
    ax.plot(x, y5_des, color=RED, lw=2.0, ls='--')
    ax.fill_between(x, y5_ads, y5_des, color='#F3E8FF', alpha=0.7)
    ax.set_title("Тип V: Пористые + слабая связь\nСорбция паров воды в порах", fontsize=7.5, fontweight='bold', color=NAVY)

    ax = axes[1, 2]
    y6 = (30 / (1 + np.exp(-(x - 0.18) / 0.018)) +
          30 / (1 + np.exp(-(x - 0.48) / 0.020)) +
          30 / (1 + np.exp(-(x - 0.78) / 0.022)))
    ax.plot(x, y6, color=NAVY, lw=2.4)
    ax.set_title("Тип VI: Ступенчатая сорбция\nАтомарно-гладкий графен / BN", fontsize=7.5, fontweight='bold', color=NAVY)

    for ax in axes.flat:
        ax.set_xlim(0, 1.0)
        ax.set_ylim(0, 105)
        ax.set_xticks([0, 0.5, 1.0])
        ax.set_yticks([])
        ax.tick_params(labelsize=7.0)
        ax.set_xlabel("P / P₀", fontsize=7.2, fontweight='bold', color=MUTED)
        ax.set_ylabel("Сорбция V", fontsize=7.2, fontweight='bold', color=MUTED)
        ax.grid(True, ls=':', alpha=0.5)

    fig.suptitle("Шесть канонических типов изотерм адсорбции по классификации ИЮПАК (IUPAC)",
                 fontsize=9.2, fontweight='bold', color=NAVY, y=1.01)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_23_iupac_isotherms.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == "__main__":
    fig_14_bauer_strain_tree()
    fig_15_fm_growth_rheed()
    fig_16_vw_island_coalescence()
    fig_17_sk_quantum_dots()
    fig_20_adsorption_potentials()
    fig_21_langmuir_isotherm()
    fig_22_bet_multilayer_linear()
    fig_23_iupac_isotherms()
    print("Part 2 figures (Slides 14-23) regenerated cleanly.")
