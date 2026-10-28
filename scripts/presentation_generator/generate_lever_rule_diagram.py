import matplotlib.pyplot as plt
import numpy as np
import os

# Set font and styling
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial']
plt.rcParams['font.size'] = 10
plt.rcParams['axes.unicode_minus'] = False

# Dimensions: 578.2 pt x 352.5 pt -> aspect ratio 1.64. At 250 DPI -> 2000 x 1220 px
fig = plt.figure(figsize=(10.5, 6.4), dpi=250)

# Layout geometry:
# Left diagram: 51% width
# Right side: 2 subplots (Lever beam top 48%, Practical engineering summary bottom 48%)
ax_diag = fig.add_axes([0.08, 0.11, 0.44, 0.81])
ax_lever = fig.add_axes([0.56, 0.54, 0.42, 0.38])
ax_summary = fig.add_axes([0.56, 0.08, 0.42, 0.38])

# ==========================================
# 1. PHASE DIAGRAM Au - Si
# ==========================================
ax = ax_diag
ax.set_title("Фазовая диаграмма Au – Si и конода (800 °C)", fontsize=11.5, fontweight='bold', pad=10, color='#002060')

from scipy.interpolate import PchipInterpolator

xE = 94.0
TE = 363.0

# Liquidus Si: exact monotonic PCHIP curve passing through (0, 1414), (30, 1000), (66, 800), (94, 363)
pts_x = np.array([0.0, 30.0, 66.0, 94.0])
pts_y = np.array([1414.0, 1000.0, 800.0, 363.0])
pchip_si = PchipInterpolator(pts_x, pts_y)
x_si = np.linspace(0, xE, 300)
T_liq_si = pchip_si(x_si)

# Liquidus Au: from (94, 363) to (100, 1064)
x_au = np.linspace(xE, 100, 100)
coeff_au = np.polyfit([94.0, 100.0], [363.0, 1064.0], 1)
T_liq_au = np.polyval(coeff_au, x_au)

# Plot liquidus
ax.plot(x_si, T_liq_si, color='#003366', lw=2.6, label='Ликвидус')
ax.plot(x_au, T_liq_au, color='#003366', lw=2.6)

# Solidus / Eutectic line
ax.axhline(TE, color='#c00000', lw=2.2, ls='-')

# Boundaries
ax.axvline(0, color='black', lw=1.2)
ax.axvline(100, color='black', lw=1.2)

# Shading
ax.fill_between(x_si, T_liq_si, 1500, color='#ebf3fa', alpha=0.7)
ax.fill_between(x_au, T_liq_au, 1500, color='#ebf3fa', alpha=0.7)
ax.fill_between(x_si, TE, T_liq_si, color='#fff9e6', alpha=0.6)
ax.fill_between(x_au, TE, T_liq_au, color='#fff0f0', alpha=0.6)
ax.fill_between([0, 100], [0, 0], [TE, TE], color='#f2f2f2', alpha=0.8)

# Region labels
ax.text(48, 1200, "Жидкий расплав\n(L)", fontsize=11, fontweight='bold', ha='center', va='center', color='#003366')
ax.text(32, 570, "Двухфазная область:\n$L + \\mathrm{Si}_{тв}$", fontsize=9.5, ha='center', va='center', color='#805500',
        bbox=dict(boxstyle='round,pad=0.35', facecolor='#fff2cc', edgecolor='#d6b656', alpha=0.85))
