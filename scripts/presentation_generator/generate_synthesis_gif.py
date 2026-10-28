import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# Set styling
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['axes.edgecolor'] = '#242834'
plt.rcParams['axes.linewidth'] = 1.1

def create_synthesis_gif(output_path='course_materials/semester_4/lectures/thermal_analysis_synthesis.gif'):
    T_min, T_max = 200, 1180
    T_A = 1000   # Melting point A
    T_B = 800    # Melting point B
    T_E = 400    # Eutectic temperature
    
    # Exact liquidus temperatures for alloys 2 (18%) and 5 (75%)
    T_2 = float(T_A - (T_A - T_E) * (18.0 / 40.0)**1.2) # exactly 770.16 °C
    T_5 = float(T_E + (T_B - T_E) * ((75.0 - 40.0) / 60.0)**1.2) # exactly 610.03 °C
    
    # Coordinates for cooling curves (time tau, Temp T)
    curves_data = [
        # 1: Pure A
        {'name': '1: чистый A', 'x_c': 0.5, 't': [4, 8, 16, 20], 'T': [1080, T_A, T_A, 280], 
         'arrest_idx': (1, 3), 'pts_diag': [(0, T_A)],
         'desc': 'Сплав 1 (чистый A): кристаллизация при T_пл(A) = const (Φ = 2, C = 0)'},
        # 2: Hypoeutectic (18%)
        {'name': '2: доэвт. (18%)', 'x_c': 18.0, 't': [24, 29, 36, 40, 43], 'T': [1080, T_2, T_E, T_E, 270], 
         'arrest_idx': (2, 4), 'infl_idx': 1, 'pts_diag': [(18.0, T_2), (18.0, T_E)],
         'desc': 'Сплав 2 (18% B): излом ликвидуса T_2 (L+A) + площадка эвтектики T_E'},
        # 4: Eutectic (40%)
        {'name': '4: эвтектика (40%)', 'x_c': 40.0, 't': [46, 52, 60, 64], 'T': [1080, T_E, T_E, 260], 
         'arrest_idx': (1, 3), 'pts_diag': [(40.0, T_E)],
         'desc': 'Сплав 4 (эвтектика): одновременное затвердевание L → A + B при T_E'},
        # 5: Hypereutectic (75%)
        {'name': '5: заэвт. (75%)', 'x_c': 75.0, 't': [66, 70, 77, 81, 84], 'T': [1020, T_5, T_E, T_E, 270], 
         'arrest_idx': (2, 4), 'infl_idx': 1, 'pts_diag': [(75.0, T_5), (75.0, T_E)],
         'desc': 'Сплав 5 (75% B): излом ликвидуса T_5 (L+B) + площадка эвтектики T_E'},
        # 6: Pure B
        {'name': '6: чистый B', 'x_c': 99.5, 't': [86, 89, 95, 98], 'T': [920, T_B, T_B, 280], 
         'arrest_idx': (1, 3), 'pts_diag': [(100.0, T_B)],
         'desc': 'Сплав 6 (чистый B): кристаллизация при T_пл(B) = const (Φ = 2, C = 0)'}
    ]
    
    # Phase diagram curve equations
    xA = np.linspace(0, 40, 100)
    yA = T_A - (T_A - T_E) * (xA / 40)**1.2
    xB = np.linspace(40, 100, 100)
    yB = T_E + (T_B - T_E) * ((xB - 40) / 60)**1.2
    
    frames = []
    steps = [0, 1, 2, 3, 4, 5]
    
    # 2/3 width ratio: figsize=(8.2, 5.0) provides a generous wide 1.64:1 canvas
    for step in steps:
        fig, (ax_cool, ax_diag) = plt.subplots(1, 2, figsize=(8.2, 5.0), dpi=180,
                                               sharey=True,
                                               gridspec_kw={'width_ratios': [1.2, 1.1], 'wspace': 0.12})
        
        # -------------------------------------------------------------
        # LEFT: Cooling Curves
        # -------------------------------------------------------------
        ax_cool.set_xlim(0, 100)
        ax_cool.set_ylim(T_min, T_max)
        ax_cool.set_xlabel('Время охлаждения, τ', fontsize=10, fontweight='bold', color='#242834')
        ax_cool.set_ylabel('Температура T, °C', fontsize=10, fontweight='bold', color='#242834')
        ax_cool.set_title('1. Кривые охлаждения серии сплавов', fontsize=11, fontweight='bold', color='#005AAA', pad=8)
        ax_cool.tick_params(colors='#242834', labelsize=9)
        
        for idx, c in enumerate(curves_data):
            is_active = (idx == step) if step < 5 else True
            alpha = 1.0 if is_active else 0.22
            lw = 2.4 if is_active else 1.2
            col = '#005AAA' if idx not in [0, 2, 4] else ('#002C5F' if idx in [0, 4] else '#E70F47')
            
            ax_cool.plot(c['t'], c['T'], color=col, lw=lw, alpha=alpha)
            # Arrest line
            a_start, a_end = c['arrest_idx']
            arr_col = '#E70F47'
            ax_cool.plot(c['t'][a_start:a_end], c['T'][a_start:a_end], color=arr_col, lw=lw+1.2, alpha=alpha)
            
            # Badge
            badge_y = 1110 if idx in [0, 1, 2] else (1060 if idx==3 else 960)
            ax_cool.text(c['t'][0]+2, badge_y, c['name'][:7], fontsize=8, fontweight='bold',
                         color=col, ha='center', alpha=alpha,
                         bbox=dict(boxstyle='round,pad=0.2', facecolor='#FFFFFF', edgecolor=col, lw=0.8, alpha=alpha))
            
            # If current active curve has an inflection
            if is_active and 'infl_idx' in c:
                ax_cool.plot(c['t'][c['infl_idx']], c['T'][c['infl_idx']], 'o', color=col, markersize=6.5)
                
        # -------------------------------------------------------------
        # RIGHT: Phase Diagram
        # -------------------------------------------------------------
        ax_diag.set_xlim(-2, 102)
        ax_diag.set_xlabel('Состав сплава, % B', fontsize=10, fontweight='bold', color='#242834')
        ax_diag.set_title('2. Синтез фазовой диаграммы T – x', fontsize=11, fontweight='bold', color='#005AAA', pad=8)
        ax_diag.tick_params(colors='#242834', labelsize=9)
        
        # Step 5: Full synthesized diagram
        if step == 5:
            ax_diag.plot(xA, yA, color='#005AAA', lw=2.6, zorder=3)
            ax_diag.plot(xB, yB, color='#005AAA', lw=2.6, zorder=3)
            ax_diag.plot([0, 100], [T_E, T_E], color='#E70F47', lw=2.6, zorder=3)
            ax_diag.fill_between(xA, yA, T_max, color='#005AAA', alpha=0.06)
            ax_diag.fill_between(xB, yB, T_max, color='#005AAA', alpha=0.06)
            ax_diag.text(50, 1040, 'Жидкий расплав (L)', fontsize=10, fontweight='bold', ha='center', color='#002C5F')
            ax_diag.text(14, 520, 'L + A', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
            ax_diag.text(78, 520, 'L + B', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
            ax_diag.text(50, 270, 'Смесь кристаллов (A + B)', fontsize=10, fontweight='bold', ha='center', color='#242834')
            ax_diag.plot(40, T_E, 'o', color='#E70F47', markersize=7.5, zorder=5)
            ax_diag.text(42, T_E + 24, 'E', fontsize=10.5, fontweight='bold', color='#E70F47')
            
            # Show all accumulated experimental points strictly on the lines:
            for c in curves_data:
                ax_diag.axvline(x=c['x_c'], color='#242834', ls=':', lw=1.1, alpha=0.35, zorder=2)
                for pt_x, pt_T in c['pts_diag']:
                    pt_col = '#E70F47' if abs(pt_T - T_E) < 1.0 else '#005AAA'
                    ax_diag.plot(pt_x, pt_T, 'o', color=pt_col, markersize=8.0, markeredgecolor='#FFFFFF', markeredgewidth=1.2, zorder=6)
        else:
            accum_curves = curves_data[:step+1]
            for c in accum_curves:
                ax_diag.axvline(x=c['x_c'], color='#242834', ls=':', lw=1.1, alpha=0.45)
                for pt_x, pt_T in c['pts_diag']:
                    pt_col = '#E70F47' if abs(pt_T - T_E) < 1.0 else '#005AAA'
                    ax_diag.plot(pt_x, pt_T, 'o', color=pt_col, markersize=8.5, markeredgecolor='#242834', markeredgewidth=1.1)
            
            # Active curve projections
            active_c = curves_data[step]
            for pt_x, pt_T in active_c['pts_diag']:
                pt_col = '#E70F47' if abs(pt_T - T_E) < 1.0 else '#005AAA'
                ax_cool.axhline(y=pt_T, color=pt_col, ls='--', lw=1.1, alpha=0.6)
                ax_diag.axhline(y=pt_T, color=pt_col, ls='--', lw=1.1, alpha=0.6)
                
            if step >= 2:
                ax_diag.plot([0, active_c['x_c']], [T_E, T_E], color='#E70F47', lw=2.2, ls='--')
                
        # Description banner at bottom
        desc_text = curves_data[step]['desc'] if step < 5 else "6. Полный синтез: изломы образуют ликвидус, площадки T_E — солидус"
        b_col = '#E70F47' if (step in [2, 5]) else '#005AAA'
        bg_col = '#FFF5F5' if (step in [2, 5]) else '#F0F7FF'
        
        fig.text(0.5, 0.02, desc_text, ha='center', fontsize=9.8, fontweight='bold', color=b_col,
                 bbox=dict(boxstyle='round,pad=0.35', facecolor=bg_col, edgecolor=b_col, lw=1.1))
        
        plt.subplots_adjust(bottom=0.14, top=0.91, left=0.09, right=0.97)
        
        # Save frame
        fig.canvas.draw()
        rgba = np.asarray(fig.canvas.buffer_rgba())
        im = Image.fromarray(rgba)
        
        frame_rgb = im.convert('RGB')
        repeat = 18 if step < 5 else 28
        for _ in range(repeat):
            frames.append(frame_rgb)
            
        plt.close(fig)
        
    frames[0].save(
        output_path,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    print(f"Wide synthesis GIF saved successfully: {output_path} ({len(frames)} frames)")

if __name__ == '__main__':
    create_synthesis_gif()
