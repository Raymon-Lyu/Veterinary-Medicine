import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# [nature-figure] Mandatory RCParams for Publication Quality
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # Ensure text is editable in Illustrator
    "pdf.fonttype": 42,         # Ensure text is editable TrueType
    "font.size": 7,             # Standard Nature font size for labels
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "xtick.major.width": 0.8,
    "ytick.major.width": 0.8,
})

def save_pub_py(fig, filename, dpi=600):
    """[nature-figure] Standard export function"""
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
    print(f"Figures saved as {filename}.svg/pdf/png")

# Data from our mirrored-corrected analysis
ha_dilutions = np.arange(1, 13)
ha_status = [1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0] # 1:Agglutination, 0:Settling

hi_groups = ["PB", "A1", "A2", "A3"]
hi_titers = [11, 10, 7, 9]
# NPG-inspired palette for high-impact journals
colors = ["#E64B35B2", "#4DBBD5B2", "#00A087B2", "#3C3C3CB2"] 

# Figure Layout: Asymmetric mixed-modality (a: trend-like, b: comparative grid)
fig = plt.figure(figsize=(7, 3))
gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.2], wspace=0.3)

# --- Panel (a): HA Titration Evidence ---
ax1 = fig.add_subplot(gs[0, 0])
# Using step plot to mimic the discrete nature of 96-well results
ax1.step(ha_dilutions, ha_status, where='post', color='#E64B35FF', linewidth=1.2)
ax1.fill_between(ha_dilutions, ha_status, step="post", alpha=0.15, color='#E64B35FF')
ax1.axvline(x=9, color='black', linestyle='--', linewidth=0.8, alpha=0.6)
ax1.annotate(r'$2^9$', xy=(9, 0.5), xytext=(9.5, 0.6), 
             arrowprops=dict(arrowstyle="->", connectionstyle="arc3", lw=0.5),
             fontweight='bold', fontsize=8)

ax1.set_xticks(range(1, 13, 2))
ax1.set_yticks([0, 1])
ax1.set_yticklabels(['Settled', 'Aggl.'])
ax1.set_xlabel('Dilution Factor ($2^n$)', fontsize=7)
ax1.set_ylabel('Hemagglutination State', fontsize=7)
ax1.set_title('a  Virus HA Titration', loc='left', fontweight='bold', fontsize=8)

# --- Panel (b): HI Efficacy Evidence ---
ax2 = fig.add_subplot(gs[0, 1])
bars = ax2.bar(hi_groups, hi_titers, color=colors, width=0.65, edgecolor='black', linewidth=0.6)

# Adding HI Titer values as exponent labels
for bar in bars:
    yval = bar.get_height()
    ax2.text(bar.get_x() + bar.get_width()/2, yval + 0.3, f'$2^{{{int(yval)}}}$', 
            ha='center', va='bottom', fontsize=7, fontweight='bold')

# Protective threshold benchmark
ax2.axhline(y=4, color='#7F7F7FFF', linestyle='--', linewidth=0.8)
ax2.text(3.4, 4.3, 'Threshold ($2^4$)', color='#7F7F7FFF', fontsize=6, ha='right', style='italic')

ax2.set_ylim(0, 13)
ax2.set_yticks(range(0, 14, 2))
ax2.set_ylabel('HI Titer ($log_2$)', fontsize=7)
ax2.set_xlabel('Immunization Groups', fontsize=7)
ax2.set_title('b  Serum Antibody Efficacy (HI)', loc='left', fontweight='bold', fontsize=8)

plt.tight_layout()

# Execute export
save_pub_py(fig, "Nature_HI_HA_Analysis")
plt.close(fig)
