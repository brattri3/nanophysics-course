import matplotlib.pyplot as plt
import numpy as np

# Фирменный стиль ГУАП
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'DejaVu Sans'],
    'axes.edgecolor': '#004080',
    'axes.linewidth': 1.2,
    'text.color': '#111827',
    'axes.labelcolor': '#111827',
    'xtick.color': '#111827',
    'ytick.color': '#111827',
})

# 1. График: Барьер зародышеобразования
r = np.linspace(0.01, 3.5, 400)
sigma = 1.0
delta_G_V = -1.0

delta_G_vol = (4 / 3) * np.pi * (r**3) * delta_G_V
delta_G_surf = 4 * np.pi * (r**2) * sigma
delta_G_tot = delta_G_vol + delta_G_surf

r_crit = -2 * sigma / delta_G_V
G_crit = (4 / 3) * np.pi * (r_crit**3) * delta_G_V + 4 * np.pi * (
    r_crit**2
) * sigma

fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
ax.plot(
    r,
    delta_G_surf,
    '--',
    color='#0284c7',
    lw=1.8,
    label=r'Поверхность: $+4\pi r^2 \sigma$',
)
ax.plot(
    r,
    delta_G_vol,
    ':',
    color='#64748b',
    lw=1.8,
    label=r'Объем: $\frac{4}{3}\pi r^3 \Delta G_V$',
)
ax.plot(
    r,
    delta_G_tot,
    '-',
    color='#004080',
    lw=2.5,
    label=r'Полная энергия $\Delta G(r)$',
)

ax.axvline(r_crit, color='#dc2626', linestyle='--', alpha=0.7)
ax.scatter([r_crit], [G_crit], color='#dc2626', s=50, zorder=5)
ax.annotate(
    f'Критический радиус $r^*$\nБарьер $\\Delta G^*$',
    xy=(r_crit, G_crit),
    xytext=(r_crit + 0.35, G_crit * 0.88),
    arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.5),
    fontsize=10,
    fontweight='bold',
    color='#dc2626',
)

ax.axhline(0, color='#94a3b8', lw=0.8)
ax.set_xlabel('Радиус зародыша $r$, нм', fontsize=11)
ax.set_ylabel(r'Энергия Гиббса $\Delta G$', fontsize=11)
ax.set_title(
    'Термодинамика образования зародыша',
    fontsize=12,
    fontweight='bold',
    color='#004080',
    pad=10,
)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)
plt.tight_layout()
plt.savefig('chart_nucleation.png')
plt.close()

# 2. График: Уравнение Гиббса–Томсона
r_nm = np.linspace(1.2, 18, 300)
T_bulk = 1064.18
const_factor = 1.3
T_melt = (T_bulk + 273.15) * (1 - const_factor / r_nm) - 273.15

fig, ax = plt.subplots(figsize=(6.5, 4.2), dpi=300)
ax.plot(
    r_nm, T_melt, '-', color='#004080', lw=2.5, label=r'$T_m(r)$ наночастиц Au'
)
ax.axhline(
    T_bulk,
    color='#64748b',
    linestyle='--',
    lw=1.5,
    label=r'$T_{m,\infty} = 1064^\circ$C (объемный Au)',
)

idx_1_5 = np.argmin(np.abs(r_nm - 1.5))
ax.scatter([1.5], [T_melt[idx_1_5]], color='#dc2626', s=50, zorder=5)
ax.annotate(
    f'$r \\approx 1.5$ нм\n$T_m \\approx 380^\\circ$C',
    xy=(1.5, T_melt[idx_1_5]),
    xytext=(3.5, 260),
    arrowprops=dict(arrowstyle='->', color='#dc2626', lw=1.5),
    fontsize=10,
    fontweight='bold',
    color='#dc2626',
)

ax.set_xlabel('Радиус частицы $r$, нм', fontsize=11)
ax.set_ylabel(r'Температура плавления $T_m$, $^\circ$C', fontsize=11)
ax.set_title(
    'Размерный эффект плавления (Гиббс–Томсон)',
    fontsize=12,
    fontweight='bold',
    color='#004080',
    pad=10,
)
ax.set_ylim(100, 1150)
ax.grid(True, linestyle=':', alpha=0.6)
ax.legend(frameon=True, facecolor='#f8fafc', edgecolor='#cbd5e1', fontsize=9)
plt.tight_layout()
plt.savefig('chart_gibbs_thomson.png')
plt.close()
print('Графики сгенерированы.')
