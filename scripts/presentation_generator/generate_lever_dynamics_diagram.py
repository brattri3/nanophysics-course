import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator
import os

# Set font and styling
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# Dimensions: 578.2 pt x 352.5 pt -> aspect ratio 1.64. At 250 DPI -> 2000 x 1220 px
fig = plt.figure(figsize=(10.5, 6.4), dpi=250)

# Layout geometry:
# Left diagram: 43% width
# Right Top: Fraction of phases vs T (43% width, from 0.54 to 0.97)
# Right Bottom: Microstructure evolution (43% width, from 0.08 to 0.45)
ax_diag = fig.add_axes([0.08, 0.11, 0.42, 0.81])
ax_curve = fig.add_axes([0.55, 0.58, 0.42, 0.34])
ax_micro = fig.add_axes([0.55, 0.08, 0.42, 0.39])

# ==========================================
# 1. PHASE DIAGRAM Au - Si WITH DYNAMIC POINTS
# ==========================================
ax = ax_diag
ax.set_title("Динамика правила рычага при охлаждении (30% Au)", fontsize=10.5, fontweight='bold', pad=10, color='#002060')

xE = 94.0
TE = 363.0

# Liquidus Si: exact monotonic PCHIP curve passing EXACTLY through all key points:
# (0, 1414) -> pure Si melting point
# (30, 1000) -> Point 2 on liquidus
# (66, 800) -> Point 3 conode endpoint
# (94, 363) -> Eutectic point E
pts_x = np.array([0.0, 30.0, 66.0, 94.0])
pts_y = np.array([1414.0, 1000.0, 800.0, 363.0])
pchip_si = PchipInterpolator(pts_x, pts_y)
x_si = np.linspace(0, xE, 300)
T_liq_si = pchip_si(x_si)

# Liquidus Au
x_au = np.linspace(xE, 100, 100)
coeff_au = np.polyfit([94.0, 100.0], [363.0, 1064.0], 1)
T_liq_au = np.polyval(coeff_au, x_au)

# Plot curves
ax.plot(x_si, T_liq_si, color='#003366', lw=2.4)
ax.plot(x_au, T_liq_au, color='#003366', lw=2.4)
ax.axhline(TE, color='#c00000', lw=2.0, ls='-')
ax.axvline(0, color='black', lw=1.2)
ax.axvline(100, color='black', lw=1.2)

# Shading
ax.fill_between(x_si, T_liq_si, 1500, color='#ebf3fa', alpha=0.6)
ax.fill_between(x_au, T_liq_au, 1500, color='#ebf3fa', alpha=0.6)
ax.fill_between(x_si, TE, T_liq_si, color='#fff9e6', alpha=0.6)
ax.fill_between(x_au, TE, T_liq_au, color='#fff0f0', alpha=0.6)
ax.fill_between([0, 100], [0, 0], [TE, TE], color='#f2f2f2', alpha=0.8)

# Vertical cooling line for 30% Au alloy
x_alloy = 30.0
ax.plot([x_alloy, x_alloy], [150, 1260], color='#002060', lw=1.8, ls='--', zorder=4)

# Tie-line at 1000 °C (Point 2 - on liquidus)
ax.plot([0, 30], [1000, 1000], color='#0070c0', lw=2.4, ls='-', zorder=5)
ax.plot(0, 1000, 'o', color='#0070c0', markersize=5, zorder=6)
ax.plot(30, 1000, 'o', color='#0070c0', markersize=5, zorder=6)

# Tie-line at 800 °C (Point 3)
ax.plot([0, 66], [800, 800], color='#e06600', lw=3.0, zorder=5)
ax.plot(0, 800, 'o', color='#0070c0', markersize=5, zorder=6)
ax.plot(66, 800, 'o', color='#e06600', markersize=5, zorder=6)

# Tie-line just above TE (Point 4: 380 °C)
x_liq_380 = float(np.interp(380.0, T_liq_si[::-1], x_si[::-1]))
ax.plot([0, x_liq_380], [380, 380], color='#2e7d32', lw=2.8, zorder=5)
ax.plot(0, 380, 'o', color='#0070c0', markersize=5, zorder=6)
ax.plot(x_liq_380, 380, 'o', color='#2e7d32', markersize=5, zorder=6)

# Points along cooling line with numbers:
pts = [
    (x_alloy, 1200, "1", "1: 1200°C (100% L, расплав)", 1200, '#002060'),
    (x_alloy, 1000, "2", "2: 1000°C (ликвидус: плечо к ликв.=0 $\\to$ $m_S=0\\%$)", 1030, '#0055a5'),
    (x_alloy, 800, "3", "3: 800°C (конода: $m_S=54.5\\%, m_L=45.5\\%$)", 835, '#b35000'),
    (x_alloy, 380, "4", "4: 380°C (предел: $m_S=68.1\\%, m_L=31.9\\%$)", 420, '#1b5e20'),
    (x_alloy, 363, "5", "5: 363°C ($T_E$: застывание 31.9% расплава L)", 340, '#c00000'),
    (x_alloy, 200, "6", "6: 200°C (Si 68.1% + эвтектика 31.9%)", 200, '#333333')
]

