import pandas as pd
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Load Data ---
cq_df = pd.read_csv('exp_last/qPCR_target_4to7.csv')
cq_map = dict(zip(cq_df['Well'], cq_df['Cq']))

layout_df = pd.read_csv('exp_last/layout_utf8.csv', header=None).iloc[0:8, 0:5]
layout_df.columns = ['Row', '4', '5', '6', '7']

# --- 2. Logic & Mapping ---
# Naming rule: [Type][Source]-[Count]
# Merging rule: Same source (e.g., Dumpling 1, Dumpling 2, Pork 1, Pork 2)
# Reversal logic: Keep controls, reverse experimental rows B-F.

mapping = {
    'A': 'A', 'B': 'F', 'C': 'E', 'D': 'D', 'E': 'C', 'F': 'B', 'G': 'G', 'H': 'H'
}

categories_map = {
    '阳性样品': 'Pos Sample',
    '阳性对照': 'Pos Ctrl',
    '肉1': 'Pork 1',
    'YQT': 'Pork 2', # YQT is Pork 2
    '丸1-1': 'Wanzi 1',
    '丸1-2': 'Wanzi 1',
    '丸2-2': 'Wanzi 2',
    '饺1': 'Dumpling 1',
    '饺2': 'Dumpling 2',
    '板1': 'Block 1',
    '板2': 'Block 2'
}

data_rows = []
for col_str in ['4', '5', '6', '7']:
    col_samples = layout_df[col_str].tolist()
    row_letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
    
    is_control = [s in ['阳性样品', '阳性对照'] for s in col_samples]
    experimental_indices = [i for i, ctrl in enumerate(is_control) if not ctrl]
    reversed_experimental_indices = experimental_indices[::-1]
    
    for i in range(8):
        sample_name = col_samples[i]
        orig_row = row_letters[i]
        
        if is_control[i]:
            physical_row = orig_row
        else:
            exp_pos = experimental_indices.index(i)
            physical_row = row_letters[reversed_experimental_indices[exp_pos]]
            
        physical_well = f"{physical_row}{int(col_str):02d}"
        cq_val = cq_map.get(physical_well, 'N/A')
        
        # Grouping by source (e.g., 'Wanzi 1', 'Pork 1')
        group_name = categories_map.get(sample_name, 'Other')
        is_valid = cq_val != 'N/A'
        float_cq = float(cq_val) if is_valid else None
        
        data_rows.append({
            'sample_name': sample_name,
            'group': group_name,
            'cq_value': float_cq,
            'is_valid': is_valid
        })

# Save JSON
with open('exp_last/qPCR_source_merged_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_rows, f, indent=4, ensure_ascii=False)

# --- 3. Plotting ---
df = pd.DataFrame(data_rows)
df = df[df['group'] != 'Other']

# Order of groups for plotting
order = ['Pos Ctrl', 'Pos Sample', 'Pork 1', 'Pork 2', 'Wanzi 1', 'Wanzi 2', 'Dumpling 1', 'Dumpling 2', 'Block 1', 'Block 2']
df['group'] = pd.Categorical(df['group'], categories=order, ordered=True)

# Stats for table
summary_data = []
for cat in order:
    vals = df[(df['group'] == cat) & (df['is_valid'])]['cq_value']
    if len(vals) > 1:
        summary_data.append([cat, f"{vals.mean():.2f} \u00B1 {vals.std():.2f}", f"n={len(vals)}"])
    elif len(vals) == 1:
        summary_data.append([cat, f"{vals.iloc[0]:.2f}", "n=1"])
    else:
        summary_data.append([cat, "N.D.", "n=0"])

# Plotting settings
mpl.rcParams.update({'font.family': 'sans-serif', 'font.size': 8})
fig = plt.figure(figsize=(195/25.4, 80/25.4)) # Extra wide for more categories
gs = fig.add_gridspec(2, 2, width_ratios=[2.5, 1.2], height_ratios=[5, 1], wspace=0.15, hspace=0.1)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
ax_tab = fig.add_subplot(gs[:, 1])

# Color Palette
# Use two main colors: Red for controls, Teal for samples
palette = {g: '#D9534F' if 'Pos' in g else '#5BC0DE' for g in order}

for ax in [ax1, ax2]:
    sns.stripplot(
        data=df[df['is_valid']], x='group', y='cq_value', hue='group', 
        order=order, palette=palette, size=5, alpha=0.8, jitter=0.2, 
        ax=ax, zorder=2, edgecolor='black', linewidth=0.5, legend=False
    )
    for i, group in enumerate(order):
        g_data = df[(df['group'] == group) & (df['is_valid'])]['cq_value']
        if not g_data.empty:
            ax.hlines(g_data.median(), i - 0.3, i + 0.3, color='black', linewidth=1.2, zorder=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

# Formatting
ax1.set_ylim(10, 36)
ax2.set_ylim(0, 2)
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(bottom=False, labelbottom=False)

d = 0.012
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False, linewidth=1)
ax1.plot((-d, +d), (-d, +d), **kwargs)
kwargs.update(transform=ax2.transAxes)
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)

ax2.set_xlabel('')
ax2.set_xticklabels(order, rotation=45, ha='right')
fig.supylabel('ASFV qPCR Cq Value', fontsize=9, fontweight='bold')
ax1.set_yticks(np.arange(10, 36, 5))
ax2.set_yticks([0])

# Table
ax_tab.axis('off')
table = ax_tab.table(cellText=summary_data, colLabels=["Group", "Cq (\u03bc \u00B1 \u03c3)", "n"], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(7.5)
table.scale(1, 1.8)

for (row, col), cell in table.get_celld().items():
    cell.set_linewidth(0)
    if row == 0:
        cell.visible_edges = 'BT'
        cell.set_linewidth(1.2)
    elif row == len(summary_data):
        cell.visible_edges = 'B'
        cell.set_linewidth(1.2)

plt.subplots_adjust(left=0.1, bottom=0.3, right=0.98, top=0.95)
fig.savefig('exp_last/ASFV_qPCR_Source_Aggregated.png', dpi=600, bbox_inches='tight')
print('Source-aggregated plot complete.')
