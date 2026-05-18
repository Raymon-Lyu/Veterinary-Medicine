import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# --- Nature Figure Styling (Per Skill Guidelines) ---
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,  # Standard for multi-panel Nature figures
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.linewidth": 0.6,
    "legend.frameon": False,
    "xtick.direction": "out",
    "ytick.direction": "out",
    "xtick.major.width": 0.6,
    "ytick.major.width": 0.6,
})

def save_pub_py(fig, filename):
    fig.savefig(f"{filename}.png", dpi=300, bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.svg", bbox_inches="tight")

# --- Data Preparation ---
file_path = r'动物传染病学\data.csv'
df = pd.read_csv(file_path, sep='\t')
days_cols = ['Day0', 'Day1', 'Day2', 'Day3', 'Day4']
x_ticks = [0, 1, 2, 3, 4]

def get_event_data(row):
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

# --- Figure Contract ---
# Archetype: Quantitative Grid (1x2)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(8, 3.5), sharey=True)

# Layout: Panel A (PO), Panel B (IP)
configs = [
    {
        'ax': ax1, 'title': 'A: Oral Administration (PO)', 
        'ctrl': 'CRL_1', 'groups': ['PO_low', 'PO_medium', 'PO_high'], 
        'color': '#1f77b4' # Nature Blue
    },
    {
        'ax': ax2, 'title': 'B: Intraperitoneal Injection (IP)', 
        'ctrl': 'CRL_2', 'groups': ['IP_low', 'IP_medium', 'IP_high'], 
        'color': '#d62728' # Nature Red
    }
]

styles = {
    'low':    {'marker': 'o', 'ls': ':', 'jitter': -0.8},
    'medium': {'marker': 's', 'ls': '--', 'jitter': 0.0},
    'high':   {'marker': '^', 'ls': '-', 'jitter': 0.8}
}

# --- Execution ---
for cfg in configs:
    ax = cfg['ax']
    # 1. Process Route-Specific Control
    c_row = df[df['group'] == cfg['ctrl']].iloc[0]
    c_dur, c_evt, n_c = get_event_data(c_row)
    c_rates = (c_row[days_cols].values / n_c) * 100
    
    # Plot Control
    ax.step(x_ticks, c_rates, where='post', color='black', linewidth=1.2, 
            label=f"Control (n={n_c})", zorder=2)
    # Censored Ticks for Control at Day 4
    if c_rates[-1] > 0:
        ax.plot(4, c_rates[-1], marker='|', color='black', markersize=6, mew=1)

    # 2. Process Experimental Groups
    for g_name in cfg['groups']:
        row = df[df['group'] == g_name].iloc[0]
        dur, evt, n = get_event_data(row)
        lvl = g_name.split('_')[1]
        s = styles[lvl]
        
        # Stats vs matched control
        res = logrank_test(dur, c_dur, event_observed_A=evt, event_observed_B=c_evt)
        stars = get_stars(res.p_value)
        
        # Survival Rates with Visual Jitter (De-confliction)
        rates = (row[days_cols].values / n) * 100 + s['jitter']
        
        # Plot Line
        ax.step(x_ticks, rates, where='post', color=cfg['color'], linestyle=s['ls'], 
                linewidth=1.0, label=f"{g_name} (n={n})")
        
        # Plot Distinct Markers
        ax.plot(x_ticks, rates, marker=s['marker'], color=cfg['color'], 
                linestyle='none', markersize=3.5, markerfacecolor='white', markeredgewidth=0.7)
        
        # Censored Ticks at Day 4
        if rates[-1] > -5:
            ax.plot(4, rates[-1], marker='|', color=cfg['color'], markersize=5, mew=0.7)
            
        # Significance Annotation (Pairwise Comparison)
        if stars != 'ns':
            # Position star at the end of the line
            ax.text(4.1, rates[-1], stars, color=cfg['color'], fontsize=8, va='center', fontweight='bold')

    # Formatting
    ax.set_title(cfg['title'], loc='left', fontsize=8, fontweight='bold')
    ax.set_xticks(x_ticks)
    ax.set_xlabel('Time (Days)')
    ax.set_ylim(-10, 110)
    ax.legend(loc='lower left', fontsize=6)

ax1.set_ylabel('Survival Rate (%)')
plt.suptitle('Survival Analysis of Salmonella Infection by Route and Dose', fontsize=9, fontweight='bold', y=0.98)
plt.tight_layout()

save_pub_py(fig, 'Salmonella_Survival_Professional')
print("Professional figure generated: Salmonella_Survival_Professional.png/pdf/svg")
