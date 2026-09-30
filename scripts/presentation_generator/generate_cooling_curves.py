import matplotlib.pyplot as plt
import numpy as np

# Set styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#242834'
plt.rcParams['axes.linewidth'] = 1.1

def generate_thermal_analysis_chart():
    # Share Y axis for perfect alignment across both plots
    fig, (ax_cool, ax_diag) = plt.subplots(1, 2, figsize=(6.8, 5.0), dpi=220, 
                                           sharey=True,
                                           gridspec_kw={'width_ratios': [1.2, 1.05], 'wspace': 0.12})
    
    # Common temperature limits
    T_min, T_max = 200, 1180
    
    # Characteristic temperatures
    T_A = 1000   # Melting point A
    T_B = 800    # Melting point B
    T_E = 400    # Eutectic temperature
    T_2 = 700    # Crystallization start for alloy 2 (x=16%)
    T_5 = 620    # Crystallization start for alloy 5 (x=75%)
    
    # -------------------------------------------------------------
    # LEFT SUBPLOT: Cooling Curves T - Time (tau)
    # -------------------------------------------------------------
    ax_cool.set_xlim(0, 100)
    ax_cool.set_ylim(T_min, T_max)
    ax_cool.set_xlabel('Время охлаждения, τ', fontsize=10, fontweight='bold', color='#242834')
    ax_cool.set_ylabel('Температура T, °C', fontsize=10, fontweight='bold', color='#242834')
    ax_cool.set_title('1. Кривые охлаждения сплавов', fontsize=11, fontweight='bold', color='#005AAA', pad=10)
    ax_cool.tick_params(colors='#242834', labelsize=9)
    
    # Curve 1: Pure A (t: 4 -> 20)
    t1 = [4, 8, 16, 20]
    T1 = [1080, T_A, T_A, 280]
    ax_cool.plot(t1, T1, color='#002C5F', lw=2.0)
    ax_cool.plot(t1[1:3], [T_A, T_A], color='#E70F47', lw=3.2) # arrest
    ax_cool.text(10, 1110, '1 (A)', fontsize=8.5, fontweight='bold', color='#002C5F', ha='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F4F8', edgecolor='#002C5F', lw=0.8))
    
    # Curve 2: Hypoeutectic (t: 24 -> 42)
    t2 = [24, 29, 36, 40, 43]
    T2 = [1080, T_2, T_E, T_E, 270]
    ax_cool.plot(t2, T2, color='#005AAA', lw=2.0)
    ax_cool.plot(t2[1], T_2, 'o', color='#005AAA', markersize=5) # inflection
    ax_cool.plot(t2[2:4], [T_E, T_E], color='#E70F47', lw=3.0) # eutectic arrest
    ax_cool.text(30, 1110, '2 (доэвт.)', fontsize=8.5, fontweight='bold', color='#005AAA', ha='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F7FF', edgecolor='#005AAA', lw=0.8))
    
    # Curve 4: Eutectic alloy (t: 46 -> 62)
    t4 = [46, 52, 60, 64]
    T4 = [1080, T_E, T_E, 260]
    ax_cool.plot(t4, T4, color='#E70F47', lw=2.2)
    ax_cool.plot(t4[1:3], [T_E, T_E], color='#E70F47', lw=3.8) # major arrest
    ax_cool.text(54, 1110, '4 (эвт. E)', fontsize=8.5, fontweight='bold', color='#E70F47', ha='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF0F2', edgecolor='#E70F47', lw=0.8))
    
    # Curve 5: Hypereutectic (t: 66 -> 82)
    t5 = [66, 70, 77, 81, 84]
    T5 = [1020, T_5, T_E, T_E, 270]
    ax_cool.plot(t5, T5, color='#005AAA', lw=2.0)
    ax_cool.plot(t5[1], T_5, 'o', color='#005AAA', markersize=5)
    ax_cool.plot(t5[2:4], [T_E, T_E], color='#E70F47', lw=3.0)
    ax_cool.text(74, 1060, '5 (заэвт.)', fontsize=8.5, fontweight='bold', color='#005AAA', ha='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F7FF', edgecolor='#005AAA', lw=0.8))
    
    # Curve 6: Pure B (t: 86 -> 98)
    t6 = [86, 89, 95, 98]
    T6 = [920, T_B, T_B, 280]
    ax_cool.plot(t6, T6, color='#002C5F', lw=2.0)
    ax_cool.plot(t6[1:3], [T_B, T_B], color='#E70F47', lw=3.0)
    ax_cool.text(92, 960, '6 (B)', fontsize=8.5, fontweight='bold', color='#002C5F', ha='center',
                 bbox=dict(boxstyle='round,pad=0.2', facecolor='#F0F4F8', edgecolor='#002C5F', lw=0.8))
    
    # Arrest labels on cooling curves
    ax_cool.text(12, T_A + 20, 'T_пл(A)', fontsize=8, color='#002C5F', fontweight='bold', ha='center')
    ax_cool.text(92, T_B + 20, 'T_пл(B)', fontsize=8, color='#002C5F', fontweight='bold', ha='center')
    ax_cool.text(50, T_E - 45, 'Площадка эвтектики (T_E = const, Φ = 3, C = 0)', 
                 fontsize=8, color='#E70F47', fontweight='bold', ha='center',
                 bbox=dict(boxstyle='round,pad=0.25', facecolor='#FFF5F5', edgecolor='#E70F47', lw=0.8))

    # -------------------------------------------------------------
    # RIGHT SUBPLOT: Binary Phase Diagram T - composition
    # -------------------------------------------------------------
    ax_diag.set_xlim(-2, 102)
    ax_diag.set_xlabel('Состав сплава, % B', fontsize=10, fontweight='bold', color='#242834')
    ax_diag.set_title('2. Фазовая диаграмма T – x', fontsize=11, fontweight='bold', color='#005AAA', pad=10)
    ax_diag.tick_params(colors='#242834', labelsize=9)
    
    # Liquidus curves
    xA = np.linspace(0, 40, 100)
    yA = T_A - (T_A - T_E) * (xA / 40)**1.2
    
    xB = np.linspace(40, 100, 100)
    yB = T_E + (T_B - T_E) * ((xB - 40) / 60)**1.2
    
    ax_diag.plot(xA, yA, color='#005AAA', lw=2.4)
    ax_diag.plot(xB, yB, color='#005AAA', lw=2.4)
    
    # Solidus / Eutectic line
    ax_diag.plot([0, 100], [T_E, T_E], color='#E70F47', lw=2.4)
    
    # Fill liquid zone subtly
    ax_diag.fill_between(xA, yA, T_max, color='#005AAA', alpha=0.06)
    ax_diag.fill_between(xB, yB, T_max, color='#005AAA', alpha=0.06)
    
    # Phase regions
    ax_diag.text(50, 1030, 'Жидкий расплав (L)', fontsize=9.5, fontweight='bold', ha='center', color='#002C5F')
    ax_diag.text(18, 520, 'L + A', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
    ax_diag.text(78, 520, 'L + B', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
    ax_diag.text(50, 270, 'Смесь кристаллов (A + B)', fontsize=9.5, fontweight='bold', ha='center', color='#242834')
    
    # Eutectic point
    ax_diag.plot(40, T_E, 'o', color='#E70F47', markersize=7, zorder=5)
    ax_diag.text(42, T_E + 24, 'E', fontsize=10, fontweight='bold', color='#E70F47')
    
    # Vertical composition lines matching the 5 curves
    comp_lines = [
        (0.5, '1: A', '#002C5F', 340),
        (16.5, '2', '#005AAA', 340),
        (40, '4: E', '#E70F47', 340),
        (75, '5', '#005AAA', 340),
        (99.5, '6: B', '#002C5F', 340)
    ]
    for x_c, lbl, col, y_pos in comp_lines:
        ax_diag.axvline(x=x_c, color=col, ls=':', lw=1.1, alpha=0.6)
        ax_diag.text(x_c, y_pos, lbl, fontsize=8, fontweight='bold',
                     color=col, ha='center',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=col, lw=0.8))
        
    # Horizontal alignment lines across both subplots (T_A, T_2, T_E, T_5, T_B)
    for T_val, col in [(T_A, '#002C5F'), (T_2, '#005AAA'), (T_E, '#E70F47'), (T_5, '#005AAA'), (T_B, '#002C5F')]:
        ax_cool.axhline(y=T_val, color=col, ls='--', lw=0.9, alpha=0.4)
        ax_diag.axhline(y=T_val, color=col, ls='--', lw=0.9, alpha=0.4)

    plt.tight_layout()
    plt.savefig('course_materials/semester_4/lectures/diagram_thermal_analysis.png')
    plt.close()
    print("Regenerated diagram_thermal_analysis.png successfully!")

if __name__ == '__main__':
    generate_thermal_analysis_chart()