for px, py, pnum, plabel, ty, col in pts:
    ax.plot(px, py, 'o', color='black', markersize=7, zorder=7)
    ax.plot(px, py, 'o', color='#ffff00', markersize=5.5, zorder=8)
    ax.text(px, py, pnum, fontsize=7.2, fontweight='bold', ha='center', va='center', color='black', zorder=9)
    ax.text(px + 3.0, ty, plabel, fontsize=6.8, ha='left', va='center', fontweight='bold', color=col, zorder=10,
            bbox=dict(boxstyle='square,pad=0.15', facecolor='white', edgecolor='none', alpha=0.75))

# Eutectic point
ax.plot(xE, TE, 'o', color='#c00000', markersize=5.5, zorder=5)
ax.text(xE - 2, TE + 22, "E (94%, 363°C)", fontsize=7.2, fontweight='bold', color='#c00000', ha='right')

# T_melt labels
ax.plot(0, 1414, 's', color='#003366', markersize=5, zorder=5)
ax.text(2, 1414, " $T_{пл}(\\mathrm{Si}) = 1414^\\circ$C", fontsize=7.5, fontweight='bold', color='#003366', va='center')
ax.plot(100, 1064, 's', color='#003366', markersize=5, zorder=5)
ax.text(98, 1064, "$T_{пл}(\\mathrm{Au}) = 1064^\\circ$C ", fontsize=7.5, fontweight='bold', color='#003366', va='center', ha='right')

# Axes styling
ax.set_xlim(-2, 102)
ax.set_ylim(80, 1500)
ax.set_xlabel("Состав сплава, масс. % Au", fontsize=8.5, fontweight='bold')
ax.set_ylabel("Температура T, °C", fontsize=8.5, fontweight='bold')
ax.set_xticks([0, 15, 30, 45, 60, 66, 80, 100])
ax.set_xticklabels(['0 (Si)', '15', '30 (сплав)', '45', '60', '66', '80', '100 (Au)'], fontsize=7.0)
ax.set_yticks([200, 363, 600, 800, 1000, 1064, 1200, 1414])
ax.set_yticklabels(['200', '363 ($T_E$)', '600', '800', '1000', '1064', '1200', '1414'], fontsize=7.0)
ax.grid(True, ls='--', alpha=0.45)

# ==========================================
# 2. PHASE FRACTIONS VS TEMPERATURE GRAPH
# ==========================================
ax_c = ax_curve
ax_c.set_title("График изменения долей фаз при охлаждении", fontsize=9.5, fontweight='bold', pad=6, color='#002060')

T_vals = np.linspace(200, 1200, 400)
frac_L = []
frac_S = []

for T in T_vals:
    if T >= 1000:
        frac_L.append(100.0)
        frac_S.append(0.0)
    elif T > 363:
        x_liq = float(np.interp(T, T_liq_si[::-1], x_si[::-1]))
        f_L = (30.0 / x_liq) * 100.0
        f_L = max(0.0, min(100.0, f_L))
        f_S = 100.0 - f_L
        frac_L.append(f_L)
        frac_S.append(f_S)
    else: # Below TE
        frac_L.append(0.0)
        frac_S.append(100.0)

ax_c.plot(frac_L, T_vals, color='#e06600', lw=2.2, label='Расплав $L$ (жидкость)')
ax_c.plot(frac_S, T_vals, color='#0070c0', lw=2.2, label='Кристаллы $\\mathrm{Si}$ (твердое)')
ax_c.axhline(363, color='#c00000', lw=1.3, ls='--', label='Линия эвтектики ($363^\\circ$C)')

# Key value annotations
ax_c.plot(45.5, 800, 'o', color='#e06600', markersize=4.5)
ax_c.plot(54.5, 800, 'o', color='#0070c0', markersize=4.5)
ax_c.text(50, 830, "800°C: $m_S=54.5\\%, m_L=45.5\\%$", fontsize=6.8, fontweight='bold', ha='center', color='#002060')

ax_c.plot(31.9, 380, 'o', color='#e06600', markersize=4.5)
ax_c.plot(68.1, 380, 'o', color='#0070c0', markersize=4.5)
ax_c.text(50, 420, "380°C: $m_S=68.1\\%, m_L=31.9\\%$", fontsize=6.8, fontweight='bold', ha='center', color='#1b5e20')

