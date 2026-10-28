import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from scipy.interpolate import PchipInterpolator

def generate_alloys_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=250)
    fig.patch.set_facecolor('white')
    
    # Macro Au-Si Liquidus curves
    c_au = np.array([0.0, 5.0, 10.0, 18.6])
    t_au = np.array([1064.0, 850.0, 600.0, 363.0])
    pchip_au = PchipInterpolator(c_au, t_au)
    c_grid_au = np.linspace(0.0, 18.6, 100)
    
    c_si = np.array([18.6, 30.0, 50.0, 70.0, 100.0])
    t_si = np.array([363.0, 770.0, 1100.0, 1280.0, 1414.0])
    pchip_si = PchipInterpolator(c_si, t_si)
    c_grid_si = np.linspace(18.6, 100.0, 150)
    
    # Plot phase diagram
    ax.plot(c_grid_au, pchip_au(c_grid_au), color='#002C5F', lw=2.2)
    ax.plot(c_grid_si, pchip_si(c_grid_si), color='#002C5F', lw=2.2)
    ax.plot([0, 100], [363, 363], color='#002C5F', lw=1.8, ls='--')
    ax.scatter([18.6], [363], color='#E74C3C', s=60, zorder=5)
    
    # Three alloys:
    # 1. Hypo-eutectic: C1 = 10% Si
    c1 = 10.0
    ax.axvline(x=c1, ymin=0.08, ymax=0.55, color='#2980B9', ls='-.', lw=1.8)
    ax.scatter([c1], [600], color='#2980B9', s=45, zorder=4)
    ax.text(c1, 160, '1. Доэвтектика\n(10% Si)', color='#2980B9', fontweight='bold', fontsize=8.5, ha='center')
    
    # 2. Eutectic: CE = 18.6% Si
    ce = 18.6
    ax.axvline(x=ce, ymin=0.08, ymax=0.35, color='#E74C3C', ls='-.', lw=1.8)
    ax.text(ce + 2, 440, '2. Эвтектика\n(18.6% Si)', color='#E74C3C', fontweight='bold', fontsize=8.5, ha='left')

    # 3. Hyper-eutectic: C2 = 45% Si
    c2 = 45.0
    ax.axvline(x=c2, ymin=0.08, ymax=0.82, color='#27AE60', ls='-.', lw=1.8)
    ax.scatter([c2], [1030], color='#27AE60', s=45, zorder=4)
    ax.text(c2, 160, '3. Заэвтектика\n(45% Si)', color='#27AE60', fontweight='bold', fontsize=8.5, ha='center')

    # Phase zone labels
    ax.text(50, 1250, 'Жидкость (L)', fontsize=10, color='#002C5F', fontweight='bold', ha='center')
    ax.text(6, 450, 'L + Au', fontsize=8.5, color='#34495E', ha='center')
    ax.text(45, 650, 'L + Si', fontsize=8.5, color='#34495E', ha='center')
    ax.text(18.6, 395, 'E (363 °C)', fontsize=8.5, color='#E74C3C', fontweight='bold', ha='center')

    # Axes styling
    ax.set_xlim(0, 70)
    ax.set_ylim(100, 1450)
    ax.set_xlabel('Концентрация Si, ат. %', fontsize=9.5, fontweight='bold', color='#1A252F')
    ax.set_ylabel('Температура $T$, °C', fontsize=9.5, fontweight='bold', color='#1A252F')
    ax.set_title('Три типа сплавов на диаграмме Au–Si', fontsize=11, fontweight='bold', color='#002C5F', pad=10)
    ax.grid(True, linestyle=':', alpha=0.5)
    
    plt.tight_layout()
    out_path = 'scripts/presentation_generator/diagram_alloys_comparison.png'
    plt.savefig(out_path, dpi=250, bbox_inches='tight')
    plt.close()
    print(f'Alloys diagram saved to {out_path}')

if __name__ == '__main__':
    generate_alloys_diagram()
