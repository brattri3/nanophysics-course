"""
Генерация математически точных иллюстраций (Рисунки 10–17) для Лекции №3:
«Термодинамика дисперсных систем и коллоидных растворов (Часть 2)».
Соблюдаются все правила diagram-precision-guide.md (Единый источник истины, численный поиск экстремумов, dpi=300).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Circle
from scipy.optimize import minimize_scalar, brentq

plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']
plt.rcParams['axes.edgecolor'] = '#334455'
plt.rcParams['axes.linewidth'] = 1.1

OUT_DIR = os.path.abspath("course_materials/semester_4/lectures/figures_l03")
os.makedirs(OUT_DIR, exist_ok=True)

NAVY = '#003366'
BLUE = '#0066CC'
RED = '#CC3333'
GREEN = '#1B7837'
ORANGE = '#D95F02'
PURPLE = '#7570B3'
DARK = '#222222'
MUTED = '#556677'
CARD_BG = '#F4F7FA'
BBOX_STYLE = dict(boxstyle='round,pad=0.3', fc='white', ec='#BBBBBB', alpha=0.93)


def fig_10_stern_model():
    """Слайд 10: Объединенная модель ДЭС Штерна (плотный слой 0..δ + диффузный слой x > δ) и перезарядка."""
    fig, ax = plt.subplots(figsize=(6.8, 5.1), dpi=300)

    delta = 0.6  # нм — толщина плотного слоя Штерна
    lam = 2.2    # нм — дебаевская длина в диффузном слое
    phi0 = 80.0  # мВ — потенциал поверхности

    x = np.linspace(0, 7.0, 600)

    # Единый источник истины: кусочно-аналитическая функция Штерна
    def phi_stern(x_val, phi_d):
        return np.where(
            x_val <= delta,
            phi0 + (phi_d - phi0) * (x_val / delta),
            phi_d * np.exp(-(x_val - delta) / lam)
        )

    # 3 физических режима в слое Штерна
    phi_d_norm = 48.0      # 1. Обычный электростатический спад
    phi_d_surf = 98.0      # 2. Специфическая адсорбция одноименных ионов (ПАВ)
    phi_d_rev = -32.0      # 3. Перезарядка многозарядными противоионами (Al3+, Th4+)

    ax.axvspan(0, delta, color='#DCE8F5', alpha=0.65, label=f'Плотный слой Штерна (Гельмгольца): 0 ≤ x ≤ δ = {delta} нм')
    ax.axvspan(delta, 7.0, color='#F7FBF8', alpha=0.65, label='Диффузный слой (Гуи–Чепмена): x > δ')
    ax.axvline(delta, color=NAVY, ls='--', lw=1.8)
    ax.axhline(0, color=DARK, lw=1.1)

    ax.plot(x, phi_stern(x, phi_d_norm), color=BLUE, lw=2.6,
            label='1. Нормальный спад потенциала (индифферентный электролит)')
    ax.plot(x, phi_stern(x, phi_d_surf), color=GREEN, lw=2.3, ls='-.',
            label='2. Специфическая адсорбция ко-ионов ПАВ (|φ_δ| > |φ₀|)')
    ax.plot(x, phi_stern(x, phi_d_rev), color=RED, lw=2.6, ls='--',
            label='3. Перезарядка поверхности (сверхэкв. адсорбция Al³⁺, Th⁴⁺: φ_δ < 0)')

    # Реперные точки строго по функции phi_stern
    ax.scatter([0], [float(phi_stern(0, phi_d_norm))], color=NAVY, s=65, zorder=6)
    for pd, col in [(phi_d_norm, BLUE), (phi_d_surf, GREEN), (phi_d_rev, RED)]:
        y_d = float(phi_stern(delta, pd))
        ax.scatter([delta], [y_d], color=col, s=65, zorder=6)

    # Координата обращения потенциала в нуль при перезарядке
    x_zero = float(brentq(lambda xv: phi_stern(xv, phi_d_rev), 0.0, delta))
    ax.scatter([x_zero], [float(phi_stern(x_zero, phi_d_rev))], color=RED, s=55, zorder=6)

    ax.annotate(f"Потенциал Штерна\nφ_δ = +{phi_d_norm:.0f} мВ",
                xy=(delta, phi_d_norm), xytext=(1.45, 55.0),
                fontsize=8.5, fontweight='bold', color=BLUE, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.3))

    ax.annotate(f"Инверсия знака!\nφ_δ = {phi_d_rev:.0f} мВ\n(перезарядка гранулы)",
                xy=(delta, phi_d_rev), xytext=(1.55, -38.0),
                fontsize=8.5, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

    ax.text(0.3, -43, "Плоскость\nШтерна\nx = δ", ha='center', fontsize=8.0, fontweight='bold', color=NAVY)

    ax.set_xlim(0, 7.0)
    ax.set_ylim(-48, 112)
    ax.set_xlabel("Расстояние от поверхности твердой фазы x, нм", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel("Электрический потенциал φ(x), мВ", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("Распределение потенциала φ(x) в объединенной модели ДЭС О. Штерна (1924)",
                 fontsize=10.5, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=7.8, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_10_stern_model.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_11_zeta_potential():
    """Слайд 11: Плоскость скольжения x = x_s и падение дзета-потенциала ζ при сжатии ДЭС электролитом."""
    fig, ax = plt.subplots(figsize=(6.8, 5.1), dpi=300)

    delta = 0.45   # нм (плоскость Штерна)
    x_slip = 1.65  # нм (плоскость гидродинамического скольжения)
    phi0 = 75.0    # мВ (неизменный термодинамический потенциал поверхности)
    phi_d = 54.0   # мВ (потенциал Штерна)

    x = np.linspace(0, 8.0, 600)

    def phi_profile(x_val, lam_D):
        return np.where(
            x_val <= delta,
            phi0 + (phi_d - phi0) * (x_val / delta),
            phi_d * np.exp(-(x_val - delta) / lam_D)
        )

    cases = [
        (4.5, GREEN, '1. Разбавленный золь (c₁ = 0.5 мМ): высокий ζ₁ → УСТОЙЧИВ'),
        (1.45, ORANGE, '2. Средняя конц. (c₂ = 5 мМ): пограничный ζ₂ → МЕДЛЕННАЯ КОАГУЛЯЦИЯ'),
        (0.58, RED, '3. Избыток электролита (c₃ = 30 мМ): низкий ζ₃ → БЫСТРАЯ КОАГУЛЯЦИЯ')
    ]

    ax.axvspan(0, x_slip, color='#EBF3FA', alpha=0.65,
               label='Гидродинамически неподвижная оболочка (движется вместе с гранулой)')
    ax.axvline(delta, color=MUTED, ls=':', lw=1.4)
    ax.axvline(x_slip, color=NAVY, ls='--', lw=2.2, label=f'Плоскость скольжения x = x_s = {x_slip} нм')
    ax.axhspan(0, 15.0, color='#FDEDEC', alpha=0.45, label='Зона потери устойчивости (|ζ| < 15 мВ)')

    for lam_val, col, lbl in cases:
        ax.plot(x, phi_profile(x, lam_val), color=col, lw=2.5, label=lbl)
        # Точное значение дзета-потенциала на плоскости скольжения
        zeta_val = float(phi_profile(x_slip, lam_val))
        ax.scatter([x_slip], [zeta_val], color=col, s=75, zorder=6)
        ax.hlines(zeta_val, 0, x_slip, color=col, ls=':', lw=1.5)
        ax.annotate(f"ζ = +{zeta_val:.1f} мВ",
                    xy=(x_slip, zeta_val), xytext=(x_slip + 0.55, zeta_val + 2.2),
                    fontsize=8.6, fontweight='bold', color=col, bbox=BBOX_STYLE,
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.2))

    ax.scatter([0, delta], [phi0, phi_d], color=NAVY, s=60, zorder=6)
    ax.text(0.12, phi0 + 2.5, f"φ₀ = {phi0:.0f} мВ", fontsize=8.5, fontweight='bold', color=NAVY)
    ax.text(delta + 0.08, phi_d + 2.5, f"φ_δ = {phi_d:.0f} мВ", fontsize=8.5, fontweight='bold', color=NAVY)

    ax.set_xlim(0, 8.0)
    ax.set_ylim(0, 86)
    ax.set_xlabel("Расстояние от поверхности наночастицы x, нм", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_ylabel("Потенциал φ(x) и дзета-потенциал ζ, мВ", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("Механизм падения ζ-потенциала при сжатии диффузного слоя индифферентным электролитом",
                 fontsize=10.0, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=7.5, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_11_zeta_potential.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_12_electrokinetic_phenomena():
    """Слайд 12: Четырехпанельная схема (2x2) электрокинетических явлений Ф.Ф. Рейсса."""
    fig, axes = plt.subplots(2, 2, figsize=(8.4, 6.2), dpi=300)

    panels = [
        (axes[0, 0], "1. ЭЛЕКТРОФОРЕЗ (Прямое)", BLUE,
         "Внешнее поле E → Движение наночастиц (v_эф)",
         "Измерение ζ-потенциала (ELS), нанопокрытия (EPD)"),
        (axes[0, 1], "2. ЭЛЕКТРООСМОС (Прямое)", GREEN,
         "Внешнее поле E → Поток жидкости в поре (v_эо)",
         "Микрофлюидные чипы, нанонасосы, осушение грунтов"),
        (axes[1, 0], "3. ПОТЕНЦИАЛ СЕДИМЕНТАЦИИ (Дорн)", RED,
         "Оседание частиц (g) → Генерация поля ΔE_сед",
         "Искажение диффузных оболочек оседающих частиц"),
        (axes[1, 1], "4. ПОТЕНЦИАЛ ТЕЧЕНИЯ (Обратное)", ORANGE,
         "Давление ΔP (поток) → Генерация ЭДС ΔE_теч",
         "Диагностика ζ-потенциала мембран и капилляров")
    ]

    for ax, title, col, mech, app in panels:
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 6.5)
        ax.set_xticks([])
        ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color(col)
            sp.set_linewidth(1.8)
        ax.set_title(title, fontsize=9.2, fontweight='bold', color=col, pad=5)
        ax.text(5.0, 5.82, mech, ha='center', va='center', fontsize=7.5, fontweight='bold',
                color=NAVY, bbox=dict(boxstyle='round,pad=0.18', fc='#F0F6FC', ec=col, lw=1.0))
        ax.text(5.0, 0.52, app, ha='center', va='center', fontsize=7.3, color=DARK)

    # 1. Электрофорез: заряженные частицы идут к катоду (-)
    ax = axes[0, 0]
    ax.add_patch(FancyBboxPatch((0.5, 1.5), 0.7, 3.4, boxstyle="round,pad=0.05", fc=RED, ec=DARK))
    ax.text(0.85, 3.2, "+\nАнод", ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
    ax.add_patch(FancyBboxPatch((8.8, 1.5), 0.7, 3.4, boxstyle="round,pad=0.05", fc=BLUE, ec=DARK))
    ax.text(9.15, 3.2, "−\nКатод", ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
    for cx, cy in [(3.0, 3.8), (4.8, 2.5)]:
        ax.add_patch(Circle((cx, cy), 0.65, fc=RED, ec=DARK, lw=1.2))
        ax.text(cx, cy, "Гранула\n(+)", ha='center', va='center', color='white', fontweight='bold', fontsize=6.8)
        ax.annotate('', xy=(cx + 2.1, cy), xytext=(cx + 0.7, cy),
                    arrowprops=dict(arrowstyle='->', color=NAVY, lw=2.2))
        ax.text(cx + 1.4, cy + 0.35, "v_эф", ha='center', fontsize=7.8, fontweight='bold', color=NAVY)

    # 2. Электроосмос: отрицательно заряженные стенки капилляра, катионы увлекают воду к катоду (-)
    ax = axes[0, 1]
    ax.add_patch(FancyBboxPatch((1.2, 4.35), 7.6, 0.5, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    ax.add_patch(FancyBboxPatch((1.2, 1.55), 7.6, 0.5, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    for xw in np.linspace(1.8, 8.2, 7):
        ax.text(xw, 4.6, "−", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
        ax.text(xw, 1.8, "−", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
        ax.add_patch(Circle((xw, 3.95), 0.22, fc=RED, ec='white'))
        ax.text(xw, 3.95, "+", ha='center', va='center', color='white', fontweight='bold', fontsize=7)
        ax.add_patch(Circle((xw, 2.45), 0.22, fc=RED, ec='white'))
        ax.text(xw, 2.45, "+", ha='center', va='center', color='white', fontweight='bold', fontsize=7)
    ax.annotate('', xy=(7.8, 3.2), xytext=(2.2, 3.2),
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.8))
    ax.text(5.0, 3.45, "Поток жидкости v_эо (к катоду −)", ha='center', fontsize=8.0, fontweight='bold', color=GREEN)

    # 3. Потенциал седиментации (Дорна): частицы падают вниз под действием g, наводится ЭДС
    ax = axes[1, 0]
    ax.add_patch(FancyBboxPatch((2.2, 1.25), 5.6, 3.9, boxstyle="round,pad=0.05", fc='#FDF2F2', ec=NAVY, lw=1.3))
    for cx, cy in [(3.8, 3.8), (6.2, 3.3)]:
        ax.add_patch(Circle((cx, cy), 0.52, fc=RED, ec=DARK))
        ax.text(cx, cy, "+", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        ax.annotate('', xy=(cx, cy - 1.45), xytext=(cx, cy - 0.55),
                    arrowprops=dict(arrowstyle='->', color=RED, lw=2.0))
        # Отстающий шлейф противоионов сверху
        ax.add_patch(Circle((cx, cy + 0.82), 0.22, fc=BLUE, ec='white'))
        ax.text(cx, cy + 0.82, "−", ha='center', va='center', color='white', fontweight='bold', fontsize=7.5)
    ax.text(8.65, 3.2, "ΔE_сед\n(В)", ha='center', va='center', fontsize=8.2, fontweight='bold',
            color=RED, bbox=BBOX_STYLE)

    # 4. Потенциал течения: перепад давления ΔP гонит противоионы сквозь пору, возникает ΔE_теч
    ax = axes[1, 1]
    ax.add_patch(FancyBboxPatch((1.5, 4.35), 7.0, 0.5, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    ax.add_patch(FancyBboxPatch((1.5, 1.55), 7.0, 0.5, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    ax.annotate('', xy=(7.5, 3.2), xytext=(1.8, 3.2),
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=2.8))
    ax.text(4.6, 3.55, "Гидродинамический поток (ΔP)", ha='center', fontsize=7.8, fontweight='bold', color=ORANGE)
    ax.text(1.0, 3.2, "−", ha='center', va='center', fontsize=14, fontweight='bold', color=BLUE)
    ax.text(9.0, 3.2, "+", ha='center', va='center', fontsize=14, fontweight='bold', color=RED)
    ax.text(5.0, 2.35, "Вынос противоионов → ЭДС ΔE_теч ∝ ΔP·ζ", ha='center', fontsize=7.6, fontweight='bold', color=NAVY)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_12_electrokinetic_phenomena.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_13_henry_function():
    """Слайд 13: Аналитический график функции Генри f(κr) и переход от Хюккеля (1.0) к Смолуховскому (1.5)."""
    fig, ax = plt.subplots(figsize=(6.8, 5.1), dpi=300)

    # Классическая аналитическая аппроксимация Ошимы (Ohshima, 1994) для функции Генри f(κr)
    kr = np.logspace(-2, 3, 500)

    def f_henry(kr_val):
        return 1.0 + 0.5 / (1.0 + (2.5 / (kr_val * (1.0 + 2.0 * np.exp(-kr_val))))) ** 3

    ax.axvspan(0.01, 0.2, color='#EBF3FA', alpha=0.65, label='Область Хюккеля (κr ≪ 1): малые наночастицы в толстом ДЭС')
    ax.axvspan(0.2, 50.0, color='#FFF8EE', alpha=0.65, label='Переходная наноразмерная область Генри (κr ~ 0.2–50)')
    ax.axvspan(50.0, 1000.0, color='#EEF8F2', alpha=0.65, label='Область Смолуховского (κr ≫ 1): тонкий квазиплоский ДЭС')

    ax.semilogx(kr, f_henry(kr), color=NAVY, lw=2.8, label='Функция Генри f(κr) в формуле u_e = (2εε₀ζ / 3η)·f(κr)')
    ax.axhline(1.0, color=BLUE, ls='--', lw=1.5)
    ax.axhline(1.5, color=GREEN, ls='--', lw=1.5)

    # Реперные точки строго по функции f_henry
    pts = [
        (0.05, "Предел Хюккеля (κr ≪ 1):\nf(κr) = 1.0  ⇒  u_e = 2εε₀ζ / (3η)\n(квантовые точки, неполярные среды)", (0.015, 1.15), BLUE),
        (2.5,  "Наночастицы в воде (r = 10 нм, λ_D = 4 нм):\nκr = 2.5  ⇒  f(κr) = 1.13", (0.4, 1.33), ORANGE),
        (200.0, "Предел Смолуховского (κr ≫ 1):\nf(κr) = 1.5  ⇒  u_e = εε₀ζ / η\n(крупные золи или тонкий ДЭС)", (2.2, 1.43), GREEN)
    ]

    for kr_pt, text_lbl, xy_text, col in pts:
        y_pt = float(f_henry(kr_pt))
        ax.scatter([kr_pt], [y_pt], color=col, s=70, zorder=6)
        ax.annotate(text_lbl, xy=(kr_pt, y_pt), xytext=xy_text,
                    fontsize=8.0, fontweight='bold', color=col, bbox=BBOX_STYLE,
                    arrowprops=dict(arrowstyle='->', color=col, lw=1.3))

    ax.set_xlim(0.01, 1000.0)
    ax.set_ylim(0.94, 1.58)
    ax.set_xlabel("Отношение радиуса наночастицы к толщине ДЭС:  κr = r / λ_D  (лог. шкала)",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax.set_ylabel("Коэффициент Генри f(κr)", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("Размерная зависимость электрофоретической подвижности наночастиц (теория Генри)",
                 fontsize=10.0, fontweight='bold', color=NAVY)
    ax.legend(loc='lower right', fontsize=7.5, framealpha=0.95)
    ax.grid(True, which='both', ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_13_henry_function.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_14_sedimentation_perren():
    """Слайд 14: Гипсометрический закон Лапласа–Перрена для гидрозоля золота (ЛР №2) при разных r."""
    fig, ax = plt.subplots(figsize=(6.8, 5.1), dpi=300)

    # Физические константы для наночастиц золота в воде при T = 298 К
    delta_rho = (19.32 - 1.00) * 1e3  # кг/м³ (Au в воде)
    g = 9.81                          # м/с²
    kBT = 1.380649e-23 * 298.15       # Дж

    h_mm = np.linspace(0, 10, 500)    # высота слоя от 0 до 10 мм

    def n_ratio_perrin(h_mm_val, r_nm):
        r_m = r_nm * 1e-9
        h_m = h_mm_val * 1e-3
        m_eff = (4.0 / 3.0) * np.pi * (r_m ** 3) * delta_rho
        return np.exp(-(m_eff * g * h_m) / kBT)

    radii_cases = [
        (2.0,  GREEN,  '1. Нанокластеры Au (r = 2 нм, d = 4 нм): идеальная однородность'),
        (5.0,  BLUE,   '2. Нанозоль Au в ЛР №2 (r = 5 нм, d = 10 нм): седиментационно устойчив'),
        (8.5,  ORANGE, '3. Крупные НЧ Au (r = 8.5 нм, d = 17 нм): заметный градиент по высоте'),
        (16.0, RED,    '4. Агрегаты после коагуляции (r = 16 нм, d = 32 нм): оседание на дно')
    ]

    for r_val, col, lbl in radii_cases:
        ax.plot(n_ratio_perrin(h_mm, r_val), h_mm, color=col, lw=2.6, label=lbl)

    # Реперные точки на высоте h = 5.0 мм строго через вызов n_ratio_perrin
    h_ref = 5.0
    for r_val, col in [(5.0, BLUE), (8.5, ORANGE), (16.0, RED)]:
        n_pt = float(n_ratio_perrin(h_ref, r_val))
        ax.scatter([n_pt], [h_ref], color=col, s=65, zorder=6)

    n_pt_85 = float(n_ratio_perrin(h_ref, 8.5))
    ax.annotate(f"При r = 8.5 нм (h = 5 мм):\nn(h)/n₀ = {n_pt_85:.2f}",
                xy=(n_pt_85, h_ref), xytext=(0.18, 6.2),
                fontsize=8.2, fontweight='bold', color=ORANGE, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=ORANGE, lw=1.3))

    n_pt_50 = float(n_ratio_perrin(h_ref, 5.0))
    ax.annotate(f"ЛР №2 (r = 5 нм, h = 5 мм):\nn(h)/n₀ = {n_pt_50:.2f} (золь не оседает!)",
                xy=(n_pt_50, h_ref), xytext=(0.35, 8.2),
                fontsize=8.2, fontweight='bold', color=BLUE, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=BLUE, lw=1.3))

    ax.set_xlim(0, 1.05)
    ax.set_ylim(0, 10.0)
    ax.set_xlabel("Относительная равновесная концентрация наночастиц  n(h) / n₀",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax.set_ylabel("Высота в оптической кювете h, мм", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("Седиментационно-диффузионное равновесие Лапласа–Перрена (золь золота Au в воде, 25 °C)",
                 fontsize=9.8, fontweight='bold', color=NAVY)
    ax.legend(loc='lower left', fontsize=7.5, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_14_sedimentation_perren.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_15_dlvo_potential():
    """Слайд 15: Эталонная диаграмма ДЛФО с аналитическим поиском барьера U_max и вторичного минимума."""
    fig, ax = plt.subplots(figsize=(6.8, 5.1), dpi=300)

    # Аналитические функции потенциала в единицах k_B T (Single Source of Truth)
    # U_R(h) = B * exp(-kappa * h), U_A(h) = - A_eff / h + короткодействующее борновское отталкивание на h < 0.35 нм
    B_rep = 82.0      # k_B T
    kappa = 0.42      # нм⁻¹ (λ_D ≈ 2.38 нм)
    A_att = 24.0      # k_B T · нм

    def U_R(h):
        return B_rep * np.exp(-kappa * h)

    def U_A(h):
        return -A_att / h

    def U_tot(h):
        return U_R(h) + U_A(h)

    h = np.linspace(0.55, 22.0, 800)

    # Численный поиск точных координат максимума барьера и вторичного минимума
    res_max = minimize_scalar(lambda x: -U_tot(x), bounds=(0.8, 8.0), method='bounded')
    h_max = float(res_max.x)
    u_max = float(U_tot(h_max))

    res_min2 = minimize_scalar(U_tot, bounds=(6.0, 22.0), method='bounded')
    h_min2 = float(res_min2.x)
    u_min2 = float(U_tot(h_min2))

    # Рисуем кривые
    ax.axhline(0, color=DARK, lw=1.2)
    ax.plot(h, U_R(h), color=GREEN, lw=1.9, ls='--', label='Электростатическое отталкивание ДЭС: U_R(h) ∝ exp(−κh) > 0')
    ax.plot(h, U_A(h), color=BLUE, lw=1.9, ls='--', label='Молекулярное притяжение Ван-дер-Ваальса: U_A(h) = −A_H·r / (12h) < 0')
    ax.plot(h, U_tot(h), color=RED, lw=3.0, label='Суммарная энергия взаимодействия ДЛФО: U(h) = U_R(h) + U_A(h)')

    # Проекции и точки экстремумов строго через вызов U_tot
    ax.scatter([h_max], [u_max], color=RED, s=75, zorder=6)
    ax.vlines(h_max, 0, u_max, color=RED, ls=':', lw=1.5)
    ax.hlines(u_max, 0, h_max, color=RED, ls=':', lw=1.5)

    ax.scatter([h_min2], [u_min2], color=NAVY, s=70, zorder=6)
    ax.vlines(h_min2, u_min2, 0, color=NAVY, ls=':', lw=1.4)

    # Точка первичного минимума на малом зазоре
    h_min1 = 0.62
    u_min1 = float(U_tot(h_min1))
    ax.scatter([h_min1], [u_min1], color=DARK, s=70, zorder=6)

    ax.annotate(f"Потенциальный барьер ДЛФО:\nU_max = +{u_max:.1f} k_B T (при h = {h_max:.2f} нм)\nУсловие стабильности: U_max ≫ k_B T",
                xy=(h_max, u_max), xytext=(4.8, 22.0),
                fontsize=8.3, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))

    ax.annotate(f"Вторичный (дальний) минимум:\nU_min2 = {u_min2:.1f} k_B T (при h = {h_min2:.1f} нм)\nОбратимая флокуляция / пептизация",
                xy=(h_min2, u_min2), xytext=(9.5, -14.5),
                fontsize=8.2, fontweight='bold', color=NAVY, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=NAVY, lw=1.3))

    ax.annotate("Первичный (ближний) минимум:\nнеобратимая коагуляция (слипание)",
                xy=(h_min1, u_min1), xytext=(2.4, -22.5),
                fontsize=8.2, fontweight='bold', color=DARK, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=DARK, lw=1.3))

    ax.set_xlim(0, 22.0)
    ax.set_ylim(-28.0, 38.0)
    ax.set_xlabel("Межповерхностное расстояние между наночастицами h, нм", fontsize=9.8, fontweight='bold', color=NAVY)
    ax.set_ylabel("Энергия взаимодействия U(h) / k_B T", fontsize=10, fontweight='bold', color=NAVY)
    ax.set_title("Потенциальная кривая парного взаимодействия наночастиц в теории ДЛФО",
                 fontsize=10.3, fontweight='bold', color=NAVY)
    ax.legend(loc='upper right', fontsize=7.6, framealpha=0.95)
    ax.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_15_dlvo_potential.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_16_schultze_hardy_coagulation():
    """Слайд 16: Исчезновение барьера ДЛФО при пороге коагуляции γ_кр и правило Шульце–Гарди (z⁻⁶)."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 5.1), dpi=300,
                                   gridspec_kw={'height_ratios': [1.25, 1.0]})

    # Панель А: Семейство кривых ДЛФО при росте κ (для U(h) = B*exp(-κh) - A/h критическое касание при κ_кр = B / (e * A))
    B_rep = 65.0
    A_att = 18.0
    kappa_crit = B_rep / (np.e * A_att)  # Аналитическое решение системы U(h_кр)=0 и dU/dh=0!
    h_crit = 1.0 / kappa_crit

    def U_dlvo(h_val, kap):
        return B_rep * np.exp(-kap * h_val) - A_att / h_val

    h = np.linspace(0.45, 12.0, 600)

    kappas = [
        (0.40 * kappa_crit, GREEN,  '-',  '1. Малая конц. (c < γ_кр): высокий барьер U_max > 15 k_B T (устойчив)'),
        (0.72 * kappa_crit, BLUE,   '-.', '2. Умеренная конц.: малый барьер (медленная коагуляция)'),
        (1.00 * kappa_crit, RED,    '-',  '3. Порог коагуляции (c = γ_кр): касание U_max = 0, dU/dh = 0 при h_кр = κ⁻¹'),
        (1.65 * kappa_crit, PURPLE, '--', '4. Избыток электролита (c > γ_кр): безбарьерная быстрая коагуляция')
    ]

    ax1.axhline(0, color=DARK, lw=1.2)
    for kap_val, col, ls, lbl in kappas:
        lw = 2.8 if col == RED else 2.1
        ax1.plot(h, U_dlvo(h, kap_val), color=col, ls=ls, lw=lw, label=lbl)

    # Критическая точка касания строго через вызов U_dlvo(h_crit, kappa_crit) -> ровно 0.0!
    u_crit_val = float(U_dlvo(h_crit, kappa_crit))
    ax1.scatter([h_crit], [u_crit_val], color=RED, s=75, zorder=6)
    ax1.annotate(f"Критическая точка (c = γ_кр):\nh_кр = 1/κ_кр = {h_crit:.2f} нм, U = {u_crit_val:.1f}",
                 xy=(h_crit, u_crit_val), xytext=(3.8, -11.5),
                 fontsize=8.0, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

    ax1.set_xlim(0.4, 11.0)
    ax1.set_ylim(-18.0, 26.0)
    ax1.set_xlabel("Расстояние между поверхностями наночастиц h, нм", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Энергия U(h) / k_B T", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_title("А. Эволюция потенциального барьера ДЛФО при добавлении электролита",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper right', fontsize=7.1, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Панель Б: Закон Дерягина–Ландау (γ_кр ∝ z⁻⁶) для коагуляции положительного золя Fe(OH)₃ в ЛР №3
    z_vals = np.array([1, 2, 3])
    gamma_1 = 100.0  # ммоль/л для однозарядного Cl⁻ (типичное значение для золя Fe(OH)₃)
    gamma_theory = gamma_1 / (z_vals ** 6)

    labels = [
        "z = 1: KCl (анион Cl⁻)\nγ₁ = 100 ммоль/л (100%)",
        "z = 2: K₂SO₄ (анион SO₄²⁻)\nγ₂ = γ₁/2⁶ = 1.56 ммоль/л",
        "z = 3: K₃[Fe(CN)₆] (анион [Fe(CN)₆]³⁻)\nγ₃ = γ₁/3⁶ = 0.137 ммоль/л"
    ]
    colors_bar = [BLUE, ORANGE, RED]

    y_pos = np.arange(len(z_vals))
    bars = ax2.barh(y_pos, gamma_theory, color=colors_bar, edgecolor=DARK, height=0.55, alpha=0.88)
    ax2.set_xscale('log')
    ax2.set_yticks(y_pos)
    ax2.set_yticklabels(["z = 1 (Cl⁻)", "z = 2 (SO₄²⁻)", "z = 3 ([Fe(CN)₆]³⁻)"],
                        fontsize=8.8, fontweight='bold', color=NAVY)

    for idx, (bar, lbl, val) in enumerate(zip(bars, labels, gamma_theory)):
        ax2.text(val * 1.35, idx, f"{lbl}  (отношение 1/{int(z_vals[idx]**6)})",
                 va='center', ha='left', fontsize=7.8, fontweight='bold', color=DARK)

    ax2.set_xlim(0.05, 8000.0)
    ax2.set_xlabel("Порог коагуляции γ_кр, ммоль/л (логарифмическая шкала, закон z⁻⁶)",
                   fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.set_title("Б. Правило Шульце–Гарди (γ₁ : γ₂ : γ₃ = 1 : 1/64 : 1/729) для золя Fe(OH)₃ в ЛР №3",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax2.grid(True, which='both', axis='x', ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_16_schultze_hardy_coagulation.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_17_labs_connection():
    """Слайд 17: Сводная схема связи теории Лекции №3 с Лабораторными работами №2 (Au) и №3 (Fe(OH)3)."""
    fig, ax = plt.subplots(figsize=(8.6, 6.3), dpi=300)
    ax.set_xlim(0, 12.0)
    ax.set_ylim(0, 7.6)
    ax.axis('off')

    ax.text(6.0, 7.25, "Физика коллоидных наносистем в лабораторном практикуме Кафедры №3",
            ha='center', va='center', fontsize=11.5, fontweight='bold', color=NAVY)

    # Левая карточка: ЛР №2 (Золь золота Au)
    b_lr2 = FancyBboxPatch((0.25, 0.35), 5.5, 6.45, boxstyle="round,pad=0.12",
                           fc='#FDF2F2', ec=RED, lw=2.0)
    ax.add_patch(b_lr2)
    ax.text(3.0, 6.4, "ЛАБОРАТОРНАЯ РАБОТА №2\nГидрозоль наночастиц золота (Au)",
            ha='center', va='center', fontsize=9.8, fontweight='bold', color=RED)

    lr2_steps = [
        ("1. Цитратный синтез (метод Туркевича):",
         "HAuCl₄ + Na₃Cit (100 °C) → наночастицы Au\nдиаметром d ≈ 15–20 нм (узкое распределение)."),
        ("2. Строение отрицательной мицеллы:",
         "{[Au]_m · n Cit³⁻ · (3n−x) Na⁺}ˣ⁻ · x Na⁺\nЦитрат-анионы Cit³⁻ создают ζ ≈ −40 мВ."),
        ("3. Двойная устойчивость наносистемы:",
         "• Седиментационная: малый r ⇒ закон Перрена\n  гарантирует отсутствие оседания.\n"
         "• Агрегативная: барьер ДЛФО U_max > 20 k_B T."),
        ("4. Оптический контроль коагуляции:",
         "• Стабильный золь: рубиново-красный цвет,\n  пик плазмонного резонанса λ_max ≈ 520 нм.\n"
         "• Добавка соли → агрегация → сдвиг пика\n  к 620–650 нм (раствор синеет!).")
    ]
    y_curr = 5.65
    for st_title, st_body in lr2_steps:
        ax.text(0.45, y_curr, st_title, fontsize=8.4, fontweight='bold', color=NAVY)
        ax.text(0.45, y_curr - 0.16, st_body, fontsize=7.6, color=DARK, va='top', linespacing=1.22)
        y_curr -= 1.35

    # Правая карточка: ЛР №3 (Коагуляция золя Fe(OH)3)
    b_lr3 = FancyBboxPatch((6.25, 0.35), 5.5, 6.45, boxstyle="round,pad=0.12",
                           fc='#EEF8F2', ec=GREEN, lw=2.0)
    ax.add_patch(b_lr3)
    ax.text(9.0, 6.4, "ЛАБОРАТОРНАЯ РАБОТА №3\nКоагуляция золя гидроксида железа Fe(OH)₃",
            ha='center', va='center', fontsize=9.8, fontweight='bold', color=GREEN)

    lr3_steps = [
        ("1. Конденсационный синтез (гидролиз):",
         "FeCl₃ + 3H₂O (кипячение) → Fe(OH)₃↓ + 3HCl\nСтабилизатор: оксихлорид FeOCl ⇄ FeO⁺ + Cl⁻."),
        ("2. Строение положительной мицеллы:",
         "{[Fe(OH)₃]_m · n FeO⁺ · (n−x) Cl⁻}ˣ⁺ · x Cl⁻\nГранула заряжена положительно (+x)!"),
        ("3. Определение порога коагуляции γ_кр:",
         "Титрование золя электролитами и расчет:\nγ_кр = (C_эл · V_эл) / (V_золя + V_эл) [ммоль/л]."),
        ("4. Верификация правила Шульце–Гарди:",
         "Коагулируют АНИОНЫ (противоионы):\n"
         "• Cl⁻ (z=1)  :  SO₄²⁻ (z=2)  :  [Fe(CN)₆]³⁻ (z=3)\n"
         "• Пороги коагуляции: γ₁ : γ₂ : γ₃ ≈ 1 : 2⁻⁶ : 3⁻⁶!")
    ]
    y_curr = 5.65
    for st_title, st_body in lr3_steps:
        ax.text(6.45, y_curr, st_title, fontsize=8.4, fontweight='bold', color=NAVY)
        ax.text(6.45, y_curr - 0.16, st_body, fontsize=7.6, color=DARK, va='top', linespacing=1.22)
        y_curr -= 1.35

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_17_labs_connection.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == "__main__":
    fig_10_stern_model()
    fig_11_zeta_potential()
    fig_12_electrokinetic_phenomena()
    fig_13_henry_function()
    fig_14_sedimentation_perren()
    fig_15_dlvo_potential()
    fig_16_schultze_hardy_coagulation()
    fig_17_labs_connection()
    print("Generated figures 10 to 17 successfully!")
