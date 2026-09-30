import matplotlib.pyplot as plt
import numpy as np

# Set font styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#242834'
plt.rcParams['axes.linewidth'] = 1.2

def make_diagram_anatomy():
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=200)
    
    ax.set_xlim(0, 100)
    ax.set_ylim(200, 1200)
    ax.set_xlabel('Состав сплава, % B', fontsize=11, fontweight='bold', color='#242834')
    ax.set_ylabel('Температура T, °C', fontsize=11, fontweight='bold', color='#242834')
    ax.set_title('Анатомия диаграммы состояния', fontsize=13, fontweight='bold', color='#005AAA', pad=10)
    
    xA = np.linspace(0, 40, 100)
    yA = 1000 - 600 * (xA / 40)**1.2
    
    xB = np.linspace(40, 100, 100)
    yB = 400 + 400 * ((xB - 40) / 60)**1.2
    
    ax.plot(xA, yA, color='#005AAA', lw=2.5, label='Ликвидус (L -> кристаллизация)')
    ax.plot(xB, yB, color='#005AAA', lw=2.5)
    ax.plot([0, 100], [400, 400], color='#E70F47', lw=2.5, label='Солидус / Эвтектика (400 °C)')
    
    ax.fill_between(xA, yA, 1200, color='#005AAA', alpha=0.08)
    ax.fill_between(xB, yB, 1200, color='#005AAA', alpha=0.08)
    ax.text(50, 1050, 'Жидкий расплав (L)', fontsize=12, fontweight='bold', ha='center', color='#002C5F')
    
    ax.text(18, 550, 'L + Кристаллы A', fontsize=10, fontweight='bold', ha='center', color='#005AAA')
    ax.text(75, 550, 'L + Кристаллы B', fontsize=10, fontweight='bold', ha='center', color='#005AAA')
    ax.text(50, 280, 'Твердая смесь: (A + B)', fontsize=11, fontweight='bold', ha='center', color='#242834')
    
    T_con = 680
    x_solid = 0
    x_liq = 40 * ((1000 - T_con) / 600)**(1/1.2)
    x_sys = 12
    
    ax.plot([x_solid, x_liq], [T_con, T_con], color='#002C5F', lw=3)
    ax.plot(x_solid, T_con, 'o', color='#E70F47', markersize=8)
    ax.plot(x_liq, T_con, 'o', color='#005AAA', markersize=8)
    ax.plot(x_sys, T_con, 's', color='#242834', markersize=9, label='Точка сплава')
    
    ax.annotate('Конода (нода)', xy=(x_sys, T_con), xytext=(x_sys + 10, T_con + 100),
                arrowprops=dict(arrowstyle="->", color='#002C5F', lw=1.5),
                fontsize=11, fontweight='bold', color='#002C5F')
    
    ax.plot([x_liq, x_liq], [200, T_con], ls='--', color='#005AAA', lw=1.2)
    ax.plot([x_sys, x_sys], [200, T_con], ls='--', color='#242834', lw=1.2)
    ax.text(x_liq, 220, ' x_L', fontsize=10, fontweight='bold', color='#005AAA')
    ax.text(x_sys, 220, ' x_сплава', fontsize=10, fontweight='bold', color='#242834', ha='right')
    
    ax.legend(loc='upper right', fontsize=9, framealpha=0.9)
    plt.tight_layout()
    plt.savefig('diagram_anatomy.png')
    plt.close()

