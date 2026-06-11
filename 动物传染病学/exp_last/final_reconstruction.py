import pandas as pd
import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --- 1. Load Data ---
# Cq data from 4-7 columns
cq_df = pd.read_csv('exp_last/qPCR_target_4to7.csv')
cq_map = dict(zip(cq_df['Well'], cq_df['Cq']))

# Layout data from Excel (via UTF-8 CSV)
layout_df = pd.read_csv('exp_last/layout_utf8.csv', header=None).iloc[0:8, 0:5]
# Column 0 is Row letters, Columns 1-4 are 4, 5, 6, 7
layout_df.columns = ['Row', '4', '5', '6', '7']

# --- 2. Apply Reversal Logic ---
# Logic: Keep A, G, H rows fixed. Reverse B, C, D, E, F rows within each column.
# B_new category comes from F_old Cq, etc. 
# Better yet: Map the Category in the layout to the REVERSED physical well's Cq.

mapping = {
    'A': 'A',
    'B': 'F', # Physical B gets F's intended sample, so Category at B gets Cq of B? 
    # Wait, "Reverse order" means the physical loading was: A, F, E, D, C, B, G, H
    # So Category B is at physical F. Category C is at physical E.
    'C': 'E',
    'D': 'D',
    'E': 'C',
    'F': 'B',
    'G': 'G',
    'H': 'H'
}

data_rows = []
categories_map = {
    '阳性样品': 'Pos Sample',
    '阳性对照': 'Pos Ctrl',
    '肉1': 'Pork',
    'YQT': 'Pork', # YQT is Pork 2
    '丸1-1': 'Wanzi',
    '丸1-2': 'Wanzi',
    '丸2-2': 'Wanzi',
    '饺1': 'Dumpling',
    '饺2': 'Dumpling',
    '板1': 'Block',
    '板2': 'Block'
}

for idx, row_data in layout_df.iterrows():
    row_letter = row_data['Row']
    target_row = mapping[row_letter] # Where this row's sample actually ended up
    
    for col in ['4', '5', '6', '7']:
        sample_name = row_data[col]
        major_cat = categories_map.get(sample_name, 'Other')
        
        physical_well = f"{target_row}{int(col):02d}"
        cq_val = cq_map.get(physical_well, 'N/A')
        
        is_valid = cq_val != 'N/A'
        float_cq = float(cq_val) if is_valid else None
        
        data_rows.append({
            'well_original': f"{row_letter}{int(col):02d}",
            'well_physical': physical_well,
            'sample': sample_name,
            'group': major_cat,
            'cq_value': float_cq,
            'is_valid': is_valid
        })

# Save JSON
with open('exp_last/qPCR_final_reversed_data.json', 'w', encoding='utf-8') as f:
    json.dump(data_rows, f, indent=4, ensure_ascii=False)

# --- 3. Generate Composite Plot ---
df = pd.DataFrame(data_rows)
df = df[df['group'] != 'Other']

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

order = ['Pos Ctrl', 'Pos Sample', 'Pork', 'Wanzi', 'Dumpling', 'Block']
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

# Create figure
fig = plt.figure(figsize=(175/25.4, 75/25.4))
gs = fig.add_gridspec(2, 2, width_ratios=[2.2, 1.3], height_ratios=[5, 1], wspace=0.15, hspace=0.08)

ax1 = fig.add_subplot(gs[0, 0])
ax2 = fig.add_subplot(gs[1, 0], sharex=ax1)
ax_tab = fig.add_subplot(gs[:, 1])

color_map = {
    'Pos Ctrl': '#D9534F', 'Pos Sample': '#D9534F',
    'Pork': '#5BC0DE', 'Wanzi': '#5BC0DE', 'Dumpling': '#5BC0DE', 'Block': '#5BC0DE'
}

for ax in [ax1, ax2]:
    sns.stripplot(
        data=df[df['is_valid']], x='group', y='cq_value',
        hue='group', order=order, palette=color_map,
        size=6, alpha=0.85, jitter=0.15, ax=ax, zorder=2, edgecolor='black', linewidth=0.6, legend=False
    )
    for i, group in enumerate(order):
        group_data = df[(df['group'] == group) & (df['is_valid'])]['cq_value']
        if not group_data.empty:
            median = group_data.median()
            ax.hlines(median, i - 0.25, i + 0.25, color='black', linewidth=1.5, zorder=3)
    ax.spines['right'].set_visible(False)
    ax.spines['top'].set_visible(False)

ax1.set_ylim(10, 36)
ax2.set_ylim(0, 2)
ax1.spines['bottom'].set_visible(False)
ax2.spines['top'].set_visible(False)
ax1.tick_params(bottom=False, labelbottom=False)

d = 0.015
kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False, linewidth=1)
ax1.plot((-d, +d), (-d, +d), **kwargs)       
kwargs.update(transform=ax2.transAxes)  
ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs) 

ax2.set_xlabel('')
ax2.set_xticklabels(order, rotation=45, ha='right')
ax1.set_ylabel('')
ax2.set_ylabel('')
fig.text(0.02, 0.5, 'ASFV qPCR Cq Value', va='center', rotation='vertical', fontsize=9, fontweight='bold')
ax1.set_yticks(np.arange(10, 36, 5))
ax2.set_yticks([0])

# Table
ax_tab.axis('off')
table = ax_tab.table(cellText=summary_data, colLabels=["Group", "Cq (\u03bc \u00B1 \u03c3)", "n"], loc='center', cellLoc='center')
table.auto_set_font_size(False)
table.set_fontsize(8)
table.scale(1, 2.0)

for (row, col), cell in table.get_celld().items():
    cell.set_linewidth(0)
    if row == 0:
        cell.set_text_props(weight='bold')
        cell.visible_edges = 'BT'
        cell.set_linewidth(1.2)
    elif row == len(summary_data):
        cell.visible_edges = 'B'
        cell.set_linewidth(1.2)

plt.subplots_adjust(left=0.1, bottom=0.25, right=0.98, top=0.95)

fig.savefig('exp_last/ASFV_qPCR_Final_Composite.png', dpi=600, bbox_inches='tight')
fig.savefig('exp_last/ASFV_qPCR_Final_Composite.pdf', bbox_inches='tight')
print('Final reconstruction and plotting complete.')
