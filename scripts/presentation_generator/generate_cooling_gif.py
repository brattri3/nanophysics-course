import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# Set styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#242834'
plt.rcParams['axes.linewidth'] = 1.1

def create_cooling_gif(output_path='course_materials/semester_4/lectures/cooling_single_alloy.gif'):
    T_min, T_max = 200, 1180
    T_A = 1000   # Melting point A
    T_B = 800    # Melting point B
    T_E = 400    # Eutectic temperature
    
    # Hypoeutectic alloy x_0 = 18% B
    x_0 = 18.0
    T_liq = T_A - (T_A - T_E) * (x_0 / 40.0)**1.2 # approx 680 °C
    
    # Sharp, distinct slopes:
    # Phase 1: Fast liquid cooling (steep): tau from 4 to 16 (dT = 420, rate ~ 35 deg/unit)
    times_p1 = np.linspace(4, 16, 13)
    temps_p1 = np.linspace(1100, T_liq, 13)
    
    # Phase 2: Crystallization of A (dramatic knee / inflection, 3.5x slower): tau from 16 to 44 (dT = 280, rate ~ 10 deg/unit)
    times_p2 = np.linspace(16, 44, 17)[1:]
    temps_p2 = np.linspace(T_liq, T_E, 17)[1:]
    
    # Phase 3: Eutectic arrest (horizontal plateau, dT = 0): tau from 44 to 62
    times_p3 = np.linspace(44, 62, 14)[1:]
    temps_p3 = np.full(13, T_E)
    
    # Phase 4: Solid cooling (steep again): tau from 62 to 74
    times_p4 = np.linspace(62, 74, 11)[1:]
    temps_p4 = np.linspace(T_E, 260, 11)[1:]
    
    all_times = np.concatenate([times_p1, times_p2, times_p3, times_p4])
    all_temps = np.concatenate([temps_p1, temps_p2, temps_p3, temps_p4])
    
    # Phase diagram curves
    xA = np.linspace(0, 40, 100)
    yA = T_A - (T_A - T_E) * (xA / 40)**1.2
    xB = np.linspace(40, 100, 100)
    yB = T_E + (T_B - T_E) * ((xB - 40) / 60)**1.2
    
    frames = []
    
    # Render frames across the wide canvas (8.2 x 5.0)
    for i in range(len(all_times)):
        t_curr = all_times[i]
        T_curr = all_temps[i]
        
        fig, (ax_cool, ax_diag) = plt.subplots(1, 2, figsize=(8.2, 5.0), dpi=180,
                                               sharey=True,
                                               gridspec_kw={'width_ratios': [1.2, 1.1], 'wspace': 0.12})
        
        # -------------------------------------------------------------
        # LEFT: Cooling Curve T(tau)
        # -------------------------------------------------------------
        ax_cool.set_xlim(0, 80)
        ax_cool.set_ylim(T_min, T_max)
        ax_cool.set_xlabel('Время охлаждения, τ [с]', fontsize=10, fontweight='bold', color='#242834')
        ax_cool.set_ylabel('Температура T, °C', fontsize=10, fontweight='bold', color='#242834')
        ax_cool.set_title('1. Кривая охлаждения сплава (18% B)', fontsize=11, fontweight='bold', color='#005AAA', pad=8)
        ax_cool.tick_params(colors='#242834', labelsize=9)
        
        # Draw full trajectory faintly in gray
        ax_cool.plot(all_times, all_temps, color='#D0D7DE', lw=2.2, ls=':', zorder=1)
        
        # Draw path traversed so far
        ax_cool.plot(all_times[:i+1], all_temps[:i+1], color='#005AAA', lw=2.6, zorder=2)
        
        # Highlight inflection point prominently
        ax_cool.plot(16, T_liq, 'o', color='#005AAA', markersize=6.5, zorder=4)
        ax_cool.annotate('Четкий излом: T_ликв\n(выделение кристаллов A)', 
                         xy=(16, T_liq), xytext=(22, T_liq + 110),
                         arrowprops=dict(arrowstyle="->", color='#005AAA', lw=1.5),
                         fontsize=8.5, fontweight='bold', color='#005AAA',
                         bbox=dict(boxstyle='round,pad=0.25', facecolor='#F0F7FF', edgecolor='#005AAA', lw=0.9))
        
        # Highlight eutectic arrest
        if t_curr >= 44:
            p3_idx = np.where(all_times[:i+1] >= 44)[0]
            if len(p3_idx) > 1:
                ax_cool.plot(all_times[p3_idx], all_temps[p3_idx], color='#E70F47', lw=3.8, zorder=3)
        
        # Annotation for eutectic arrest
        ax_cool.text(53, T_E - 45, 'Площадка эвтектики (T_E = const)', 
                     fontsize=8.5, color='#E70F47', fontweight='bold', ha='center',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFF5F5', edgecolor='#E70F47', lw=0.8))
        
        # Current active dot on cooling curve
        pt_color = '#E70F47' if abs(T_curr - T_E) < 1.0 else '#005AAA'
        ax_cool.plot(t_curr, T_curr, 'o', color=pt_color, markersize=8.5, markeredgecolor='#FFFFFF', markeredgewidth=1.2, zorder=6)
        
        # Reference dashed lines for T_liq and T_E
        ax_cool.axhline(y=T_liq, color='#005AAA', ls='--', lw=0.9, alpha=0.35)
        ax_cool.axhline(y=T_E, color='#E70F47', ls='--', lw=0.9, alpha=0.35)
        
        # -------------------------------------------------------------
        # RIGHT: Phase Diagram T(x)
        # -------------------------------------------------------------
        ax_diag.set_xlim(-2, 102)
        ax_diag.set_xlabel('Состав сплава, % B', fontsize=10, fontweight='bold', color='#242834')
        ax_diag.set_title('2. Фазовая диаграмма T – x', fontsize=11, fontweight='bold', color='#005AAA', pad=8)
        ax_diag.tick_params(colors='#242834', labelsize=9)
        
        # Liquidus and solidus
        ax_diag.plot(xA, yA, color='#005AAA', lw=2.4)
        ax_diag.plot(xB, yB, color='#005AAA', lw=2.4)
        ax_diag.plot([0, 100], [T_E, T_E], color='#E70F47', lw=2.4)
        
        # Fill liquid zone subtly
        ax_diag.fill_between(xA, yA, T_max, color='#005AAA', alpha=0.06)
        ax_diag.fill_between(xB, yB, T_max, color='#005AAA', alpha=0.06)
        
        # Phase labels
        ax_diag.text(50, 1040, 'Жидкий расплав (L)', fontsize=10, fontweight='bold', ha='center', color='#002C5F')
        ax_diag.text(8, 520, 'L + A', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
        ax_diag.text(78, 520, 'L + B', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
        ax_diag.text(55, 230, 'Смесь кристаллов (A + B)', fontsize=10, fontweight='bold', ha='center', color='#242834')
        
        # Eutectic point
        ax_diag.plot(40, T_E, 'o', color='#E70F47', markersize=7.5)
        ax_diag.text(42, T_E + 24, 'E (эвтектика)', fontsize=10, fontweight='bold', color='#E70F47')
        
        # Intersection on liquidus
        ax_diag.plot(x_0, T_liq, 'o', color='#005AAA', markersize=6.5)
        
        # Vertical isopleth line of the alloy x = x_0
        ax_diag.axvline(x=x_0, color='#242834', ls=':', lw=1.2, alpha=0.45)
        ax_diag.text(x_0, 320, 'x = 18%', fontsize=8.5, fontweight='bold', color='#242834', ha='center',
                     bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor='#242834', lw=0.8))
        
        # Path traversed by figurative point (straight down along x = x_0)
        ax_diag.plot([x_0, x_0], [all_temps[0], T_curr], color='#002C5F', lw=2.4, zorder=2)
        
        # Current active dot on phase diagram
        ax_diag.plot(x_0, T_curr, 'o', color=pt_color, markersize=8.5, markeredgecolor='#FFFFFF', markeredgewidth=1.2, zorder=6)
        
        # Horizontal dashed tie-line linking both dots across subplots
        ax_cool.axhline(y=T_curr, color=pt_color, ls='-', lw=1.2, alpha=0.6)
        ax_diag.axhline(y=T_curr, color=pt_color, ls='-', lw=1.2, alpha=0.6)
        
        # Active status banner at the bottom
        if T_curr > T_liq + 5:
            state_text = f"1. Охлаждение жидкого расплава L (C = 2) | T = {T_curr:.0f} °C"
            state_col = "#002C5F"
            bg_col = "#F0F4F8"
        elif abs(T_curr - T_liq) <= 5 or (T_curr < T_liq and T_curr > T_E + 5):
            state_text = f"2. Излом: выделение кристаллов A (скорость падает из-за ΔH_пл, C = 1) | T = {T_curr:.0f} °C"
            state_col = "#005AAA"
            bg_col = "#F0F7FF"
        elif abs(T_curr - T_E) <= 5:
            state_text = f"3. Площадка эвтектики: кристаллизация L → A + B (T = const, C = 0) | T = 400 °C"
            state_col = "#E70F47"
            bg_col = "#FFF0F2"
        else:
            state_text = f"4. Охлаждение смеси твердых кристаллов (A + B, C = 1) | T = {T_curr:.0f} °C"
            state_col = "#242834"
            bg_col = "#F5F7FA"
            
        fig.text(0.5, 0.02, state_text, ha='center', fontsize=9.8, fontweight='bold', color=state_col,
                 bbox=dict(boxstyle='round,pad=0.35', facecolor=bg_col, edgecolor=state_col, lw=1.1))
        
        plt.subplots_adjust(bottom=0.14, top=0.91, left=0.09, right=0.97)
        
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        im = Image.fromarray(rgba)
        frames.append(im.convert('RGB'))
        plt.close(fig)
    
    # Save the penultimate keyframe as static high-res overview
    frames[-1].save('course_materials/semester_4/lectures/diagram_single_alloy_static.png')
    
    # Add end pause frames (15 frames = ~1.2 sec pause)
    for _ in range(15):
        frames.append(frames[-1])
        
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=75,
        loop=0
    )
    print(f"Wide cooling GIF saved successfully: {output_path} ({len(frames)} frames)")

if __name__ == '__main__':
    create_cooling_gif()
