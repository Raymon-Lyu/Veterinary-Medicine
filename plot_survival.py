import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import os

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
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=300, bbox_inches="tight") # PNG for quick preview

# --- Data Loading ---
file_path = r'动物传染病学\data.csv'
# The file seems to use tabs based on the preview
df = pd.read_csv(file_path, sep='\t')

# --- Plotting ---
fig, ax = plt.subplots(figsize=(4, 3))

days = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']
x_ticks = [0, 1, 2, 3, 4]

colors = {
    'CRL': '#333333',
    'PO': '#1f77b4',
    'IP': '#d62728'
}

for index, row in df.iterrows():
    group = row['group']
    values = row[days].values
    
    # Simple classification for color
    if 'CRL' in group:
        color = colors['CRL']
        ls = '-'
    elif 'PO' in group:
        color = colors['PO']
        if 'low' in group: ls = ':'
        elif 'medium' in group: ls = '--'
        else: ls = '-'
    elif 'IP' in group:
        color = colors['IP']
        if 'low' in group: ls = ':'
        elif 'medium' in group: ls = '--'
        else: ls = '-'
    else:
        color = 'gray'
        ls = '-'

    ax.step(x_ticks, values, where='post', label=group, color=color, linestyle=ls, linewidth=1.2)

ax.set_xlabel('Time (Days)')
ax.set_ylabel('Survival Count')
ax.set_xticks(x_ticks)
ax.set_ylim(0, 4.5)
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)

plt.tight_layout()
save_pub_py(fig, 'survival_curve')
print("Figure saved as survival_curve.png/pdf/svg")