def make_diagram_lever_rule():
    fig, ax = plt.subplots(figsize=(6.2, 4.8), dpi=200)
    ax.set_xlim(-5, 105)
    ax.set_ylim(0, 10)
    ax.axis('off')
    
    ax.text(50, 9.2, 'Схема правила рычага вдоль коноды', fontsize=13, fontweight='bold', ha='center', color='#005AAA')
    
    y_bar = 6.8
    x_solid = 10
    x_sys = 38
    x_liq = 85
    
    ax.plot([x_solid, x_liq], [y_bar, y_bar], color='#242834', lw=3, zorder=1)
    ax.plot([x_solid, x_sys], [y_bar, y_bar], color='#005AAA', lw=6, zorder=2)
    ax.plot([x_sys, x_liq], [y_bar, y_bar], color='#E70F47', lw=6, zorder=2)
    
    ax.plot(x_solid, y_bar, 'o', color='#002C5F', markersize=10, zorder=3)
    ax.plot(x_liq, y_bar, 'o', color='#005AAA', markersize=10, zorder=3)
    ax.plot(x_sys, y_bar, 'D', color='#E70F47', markersize=12, zorder=4)
    
    ax.text(x_solid, y_bar + 0.6, 'Кристаллы S\n(состав x_S)', ha='center', fontsize=9.5, fontweight='bold', color='#002C5F')
    ax.text(x_sys, y_bar + 0.6, 'Сплав\n(состав x)', ha='center', fontsize=10, fontweight='bold', color='#E70F47')
    ax.text(x_liq, y_bar + 0.6, 'Расплав L\n(состав x_L)', ha='center', fontsize=9.5, fontweight='bold', color='#005AAA')
    
    ax.annotate('', xy=(x_solid, y_bar - 0.4), xytext=(x_sys, y_bar - 0.4),
                arrowprops=dict(arrowstyle='<->', color='#005AAA', lw=1.5))
    ax.text((x_solid + x_sys)/2, y_bar - 0.9, 'Отрезок l1', ha='center', fontsize=10, fontweight='bold', color='#005AAA')
    
    ax.annotate('', xy=(x_sys, y_bar - 0.4), xytext=(x_liq, y_bar - 0.4),
                arrowprops=dict(arrowstyle='<->', color='#E70F47', lw=1.5))
    ax.text((x_sys + x_liq)/2, y_bar - 0.9, 'Отрезок l2', ha='center', fontsize=10, fontweight='bold', color='#E70F47')
    
    y_beam = 3.8
    ax.plot([20, 80], [y_beam, y_beam], color='#242834', lw=2.5)
    ax.plot([50, 46, 54, 50], [y_beam, y_beam - 0.7, y_beam - 0.7, y_beam], color='#E70F47', lw=2)
    ax.text(25, y_beam + 0.4, 'Масса кристаллов m_S', ha='center', fontsize=9.5, fontweight='bold', color='#002C5F')
    ax.text(75, y_beam + 0.4, 'Масса расплава m_L', ha='center', fontsize=9.5, fontweight='bold', color='#005AAA')
    
    box_text = (
        "Уравнение моментов:   m_L · l1 = m_S · l2\n"
        "Доля расплава:        w_L = l1 / (l1 + l2)\n"
        "Доля кристаллов:      w_S = l2 / (l1 + l2)"
    )
    ax.text(50, 1.2, box_text, ha='center', va='center', fontsize=10.5, fontweight='bold',
            color='#242834', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F7FA', edgecolor='#005AAA', lw=1.2))
    
    plt.tight_layout()
    plt.savefig('diagram_lever_rule.png')
    plt.close()

def make_diagram_degrees_of_freedom():
    fig, ax = plt.subplots(figsize=(6.2, 5.2), dpi=200)
    ax.set_xlim(0, 100)
    ax.set_ylim(200, 1200)
    ax.set_xlabel('Состав сплава, % B', fontsize=11, fontweight='bold', color='#242834')
    ax.set_ylabel('Температура T, °C', fontsize=11, fontweight='bold', color='#242834')
    ax.set_title('Степени свободы f = 3 - phi (P = const)', fontsize=12.5, fontweight='bold', color='#005AAA', pad=10)
    
    xA = np.linspace(0, 40, 100)
    yA = 1000 - 600 * (xA / 40)**1.2
    xB = np.linspace(40, 100, 100)
    yB = 400 + 400 * ((xB - 40) / 60)**1.2
    
    ax.plot(xA, yA, color='#005AAA', lw=2)
    ax.plot(xB, yB, color='#005AAA', lw=2)
    ax.plot([0, 100], [400, 400], color='#E70F47', lw=2)
    
    points = [
        (50, 950, '1', '#005AAA'),
        (20, 750, '2', '#002C5F'),
        (40, 400, '3', '#E70F47'),
        (50, 280, '4', '#242834')
    ]
    
    for x, y, num, col in points:
        ax.plot(x, y, 'o', color=col, markersize=14)
        ax.text(x, y, num, ha='center', va='center', color='white', fontweight='bold', fontsize=10)
        
    card_text = (
        "1. Расплав L:     phi = 1 -> f = 3 - 1 = 2 (T и состав свободны)\n"
        "2. Зона L + A:    phi = 2 -> f = 3 - 2 = 1 (задав T, состав фиксирован)\n"
        "3. Эвтектика E:   phi = 3 -> f = 3 - 3 = 0 (точка жестко фиксирована!)\n"
        "4. Смесь A + B:   phi = 2 -> f = 3 - 2 = 1 (T свободна, составы 100%)"
    )
    ax.text(50, 100, card_text, ha='center', va='center', fontsize=9.5, fontweight='bold',
            color='#242834', bbox=dict(boxstyle='round,pad=0.5', facecolor='#F5F7FA', edgecolor='#002C5F', lw=1.2))
            
    plt.tight_layout()
    plt.savefig('diagram_degrees_of_freedom.png')
    plt.close()

def make_diagram_solid_solution():
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.8, 4.2), dpi=200, gridspec_kw={'width_ratios': [1.3, 1]})
    
    ax1.set_xlim(0, 100)
    ax1.set_ylim(900, 1150)
    ax1.set_xlabel('Содержание Au, ат.%', fontsize=9.5, fontweight='bold', color='#242834')
    ax1.set_ylabel('Температура T, °C', fontsize=9.5, fontweight='bold', color='#242834')
    ax1.set_title('Диаграмма Au-Ag (Тип II)', fontsize=11, fontweight='bold', color='#005AAA')
    
    x = np.linspace(0, 100, 100)
    y_liq = 962 + 1.02 * x - 0.001 * x**2
    y_sol = 962 + 0.85 * x + 0.0017 * x**2
    
    ax1.plot(x, y_liq, color='#005AAA', lw=2, label='Ликвидус')
    ax1.plot(x, y_sol, color='#E70F47', lw=2, label='Солидус')
    ax1.fill_between(x, y_sol, y_liq, color='#005AAA', alpha=0.1)
    
    ax1.text(50, 1090, 'Жидкий расплав (L)', fontsize=9.5, fontweight='bold', ha='center', color='#002C5F')
    ax1.text(50, 1015, 'L + alpha', fontsize=9.5, fontweight='bold', ha='center', color='#005AAA')
    ax1.text(50, 930, 'Твердый раствор alpha (Au-Ag)', fontsize=9, fontweight='bold', ha='center', color='#242834')
    ax1.legend(loc='lower right', fontsize=8)
    
    ax2.set_xlim(-0.5, 4.5)
    ax2.set_ylim(-0.5, 4.5)
    ax2.axis('off')
    ax2.set_title('Решетка твердого\nраствора замещения', fontsize=10.5, fontweight='bold', color='#002C5F')
    
    np.random.seed(12)
    is_gold = np.random.rand(5, 5) > 0.5
    for r in range(5):
        for c in range(5):
            col = '#DAA520' if is_gold[r, c] else '#A8A8A8'
            ax2.plot(c, r, 'o', color=col, markersize=14, markeredgecolor='#242834', markeredgewidth=1.0)
            if c < 4: ax2.plot([c, c+1], [r, r], color='#D0D0D0', lw=1, zorder=0)
            if r < 4: ax2.plot([c, c], [r, r+1], color='#D0D0D0', lw=1, zorder=0)
            
    ax2.plot([], [], 'o', color='#DAA520', markeredgecolor='#242834', label='Атом Au (золото)')
    ax2.plot([], [], 'o', color='#A8A8A8', markeredgecolor='#242834', label='Атом Ag (серебро)')
    ax2.legend(loc='lower center', bbox_to_anchor=(0.5, -0.15), fontsize=8, frameon=False)
    
    plt.tight_layout()
    plt.savefig('diagram_solid_solution.png')
    plt.close()

if __name__ == '__main__':
    make_diagram_anatomy()
    make_diagram_lever_rule()
    make_diagram_degrees_of_freedom()
    make_diagram_solid_solution()
    print("All 4 diagrams generated successfully!")