ax.text(97.2, 570, "$L+\\mathrm{Au}_{тв}$", fontsize=7.5, ha='center', va='center', color='#800000', rotation=90)
ax.text(50, 210, "Эвтектическая смесь кристаллов: $\\mathrm{Si}_{тв} + \\mathrm{Au}_{тв}$", 
        fontsize=8.5, ha='center', va='center', color='#333333',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#ffffff', edgecolor='#b0b0b0', alpha=0.9))

# Eutectic point
ax.plot(xE, TE, 'o', color='#c00000', markersize=6.5, zorder=5)
ax.annotate("E (94%, 363°C)\nэвтектика", xy=(xE, TE), xytext=(xE - 12, TE + 50),
            arrowprops=dict(facecolor='#c00000', edgecolor='#c00000', arrowstyle='->', lw=1.2),
            fontsize=7.8, fontweight='bold', color='#c00000', ha='center')

# T_melt labels
ax.plot(0, 1414, 's', color='#003366', markersize=6, zorder=5)
ax.text(2, 1414, " $T_{пл}(\\mathrm{Si}) = 1414^\\circ$C", fontsize=8.5, fontweight='bold', color='#003366', va='center')
ax.plot(100, 1064, 's', color='#003366', markersize=6, zorder=5)
ax.text(98, 1064, "$T_{пл}(\\mathrm{Au}) = 1064^\\circ$C ", fontsize=8.5, fontweight='bold', color='#003366', va='center', ha='right')

# TIE-LINE AT 800 °C
T_iso = 800.0
x_a = 0.0
x_b = 30.0
x_d = 66.0

# Tie-line segments
ax.plot([x_a, x_b], [T_iso, T_iso], color='#0070c0', lw=5.0, zorder=6) # Left arm ab
ax.plot([x_b, x_d], [T_iso, T_iso], color='#e06600', lw=5.0, zorder=6) # Right arm bd

# Points
ax.plot(x_a, T_iso, 'o', color='#0070c0', markersize=7.5, zorder=7)
ax.plot(x_b, T_iso, 'ko', markersize=8.5, zorder=7)
ax.plot(x_d, T_iso, 'o', color='#e06600', markersize=7.5, zorder=7)

# Point labels
ax.text(x_a + 1.5, T_iso + 38, "a ($0\\%$ Au)\n$\\mathrm{Si}_{тв}$", fontsize=8.5, fontweight='bold', color='#0070c0')
ax.text(x_b, T_iso + 38, "b ($30\\%$ Au)\nСплав ($m_0=400$г)", fontsize=8.5, fontweight='bold', color='black', ha='center')
ax.text(x_d + 1.5, T_iso + 38, "d ($66\\%$ Au)\nРасплав L", fontsize=8.5, fontweight='bold', color='#b35000')

# Arm length annotations below tie-line
ax.annotate('', xy=(x_a, T_iso - 35), xytext=(x_b, T_iso - 35),
            arrowprops=dict(arrowstyle='<->', color='#0070c0', lw=1.6))
ax.text((x_a + x_b)/2, T_iso - 75, "$l_S = 30\\%$\n(для расплава L)", fontsize=8, color='#0070c0', ha='center', fontweight='bold')

ax.annotate('', xy=(x_b, T_iso - 35), xytext=(x_d, T_iso - 35),
            arrowprops=dict(arrowstyle='<->', color='#e06600', lw=1.6))
ax.text((x_b + x_d)/2, T_iso - 75, "$l_L = 36\\%$\n(для кристаллов Si)", fontsize=8, color='#b35000', ha='center', fontweight='bold')

# Drop lines to X axis
ax.plot([x_b, x_b], [0, T_iso], color='gray', ls=':', lw=1.3)
ax.plot([x_d, x_d], [0, T_iso], color='#e06600', ls=':', lw=1.3)

# Axis limits and labels
ax.set_xlim(-2, 102)
ax.set_ylim(80, 1520)
ax.set_xlabel("Состав сплава, масс. % Au (компонент B)", fontsize=9.5, fontweight='bold')
ax.set_ylabel("Температура T, °C", fontsize=9.5, fontweight='bold')
ax.set_xticks([0, 15, 30, 45, 60, 66, 80, 100])
ax.set_xticklabels(['0 (Si)', '15', '30 (b)', '45', '60', '66 (d)', '80', '100 (Au)'], fontsize=8)
ax.set_yticks([200, 363, 600, 800, 1000, 1064, 1200, 1414])
ax.set_yticklabels(['200', '363 ($T_E$)', '600', '800', '1000', '1064', '1200', '1414'], fontsize=8)
ax.grid(True, ls='--', alpha=0.45)

# ==========================================
# 2. MECHANICAL LEVER ANALOGY (Top Right)
# ==========================================
ax_l = ax_lever
ax_l.set_title("Схема правила рычага (уравнение моментов)", fontsize=10.5, fontweight='bold', pad=8, color='#002060')
ax_l.set_xlim(-52, 58)
ax_l.set_ylim(-38, 32)
ax_l.axis('off')

# Fulcrum at (0, 0)
triangle = plt.Polygon([[0, 0], [-4.5, -9], [4.5, -9]], color='#444444', zorder=4)
ax_l.add_patch(triangle)
ax_l.plot([-9, 9], [-9, -9], color='black', lw=2, zorder=4)
ax_l.text(0, -13, "Опора b\n($x_0 = 30\\%$)", fontsize=7.5, ha='center', va='top', fontweight='bold', color='#333333', zorder=10)

# Lever beam
ax_l.plot([-30, 0], [0, 0], color='#0070c0', lw=5.5, zorder=5) # Left arm (30)
ax_l.plot([0, 36], [0, 0], color='#e06600', lw=5.5, zorder=5) # Right arm (36)

# Arm labels above beam
ax_l.text(-15, 5, "Плечо $l_S = 30\\%$\n(отрезок ab)", fontsize=7.5, ha='center', fontweight='bold', color='#0070c0', zorder=10)
ax_l.text(18, 5, "Плечо $l_L = 36\\%$\n(отрезок bd)", fontsize=7.5, ha='center', fontweight='bold', color='#b35000', zorder=10)

# Left weight (Solid Si crystals): suspended at x = -30
ax_l.plot([-30, -30], [0, -8], color='#0070c0', lw=1.5, zorder=5)
box_s = plt.Rectangle((-42, -26), 24, 18, facecolor='#d9e1f2', edgecolor='#0070c0', lw=1.8, zorder=6)
ax_l.add_patch(box_s)
ax_l.text(-30, -17, "$m_S = 218.2$ г\nКристаллы Si", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#002060', zorder=10)

# Right weight (Liquid melt L): suspended at x = +36
ax_l.plot([36, 36], [0, -8], color='#e06600', lw=1.5, zorder=5)
box_l = plt.Rectangle((24, -26), 24, 18, facecolor='#fce4d6', edgecolor='#e06600', lw=1.8, zorder=6)
ax_l.add_patch(box_l)
ax_l.text(36, -17, "$m_L = 181.8$ г\nРасплав L", fontsize=7.5, ha='center', va='center', fontweight='bold', color='#833c0c', zorder=10)

# Balance formula banner at top
ax_l.text(3, 22, "Условие равновесия: $m_S \\cdot l_S = m_L \\cdot l_L$\n$218.2 \\text{ г} \\times 30\\% = 181.8 \\text{ г} \\times 36\\% \\approx 6546$", 
          fontsize=8.3, ha='center', va='center', color='#002060', fontweight='bold', zorder=10,
          bbox=dict(boxstyle='round,pad=0.35', facecolor='#eaf2f8', edgecolor='#0070c0', lw=1.1))

# Bottom insight
ax_l.text(3, -33, "Меньшее плечо держит большую массу: $m_S > m_L$!", 
          fontsize=7.8, ha='center', va='center', color='#c00000', fontweight='bold', zorder=10)

# ==========================================
# 3. PRACTICAL ENGINEERING & NANO SUMMARY (Bottom Right)
# ==========================================
ax_s = ax_summary
ax_s.set_title("Практический итог расчета для инженера", fontsize=10.5, fontweight='bold', pad=8, color='#002060')
ax_s.set_xlim(0, 100)
ax_s.set_ylim(0, 100)
ax_s.axis('off')

# Outer card background
card = plt.Rectangle((2, 2), 96, 96, facecolor='#f8f9fa', edgecolor='#002060', lw=1.5, zorder=2)
ax_s.add_patch(card)

# Content inside card
ax_s.text(50, 86, "Исходные данные: 400 г сплава Au–Si (30% Au) при 800 °C", 
          fontsize=8.0, ha='center', va='center', fontweight='bold', color='#002060', zorder=5)

# Split boxes
# Left box: Liquid melt
card_l = plt.Rectangle((6, 32), 41, 46, facecolor='#fce4d6', edgecolor='#e06600', lw=1.3, zorder=3)
ax_s.add_patch(card_l)
ax_s.text(26.5, 71, "Жидкая фаза (L)", fontsize=8.0, fontweight='bold', color='#833c0c', ha='center', zorder=5)
ax_s.text(26.5, 59, "Масса: 181.8 г (45.5%)\nСостав: 66% Au, 34% Si\nЗолото: 120 г (100% Au)", 
          fontsize=7.2, color='#202020', ha='center', va='center', zorder=5)
ax_s.text(26.5, 38, "Обогащение Au в 2.2 раза!", fontsize=6.8, fontweight='bold', color='#c00000', ha='center', zorder=5)

# Right box: Solid silicon
card_s = plt.Rectangle((53, 32), 41, 46, facecolor='#d9e1f2', edgecolor='#0070c0', lw=1.3, zorder=3)
ax_s.add_patch(card_s)
ax_s.text(73.5, 71, "Твердая фаза (Si)", fontsize=8.0, fontweight='bold', color='#002060', ha='center', zorder=5)
ax_s.text(73.5, 59, "Масса: 218.2 г (54.5%)\nСостав: 100% Si, 0% Au\nКремний: 218.2 г в осадке", 
          fontsize=7.2, color='#202020', ha='center', va='center', zorder=5)
ax_s.text(73.5, 38, "Абсолютно чистый кристалл!", fontsize=6.8, fontweight='bold', color='#002060', ha='center', zorder=5)

# Bottom engineering takeaway
ax_s.text(50, 20, "• Инженерия: бесконтактный расчет разделения компонентов в печи.", fontsize=7.0, ha='center', color='#333333', zorder=5)
ax_s.text(50, 9, "• Нанотехнологии: капли Au–Si катализируют VLS-рост Si нанонитей.", fontsize=7.0, ha='center', color='#002060', fontweight='bold', zorder=5)

# Save diagram
out_dir = r"course_materials/semester_4/lectures"
os.makedirs(out_dir, exist_ok=True)
out_path = os.path.join(out_dir, "diagram_lever_rule_au_si.png")
plt.savefig(out_path, dpi=250, bbox_inches='tight')
plt.close()
print("Saved complete practical lever diagram to:", out_path)
