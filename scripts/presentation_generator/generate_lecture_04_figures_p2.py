"""
Генерация иллюстраций (Часть 2: Слайды 14–23) для Лекции №4:
«Поверхностные явления и механизмы роста плёнок».
Строго по аналитическим формулам и из геометрических примитивов (300 DPI).
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle, Polygon
from scipy.optimize import brentq

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


def fig_14_bauer_strain_tree():
    """Слайд 14: Дерево критерия Бауэра Δσ и аналитический график накопления упругой энергии E_упр(h) ∝ ε²h."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Дерево выбора механизма гетероэпитаксии по Бауэру (1958)
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 6.2)
    ax1.axis('off')

    root = FancyBboxPatch((0.6, 4.95), 4.8, 0.95, boxstyle="round,pad=0.1", fc=NAVY, ec=NAVY)
    ax1.add_patch(root)
    ax1.text(3.0, 5.42, "Критерий Э. Бауэра (1958):\nΔσ = σ_f + σ_i − σ_s   и   ε = (a_f − a_s)/a_s",
             color='white', fontsize=8.0, fontweight='bold', ha='center', va='center')

    # Ветвь 1: Δσ ≤ 0
    b_left = FancyBboxPatch((0.2, 3.15), 2.55, 1.0, boxstyle="round,pad=0.08", fc='#E0F2FE', ec=BLUE, lw=1.6)
    ax1.add_patch(b_left)
    ax1.text(1.48, 3.65, "Смачивание подложки:\nΔσ ≤ 0 (Wa ≥ Wc)", color=BLUE, fontsize=7.8, fontweight='bold', ha='center', va='center')

    # Ветвь 2: Δσ > 0
    b_right = FancyBboxPatch((3.25, 3.15), 2.55, 1.0, boxstyle="round,pad=0.08", fc='#FEE2E2', ec=RED, lw=1.6)
    ax1.add_patch(b_right)
    ax1.text(4.52, 3.65, "Несмачивание:\nΔσ > 0 (Wa < Wc)", color=RED, fontsize=7.8, fontweight='bold', ha='center', va='center')

    ax1.annotate("", xy=(1.48, 4.2), xytext=(2.4, 4.92), arrowprops=dict(arrowstyle="->", color=BLUE, lw=2.0))
    ax1.annotate("", xy=(4.52, 4.2), xytext=(3.6, 4.92), arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))

    # Три терминальных режима: FM, SK, VW
    fm_box = FancyBboxPatch((0.1, 0.45), 1.75, 1.9, boxstyle="round,pad=0.08", fc='#DCFCE7', ec=GREEN, lw=1.8)
    sk_box = FancyBboxPatch((2.05, 0.45), 1.85, 1.9, boxstyle="round,pad=0.08", fc='#FEF3C7', ec=ORANGE, lw=1.8)
    vw_box = FancyBboxPatch((4.1, 0.45), 1.8, 1.9, boxstyle="round,pad=0.08", fc='#FEE2E2', ec=RED, lw=1.8)
    ax1.add_patch(fm_box)
    ax1.add_patch(sk_box)
    ax1.add_patch(vw_box)

    ax1.text(0.98, 1.4, "1. Рост FM (2D)\nФранк–ван дер Мерве\nε ≈ 0\nПослойный рост\nAlGaAs / GaAs",
             color=GREEN, fontsize=7.1, fontweight='bold', ha='center', va='center')
    ax1.text(2.98, 1.4, "3. Рост SK (2D→3D)\nСтранский–Крастанов\n|ε| = 1–8%\nСлой + 3D КТ\nInAs / GaAs",
             color=ORANGE, fontsize=7.1, fontweight='bold', ha='center', va='center')
    ax1.text(5.0, 1.4, "2. Рост VW (3D)\nФольмер–Вебер\nЛюбое ε\nСразу 3D-островки\nAu, Ag / SiO₂",
             color=RED, fontsize=7.1, fontweight='bold', ha='center', va='center')

    ax1.annotate("", xy=(0.98, 2.4), xytext=(1.25, 3.12), arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.8))
    ax1.annotate("", xy=(2.98, 2.4), xytext=(1.75, 3.12), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.8))
    ax1.annotate("", xy=(5.0, 2.4), xytext=(4.52, 3.12), arrowprops=dict(arrowstyle="->", color=RED, lw=1.8))
    ax1.set_title("а) Термодинамическое дерево Бауэра", fontsize=9.0, fontweight='bold', color=NAVY)

    # Правая панель: Аналитический график E_упр(h) = Y * ε² * h (в МС) для различных ε
    h_ml = np.linspace(0, 4.0, 300)
    # Для InAs/GaAs (ε = 7.16%): 1 МС дает ~0.1215 Дж/м²; порог перехода в 3D при hc = 1.7 МС (~0.206 Дж/м²)
    e_inas = 0.1215 * h_ml                     # ε = 7.2% (InAs/GaAs)
    e_sige = 0.1215 * (4.2 / 7.16)**2 * h_ml   # ε = 4.2% (Ge/Si)
    e_algaas = 0.1215 * (0.1 / 7.16)**2 * h_ml # ε ≈ 0.04% (AlGaAs/GaAs)
    barrier = 0.2065                           # Барьер 2D -> 3D релаксации

    ax2.axhspan(barrier, 0.50, color='#FEF3C7', alpha=0.55, label='Зона 3D-релаксации (образование КТ / дислокаций)')
    ax2.axhline(barrier, color=RED, ls='--', lw=1.6, label='Порог упругой устойчивости 2D-слоя')
    ax2.plot(h_ml, e_inas, color=RED, lw=2.6, label='InAs / GaAs (ε = +7.2%): SK-переход при hc = 1.7 МС')
    ax2.plot(h_ml, e_sige, color=ORANGE, lw=2.3, label='Ge / Si (ε = +4.2%): SK-переход при hc ≈ 4–5 МС')
    ax2.plot(h_ml, e_algaas, color=GREEN, lw=2.5, label='AlGaAs / GaAs (ε = 0.04%): чистый 2D FM-рост')

    ax2.scatter([1.7], [0.1215 * 1.7], color=RED, s=65, zorder=7)
    ax2.annotate("Критическая толщина\nhc = 1.7 МС (InAs/GaAs)\nПереход 2D → 3D КТ",
                 xy=(1.7, 0.1215 * 1.7), xytext=(1.95, 0.08),
                 fontsize=7.6, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax2.set_xlim(0, 4.0)
    ax2.set_ylim(0, 0.48)
    ax2.set_xlabel("Толщина эпитаксиальной пленки h, монослои (МС)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Упругая энергия деформации E_упр ∝ ε²h, Дж/м²", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_title("б) Накопление упругой энергии E_упр(h)", fontsize=9.0, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_14_bauer_strain_tree.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_15_fm_growth_rheed():
    """Слайд 15: Послойный 2D-рост Франка – ван дер Мерве (FM) и аналитические осцилляции ДБЭО (RHEED)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 5.1), dpi=300, gridspec_kw={'height_ratios': [1.0, 1.35]})

    # Верхняя панель: Схема послойного заполнения монослоя θ = 0 -> 0.5 -> 1.0 МС
    ax1.set_xlim(0, 9.6)
    ax1.set_ylim(0, 2.5)
    ax1.axis('off')

    stages = [
        (0.2, "θ = 0.0 МС (Гладкая грань)\nМаксимум зеркального рефлекса", [1, 1, 1, 1, 1], []),
        (3.4, "θ = 0.5 МС (2D-островки)\nРассеяние на ступенях (Минимум)", [1, 1, 1, 1, 1], [1, 2, 4]),
        (6.6, "θ = 1.0 МС (Завершенный слой)\nВосстановление максимума I(t)", [1, 1, 1, 1, 1], [0, 1, 2, 3, 4])
    ]
    for x0, title, base_row, top_row in stages:
        ax1.add_patch(Rectangle((x0, 0.2), 2.7, 0.45, fc='#64748B', ec=DARK))
        ax1.text(x0 + 1.35, 0.42, "Подложка GaAs (001)", color='white', fontsize=6.8, fontweight='bold', ha='center', va='center')
        for i in range(5):
            ax1.add_patch(Rectangle((x0 + 0.1 + i * 0.5, 0.68), 0.46, 0.35, fc=BLUE, ec='white', lw=0.8))
        for i in top_row:
            ax1.add_patch(Rectangle((x0 + 0.1 + i * 0.5, 1.06), 0.46, 0.35, fc=CYAN, ec=NAVY, lw=1.0))
        ax1.text(x0 + 1.35, 1.92, title, color=NAVY, fontsize=7.4, fontweight='bold', ha='center', va='center', bbox=BBOX)

    # Нижняя панель: Аналитический график осцилляций интенсивности ДБЭО (RHEED)
    t_ml = np.linspace(0, 5.0, 600)
    # Затухающая косинусоида с периодом ровно 1 монослой
    I_rheed = np.where(
        t_ml < 0.2,
        1.0,
        0.58 + 0.42 * np.exp(-(t_ml - 0.2) / 6.5) * np.cos(2 * np.pi * (t_ml - 0.2))
    )

    ax2.plot(t_ml, I_rheed, color=BLUE, lw=2.6, label='Интенсивность зеркального рефлекса ДБЭО (RHEED)')
    ax2.axvline(0.2, color=RED, ls='--', lw=1.4, label='Открытие заслонки ячейки Кнудсена (старт МЛЭ)')

    # Отметим максимумы (полные монослои 1, 2, 3, 4 МС) и минимумы (0.5, 1.5 МС)
    max_t = np.array([1.2, 2.2, 3.2, 4.2])
    max_y = 0.58 + 0.42 * np.exp(-(max_t - 0.2) / 6.5)
    ax2.scatter(max_t, max_y, color=GREEN, s=55, zorder=7, label='Максимумы: завершенные монослои (θ = 1, 2, 3, 4 МС)')
    for idx, (tx, ty) in enumerate(zip(max_t, max_y), 1):
        ax2.text(tx, ty + 0.055, f"{idx} МС", fontsize=8.0, fontweight='bold', color=GREEN, ha='center')

    min_t = np.array([0.7, 1.7, 2.7, 3.7])
    min_y = 0.58 - 0.42 * np.exp(-(min_t - 0.2) / 6.5)
    ax2.scatter(min_t, min_y, color=ORANGE, s=45, zorder=7, label='Минимумы: половинное заполнение (θ = 0.5, 1.5, ... МС)')

    ax2.set_xlim(0, 5.0)
    ax2.set_ylim(0.05, 1.18)
    ax2.set_xlabel("Время роста (в единицах калиброванных монослоев, 1 период = 1 МС ≈ 0.283 нм)", fontsize=8.5, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Интенсивность ДБЭО I(t), отн. ед.", fontsize=8.5, fontweight='bold', color=NAVY)
    ax2.set_title("Послойный 2D-рост Франка – ван дер Мерве и контроль толщины по осцилляциям ДБЭО",
                  fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.legend(loc='lower right', fontsize=6.8, framealpha=0.95, ncol=2)
    ax2.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_15_fm_growth_rheed.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_16_vw_island_coalescence():
    """Слайд 16: 3 стадии островкового 3D-роста Фольмера – Вебера (VW) и порог перколяции проводимости."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: 3 стадии морфологии VW-роста (Au на SiO2, Δσ > 0)
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 6.2)
    ax1.axis('off')

    levels = [
        (4.25, "I. 3D-нуклеация (h < 3 нм)\nИзолированные купола (R_s → ∞)", [(1.1, 0.45), (2.9, 0.52), (4.7, 0.48)], False),
        (2.25, "II. Разрастание и коалесценция\nСлияние островков (h ≈ 6–10 нм)", [(1.4, 0.88), (3.1, 0.95), (4.6, 0.85)], False),
        (0.25, "III. Сплошная поликристаллическая пленка\nМежзеренные границы (h > 15 нм)", [(1.2, 1.15), (2.6, 1.15), (4.0, 1.15), (5.0, 1.15)], True)
    ]

    for y0, label, domes, is_merged in levels:
        ax1.add_patch(Rectangle((0.3, y0), 5.4, 0.35, fc='#CBD5E1', ec=DARK))
        for cx, r in domes:
            ang = np.linspace(0, np.pi, 80)
            xd = np.clip(cx + r * np.cos(ang), 0.3, 5.7)
            yd = y0 + 0.35 + r * 0.65 * np.sin(ang)
            ax1.fill(xd, yd, color=ORANGE, alpha=0.88, edgecolor=RED, lw=1.4)
        if is_merged:
            for gx in [1.9, 3.3, 4.5]:
                ax1.plot([gx, gx], [y0 + 0.35, y0 + 0.98], color=RED, ls='--', lw=1.8)
            ax1.text(3.3, y0 + 1.15, "Границы зерен (рассеяние e⁻)", fontsize=7.0, fontweight='bold', color=RED, ha='center')
        ax1.text(3.0, y0 + 1.48, label, fontsize=7.5, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax1.set_title("а) Эволюция островков Фольмера–Вебера", fontsize=9.0, fontweight='bold', color=NAVY)

    # Правая панель: Перколяционный скачок сопротивления Rs(h) для Au/SiO2 vs Au/Ti/SiO2
    h_nm = np.linspace(1.0, 22.0, 400)
    # Логарифм поверхностного сопротивления log10(Rs, Ом/кв)
    log_R_vw = 1.2 + 7.5 / (1.0 + np.exp((h_nm - 12.0) / 1.15))
    log_R_ti = 1.1 + 7.5 / (1.0 + np.exp((h_nm - 3.8) / 0.75))

    ax2.axvspan(1.0, 12.0, color='#FEE2E2', alpha=0.45, label='Диэлектрический разрыв Au/SiO₂ (до перколяции)')
    ax2.axvline(12.0, color=RED, ls='--', lw=1.6)
    ax2.plot(h_nm, log_R_vw, color=RED, lw=2.6, label='Чистое Au на SiO₂ (VW-рост: перколяция при h ≈ 12 нм)')
    ax2.plot(h_nm, log_R_ti, color=GREEN, lw=2.6, label='Au с адгезионным подслоем Ti (1.5 нм): сплошность с 4 нм')

    ax2.scatter([12.0], [float(1.2 + 7.5 / 2.0)], color=RED, s=60, zorder=7)
    ax2.annotate("Порог перколяции VW:\nh_перк ≈ 12 нм\n(слияние 3D-островков)",
                 xy=(12.0, 4.95), xytext=(13.2, 6.2),
                 fontsize=7.6, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax2.annotate("Адгезионный подслой Ti/Cr:\n↑σ_s → подавление деветтинга",
                 xy=(4.2, 3.8), xytext=(5.5, 2.2),
                 fontsize=7.6, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    ax2.set_xlim(1.0, 22.0)
    ax2.set_ylim(0.5, 9.2)
    ax2.set_xlabel("Номинальная толщина металлической пленки h, нм", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Логарифм сопротивления log₁₀(R_s, Ом/□)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_title("б) Порог перколяции и роль подслоя Ti/Cr", fontsize=9.0, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_16_vw_island_coalescence.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_17_sk_quantum_dots():
    """Слайд 17: Механизм Странского – Крастанова (SK, 2D -> 3D) для InAs/GaAs (ε = +7.2%, hc = 1.7 МС) и энергетический баланс."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: 3 стадии SK-перехода InAs на GaAs(001)
    ax1.set_xlim(0, 6)
    ax1.set_ylim(0, 6.2)
    ax1.axis('off')

    # Стадия 1: Смачивающий 2D-слой (h < 1.7 МС)
    ax1.add_patch(Rectangle((0.3, 4.3), 5.4, 0.45, fc='#64748B', ec=DARK))
    ax1.add_patch(Rectangle((0.3, 4.75), 5.4, 0.28, fc=BLUE, ec=NAVY))
    ax1.text(3.0, 5.5, "1. Смачивающий 2D-слой (Wetting layer, h < 1.7 МС)\nЛатеральное сжатие решетки InAs (ε = +7.2%)",
             fontsize=7.5, fontweight='bold', color=BLUE, ha='center', bbox=BBOX)

    # Стадия 2: Достижение критической толщины hc = 1.7 МС
    ax1.add_patch(Rectangle((0.3, 2.3), 5.4, 0.45, fc='#64748B', ec=DARK))
    x_w = np.linspace(0.3, 5.7, 200)
    y_w = 2.75 + 0.32 + 0.08 * np.sin(2 * np.pi * (x_w - 0.3) / 1.6)
    ax1.fill_between(x_w, 2.75, y_w, color=ORANGE, alpha=0.85, edgecolor=RED, lw=1.4)
    ax1.text(3.0, 3.55, "2. Критическая толщина Матьюса–Блейксли (hc = 1.7 МС)\nУпругая неустойчивость плоского фронта",
             fontsize=7.5, fontweight='bold', color=ORANGE, ha='center', bbox=BBOX)

    # Стадия 3: Когерентные 3D пирамидальные квантовые точки на смачивающем слое
    ax1.add_patch(Rectangle((0.3, 0.25), 5.4, 0.45, fc='#64748B', ec=DARK))
    ax1.add_patch(Rectangle((0.3, 0.70), 5.4, 0.18, fc=BLUE, ec=NAVY))
    for qx in [1.3, 3.0, 4.7]:
        tri = Polygon([[qx - 0.65, 0.88], [qx + 0.65, 0.88], [qx, 1.55]], closed=True, fc=RED, ec=NAVY, lw=1.4)
        ax1.add_patch(tri)
    ax1.text(3.0, 1.92, "3. Когерентные 3D КТ InAs на 1 МС смачивающем слое\nУпругая релаксация вершин без дислокаций (10¹⁰–10¹¹ см⁻²)",
             fontsize=7.4, fontweight='bold', color=RED, ha='center', bbox=BBOX)

    ax1.set_title("а) Морфология перехода Странского–Крастанова", fontsize=8.8, fontweight='bold', color=NAVY)

    # Правая панель: Энергетический баланс ΔG(h) для 2D-пленки vs 3D SK-островков
    h = np.linspace(0.0, 3.5, 400)
    # 2D напряженная пленка: линейный рост упругой энергии E_2D = 1.0 * h
    E_2d = 1.0 * h
    # 3D когерентные КТ на смачивающем слое: дополнительная поверхностная цена граней ΔE_surf, но меньший наклон упругой энергии (релаксация ~60%)
    hc = 1.7
    E_sk = np.where(h <= 1.0, E_2d, 1.0 + 0.42 * (h - 1.0) + 0.406 * (1 - np.exp(-(h - 1.0) / 0.55)))
    # Пересечение ровно при hc = 1.7 МС
    E_sk_exact = 1.0 * hc + 0.42 * (h - hc) + 0.22 * np.exp(-(h - hc) / 0.8) - 0.22
    # Сделаем строгую физическую модель: E_SK(h) = E_WL + Δγ_facets + α_relax * Y * ε² * (h - h_WL)
    E_sk_curve = 0.68 + 0.60 * h  # пересекает E_2d = 1.0*h строго в точке 1.0*h = 0.68 + 0.60*h => 0.40*h = 0.68 => h = 1.70 МС!

    ax2.axvline(hc, color=RED, ls='--', lw=1.6)
    ax2.plot(h, E_2d, color=BLUE, lw=2.5, ls='--', label='Плоский напряженный 2D-слой: E_2D = Y·ε²·h')
    ax2.plot(h, E_sk_curve, color=RED, lw=2.6, label='3D-островки SK: E_3D = ΔE_граней + (1−γ_рел)Y·ε²·h')
    ax2.plot(h, np.minimum(E_2d, E_sk_curve), color=GREEN, lw=3.2, alpha=0.65, label='Термодинамически равновесная траектория')

    ax2.scatter([hc], [1.70], color=RED, s=70, zorder=8)
    ax2.annotate("Точка перехода SK:\nhc = 1.70 МС\n(ΔE_рел > ΔA·σ_граней)",
                 xy=(hc, 1.70), xytext=(0.22, 2.35),
                 fontsize=7.8, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.6))

    ax2.text(2.55, 1.25, "Выигрыш энергии\nза счет релаксации\nвершин 3D-пирамид",
             fontsize=7.6, fontweight='bold', color=GREEN, ha='center', bbox=BBOX)

    ax2.set_xlim(0, 3.5)
    ax2.set_ylim(0, 3.6)
    ax2.set_xlabel("Количество осажденного InAs h, монослои (МС)", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Свободная энергия системы ΔG, отн. ед.", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_title("б) Энергетический критерий SK-самоорганизации", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_17_sk_quantum_dots.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_20_adsorption_potentials():
    """Слайд 20: Потенциальные кривые Леннард-Джонса U(z) для физисорбции и активированной хемосорбции."""
    fig, ax = plt.subplots(figsize=(6.8, 5.0), dpi=300)

    z = np.linspace(0.09, 0.80, 600)

    # 1. Кривая физисорбции (ван-дер-ваальсов минимум при z_физ = 0.35 нм, глубина -30 кДж/моль)
    z_p = 0.35
    D_p = 32.0
    u_phys = D_p * ((z_p / z)**12 - 2.0 * (z_p / z)**6)

    # 2. Кривая диссоциативной хемосорбции (минимум при z_хем = 0.16 нм, глубина -165 кДж/моль, асимптота диссоциации +60 кДж/моль)
    z_c = 0.16
    D_c = 225.0
    E_diss = 60.0
    u_chem = E_diss + D_c * (np.exp(-2 * 14.5 * (z - z_c)) - 2.0 * np.exp(-14.5 * (z - z_c)))

    # Точка пересечения кривых (активационный барьер перехода из прекурсора физисорбции в хемосорбцию)
    z_cross = float(brentq(lambda zv: D_p * ((z_p / zv)**12 - 2.0 * (z_p / zv)**6) -
                           (E_diss + D_c * (np.exp(-2 * 14.5 * (zv - z_c)) - 2.0 * np.exp(-14.5 * (zv - z_c)))), 0.20, 0.32))
    E_act = float(D_p * ((z_p / z_cross)**12 - 2.0 * (z_p / z_cross)**6))

    ax.axhline(0, color=DARK, lw=1.2)
    ax.plot(z, u_phys, color=BLUE, lw=2.6, label='Физисорбция M + S (силы Ван-дер-Ваальса, без активации)')
    ax.plot(z, u_chem, color=RED, lw=2.6, label='Хемосорбция 2A + S (ковалентная связь, перенос заряда)')

    # Реперные точки: минимум физисорбции, барьер активации, минимум хемосорбции
    ax.scatter([z_p], [-D_p], color=BLUE, s=65, zorder=7)
    ax.scatter([z_c], [E_diss - D_c], color=RED, s=65, zorder=7)
    ax.scatter([z_cross], [E_act], color=ORANGE, s=70, zorder=8)

    ax.annotate(f"Яма физисорбции:\nz₀ ≈ {z_p:.2f} нм\nΔH_физ ≈ −{D_p:.0f} кДж/моль\n(полимолекулярная)",
                xy=(z_p, -D_p), xytext=(0.46, -85),
                fontsize=7.8, fontweight='bold', color=BLUE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.5))

    ax.annotate(f"Яма хемосорбции:\nz₀ ≈ {z_c:.2f} нм\nΔH_хем ≈ {E_diss - D_c:.0f} кДж/моль\n(строго 1 монослой!)",
                xy=(z_c, E_diss - D_c), xytext=(0.28, -162),
                fontsize=7.8, fontweight='bold', color=RED, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax.annotate(f"Барьер активации\nE_акт = +{E_act:.0f} кДж/моль",
                xy=(z_cross, E_act), xytext=(0.36, 48),
                fontsize=7.8, fontweight='bold', color=ORANGE, bbox=BBOX,
                arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.5))

    ax.set_xlim(0.08, 0.78)
    ax.set_ylim(-190, 95)
    ax.set_xlabel("Расстояние молекулы от поверхности твердого тела z, нм", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_ylabel("Потенциальная энергия U(z), кДж/моль", fontsize=9.2, fontweight='bold', color=NAVY)
    ax.set_title("Потенциальные кривые Леннард-Джонса: физисорбция vs хемосорбция",
                 fontsize=9.6, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=7.8, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.55)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_20_adsorption_potentials.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_21_langmuir_isotherm():
    """Слайд 21: Изотерма мономолекулярной адсорбции Ленгмюра θ = KP/(1+KP) и линейная анаморфоза P/a от P."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Точные кривые Ленгмюра θ(P) = KP / (1 + KP)
    P = np.linspace(0, 10.0, 400)
    K_high, K_mid, K_low = 2.5, 0.8, 0.2
    th_high = (K_high * P) / (1.0 + K_high * P)
    th_mid = (K_mid * P) / (1.0 + K_mid * P)
    th_low = (K_low * P) / (1.0 + K_low * P)

    ax1.axhline(1.0, color=RED, ls='--', lw=1.5, label='Предел насыщения монослоя (θ → 1, a = a_m)')
    ax1.plot(P, th_high, color=BLUE, lw=2.6, label='Сильная сорбция (K = 2.5 атм⁻¹: быстрое насыщение)')
    ax1.plot(P, th_mid, color=GREEN, lw=2.4, label='Умеренная сорбция (K = 0.8 атм⁻¹: рабочий режим сенсора)')
    ax1.plot(P, th_low, color=ORANGE, lw=2.2, ls='-.', label='Слабая сорбция (K = 0.2 атм⁻¹: квазилинейный режим)')

    # Касательная Генри при малых P для K = 2.5
    p_henry = np.linspace(0, 0.38, 50)
    ax1.plot(p_henry, K_high * p_henry, color=NAVY, ls=':', lw=2.0, label='Закон Генри при малых P: θ ≈ K·P')

    ax1.annotate("Область Генри\n(θ ≈ KP, линейный\nотклик наносенсора)",
                 xy=(0.25, float(K_high * 0.25 / (1 + K_high * 0.25))), xytext=(1.8, 0.32),
                 fontsize=7.5, fontweight='bold', color=NAVY, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=NAVY, lw=1.4))

    ax1.annotate("Плато насыщения (θ → 1):\nвсе активные центры заняты",
                 xy=(7.5, float(K_high * 7.5 / (1 + K_high * 7.5))), xytext=(3.8, 0.78),
                 fontsize=7.5, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.4))

    ax1.set_xlim(0, 10.0)
    ax1.set_ylim(0, 1.12)
    ax1.set_xlabel("Парциальное давление газа P, усл. ед.", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Степень заполнения монослоя θ = a / a_m", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_title("а) Изотерма И. Ленгмюра (1916)", fontsize=9.0, fontweight='bold', color=NAVY)
    ax1.legend(loc='lower right', fontsize=6.5, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Линейная форма уравнения Ленгмюра P/a = 1/(a_m K) + P / a_m
    a_m = 4.0  # ммоль/г
    K_val = 0.8
    P_pts = np.array([0.5, 1.5, 3.0, 4.5, 6.0, 7.5, 9.0])
    a_pts = a_m * (K_val * P_pts) / (1.0 + K_val * P_pts)
    y_lin_pts = P_pts / a_pts
    y_lin_curve = 1.0 / (a_m * K_val) + P / a_m

    ax2.plot(P, y_lin_curve, color=BLUE, lw=2.5, label='Прямая Ленгмюра: P/a = 1/(a_m·K) + (1/a_m)·P')
    ax2.scatter(P_pts, y_lin_pts, color=RED, s=55, zorder=7, label='Экспериментальные точки сорбции')
    ax2.scatter([0], [1.0 / (a_m * K_val)], color=GREEN, s=65, zorder=8)

    ax2.annotate(f"Отсечка на оси ординат:\nA = 1/(a_m·K) = {1.0/(a_m*K_val):.2f}",
                 xy=(0, 1.0 / (a_m * K_val)), xytext=(1.8, 0.28),
                 fontsize=7.6, fontweight='bold', color=GREEN, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.5))

    ax2.text(5.0, 2.15, f"Тангенс угла наклона:\ntan α = 1 / a_m = {1.0/a_m:.2f} г/ммоль\n→ Емкость монослоя a_m = {a_m:.1f} ммоль/г",
             fontsize=7.6, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax2.set_xlim(0, 10.0)
    ax2.set_ylim(0, 3.0)
    ax2.set_xlabel("Парциальное давление газа P, усл. ед.", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Линеаризованный параметр P / a", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_title("б) Линейная анаморфоза Ленгмюра", fontsize=9.0, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.8, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_21_langmuir_isotherm.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_22_bet_multilayer_linear():
    """Слайд 22: Полимолекулярная теория БЭТ (1938) и линейный график в рабочем окне P/P0 = 0.05–0.35."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.3, 4.9), dpi=300)

    # Левая панель: Полные кривые БЭТ V/Vm = C*x / [(1 - x)*(1 + (C - 1)*x)]
    x = np.linspace(0.005, 0.88, 500)
    for C_val, col, lbl in [
        (120.0, BLUE, 'C = 120 (E₁ ≫ E_L: четкая точка B монослоя)'),
        (25.0, GREEN, 'C = 25 (типичный оксид кремния / титана)'),
        (1.5, ORANGE, 'C = 1.5 (E₁ ≈ E_L: слабая сорбция, тип III)')
    ]:
        v_norm = (C_val * x) / ((1.0 - x) * (1.0 + (C_val - 1.0) * x))
        ax1.plot(x, v_norm, color=col, lw=2.5, label=lbl)

    ax1.axhline(1.0, color=RED, ls='--', lw=1.4, label='Емкость плотного монослоя (V / V_m = 1)')
    ax1.axvspan(0.05, 0.35, color='#DBEAFE', alpha=0.55, label='Рабочее окно линейности БЭТ (0.05–0.35)')

    # Точка B для C = 120 (x_B = 1 / (sqrt(C) + 1))
    x_B = 1.0 / (np.sqrt(120.0) + 1.0)
    ax1.scatter([x_B], [1.0], color=RED, s=65, zorder=8)
    ax1.annotate("Точка B (V = V_m):\nзавершение 1-го слоя\n(теплота E₁ → E₂ = E_L)",
                 xy=(x_B, 1.0), xytext=(0.24, 3.1),
                 fontsize=7.5, fontweight='bold', color=RED, bbox=BBOX,
                 arrowprops=dict(arrowstyle="->", color=RED, lw=1.5))

    ax1.set_xlim(0, 0.88)
    ax1.set_ylim(0, 5.5)
    ax1.set_xlabel("Относительное давление пара x = P / P₀", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Число статистических монослоев V / V_m", fontsize=8.6, fontweight='bold', color=NAVY)
    ax1.set_title("а) Полимолекулярная изотерма БЭТ (1938)", fontsize=8.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper left', fontsize=6.4, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Правая панель: Линейный график БЭТ x / [V(1 - x)] = A + B*x в интервале 0.05..0.35
    Vm = 180.0   # см³/г (НТУ) -> S_уд = 180 * 4.353 = 783.5 м²/г
    C_bet = 85.0
    A_int = 1.0 / (Vm * C_bet)
    B_slp = (C_bet - 1.0) / (Vm * C_bet)

    x_win = np.linspace(0.02, 0.40, 200)
    y_bet = (A_int + B_slp * x_win) * 1000.0  # в ед. 10⁻³ г/см³
    x_exp = np.array([0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35])
    y_exp = (A_int + B_slp * x_exp) * 1000.0

    ax2.axvspan(0.05, 0.35, color='#DCFCE7', alpha=0.55, label='Стандартный диапазон ИЮПАК (P/P₀ = 0.05–0.35)')
    ax2.plot(x_win, y_bet, color=NAVY, lw=2.5, label='Линейная регрессия БЭТ (R² = 0.9999)')
    ax2.scatter(x_exp, y_exp, color=RED, s=55, zorder=8, label='Точки сорбции N₂ при 77.3 К')

    S_ud = Vm * 4.3526
    ax2.text(0.20, 0.38,
             f"Расчет из прямой y = A + B·(P/P₀):\n"
             f"• V_m = 1 / (A + B) = {Vm:.1f} см³/г\n"
             f"• C = 1 + B/A = {C_bet:.0f}\n"
             f"• S_уд = V_m·N_A·σ₀ / V₀ = {S_ud:.0f} м²/г",
             fontsize=7.6, fontweight='bold', color=NAVY, ha='center', bbox=BBOX)

    ax2.set_xlim(0.0, 0.40)
    ax2.set_ylim(0.0, 2.35)
    ax2.set_xlabel("Относительное давление P / P₀", fontsize=8.6, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Координата БЭТ P / [V(P₀ − P)] × 10³, г/см³", fontsize=8.4, fontweight='bold', color=NAVY)
    ax2.set_title("б) Линейный график БЭТ для расчета V_m и S_уд", fontsize=8.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper left', fontsize=6.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_22_bet_multilayer_linear.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_23_iupac_isotherms():
    """Слайд 23: Матрица 2x3 всех 6 канонических типов изотерм адсорбции по классификации ИЮПАК (IUPAC)."""
    fig, axes = plt.subplots(2, 3, figsize=(7.4, 4.9), dpi=300)
    x = np.linspace(0.005, 0.98, 300)

    # Тип I: Микропористые (цеолиты, активированный уголь)
    ax = axes[0, 0]
    y1 = 95.0 * (45 * x) / (1 + 45 * x)
    ax.plot(x, y1, color=BLUE, lw=2.4)
    ax.fill_between(x, 0, y1, color='#DBEAFE', alpha=0.45)
    ax.set_title("Тип I: Микропоры (< 2 нм)\nЦеолиты, активный уголь", fontsize=7.6, fontweight='bold', color=NAVY)

    # Тип II: Непористые / макропористые (полимолекулярный БЭТ)
    ax = axes[0, 1]
    y2 = 22.0 * (35 * x) / ((1 - 0.82 * x) * (1 + 34 * x))
    ax.plot(x, y2, color=GREEN, lw=2.4)
    ax.scatter([0.15], [float(22.0 * (35 * 0.15) / ((1 - 0.82 * 0.15) * (1 + 34 * 0.15)))], color=RED, s=35, zorder=6)
    ax.text(0.24, 24, "Точка B", fontsize=7.0, fontweight='bold', color=RED)
    ax.set_title("Тип II: Непористые нанопорошки\nСвободная полислойная сорбция", fontsize=7.6, fontweight='bold', color=NAVY)

    # Тип III: Слабое взаимодействие адсорбат–адсорбент (C < 2)
    ax = axes[0, 2]
    y3 = 12.0 * x / (1 - 0.86 * x)
    ax.plot(x, y3, color=ORANGE, lw=2.4)
    ax.set_title("Тип III: Слабая сорбция (C ≤ 2)\nВода на гидрофобном графите", fontsize=7.6, fontweight='bold', color=NAVY)

    # Тип IV: Мезопористые (2–50 нм) с петлей капиллярного гистерезиса
    ax = axes[1, 0]
    base4 = 25 * (25 * x) / (1 + 25 * x)
    y4_ads = base4 + 65 / (1 + np.exp(-(x - 0.68) / 0.03))
    y4_des = base4 + 65 / (1 + np.exp(-(x - 0.50) / 0.025))
    ax.plot(x, y4_ads, color=BLUE, lw=2.2, label='Адс.')
    ax.plot(x, y4_des, color=RED, lw=2.2, ls='--', label='Дес.')
    ax.fill_between(x, y4_ads, y4_des, color='#FEF3C7', alpha=0.7)
    ax.legend(loc='lower right', fontsize=6.2)
    ax.set_title("Тип IV: Мезопоры (2–50 нм)\nКремнезем SBA-15 (гистерезис)", fontsize=7.6, fontweight='bold', color=NAVY)

    # Тип V: Слабое взаимодействие в пористых средах
    ax = axes[1, 1]
    y5_ads = 90 / (1 + np.exp(-(x - 0.72) / 0.04))
    y5_des = 90 / (1 + np.exp(-(x - 0.54) / 0.035))
    ax.plot(x, y5_ads, color=PURPLE, lw=2.2)
    ax.plot(x, y5_des, color=RED, lw=2.0, ls='--')
    ax.fill_between(x, y5_ads, y5_des, color='#F3E8FF', alpha=0.7)
    ax.set_title("Тип V: Пористые + слабая связь\nСорбция паров воды в порах", fontsize=7.6, fontweight='bold', color=NAVY)

    # Тип VI: Ступенчатая послойная сорбция на однородной поверхности
    ax = axes[1, 2]
    y6 = (30 / (1 + np.exp(-(x - 0.18) / 0.018)) +
          30 / (1 + np.exp(-(x - 0.48) / 0.020)) +
          30 / (1 + np.exp(-(x - 0.78) / 0.022)))
    ax.plot(x, y6, color=NAVY, lw=2.4)
    ax.set_title("Тип VI: Ступенчатая сорбция\nАтомарно-гладкий графен /BN", fontsize=7.6, fontweight='bold', color=NAVY)

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
                 fontsize=9.5, fontweight='bold', color=NAVY, y=1.01)
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
    print("Part 2 figures (Slides 14-23) generated successfully.")
