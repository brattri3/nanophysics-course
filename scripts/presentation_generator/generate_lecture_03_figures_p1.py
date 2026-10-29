"""
Генерация математически точных иллюстраций (Рисунки 1–9) для Лекции №3:
«Термодинамика дисперсных систем и коллоидных растворов (Часть 2)».
Соблюдаются все правила diagram-precision-guide.md (Единый источник истины, dpi=300).
"""

import os
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Circle, FancyArrowPatch

# Настройка шрифтов и стиля
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Segoe UI', 'Arial']
plt.rcParams['axes.edgecolor'] = '#334455'
plt.rcParams['axes.linewidth'] = 1.1

OUT_DIR = os.path.abspath("course_materials/semester_4/lectures/figures_l03")
os.makedirs(OUT_DIR, exist_ok=True)

# Цветовая палитра навыка scientific-presentation-creator
NAVY = '#003366'
BLUE = '#0066CC'
RED = '#CC3333'
GREEN = '#1B7837'
ORANGE = '#D95F02'
PURPLE = '#7570B3'
DARK = '#222222'
MUTED = '#556677'
CARD_BG = '#F4F7FA'
BBOX_STYLE = dict(boxstyle='round,pad=0.3', fc='white', ec='#BBBBBB', alpha=0.92)


def fig_01_roadmap():
    """Слайд 1: Маршрутная карта лекции №3 (4 связанных блока)."""
    fig, ax = plt.subplots(figsize=(7.6, 5.6), dpi=300)
    ax.set_xlim(0, 11.2)
    ax.set_ylim(0, 8.0)
    ax.axis('off')

    blocks = [
        (0.3, 5.8, 10.6, 1.55, NAVY, '#EBF3FA',
         "РАЗДЕЛ 1. Слипание наночастиц и коллапс нанопор (Слайды 4–9)",
         "• Скачок S_уд = 3/r, термодинамика Гиббса ΔG = σ·ΔA > 0, критерий Ребиндера\n"
         "• Капиллярное давление Лапласа P_L ~ 200 МПа и схлопывание пор в ксерогель\n"
         "• Сверхкритическая сушка аэрогеля SiO₂ и матричный синтез КТ в цеолитах"),
        (0.3, 3.95, 10.6, 1.55, BLUE, '#F0F6FC',
         "РАЗДЕЛ 2. Потеря заряда и разрушение оболочки мицеллы (Слайды 10–15)",
         "• Правило Панета–Фаянса–Пескова, анатомия мицеллы (ядро, ПОИ, гранула, ПИ)\n"
         "• Конструктор формул золей AgI (перезарядка) и Fe(OH)₃ (гидролиз)\n"
         "• Модели ДЭС (Гельмгольц, Гуи–Чепмен, Штерн) и сжатие оболочки λ_D ∝ 1/(z√c)"),
        (0.3, 2.1, 10.6, 1.55, GREEN, '#EEF8F2',
         "РАЗДЕЛ 3. Слепой контроль и микрофлюидика на чипе (Слайды 16–20)",
         "• Плоскость скольжения, дзета-потенциал ζ, критерий «30 мВ» и ИЭТ\n"
         "• 4 явления Ф.Ф. Рейсса: электрофорез, электроосмос, потенциалы течения и оседания\n"
         "• Уравнение Генри, пределы Хюккеля и Смолуховского, чипы Lab-on-a-Chip"),
        (0.3, 0.25, 10.6, 1.55, RED, '#FDF2F2',
         "РАЗДЕЛ 4. Седиментация, солевой шок и барьер ДЛФО (Слайды 21–26)",
         "• Баланс Перрена (r ≤ 10 нм) и седиментационная устойчивость феррожидкости\n"
         "• Теория ДЛФО: ван-дер-ваальс vs ДЭС, барьер U_max ≥ 15 k_B T, коагуляция\n"
         "• Правило Шульце–Гарди (1/z⁶), кинетика Смолуховского, стерическая защита ПАВ")
    ]

    for (x, y, w, h, border_col, bg_col, title, body) in blocks:
        box = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                             fc=bg_col, ec=border_col, lw=2.0)
        ax.add_patch(box)
        ax.text(x + 0.22, y + h - 0.34, title, fontsize=9.5, fontweight='bold', color=border_col)
        ax.text(x + 0.22, y + 0.14, body, fontsize=8.0, color=DARK, linespacing=1.25)

    # Стрелки между блоками
    for y_top in [5.8, 3.95, 2.1]:
        ax.annotate('', xy=(5.6, y_top - 0.30), xytext=(5.6, y_top),
                    arrowprops=dict(arrowstyle='->', lw=2.2, color=NAVY))

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_01_roadmap.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_02_specific_surface():
    """Слайд 5: Эффект Фарадея–Тиндаля, удельная поверхность S_уд(a) и доля поверхностных атомов."""
    import matplotlib.gridspec as gridspec
    from PIL import Image

    tyndall_path = os.path.join(OUT_DIR, "fig_02_tyndall_effect.jpg")
    fig = plt.figure(figsize=(7.2, 5.2), dpi=300)
    gs = gridspec.GridSpec(2, 2, height_ratios=[1.1, 1.3], hspace=0.35, wspace=0.30)

    # Панель А: Фотография эффекта Фарадея–Тиндаля (лазер в растворе vs нанозоле)
    ax_photo = fig.add_subplot(gs[0, :])
    if os.path.exists(tyndall_path):
        im = Image.open(tyndall_path)
        w, h = im.size
        cropped = im.crop((0, int(h * 0.18), w, int(h * 0.58)))
        ax_photo.imshow(cropped)
    ax_photo.axis('off')
    ax_photo.set_title("А. Эффект Фарадея–Тиндаля: истинный раствор (слева, луч невидим) vs нанозоль (справа, рассеяние)",
                       fontsize=9.2, fontweight='bold', color=NAVY, pad=4)

    # Единый источник истины: аналитические функции
    a_nm = np.logspace(0, 3, 400)  # от 1 нм до 1000 нм
    rho_sio2 = 2.2e6  # г/м³ (диоксид кремния)

    def S_ud_m2_g(a_nm_val, k):
        a_m = a_nm_val * 1e-9
        return k / (rho_sio2 * a_m)

    # Панель Б: Удельная поверхность для сферы (k=6), нанонити (k=4), пленки (k=2)
    ax1 = fig.add_subplot(gs[1, 0])
    ax1.axvspan(1, 100, color='#E6F4EA', alpha=0.7, label='1–100 нм')
    ax1.loglog(a_nm, S_ud_m2_g(a_nm, 6), color=RED, lw=2.2, label='3D (k=6)')
    ax1.loglog(a_nm, S_ud_m2_g(a_nm, 4), color=BLUE, lw=1.8, ls='--', label='1D (k=4)')
    ax1.loglog(a_nm, S_ud_m2_g(a_nm, 2), color=GREEN, lw=1.8, ls='-.', label='2D (k=2)')

    pts_s = [(2.0, 2.5, 1500.0), (10.0, 3.8, 22.0), (100.0, 130.0, 32.0)]
    for a_pt, xt, yt in pts_s:
        s_pt = float(S_ud_m2_g(a_pt, 6))
        ax1.scatter([a_pt], [s_pt], color=RED, s=35, zorder=5)
        ax1.annotate(f"{int(a_pt)} нм:\n{s_pt:.0f} м²/г",
                     xy=(a_pt, s_pt), xytext=(xt, yt),
                     fontsize=7.2, fontweight='bold', color=NAVY, bbox=BBOX_STYLE,
                     arrowprops=dict(arrowstyle='->', color=RED, lw=0.8))

    ax1.set_xlabel("Размер a, нм", fontsize=8.5, fontweight='bold', color=NAVY)
    ax1.set_ylabel("S_уд, м²/г (SiO₂)", fontsize=8.5, fontweight='bold', color=NAVY)
    ax1.set_title("Б. Скачок S_уд = k / (ρ·a)", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.grid(True, which='both', ls=':', alpha=0.5)
    ax1.legend(loc='upper right', fontsize=7.2, framealpha=0.95)

    # Панель В: Доля поверхностных атомов в сферической наночастице золота (d_at = 0.288 нм)
    ax2 = fig.add_subplot(gs[1, 1])
    d_at = 0.288

    def frac_surface_atoms(a_nm_val):
        r = a_nm_val / 2.0
        ratio = 1.0 - np.maximum(0.0, (r - d_at) / r) ** 3
        return ratio * 100.0

    ax2.axvspan(1, 100, color='#E6F4EA', alpha=0.7)
    ax2.plot(a_nm, frac_surface_atoms(a_nm), color=NAVY, lw=2.2, label='N_s / N_tot (%)')

    for a_pt, x_off, y_off in [(2.0, 2.8, 72), (5.0, 7.5, 42), (20.0, 28.0, 22)]:
        f_pt = float(frac_surface_atoms(a_pt))
        ax2.scatter([a_pt], [f_pt], color=RED, s=35, zorder=5)
        ax2.annotate(f"d = {int(a_pt)} нм: {f_pt:.1f}%",
                     xy=(a_pt, f_pt), xytext=(x_off, y_off),
                     fontsize=7.5, fontweight='bold', color=DARK, bbox=BBOX_STYLE,
                     arrowprops=dict(arrowstyle='->', color=NAVY, lw=0.8))

    ax2.set_xscale('log')
    ax2.set_ylim(0, 100)
    ax2.set_xlabel("Диаметр d, нм", fontsize=8.5, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Поверхностные атомы, %", fontsize=8.5, fontweight='bold', color=NAVY)
    ax2.set_title("В. Доля поверхностных атомов Au", fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.grid(True, which='both', ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_02_specific_surface.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_03_classification_matrix():
    """Слайд 3: Матрица 3x3 классификации дисперсных систем по агрегатному состоянию ДФ и ДС."""
    fig, ax = plt.subplots(figsize=(8.4, 6.2), dpi=300)
    ax.set_xlim(0, 12.2)
    ax.set_ylim(0, 8.2)
    ax.axis('off')

    ax.text(6.1, 7.85, "Матрица классов дисперсных систем (ДФ × ДС) и наноматериалы",
            ha='center', va='center', fontsize=12.0, fontweight='bold', color=NAVY)

    cols = ["ДС: Газ (Г)", "ДС: Жидкость (Ж)", "ДС: Твердое тело (Т)"]
    rows = ["ДФ:\nГаз (Г)", "ДФ:\nЖидкость (Ж)", "ДФ:\nТвердое (Т)"]

    cells = [
        # Row 0: DF = Gas
        [("Г / Г (Гомогенная смесь)", "• Не образует гетерогенной\n  дисперсной системы\n• Полная смешиваемость газов", '#EEEEEE', MUTED),
         ("Г / Ж: Газовые эмульсии и пены", "• Микропузырьки в жидкости\n• Нанопены и флотационные\n  дисперсные системы", '#F0F6FC', BLUE),
         ("Г / Т: Пористые тела и ксерогели", "• Аэрогели SiO₂ (до 99% пор)\n• Цеолиты, силикагель\n• Нанопористый Si и анодный Al₂O₃", '#EEF8F2', GREEN)],
        # Row 1: DF = Liquid
        [("Ж / Г: Аэрозоли (туманы)", "• Облака, спреи, туманы\n• Капельный CVD-аэрозоль\n  прекурсоров", '#F0F6FC', BLUE),
         ("Ж / Ж: Эмульсии (прямые/обр.)", "• Микроэмульсии «вода в масле»\n• Обратные мицеллы как\n  нанореакторы синтеза НЧ", '#FFF8EE', ORANGE),
         ("Ж / Т: Гели и капиллярные с-мы", "• Гидрогели, студни\n• Жидкость в нанокапиллярах\n  и трековых мембранах", '#F0F6FC', BLUE)],
        # Row 2: DF = Solid
        [("Т / Г: Аэрозоли (дымы, порошки)", "• Нанопорошки оксидов (ZnO)\n• Газофазный синтез и\n  лазерная абляция", '#F0F6FC', BLUE),
         ("Т / Ж: Золи (гидрозоли) и суспензии", "• Плазмонные золи Ag и Au\n• Гидрозоли Fe(OH)₃ и AgI\n• Коллоидные квантовые точки", '#FDF2F2', RED),
         ("Т / Т: Твердые золи и композиты", "• Рубиновое стекло (НЧ Au в SiO₂)\n• Дисперсно-упрочненные сплавы\n• Квантовые точки в матрице", '#EEF8F2', GREEN)]
    ]

    x0, y0 = 1.65, 0.25
    cw, ch = 3.32, 2.20

    for c_idx, c_title in enumerate(cols):
        ax.text(x0 + c_idx * (cw + 0.14) + cw / 2, 7.25, c_title,
                ha='center', va='center', fontsize=10.0, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle='round,pad=0.25', fc='#DCE8F5', ec=NAVY, lw=1.2))

    for r_idx, r_title in enumerate(rows):
        ry = y0 + (2 - r_idx) * (ch + 0.15)
        ax.text(0.78, ry + ch / 2, r_title,
                ha='center', va='center', fontsize=9.5, fontweight='bold', color=NAVY,
                bbox=dict(boxstyle='round,pad=0.25', fc='#DCE8F5', ec=NAVY, lw=1.2))
        for c_idx in range(3):
            cx = x0 + c_idx * (cw + 0.14)
            head, desc, bg, ec = cells[r_idx][c_idx]
            rect = FancyBboxPatch((cx, ry), cw, ch, boxstyle="round,pad=0.06",
                                  fc=bg, ec=ec, lw=1.6)
            ax.add_patch(rect)
            ax.text(cx + cw / 2, ry + ch - 0.32, head, ha='center', va='center',
                    fontsize=8.2, fontweight='bold', color=ec if ec != MUTED else DARK)
            ax.text(cx + 0.14, ry + 0.22, desc, ha='left', va='bottom',
                    fontsize=7.8, color=DARK, linespacing=1.28)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_03_classification_matrix.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_04_sol_gel_xerogel():
    """Слайд 4: Полноширинная многопанельная схема Золь -> Гель -> Ксерогель / Аэрогель."""
    fig, axes = plt.subplots(1, 4, figsize=(12.1, 3.6), dpi=300)

    titles = [
        "1. ЗОЛЬ (Лиозоль)\nСвободнодисперсная система",
        "2. МОКРЫЙ ГЕЛЬ (Лиогель)\nПерколяционная 3D-сетка",
        "3А. КСЕРОГЕЛЬ (Обычная сушка)\nСжатие капиллярным давлением P_L",
        "3Б. АЭРОГЕЛЬ (Сверхкрит. сушка)\nСохранение 95–99% нанопор"
    ]
    border_colors = [BLUE, NAVY, RED, GREEN]

    np.random.seed(42)

    for idx, ax in enumerate(axes):
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 10)
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_color(border_colors[idx])
            spine.set_linewidth(2.0)
        ax.set_title(titles[idx], fontsize=9.8, fontweight='bold', color=border_colors[idx], pad=8)

    # Панель 1: Золь (свободные частицы с векторами броуновского движения)
    axes[0].set_facecolor('#EBF5FB')
    sol_pts = [(2.2, 7.5), (5.5, 8.0), (8.0, 6.8), (3.0, 4.8), (6.5, 4.5), (2.5, 2.2), (7.5, 2.3), (4.8, 6.2)]
    vecs = [(0.9, 0.6), (-0.8, 0.5), (-0.6, -0.9), (0.9, -0.5), (-0.7, 0.8), (0.8, 0.7), (-0.9, 0.4), (0.5, -0.9)]
    for (x, y), (dx, dy) in zip(sol_pts, vecs):
        c = Circle((x, y), 0.58, fc=BLUE, ec=NAVY, lw=1.4, zorder=4)
        axes[0].add_patch(c)
        axes[0].annotate('', xy=(x + dx * 1.2, y + dy * 1.2), xytext=(x, y),
                         arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))
    axes[0].text(5.0, 0.7, "Броуновское движение\nТекучая жидкость (η ≈ η₀)", ha='center', fontsize=8.3,
                 fontweight='bold', color=NAVY, bbox=BBOX_STYLE)

    # Панель 2: Гель (связный каркас в жидкости)
    axes[1].set_facecolor('#EBF5FB')
    gel_nodes = [(1.5, 8.2), (3.5, 7.8), (5.8, 8.1), (8.2, 7.9),
                 (2.2, 5.8), (4.6, 5.9), (7.0, 5.7), (8.5, 5.5),
                 (1.8, 3.6), (4.0, 3.8), (6.2, 3.5), (8.0, 3.2),
                 (2.8, 1.8), (5.2, 2.0), (7.3, 1.9)]
    edges = [(0, 1), (1, 2), (2, 3), (0, 4), (1, 5), (2, 6), (3, 7),
             (4, 5), (5, 6), (6, 7), (4, 8), (5, 9), (6, 10), (7, 11),
             (8, 9), (9, 10), (10, 11), (8, 12), (9, 13), (10, 14), (12, 13), (13, 14)]
    for i, j in edges:
        axes[1].plot([gel_nodes[i][0], gel_nodes[j][0]], [gel_nodes[i][1], gel_nodes[j][1]],
                     color=NAVY, lw=3.0, zorder=3)
    for (x, y) in gel_nodes:
        axes[1].add_patch(Circle((x, y), 0.48, fc=BLUE, ec=NAVY, lw=1.3, zorder=4))
    axes[1].text(5.0, 0.65, "Потеря текучести (точка геля)\nЖидкость внутри ячеек 3D-сетки", ha='center',
                 fontsize=8.3, fontweight='bold', color=NAVY, bbox=BBOX_STYLE)

    # Панель 3А: Ксерогель (сжатый каркас в центре, стрелки Лапласова сжатия)
    axes[2].set_facecolor('#FDEDEC')
    for (x, y) in gel_nodes:
        xs = 5.0 + (x - 5.0) * 0.46
        ys = 4.9 + (y - 5.0) * 0.46
        axes[2].add_patch(Circle((xs, ys), 0.46, fc=RED, ec='#660000', lw=1.2, zorder=4))
    for i, j in edges:
        x1, y1 = 5.0 + (gel_nodes[i][0] - 5.0) * 0.46, 4.9 + (gel_nodes[i][1] - 5.0) * 0.46
        x2, y2 = 5.0 + (gel_nodes[j][0] - 5.0) * 0.46, 4.9 + (gel_nodes[j][1] - 5.0) * 0.46
        axes[2].plot([x1, x2], [y1, y2], color='#880000', lw=2.8, zorder=3)
    # Стрелки сжатия
    for (ax_x, ax_y, dx, dy) in [(1.5, 5.0, 1.5, 0), (8.5, 5.0, -1.5, 0), (5.0, 8.8, 0, -1.3)]:
        axes[2].annotate('', xy=(ax_x + dx, ax_y + dy), xytext=(ax_x, ax_y),
                         arrowprops=dict(arrowstyle='->', color=RED, lw=2.2))
    axes[2].text(5.0, 8.95, "P_L = 2σ·cosθ / r_пор ≫ 10 МПа", ha='center', fontsize=8.3,
                 fontweight='bold', color=RED, bbox=BBOX_STYLE)
    axes[2].text(5.0, 0.65, "Усадка объема в 5–10 раз\nСиликагель, алюмогель", ha='center',
                 fontsize=8.3, fontweight='bold', color=DARK, bbox=BBOX_STYLE)

    # Панель 3Б: Аэрогель (сохраненный каркас на воздухе/газе, σ = 0)
    axes[3].set_facecolor('#F4FBF7')
    for i, j in edges:
        axes[3].plot([gel_nodes[i][0], gel_nodes[j][0]], [gel_nodes[i][1], gel_nodes[j][1]],
                     color=GREEN, lw=2.8, zorder=3)
    for (x, y) in gel_nodes:
        axes[3].add_patch(Circle((x, y), 0.46, fc='#2ECC71', ec=GREEN, lw=1.3, zorder=4))
    axes[3].text(5.0, 8.95, "T > T_кр, P > P_кр  ⇒  σ = 0, P_L = 0", ha='center', fontsize=8.3,
                 fontweight='bold', color=GREEN, bbox=BBOX_STYLE)
    axes[3].text(5.0, 0.65, "Нулевая усадка каркаса!\nρ ≈ 0.003–0.1 г/см³ (рекордная теплоизоляция)", ha='center',
                 fontsize=8.2, fontweight='bold', color=DARK, bbox=BBOX_STYLE)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_04_sol_gel_xerogel.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_05_zeolites():
    """Слайд 5: Цеолиты — кристаллическая решетка и селективный эффект молекулярного сита."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 5.1), dpi=300,
                                   gridspec_kw={'height_ratios': [1.15, 1.0]})

    # Панель А: Иерархия сборки цеолита и молекулярное сито
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 4.8)
    ax1.axis('off')
    ax1.set_title("А. Архитектура алюмосиликатного каркаса цеолита и эффект молекулярного сита",
                  fontsize=10.2, fontweight='bold', color=NAVY)

    # Блок 1: Первичные тетраэдры
    b1 = FancyBboxPatch((0.2, 0.5), 2.6, 3.8, boxstyle="round,pad=0.1", fc=CARD_BG, ec=NAVY, lw=1.5)
    ax1.add_patch(b1)
    ax1.text(1.5, 3.9, "1. Тетраэдры\n[SiO₄]⁴⁻ и [AlO₄]⁵⁻", ha='center', va='center',
             fontsize=8.8, fontweight='bold', color=NAVY)
    # Рисуем тетраэдр
    tri_x = [1.5, 0.8, 2.2, 1.5]
    tri_y = [3.1, 1.7, 1.7, 3.1]
    ax1.plot(tri_x, tri_y, color=BLUE, lw=1.8)
    for vx, vy in [(1.5, 3.1), (0.8, 1.7), (2.2, 1.7), (1.5, 2.25)]:
        ax1.plot([1.5, vx], [2.25, vy], color=NAVY, lw=1.3, ls='--')
        ax1.add_patch(Circle((vx, vy), 0.16, fc=RED if (vx, vy) != (1.5, 2.25) else BLUE, ec=DARK, zorder=5))
    ax1.text(1.5, 0.95, "Замещение Si⁴⁺ → Al³⁺\nдает заряд −1 (катион Na⁺)", ha='center', fontsize=7.6, color=DARK)

    ax1.annotate('', xy=(3.3, 2.4), xytext=(2.85, 2.4), arrowprops=dict(arrowstyle='->', lw=2.0, color=NAVY))

    # Блок 2: Полость цеолита с окном d_0 = 0.45 нм
    b2 = FancyBboxPatch((3.35, 0.5), 6.45, 3.8, boxstyle="round,pad=0.1", fc='#F4FBF7', ec=GREEN, lw=1.5)
    ax1.add_patch(b2)
    ax1.text(6.55, 4.02, "2. Селективное окно цеолита (d_окна = 0.45 нм)",
             ha='center', va='center', fontsize=8.3, fontweight='bold', color=GREEN)

    # Стенки входного окна цеолита
    ax1.add_patch(FancyBboxPatch((6.1, 2.85), 0.7, 0.65, boxstyle="round,pad=0.04", fc=NAVY, ec=DARK))
    ax1.add_patch(FancyBboxPatch((6.1, 0.65), 0.7, 0.65, boxstyle="round,pad=0.04", fc=NAVY, ec=DARK))
    ax1.annotate('', xy=(6.45, 2.8), xytext=(6.45, 1.35),
                 arrowprops=dict(arrowstyle='<->', color=RED, lw=1.6))
    ax1.text(6.45, 3.68, "0.45 нм", ha='center', fontsize=7.6, fontweight='bold', color=RED)

    # Полость справа (альфа-клетка с темплатным нанокластером)
    cavity = Circle((8.55, 2.1), 1.10, fc='#EBF5FB', ec=BLUE, lw=2.0, ls='--')
    ax1.add_patch(cavity)
    ax1.text(8.55, 2.1, "α-полость\n(d ≈ 1.14 нм)\nНанореактор\nкластера CdS", ha='center', va='center',
             fontsize=7.5, fontweight='bold', color=NAVY)

    # Линейная молекула (проходит)
    ax1.add_patch(FancyBboxPatch((3.55, 2.22), 1.85, 0.34, boxstyle="round,pad=0.05", fc='#2ECC71', ec=GREEN, lw=1.3))
    ax1.text(4.47, 2.39, "н-алкан (0.43 нм)", ha='center', va='center', fontsize=7.4, fontweight='bold', color='white')
    ax1.annotate('', xy=(7.35, 2.39), xytext=(5.45, 2.39), arrowprops=dict(arrowstyle='->', color=GREEN, lw=2.2))

    # Разветвленная молекула (блокируется)
    ax1.add_patch(FancyBboxPatch((3.60, 0.95), 1.75, 0.80, boxstyle="round,pad=0.05", fc='#E74C3C', ec=RED, lw=1.3))
    ax1.text(4.47, 1.35, "изо-алкан\n(0.56 нм > d)", ha='center', va='center', fontsize=7.2, fontweight='bold', color='white')
    ax1.text(5.75, 1.35, "✖", ha='center', va='center', fontsize=14, fontweight='bold', color=RED)

    # Панель Б: Сравнение распределения пор по размерам (Цеолит vs Ксерогель)
    d_grid = np.linspace(0.2, 4.5, 500)

    def pore_dist_zeolite(d):
        return 1.0 * np.exp(-((d - 0.45) / 0.045) ** 2) + 0.75 * np.exp(-((d - 0.74) / 0.055) ** 2)

    def pore_dist_xerogel(d):
        return 0.48 * np.exp(-((d - 2.3) / 0.95) ** 2)

    ax2.plot(d_grid, pore_dist_zeolite(d_grid), color=GREEN, lw=2.4,
             label='Кристаллические цеолиты (строго калиброванные микропоры: 0.45 нм — 4A, 0.74 нм — X/Y)')
    ax2.fill_between(d_grid, 0, pore_dist_zeolite(d_grid), color=GREEN, alpha=0.2)

    ax2.plot(d_grid, pore_dist_xerogel(d_grid), color=ORANGE, lw=2.2, ls='--',
             label='Аморфный ксерогель SiO₂ (широкое распределение пор)')
    ax2.fill_between(d_grid, 0, pore_dist_xerogel(d_grid), color=ORANGE, alpha=0.15)

    ax2.axvline(2.0, color=RED, ls=':', lw=1.5)
    ax2.text(2.05, 0.56, "Граница ИЮПАК:\n← Микропоры (< 2 нм) | Мезопоры (2–50 нм) →",
             fontsize=7.6, fontweight='bold', color=RED)

    ax2.set_xlabel("Диаметр входных окон и пор d_пор, нм", fontsize=9.5, fontweight='bold', color=NAVY)
    ax2.set_ylabel("dV / dd (отн. ед.)", fontsize=9.5, fontweight='bold', color=NAVY)
    ax2.set_title("Б. Монодисперсность каналов цеолитов по сравнению с аморфными сорбентами",
                  fontsize=10.0, fontweight='bold', color=NAVY)
    ax2.set_ylim(0, 1.32)
    ax2.legend(loc='upper right', fontsize=7.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_05_zeolites.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_06_micelle_anatomy():
    """Слайд 6: Концентрическая анатомия коллоидной мицеллы и иерархия ее структурных единиц."""
    fig, ax = plt.subplots(figsize=(7.6, 5.7), dpi=300)
    ax.set_xlim(-6.5, 6.5)
    ax.set_ylim(-5.6, 4.6)
    ax.set_aspect('equal')
    ax.axis('off')

    ax.text(0, 4.3, "Иерархическое строение коллоидной мицеллы лиофобного золя",
            ha='center', va='center', fontsize=11.0, fontweight='bold', color=NAVY)

    # Концентрические оболочки (сверху вниз по радиусу: от внешней мицеллы к ядру)
    radii = [
        (3.8, '#F2F7FC', BLUE, '--', 1.8),    # Граница мицеллы (диффузный слой)
        (2.55, '#E2EEF8', RED, '-', 2.2),     # Плоскость скольжения (граница гранулы)
        (1.85, '#FADBD8', ORANGE, ':', 1.6),  # Слой ПОИ (граница ядра)
        (1.25, '#85C1E9', NAVY, '-', 2.0)     # Агрегат [M]_m
    ]
    for r, fc, ec, ls, lw in radii:
        ax.add_patch(Circle((0, 0.3), r, fc=fc, ec=ec, ls=ls, lw=lw))

    # Текст в центре агрегата
    ax.text(0, 0.3, "Агрегат\n[M]_m\n(m ~ 10³–10⁶)", ha='center', va='center',
            fontsize=8.5, fontweight='bold', color=NAVY)

    # Потенциалопределяющие ионы (ПОИ, +) на радиусе 1.55
    for ang in np.linspace(0, 2 * np.pi, 12, endpoint=False):
        px, py = 1.55 * np.cos(ang), 0.3 + 1.55 * np.sin(ang)
        ax.add_patch(Circle((px, py), 0.21, fc=RED, ec='white', lw=0.8, zorder=5))
        ax.text(px, py, "+", ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=6)

    # Противоионы плотного слоя Штерна (n - x, -) на радиусе 2.2
    for ang in np.linspace(0.25, 2 * np.pi + 0.25, 8, endpoint=False):
        px, py = 2.20 * np.cos(ang), 0.3 + 2.20 * np.sin(ang)
        ax.add_patch(Circle((px, py), 0.19, fc=BLUE, ec='white', lw=0.8, zorder=5))
        ax.text(px, py, "−", ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=6)

    # Противоионы диффузного слоя (x, -) на радиусах 2.9–3.45
    diff_angles = [0.4, 1.2, 2.1, 3.0, 3.9, 4.7, 5.5]
    diff_r = [3.1, 3.35, 2.95, 3.4, 3.05, 3.3, 2.95]
    for ang, dr in zip(diff_angles, diff_r):
        px, py = dr * np.cos(ang), 0.3 + dr * np.sin(ang)
        ax.add_patch(Circle((px, py), 0.19, fc=GREEN, ec='white', lw=0.8, zorder=5))
        ax.text(px, py, "−", ha='center', va='center', fontsize=8.5, fontweight='bold', color='white', zorder=6)

    # Выноски справа и слева
    ax.annotate("Ядро мицеллы:\nАгрегат + n ПОИ (+)", xy=(1.55, 0.3), xytext=(3.1, 3.1),
                fontsize=8.2, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))

    ax.annotate("Плоскость скольжения\n(граница ГРАНУЛЫ, заряд +x)", xy=(-2.55, 0.3), xytext=(-6.2, 3.0),
                fontsize=8.2, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=RED, lw=1.4))

    ax.annotate("Диффузный слой:\nx противоионов (−)", xy=(2.9, -1.3), xytext=(3.0, -3.1),
                fontsize=8.2, fontweight='bold', color=GREEN, bbox=BBOX_STYLE,
                arrowprops=dict(arrowstyle='->', color=GREEN, lw=1.4))

    # Нижняя плашка с формулой и скобками уровней
    formula_box = FancyBboxPatch((-6.2, -5.45), 12.4, 1.75, boxstyle="round,pad=0.1",
                                 fc='#F8FAFC', ec=NAVY, lw=1.5)
    ax.add_patch(formula_box)
    ax.text(0, -4.15, "Общая структура мицеллы:   { [M]_m  ·  n ПОИ⁺  ·  (n − x) ПИ⁻ }ˣ⁺   ·   x ПИ⁻",
            ha='center', va='center', fontsize=9.2, fontweight='bold', color=NAVY)
    ax.text(0, -4.90,
            "Агрегат: [M]_m   ⊂   Ядро: [M]_m·nПОИ⁺   ⊂   Гранула (заряд +x)   ⊂   Мицелла (заряд = 0)",
            ha='center', va='center', fontsize=8.1, fontweight='bold', color=DARK)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_06_micelle_anatomy.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_07_agi_feoh3_micelles():
    """Слайд 7: Сравнение отрицательной мицеллы AgI (в избытке KI) и положительной мицеллы Fe(OH)3."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 5.1), dpi=300)

    panels = [
        (ax1, "А. Отрицательный золь AgI\n(в избытке стабилизатора KI)",
         BLUE, '#EBF5FB', "[AgI]_m\n(желтый золь)", '#F7DC6F',
         "I⁻", BLUE, "K⁺", RED,
         "{[AgI]_m · n I⁻ · (n−x) K⁺}ˣ⁻ · x K⁺",
         "• ПОИ: анионы I⁻ (достраивают решетку)\n• Противоионы: катионы K⁺\n• Гранула движется к АНОДУ (+)"),
        (ax2, "Б. Положительный золь Fe(OH)₃\n(гидролиз FeCl₃ в кипящей воде)",
         RED, '#FDEDEC', "[Fe(OH)₃]_m\n(винно-красный)", '#C0392B',
         "FeO⁺", RED, "Cl⁻", BLUE,
         "{[Fe(OH)₃]_m · n FeO⁺ · (n−x) Cl⁻}ˣ⁺ · x Cl⁻",
         "• ПОИ: катионы FeO⁺ (из стабилизатора FeOCl)\n• Противоионы: анионы Cl⁻\n• Коагулируется анионами (Cl⁻, SO₄²⁻, [Fe(CN)₆]³⁻)")
    ]

    for (ax, title, main_col, bg_col, core_txt, core_fc, poi_lbl, poi_col, pi_lbl, pi_col, formula, notes) in panels:
        ax.set_xlim(-3.5, 3.5)
        ax.set_ylim(-4.6, 3.6)
        ax.set_aspect('equal')
        ax.axis('off')
        ax.set_title(title, fontsize=9.5, fontweight='bold', color=main_col, pad=6)

        # Оболочки
        ax.add_patch(Circle((0, 0.4), 2.85, fc=bg_col, ec=main_col, ls='--', lw=1.6))
        ax.add_patch(Circle((0, 0.4), 2.05, fc='white', ec=main_col, ls='-', lw=2.0))
        ax.add_patch(Circle((0, 0.4), 1.15, fc=core_fc, ec=DARK, lw=1.6))

        txt_col = 'white' if core_fc == '#C0392B' else DARK
        ax.text(0, 0.4, core_txt, ha='center', va='center', fontsize=8.0, fontweight='bold', color=txt_col)

        # ПОИ на границе агрегата
        for ang in np.linspace(0, 2 * np.pi, 8, endpoint=False):
            px, py = 1.42 * np.cos(ang), 0.4 + 1.42 * np.sin(ang)
            ax.add_patch(Circle((px, py), 0.25, fc=poi_col, ec='white', lw=0.8, zorder=5))
            ax.text(px, py, poi_lbl, ha='center', va='center', fontsize=6.2, fontweight='bold', color='white', zorder=6)

        # Противоионы в плотном и диффузном слоях
        for ang, rad in zip(np.linspace(0.35, 2 * np.pi + 0.35, 6, endpoint=False), [1.82, 2.45, 1.82, 2.45, 1.82, 2.45]):
            px, py = rad * np.cos(ang), 0.4 + rad * np.sin(ang)
            ax.add_patch(Circle((px, py), 0.23, fc=pi_col, ec='white', lw=0.8, zorder=5))
            ax.text(px, py, pi_lbl, ha='center', va='center', fontsize=6.5, fontweight='bold', color='white', zorder=6)

        # Карточка внизу
        card = FancyBboxPatch((-3.35, -4.45), 6.7, 1.7, boxstyle="round,pad=0.08",
                              fc=CARD_BG, ec=main_col, lw=1.4)
        ax.add_patch(card)
        ax.text(0, -3.0, formula, ha='center', va='center', fontsize=7.8, fontweight='bold', color=NAVY)
        ax.text(-3.2, -4.3, notes, ha='left', va='bottom', fontsize=7.3, color=DARK, linespacing=1.25)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_07_agi_feoh3_micelles.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_08_helmholtz_vs_gouy():
    """Слайд 8: Сопоставление моделей ДЭС Гельмгольца (конденсатор) и Гуи–Чепмена (диффузный слой)."""
    fig, (ax_top, ax_bot) = plt.subplots(2, 1, figsize=(6.8, 5.1), dpi=300,
                                         gridspec_kw={'height_ratios': [1.0, 1.35]})

    # Верхняя панель: Расположение ионов
    ax_top.set_xlim(0, 10)
    ax_top.set_ylim(0, 3.6)
    ax_top.axis('off')
    ax_top.set_title("А. Пространственное распределение противоионов у заряженной поверхности",
                     fontsize=10.0, fontweight='bold', color=NAVY)

    # Левая половина: Гельмгольц
    ax_top.add_patch(FancyBboxPatch((0.2, 0.2), 4.5, 3.0, boxstyle="round,pad=0.06", fc='#F8F9FA', ec=BLUE, lw=1.4))
    ax_top.add_patch(FancyBboxPatch((0.2, 0.2), 0.45, 3.0, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    ax_top.text(2.6, 2.85, "1. Модель Гельмгольца (1879)", ha='center', fontsize=8.8, fontweight='bold', color=BLUE)
    for y_pos in np.linspace(0.55, 2.45, 5):
        ax_top.text(0.42, y_pos, "+", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
        ax_top.add_patch(Circle((1.35, y_pos), 0.18, fc=BLUE, ec='white'))
        ax_top.text(1.35, y_pos, "−", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    ax_top.axvline(1.35, ymin=0.08, ymax=0.82, color=BLUE, ls='--', lw=1.2)
    ax_top.text(3.0, 1.4, "Жесткая плоскость x = d\n(плоский конденсатор,\nтепловое движение\nне учитывается)",
                ha='center', va='center', fontsize=7.8, color=DARK)

    # Правая половина: Гуи-Чепмен
    ax_top.add_patch(FancyBboxPatch((5.2, 0.2), 4.6, 3.0, boxstyle="round,pad=0.06", fc='#F8F9FA', ec=RED, lw=1.4))
    ax_top.add_patch(FancyBboxPatch((5.2, 0.2), 0.45, 3.0, boxstyle="square,pad=0", fc=NAVY, ec=DARK))
    ax_top.text(7.6, 2.85, "2. Модель Гуи–Чепмена (1910–1913)", ha='center', fontsize=8.8, fontweight='bold', color=RED)
    for y_pos in np.linspace(0.55, 2.45, 5):
        ax_top.text(5.42, y_pos, "+", ha='center', va='center', color='white', fontweight='bold', fontsize=9)
    diff_ions = [(6.0, 2.3), (6.1, 1.5), (5.95, 0.8), (6.5, 2.0), (6.6, 1.1),
                 (7.2, 2.2), (7.4, 0.9), (8.1, 1.6), (8.9, 1.2)]
    for ix, iy in diff_ions:
        ax_top.add_patch(Circle((ix, iy), 0.17, fc=RED, ec='white'))
        ax_top.text(ix, iy, "−", ha='center', va='center', color='white', fontweight='bold', fontsize=8.5)
    ax_top.text(8.3, 2.25, "Тепловое облако\n(Больцман, k_B T)", ha='center', fontsize=7.8, color=RED, fontweight='bold')

    # Нижняя панель: Точный математический график потенциала φ(x)
    x = np.linspace(0, 10, 500)
    phi0 = 80.0  # мВ
    d_helm = 1.8  # нм
    lam_D = 3.0   # нм

    def phi_helmholtz(x_val):
        return np.where(x_val <= d_helm, phi0 * (1.0 - x_val / d_helm), 0.0)

    def phi_gouy(x_val):
        return phi0 * np.exp(-x_val / lam_D)

    ax_bot.plot(x, phi_helmholtz(x), color=BLUE, lw=2.5, ls='--',
                label=f'Модель Гельмгольца: φ(x) = φ₀(1 − x/d), линейный спад до x = d = {d_helm} нм')
    ax_bot.plot(x, phi_gouy(x), color=RED, lw=2.6,
                label=f'Модель Гуи–Чепмена: φ(x) = φ₀·exp(−κx), экспонента с λ_D = κ⁻¹ = {lam_D} нм')

    # Реперные точки строго по функциям
    ax_bot.scatter([d_helm], [float(phi_helmholtz(d_helm))], color=BLUE, s=60, zorder=5)
    y_debye = float(phi_gouy(lam_D))
    ax_bot.scatter([lam_D], [y_debye], color=RED, s=65, zorder=5)
    ax_bot.vlines(lam_D, 0, y_debye, color=RED, ls=':', lw=1.4)
    ax_bot.hlines(y_debye, 0, lam_D, color=RED, ls=':', lw=1.4)

    ax_bot.annotate(f"Толщина ДЭС Дебая:\nx = λ_D = {lam_D:.1f} нм\nφ(λ_D) = φ₀ / e = {y_debye:.1f} мВ",
                    xy=(lam_D, y_debye), xytext=(4.3, 35.0),
                    fontsize=8.3, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                    arrowprops=dict(arrowstyle='->', color=RED, lw=1.3))

    ax_bot.set_xlim(0, 10)
    ax_bot.set_ylim(-4, 92)
    ax_bot.set_xlabel("Расстояние от поверхности твердой фазы x, нм", fontsize=9.8, fontweight='bold', color=NAVY)
    ax_bot.set_ylabel("Потенциал φ(x), мВ", fontsize=9.8, fontweight='bold', color=NAVY)
    ax_bot.set_title("Б. Сравнение аналитических профилей потенциала φ(x) в двух моделях",
                     fontsize=10.0, fontweight='bold', color=NAVY)
    ax_bot.legend(loc='upper right', fontsize=8.0, framealpha=0.95)
    ax_bot.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_08_helmholtz_vs_gouy.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


def fig_09_debye_screening():
    """Слайд 9: Сжатие диффузного слоя Дебая при росте ионной силы и распределение ионов Больцмана."""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6.8, 5.1), dpi=300)

    # Панель А: Сжатие ДЭС при росте концентрации 1:1 электролита (λ_D = 0.304 / sqrt(c))
    x = np.linspace(0, 25, 500)
    phi0 = 50.0  # мВ

    concs = [
        (1e-4, 30.4, GREEN, 'c₁ = 10⁻⁴ М (λ_D = 30.4 нм — протяженный ДЭС)'),
        (1e-3, 9.61, BLUE,  'c₂ = 10⁻³ М (λ_D = 9.6 нм — средняя толщина)'),
        (1e-2, 3.04, RED,   'c₃ = 10⁻² М (λ_D = 3.04 нм — сильное сжатие ДЭС)')
    ]

    for c_val, lam, col, lbl in concs:
        def phi_curve(xv, l_val=lam):
            return phi0 * np.exp(-xv / l_val)

        ax1.plot(x, phi_curve(x), color=col, lw=2.4, label=lbl)
        if lam <= 25:
            y_pt = float(phi_curve(lam))
            ax1.scatter([lam], [y_pt], color=col, s=55, zorder=5)
            ax1.vlines(lam, 0, y_pt, color=col, ls=':', lw=1.3)

    ax1.axhline(phi0 / np.e, color=MUTED, ls='--', lw=1.1, label=f'Уровень спада в e раз: φ₀/e = {phi0/np.e:.1f} мВ')
    ax1.set_xlim(0, 25)
    ax1.set_ylim(0, 55)
    ax1.set_xlabel("Расстояние от поверхности x, нм", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_ylabel("Потенциал φ(x), мВ", fontsize=9.2, fontweight='bold', color=NAVY)
    ax1.set_title("А. Сжатие диффузного слоя при росте концентрации электролита (λ_D ∝ 1 / [z√c])",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax1.legend(loc='upper right', fontsize=7.6, framealpha=0.95)
    ax1.grid(True, ls=':', alpha=0.5)

    # Панель Б: Распределение Больцмана для противоионов n_-(x) и ко-ионов n_+(x) у положительной стенки
    x2 = np.linspace(0, 15, 400)
    lam_ref = 4.0  # нм
    kBT_mV = 25.7  # при 298 К

    def phi_ref(xv):
        return 40.0 * np.exp(-xv / lam_ref)

    def n_counter(xv):
        return np.exp(+phi_ref(xv) / kBT_mV)

    def n_coion(xv):
        return np.exp(-phi_ref(xv) / kBT_mV)

    ax2.plot(x2, n_counter(x2), color=RED, lw=2.5, label='Противоионы (притяжение): n_−(x)/n₀ = exp(+zeφ / k_B T)')
    ax2.plot(x2, n_coion(x2), color=BLUE, lw=2.5, label='Ко-ионы (отталкивание): n_+(x)/n₀ = exp(−zeφ / k_B T)')
    ax2.axhline(1.0, color=DARK, ls='--', lw=1.2, label='Объемная концентрация раствора (n = n₀ при x ≫ λ_D)')
    ax2.fill_between(x2, 1.0, n_counter(x2), color=RED, alpha=0.14)
    ax2.fill_between(x2, n_coion(x2), 1.0, color=BLUE, alpha=0.14)

    x_m = 2.0
    ax2.scatter([x_m, x_m], [float(n_counter(x_m)), float(n_coion(x_m))], color=NAVY, s=45, zorder=5)
    ax2.annotate("Избыток противоионов\nв диффузном слое", xy=(x_m, float(n_counter(x_m))), xytext=(3.0, 2.15),
                 fontsize=7.8, fontweight='bold', color=RED, bbox=BBOX_STYLE,
                 arrowprops=dict(arrowstyle='->', color=RED, lw=1.2))

    ax2.set_xlim(0, 15)
    ax2.set_ylim(0, 4.9)
    ax2.set_xlabel("Расстояние от поверхности x, нм", fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.set_ylabel("Относительная конц. n(x) / n₀", fontsize=9.2, fontweight='bold', color=NAVY)
    ax2.set_title("Б. Распределение Больцмана для противоионов и ко-ионов в диффузном слое",
                  fontsize=9.8, fontweight='bold', color=NAVY)
    ax2.legend(loc='upper right', fontsize=7.6, framealpha=0.95)
    ax2.grid(True, ls=':', alpha=0.5)

    fig.tight_layout()
    fig.savefig(os.path.join(OUT_DIR, "fig_09_debye_screening.png"), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close(fig)


if __name__ == "__main__":
    fig_01_roadmap()
    fig_02_specific_surface()
    fig_03_classification_matrix()
    fig_04_sol_gel_xerogel()
    fig_05_zeolites()
    fig_06_micelle_anatomy()
    fig_07_agi_feoh3_micelles()
    fig_08_helmholtz_vs_gouy()
    fig_09_debye_screening()
    print("Generated figures 01 to 09 successfully!")
