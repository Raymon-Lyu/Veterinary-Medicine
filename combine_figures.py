import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.image as mpimg
import numpy as np
import os
from lifelines.statistics import logrank_test

# --- Nature Figure Styling ---
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

# --- Configuration & Paths ---
base_dir = r"D:\just_soso\horse cow\Veterinary Medicine"
csv_path = os.path.join(base_dir, "动物传染病学", "data.csv")
img_dir = os.path.join(base_dir, "动物传染病学")

img_paths = {
    "CRL": [os.path.join(img_dir, f"CRL_day{i}.jpg") for i in range(1, 5)],
    "PO": [os.path.join(img_dir, f"PO_day{i}.jpg") for i in range(1, 5)]
}

# --- Data Helper Functions ---
def get_event_data(row):
    days_cols = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']
    durations, events = [], []
    initial = int(row['Day0'])
    current = initial
    for i in range(1, len(days_cols)):
        deaths = int(row[days_cols[i-1]] - row[days_cols[i]])
        for _ in range(deaths):
            durations.append(i-1)
            events.append(1)
        current -= deaths
    for _ in range(current):
        durations.append(4)
        events.append(0)
    return durations, events, initial

def get_stars(p):
    if p < 0.001: return '***'
    if p < 0.01: return '**'
    if p < 0.05: return '*'
    return 'ns'

# --- Main Figure Construction ---
# We'll use a complex GridSpec to manage the two distinct parts
fig = plt.figure(figsize=(8, 9), constrained_layout=True)
# gs_top for Survival (Panel A, B), gs_bottom for Timeline (Panel C)
gs = fig.add_gridspec(2, 1, height_ratios=[1, 1.2])

# --- PART 1: Survival Analysis (Upper) ---
gs_survival = gs[0].subgridspec(1, 2)
ax_po = fig.add_subplot(gs_survival[0, 0])
ax_ip = fig.add_subplot(gs_survival[0, 1])

df = pd.read_csv(csv_path, sep='\t')
days_cols = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']
x_ticks = [0, 1, 2, 3, 4]

survival_configs = [
    {'ax': ax_po, 'title': 'A: Survival Analysis (Oral - PO)', 'ctrl': 'CRL_1', 'groups': ['PO_low', 'PO_medium', 'PO_high'], 'color': '#1f77b4'},
    {'ax': ax_ip, 'title': 'B: Survival Analysis (IP Injection)', 'ctrl': 'CRL_2', 'groups': ['IP_low', 'IP_medium', 'IP_high'], 'color': '#d62728'}
]

styles = {
    'low':    {'marker': 'o', 'ls': ':', 'jitter': -0.8},
    'medium': {'marker': 's', 'ls': '--', 'jitter': 0.0},
    'high':   {'marker': '^', 'ls': '-', 'jitter': 0.8}
}

for cfg in survival_configs:
    ax = cfg['ax']
    c_row = df[df['group'] == cfg['ctrl']].iloc[0]
    c_dur, c_evt, n_c = get_event_data(c_row)
    c_rates = (c_row[days_cols].values / n_c) * 100
    ax.step(x_ticks, c_rates, where='post', color='black', linewidth=1.2, label=f"Control (n={n_c})")
    
    for g_name in cfg['groups']:
        row = df[df['group'] == g_name].iloc[0]
        dur, evt, n = get_event_data(row)
        lvl = g_name.split('_')[1]
        s = styles[lvl]
        res = logrank_test(dur, c_dur, event_observed_A=evt, event_observed_B=c_evt)
        stars = get_stars(res.p_value)
        rates = (row[days_cols].values / n) * 100 + s['jitter']
        ax.step(x_ticks, rates, where='post', color=cfg['color'], linestyle=s['ls'], linewidth=1.0, label=f"{g_name} (n={n})")
        ax.plot(x_ticks, rates, marker=s['marker'], color=cfg['color'], linestyle='none', markersize=3.5, markerfacecolor='white', markeredgewidth=0.7)
        if stars != 'ns':
            ax.text(4.1, rates[-1], stars, color=cfg['color'], fontsize=7, va='center', fontweight='bold')

    ax.set_title(cfg['title'], loc='left', fontsize=8, fontweight='bold')
    ax.set_xticks(x_ticks)
    ax.set_xlabel('Time (Days)')
    ax.set_ylim(-10, 110)
    ax.legend(loc='lower left', fontsize=6)

ax_po.set_ylabel('Survival Rate (%)')

# --- PART 2: Pathology Timeline (Lower) ---
gs_path = gs[1].subgridspec(4, 4, height_ratios=[0.1, 1, 1, 0.15])

# Title for Part 2
ax_title_c = fig.add_subplot(gs_path[0, :])
ax_title_c.axis('off')
ax_title_c.text(0, 0.5, 'C: Longitudinal Pathology Progression (CRL vs PO)', 
                fontsize=8, fontweight='bold', va='center')

# Image Grid
for i, group in enumerate(["CRL", "PO"]):
    for j in range(4):
        ax_img = fig.add_subplot(gs_path[i+1, j])
        try:
            img = mpimg.imread(img_paths[group][j])
            ax_img.imshow(img)
            ax_img.set_xticks([])
            ax_img.set_yticks([])
            if j == 0:
                ax_img.set_ylabel(group, fontsize=8, fontweight='bold', labelpad=5)
            if i == 0:
                ax_img.set_title(f"Day {j+1}", fontsize=7)
        except Exception:
            ax_img.text(0.5, 0.5, "Missing", ha='center', va='center')
            ax_img.axis('off')

# Timeline Arrow at the very bottom
ax_arrow = fig.add_subplot(gs_path[3, :])
ax_arrow.axis('off')
ax_arrow.annotate('', xy=(0.95, 0.7), xytext=(0.05, 0.7),
                  arrowprops=dict(arrowstyle="->", color='black', lw=1.2, mutation_scale=10))
ax_arrow.text(0.5, 0.2, "Timeline of Progression", ha='center', va='top', fontsize=8, fontweight='bold')

# --- Final Export ---
output_path = os.path.join(base_dir, "Combined_Survival_Pathology_Figure")
plt.savefig(output_path + ".png", dpi=300, bbox_inches='tight')
plt.savefig(output_path + ".pdf", bbox_inches='tight')
plt.savefig(output_path + ".svg", bbox_inches='tight')

print(f"Combined figure saved to: {output_path}.png")
