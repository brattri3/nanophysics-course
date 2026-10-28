import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import PchipInterpolator

def generate_nano_eutectic_diagram():
    fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=250)
    fig.patch.set_facecolor('white')
    
    # -------------------------------------------------------------
    # Macro Au-Si Phase Diagram
    # -------------------------------------------------------------
    # Liquidus Au side (Macro)
    c_macro_au = np.array([0.0, 5.0, 10.0, 18.6])
    t_macro_au = np.array([1064.0, 850.0, 600.0, 363.0])
    pchip_macro_au = PchipInterpolator(c_macro_au, t_macro_au)
    c_grid_macro_au = np.linspace(0.0, 18.6, 100)
    
    # Liquidus Si side (Macro)
    c_macro_si = np.array([18.6, 30.0, 50.0, 70.0, 100.0])
    t_macro_si = np.array([363.0, 770.0, 1100.0, 1280.0, 1414.0])
    pchip_macro_si = PchipInterpolator(c_macro_si, t_macro_si)
    c_grid_macro_si = np.linspace(18.6, 100.0, 150)
    
    # Plot Macro Liquidus
    ax.plot(c_grid_macro_au, pchip_macro_au(c_grid_macro_au), color='#002C5F', lw=2.2, label='Макро (массивный сплав)')
    ax.plot(c_grid_macro_si, pchip_macro_si(c_grid_macro_si), color='#002C5F', lw=2.2)
    # Macro Eutectic line
    ax.plot([0, 100], [363, 363], color='#002C5F', lw=1.8, ls=':')
    ax.scatter([18.6], [363], color='#002C5F', s=55, zorder=5)
    ax.text(18.6, 385, r'$E_\infty$ (363 °C)', color='#002C5F', fontweight='bold', fontsize=8.5, ha='center')

    # -------------------------------------------------------------
    # Nano Au-Si Phase Diagram (e.g. r = 5 nm)
    # -------------------------------------------------------------
    # Depression: Au drops from 1064 to ~850, Si drops from 1414 to ~1180, E drops from 363 to ~270, C_E shifts from 18.6 to ~22%
    c_nano_au = np.array([0.0, 6.0, 12.0, 22.0])
    t_nano_au = np.array([850.0, 670.0, 480.0, 270.0])
    pchip_nano_au = PchipInterpolator(c_nano_au, t_nano_au)
    c_grid_nano_au = np.linspace(0.0, 22.0, 100)
    
    c_nano_si = np.array([22.0, 35.0, 55.0, 75.0, 100.0])
    t_nano_si = np.array([270.0, 620.0, 900.0, 1060.0, 1180.0])
    pchip_nano_si = PchipInterpolator(c_nano_si, t_nano_si)
    c_grid_nano_si = np.linspace(22.0, 100.0, 150)
    
    # Plot Nano Liquidus
    ax.plot(c_grid_nano_au, pchip_nano_au(c_grid_nano_au), color='#E74C3C', lw=2.2, ls='--', label='Нано (капли $r = 5$ нм)')
    ax.plot(c_grid_nano_si, pchip_nano_si(c_grid_nano_si), color='#E74C3C', lw=2.2, ls='--')
    # Nano Eutectic line
    ax.plot([0, 100], [270, 270], color='#E74C3C', lw=1.8, ls='--')
    ax.scatter([22.0], [270], color='#E74C3C', s=55, zorder=5)
    ax.text(23.0, 215, r'$E_{\mathrm{nano}}$ (270 °C)', color='#E74C3C', fontweight='bold', fontsize=8.5, ha='left')

    # Formatting
    ax.set_xlim(0, 100)
    ax.set_ylim(150, 1500)
    ax.set_xlabel('Концентрация Si, ат. %', fontsize=9.5, fontweight='bold', color='#1A252F')
    ax.set_ylabel('Температура $T$, °C', fontsize=9.5, fontweight='bold', color='#1A252F')
    ax.set_title('Размерный сдвиг диаграммы состояния Au–Si', fontsize=11, fontweight='bold', color='#002C5F', pad=10)
    
    ax.grid(True, linestyle=':', alpha=0.5)
    ax.legend(loc='upper center', fontsize=8.5, framealpha=0.9)
    
    # Text annotations for depression
    ax.annotate('Падение $T_m$\nна ~200 °C', xy=(0, 950), xytext=(12, 1100),
                arrowprops=dict(arrowstyle='->', color='#E74C3C', lw=1.5),
                fontsize=8, color='#E74C3C', fontweight='bold', ha='center')
    
    plt.tight_layout()
    out_path = 'scripts/presentation_generator/diagram_nano_eutectic.png'
    plt.savefig(out_path, dpi=250, bbox_inches='tight')
    plt.close()
    print(f'Nano eutectic diagram saved to {out_path}')

if __name__ == '__main__':
    generate_nano_eutectic_diagram()
