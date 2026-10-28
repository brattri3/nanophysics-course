import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_vls_diagram():
    fig, axes = plt.subplots(1, 3, figsize=(10, 4.2), dpi=250)
    fig.patch.set_facecolor('white')
    
    # Colors
    c_si_sub = '#7F8C8D'     # Gray Si substrate
    c_au = '#F1C40F'         # Gold catalyst
    c_eutectic = '#E67E22'   # Orange-amber Au-Si liquid
    c_wire = '#2980B9'       # Blue Si nanowire
    c_text = '#1A252F'
    c_title = '#002C5F'      # GUAP blue
    
    # Common dimensions
    center_x = 2.0
    wire_w = 1.1
    
    # -------------------------------------------------------------
    # Panel 1: Catalyst deposition
    # -------------------------------------------------------------
    ax = axes[0]
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.2, 4.2)
    ax.axis('off')
    
    # Substrate
    sub = patches.Rectangle((0.4, 0.7), 3.2, 0.7, facecolor=c_si_sub, edgecolor='#34495E', lw=1.5)
    ax.add_patch(sub)
    ax.text(center_x, 1.05, 'Si подложка', ha='center', va='center', color='white', fontweight='bold', fontsize=10.5)
    
    # Solid Au nanoparticle
    au_drop = patches.Circle((center_x, 1.8), radius=0.42, facecolor=c_au, edgecolor='#B7950B', lw=1.5)
    ax.add_patch(au_drop)
    ax.text(center_x, 1.8, 'Au', ha='center', va='center', color='#7D6608', fontweight='bold', fontsize=11)
    
    ax.set_title('1. Катализатор (Au)', fontsize=12, fontweight='bold', color=c_title, pad=12)
    ax.text(center_x, 0.35, 'Осаждение нанокапель Au\nна поверхность кремния', ha='center', va='top', fontsize=9, color=c_text)

    # -------------------------------------------------------------
    # Panel 2: Eutectic formation & gas precursor
    # -------------------------------------------------------------
    ax = axes[1]
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.2, 4.2)
    ax.axis('off')
    
    # Substrate
    sub = patches.Rectangle((0.4, 0.7), 3.2, 0.7, facecolor=c_si_sub, edgecolor='#34495E', lw=1.5)
    ax.add_patch(sub)
    ax.text(center_x, 1.05, 'Si подложка', ha='center', va='center', color='white', fontweight='bold', fontsize=10.5)
    
    # Liquid eutectic droplet (flattened on substrate)
    eut_drop = patches.Ellipse((center_x, 1.7), width=1.1, height=0.65, facecolor=c_eutectic, edgecolor='#A04000', lw=1.5)
    ax.add_patch(eut_drop)
    ax.text(center_x, 1.7, 'Au–Si (ж)', ha='center', va='center', color='white', fontweight='bold', fontsize=10)
    
    # Gas precursor arrows (SiH4 -> Si + 2H2)
    ax.annotate(r'$\mathrm{SiH_4} \to \mathrm{Si} + 2\mathrm{H_2}$', xy=(center_x, 2.1), xytext=(center_x, 3.1),
                ha='center', va='bottom', fontsize=10, fontweight='bold', color='#C0392B',
                arrowprops=dict(arrowstyle='->', color='#C0392B', lw=2, mutation_scale=15))
    
    ax.set_title('2. Плавление и насыщение', fontsize=12, fontweight='bold', color=c_title, pad=12)
    ax.text(center_x, 0.35, r'Нагрев $T > 363^\circ\mathrm{C}$' + '\nОбразование эвтектики и приток Si', ha='center', va='top', fontsize=9, color=c_text)

    # -------------------------------------------------------------
    # Panel 3: Nanowire Growth
    # -------------------------------------------------------------
    ax = axes[2]
    ax.set_xlim(0, 4)
    ax.set_ylim(-0.2, 4.2)
    ax.axis('off')
    
    # Substrate
    sub = patches.Rectangle((0.4, 0.7), 3.2, 0.7, facecolor=c_si_sub, edgecolor='#34495E', lw=1.5)
    ax.add_patch(sub)
    ax.text(center_x, 1.05, 'Si подложка', ha='center', va='center', color='white', fontweight='bold', fontsize=10.5)
    
    # Growing Si Nanowire
    wire_h = 1.7
    wire = patches.Rectangle((center_x - wire_w/2, 1.4), wire_w, wire_h, facecolor=c_wire, edgecolor='#1B4F72', lw=1.5)
    ax.add_patch(wire)
    ax.text(center_x, 1.4 + wire_h/2, 'Si нанонить\n(кристалл)', ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)
    
    # Catalyst droplet riding on top
    top_drop = patches.Ellipse((center_x, 1.4 + wire_h), width=wire_w, height=0.55, facecolor=c_eutectic, edgecolor='#A04000', lw=1.5)
    ax.add_patch(top_drop)
    ax.text(center_x, 1.4 + wire_h, 'Au–Si', ha='center', va='center', color='white', fontweight='bold', fontsize=9.5)
    
    # Upward growth arrow
    ax.annotate('', xy=(3.3, 3.1), xytext=(3.3, 1.6),
                arrowprops=dict(arrowstyle='->', color='#27AE60', lw=2.5, mutation_scale=15))
    ax.text(3.4, 2.35, 'Рост', color='#27AE60', fontweight='bold', fontsize=10, va='center')
    
    ax.set_title('3. Рост нанопроволоки', fontsize=12, fontweight='bold', color=c_title, pad=12)
    ax.text(center_x, 0.35, 'Осаждение Si на границе\nДиаметр задается каплей Au', ha='center', va='top', fontsize=9, color=c_text)

    plt.tight_layout()
    out_path = 'scripts/presentation_generator/diagram_vls_mechanism.png'
    plt.savefig(out_path, dpi=250, bbox_inches='tight')
    plt.close()
    print(f'VLS diagram saved to {out_path}')

if __name__ == '__main__':
    generate_vls_diagram()
