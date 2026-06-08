import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

# Nature Figure Contract
# Core conclusion: Detection of ASFV across different pooled sample matrices.
# Backend: Python (matplotlib/seaborn)

mpl.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['Arial', 'Helvetica', 'DejaVu Sans', 'sans-serif'],
    'svg.fonttype': 'none',
    'pdf.fonttype': 42,
    'font.size': 8,
    'axes.linewidth': 1.0,
    'xtick.major.width': 1.0,
    'ytick.major.width': 1.0,
    'legend.frameon': False,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f'{filename}.svg', bbox_inches='tight')
    fig.savefig(f'{filename}.pdf', bbox_inches='tight')
    fig.savefig(f'{filename}.png', dpi=dpi, bbox_inches='tight')

# Load data
with open('exp_last/qPCR_grouped_analysis.json', 'r') as f:
    raw_data = json.load(f)

rows = []
for group, wells in raw_data.items():
    major_category = group
    if group.startswith('pork'): major_category = 'Pork'
    elif group.startswith('wanzi'): major_category = 'Wanzi'
    elif group.startswith('dumpling'): major_category = 'Dumpling'
    elif group.startswith('block'): major_category = 'Block'
    elif group == 'positive_control': major_category = 'Pos Ctrl'
    elif group == 'positive_sample': major_category = 'Pos Sample'

    for well in wells:
        if well['is_valid']:
            rows.append({'Category': major_category, 'Cq': well['cq_value']})

df = pd.DataFrame(rows)

order = ['Pos Ctrl', 'Pos Sample', 'Pork', 'Wanzi', 'Dumpling', 'Block']
df['Category'] = pd.Categorical(df['Category'], categories=order, ordered=True)

# Calculate statistics for table
summary_data = []
for cat in order:
    vals = df[df['Category'] == cat]['Cq']
    if len(vals) > 1:
        summary_data.append([cat, f"{vals.mean():.2f} \u00B1 {vals.std():.2f}", f"n={len(vals)}"])
    elif len(vals) == 1:
        summary_data.append([cat, f"{vals.iloc[0]:.2f}", "n=1"])
    else:
        summary_data.append([cat, "N.D.", "n=0"])

# Create figure using GridSpec to allow table on the right
fig = plt.figure(figsize=(170/25.4, 70/25.4)) # wider figure to fit table
gs = fig.add_gridspec(2, 2, width_ratios=[2.0, 1.5], height_ratios=[5, 1], wspace=0.1, hspace=0.08)

ax1 = fig.add_subplot(gs[0, 0]) # Top plot
ax2 = fig.add_subplot(gs[1, 0], sharex=ax1) # Bottom plot
ax_tab = fig.add_subplot(gs[:, 1]) # Table spanning both rows

color_map = {
    'Pos Ctrl': '#D9534F', 'Pos Sample': '#D9534F',
    'Pork': '#5BC0DE', 'Wanzi': '#5BC0DE', 'Dumpling': '#5BC0DE', 'Block': '#5BC0DE'
}

# Plot on both axes
for ax in [ax1, ax2]:
    sns.stripplot(
        data=df, x='Category', y='Cq',
        hue='Category', order=order, palette=color_map,
        size=6, alpha=0.85, jitter=0.15, ax=ax, zorder=2, edgecolor='black', linewidth=0.6, legend=False
    )
    
    # Plot medians
    for i, group in enumerate(order):
        group_data = df[df['Category'] == group]['Cq']
        if not group_data.empty:
            median = group_data.median()
            ax.hlines(median, i - 0.25, i + 0.25, color='black', linewidth=1.5, zorder=3)
            
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

# Set limits
ax1.set_ylim(10, 36) # Top plot
ax2.set_ylim(0, 2)   # Bottom plot

# Hide spines between ax1 and ax2
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(bottom=False, labelbottom=False)

# Draw break marks
d = 0.015 # size of diagonal lines
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False, linewidth=1)
ax1.plot((-d, +d), (-d, +d), **kwargs)       
kwargs.update(transform=ax2.transAxes)  
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs) 

# Labels for plots
ax2.set_xlabel('')
ax2.set_xticklabels(order, rotation=45, ha='right')

# Common Y-label hack for broken axis
ax1.set_ylabel('')
ax2.set_ylabel('')
fig.text(0.02, 0.5, 'ASFV qPCR Cq Value', va='center', rotation='vertical', fontsize=9, fontweight='bold')

# Set ticks
ax1.set_yticks(np.arange(10, 36, 5))
ax2.set_yticks([0])

# --- Draw Table ---
ax_tab.axis('off')
table = ax_tab.table(
    cellText=summary_data,
    colLabels=["Group", "Cq (\u03bc \u00B1 \u03c3)", "Replicates"],
    loc='center',
    cellLoc='center'
)
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 1.8) # Adjust cell height

# Style the table like a scientific paper
for (row, col), cell in table.get_celld().items():
    cell.set_linewidth(0)
    if row == 0:
        cell.set_text_props(weight='bold')
        cell.visible_edges = 'BT' # Top and bottom borders for header
        cell.set_linewidth(1.0)
        cell.set_edgecolor('black')
    elif row == len(summary_data):
        cell.visible_edges = 'B' # Bottom border for last row
        cell.set_linewidth(1.0)
        cell.set_edgecolor('black')

plt.subplots_adjust(left=0.08, bottom=0.25, right=0.98, top=0.95)

# Save
save_pub_py(fig, 'exp_last/ASFV_qPCR_Results_Composite')
print('Plot and table generated successfully.')