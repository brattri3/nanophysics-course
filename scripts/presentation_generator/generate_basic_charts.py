import matplotlib.pyplot as plt
import numpy as np

def draw_surface_energy():
    plt.figure(figsize=(6, 4), dpi=300)
    
    # Bulk atoms
    for x in range(1, 6):
        for y in range(1, 4):
            plt.plot(x, y, 'bo', markersize=25, alpha=0.6)
            
            # Draw bonds
            if x < 5: plt.plot([x, x+1], [y, y], 'k-', lw=1.5, zorder=0)
            if y < 3: plt.plot([x, x], [y, y+1], 'k-', lw=1.5, zorder=0)
            
    # Highlight a bulk atom
    plt.plot(3, 2, 'bo', markersize=25, label='Атом в объеме (связи уравновешены)')
    plt.plot(3, 2, 'go', markersize=25) # highlight
    
    # Highlight a surface atom
    plt.plot(3, 3, 'ro', markersize=25, label='Атом на поверхности (оборванные связи)')
    
    # Draw missing bonds for surface atom to show tension
    plt.plot([3, 3], [3, 3.5], 'r--', lw=2)
    plt.plot([3, 2.5], [3, 3.5], 'r--', lw=2)
    plt.plot([3, 3.5], [3, 3.5], 'r--', lw=2)
    
    plt.title('Природа поверхностной энергии', fontsize=16, pad=15)
    plt.legend(loc='lower center', bbox_to_anchor=(0.5, -0.25), frameon=False, fontsize=12)
    plt.axis('off')
    plt.tight_layout()
    plt.savefig('chart_surface_energy.png', bbox_inches='tight')
    plt.close()

def draw_entropy():
    plt.figure(figsize=(8, 4), dpi=300)
    
    # Solid
    plt.subplot(121)
    plt.title('Низкая энтропия\n(Кристалл)', fontsize=14)
    for x in range(1, 5):
        for y in range(1, 5):
            plt.plot(x, y, 'bo', markersize=15)
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.xticks([])
    plt.yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    
    # Gas
    plt.subplot(122)
    plt.title('Высокая энтропия\n(Газ)', fontsize=14)
    np.random.seed(42)
    for _ in range(16):
        x = np.random.uniform(0.5, 4.5)
        y = np.random.uniform(0.5, 4.5)
        plt.plot(x, y, 'ro', markersize=15)
        # Add random motion vectors
        dx = np.random.uniform(-0.5, 0.5)
        dy = np.random.uniform(-0.5, 0.5)
        plt.arrow(x, y, dx, dy, head_width=0.1, head_length=0.1, fc='r', ec='r', alpha=0.5)
        
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.xticks([])
    plt.yticks([])
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    
    plt.tight_layout()
    plt.savefig('chart_entropy.png', bbox_inches='tight')
    plt.close()

if __name__ == "__main__":
    draw_surface_energy()
    draw_entropy()
