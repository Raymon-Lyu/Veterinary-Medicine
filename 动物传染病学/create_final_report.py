import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# [nature-figure] Final Polish
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8.5,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
    print(f"Final polished report saved as {filename}.svg/pdf/png")

# 1. Load and Flip Images
ha_img = mpimg.imread('HA.jpg')
hi_img = mpimg.imread('HI.jpg')
ha_img_flipped = np.fliplr(ha_img)
hi_img_flipped = np.fliplr(hi_img)

# 2. Setup Figure Layout
fig = plt.figure(figsize=(11, 8)) 
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.45], hspace=0.3, wspace=0.1)

# --- Panel (a): HA Plate ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(ha_img_flipped)
ax1.set_axis_off()
ax1.set_title('a  Virus HA Assay (Well 1-12)', loc='left', fontweight='bold', pad=15)
for i in range(12):
    ax1.text(ha_img_flipped.shape[1] * (i + 0.5) / 12, -30, str(i+1), 
             ha='center', fontsize=7, color='#E64B35', fontweight='bold')

# --- Panel (b): HI Plate ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(hi_img_flipped)
ax2.set_axis_off()
ax2.set_title('b  Serum HI Assay (PB, A1-A3)', loc='left', fontweight='bold', pad=15)
rows = ["PB", "A1", "A2", "A3"]
for i, label in enumerate(rows):
    ax2.text(-50, hi_img_flipped.shape[0] * (i + 1.2) / 6.5, label, 
             va='center', ha='right', fontsize=9, fontweight='bold', color='#4DBBD5')

# --- Panel (c): Results Table ---
ax3 = fig.add_subplot(gs[1, :])
ax3.set_axis_off()
ax3.text(0.0, 0.95, 'c  Summary of Quantified Experimental Data', fontweight='bold', fontsize=10)

# Table Data
table_data = [
    ["Assay Type", "Sample Group", "Observation Description", "Titer ($log_2$)"],
    ["HA (Virus)", "Standard Ag", "Complete agglutination observed up to Well 9", "9"],
    ["HI (Serum)", "Positive Blood (PB)", "Complete inhibition observed up to Well 11", "11"],
    ["HI (Serum)", "Group A1", "Complete inhibition observed up to Well 10", "10"],
    ["HI (Serum)", "Group A2", "Complete inhibition observed up to Well 7", "7"],
    ["HI (Serum)", "Group A3", "Complete inhibition observed up to Well 9", "9"]
]

# Set explicit column widths to prevent text cutoff
# The third column is much wider now (0.45)
col_widths = [0.15, 0.20, 0.50, 0.15]

the_table = ax3.table(cellText=table_data, loc='center', cellLoc='center', 
                      bbox=[0.0, 0.05, 1.0, 0.85], colWidths=col_widths) 
the_table.auto_set_font_size(False)
the_table.set_fontsize(8.5)

# Formatting
for (row, col), cell in the_table.get_celld().items():
    if row == 0:
        cell.set_text_props(fontweight='bold', color='#333333')
        cell.set_facecolor('#F2F2F2')
    else:
        cell.set_edgecolor('#CCCCCC')
        cell.set_linewidth(0.5)

plt.subplots_adjust(top=0.9, bottom=0.08, left=0.05, right=0.95)

save_pub_py(fig, "HI_HA_Final_Report")
plt.close(fig)
