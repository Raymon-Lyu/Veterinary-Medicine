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
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=300, bbox_inches="tight")

# --- Data Loading & Processing ---
file_path = r'动物传染病学\data.csv'
df = pd.read_csv(file_path, sep='\t')

days = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']
x_ticks = [0, 1, 2, 3, 4]

# Calculate survival rates (%)
for day in days:
    df[f'{day}_rate'] = (df[day] / df['Day0']) * 100

rate_cols = [f'{day}_rate' for day in days]

# --- Plotting ---
fig, ax = plt.subplots(figsize=(4, 3))

colors = {
    'Control': '#333333',
    'PO': '#1f77b4',
    'IP': '#d62728'
}

# 1. Handle Control groups (Merged)
crl_data = df[df['group'].str.contains('CRL')]
crl_mean = crl_data[rate_cols].mean().values
ax.step(x_ticks, crl_mean, where='post', label='Control', color=colors['Control'], linewidth=1.5)

# 2. Handle Experimental groups
exp_df = df[~df['group'].str.contains('CRL')]

for index, row in exp_df.iterrows():
    group = row['group']
    values = row[rate_cols].values
    
    if 'PO' in group:
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

# Styling
ax.set_xlabel('Time (Days)')
ax.set_ylabel('Survival Rate (%)')
ax.set_xticks(x_ticks)
ax.set_ylim(0, 105)
ax.set_yticks([0, 20, 40, 60, 80, 100])

# Better legend management
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=7)

plt.tight_layout()
save_pub_py(fig, 'survival_curve_refined')
print("Figure saved as survival_curve_refined.png/pdf/svg")
