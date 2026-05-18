import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

# --- Nature Figure Styling ---
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.8,
    "legend.frameon": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")

# --- Data Preparation ---
# Based on the summary table generated previously
data = {
    'Route': ['PO', 'PO', 'PO', 'IP', 'IP', 'IP'],
    'Dose_Level': [1, 2, 3, 1, 2, 3], # 1:low, 2:medium, 3:high
    'Dose_Label': ['Low', 'Medium', 'High'],
    'Mortality': [25.0, 0.0, 0.0, 0.0, 75.0, 100.0]
}

# Separate by route
po_mortality = [25.0, 0.0, 0.0]
ip_mortality = [0.0, 75.0, 100.0]
dose_levels = [1, 2, 3]
dose_labels = ['Low', 'Medium', 'High']

# --- Plotting ---
fig, ax = plt.subplots(figsize=(4, 3))

# Plot lines with markers
ax.plot(dose_levels, po_mortality, marker='o', color='#1f77b4', linestyle='--', label='PO (Oral)', linewidth=1.5, markersize=6)
ax.plot(dose_levels, ip_mortality, marker='s', color='#d62728', linestyle='-', label='IP (Injection)', linewidth=1.5, markersize=6)

# Labels and Styling
ax.set_xlabel('Dose Concentration')
ax.set_ylabel('Final Mortality (%)')
ax.set_xticks(dose_levels)
ax.set_xticklabels(dose_labels)
ax.set_ylim(-5, 110)
ax.set_yticks([0, 20, 40, 60, 80, 100])

# Grid for better readability in Dose-Response
ax.yaxis.grid(True, linestyle='--', alpha=0.3)

ax.legend(loc='upper left', fontsize=8)
ax.set_title('Dose-Response Relationship (Day 4)', fontsize=9, fontweight='bold')

plt.tight_layout()
save_pub_py(fig, 'Salmonella_Dose_Response')
print("Dose-Response figure saved as Salmonella_Dose_Response.png/pdf")