ax_c.set_xlim(-5, 105)
ax_c.set_ylim(200, 1200)
ax_c.set_xlabel("Массовая доля фазы в сплаве, %", fontsize=7.8, fontweight='bold')
ax_c.set_ylabel("Температура T, °C", fontsize=7.8, fontweight='bold')
ax_c.legend(loc='upper center', fontsize=7.0, framealpha=0.9, ncol=2)
ax_c.grid(True, ls='--', alpha=0.45)

# ==========================================
# 3. MICROSTRUCTURE EVOLUTION (3 DISTINCT STAGES)
# ==========================================
ax_m = ax_micro
ax_m.set_title("Эволюция микроструктуры сплава по точкам", fontsize=9.5, fontweight='bold', pad=6, color='#002060')
ax_m.set_xlim(0, 100)
ax_m.set_ylim(0, 100)
ax_m.axis('off')

# 3 stages with generous spacing: x = 16, 50, 84
xs = [16, 50, 84]
box_w = 24
box_h = 42

stages_info = [
    ("Точка 1 (1200 °C)", "100% Расплав L\n(однородная жидкость)", "#ebf3fa", "liquid"),
    ("Точка 3 (800 °C)", "Пульпа при 800°C\n54.5% Si + 45.5% L", "#fff9e6", "crystals_liquid"),
    ("Точка 6 (200 °C)", "Застывший слиток\n68.1% Si + 31.9% эвт.", "#fff2cc", "solid_eutectic")
]

for (cx, (st_title, st_desc, bg_col, mode)) in zip(xs, stages_info):
    rect = plt.Rectangle((cx - box_w/2, 45), box_w, box_h, facecolor=bg_col, edgecolor='#002060', lw=1.3, zorder=3)
    ax_m.add_patch(rect)
    
    if mode == "liquid":
        ax_m.plot([cx - 8, cx + 8], [68, 68], color='#2e75b6', lw=1.0, ls=':', zorder=4)
        ax_m.plot([cx - 8, cx + 8], [60, 60], color='#2e75b6', lw=1.0, ls=':', zorder=4)
        ax_m.text(cx, 66, "Гомогенная\nжидкость", fontsize=6.2, ha='center', color='#002060', zorder=5)
    elif mode == "crystals_liquid":
        for (dx, dy) in [(-5, 4), (4, -4), (-3, -10), (5, 6), (-1, -1)]:
            p = plt.Rectangle((cx + dx - 2, 66 + dy - 2), 4.5, 4.5, facecolor='#2e75b6', edgecolor='#002060', lw=0.8, zorder=5)
            ax_m.add_patch(p)
        ax_m.text(cx, 49, "Кристаллы Si\nв расплаве L", fontsize=5.8, ha='center', color='#805500', fontweight='bold', zorder=6)
    elif mode == "solid_eutectic":
        for y_line in range(48, 85, 4):
            ax_m.plot([cx - box_w/2 + 1, cx + box_w/2 - 1], [y_line, y_line], color='#d6b656', lw=0.8, ls='--', zorder=4)
        for (dx, dy) in [(-5, 5), (4, -3), (-3, -8), (5, 7), (-1, 0)]:
            p = plt.Rectangle((cx + dx - 2.5, 66 + dy - 2.5), 5.5, 5.5, facecolor='#002060', edgecolor='black', lw=0.8, zorder=5)
            ax_m.add_patch(p)
        ax_m.text(cx, 49, "Первичный Si\n+ эвтектика", fontsize=5.8, ha='center', color='#002060', fontweight='bold', zorder=6)

    ax_m.text(cx, 91, st_title, fontsize=7.2, fontweight='bold', ha='center', color='#002060')
    ax_m.text(cx, 37, st_desc, fontsize=6.5, ha='center', va='top', color='#202020')

# Arrows between stages
ax_m.annotate('', xy=(38 - 1, 66), xytext=(28 + 1, 66),
              arrowprops=dict(arrowstyle='->', color='#c00000', lw=1.5), zorder=6)
ax_m.annotate('', xy=(72 - 1, 66), xytext=(62 + 1, 66),
              arrowprops=dict(arrowstyle='->', color='#c00000', lw=1.5), zorder=6)

# Bottom conclusion
ax_m.text(50, 12, "Правило рычага дает точный количественный расчет структуры слитка при любой T!",
          fontsize=7.0, ha='center', va='center', fontweight='bold', color='#002060',
          bbox=dict(boxstyle='round,pad=0.3', facecolor='#eaf2f8', edgecolor='#0070c0', lw=0.9))

# Save diagram
out_dir = r"course_materials/semester_4/lectures"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "diagram_lever_dynamics.png")
plt.savefig(out_path, dpi=250, bbox_inches='tight')
plt.close()
print("Saved perfect lever dynamics diagram to:", out_path)
