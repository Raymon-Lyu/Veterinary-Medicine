import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# [nature-figure] Publication-grade settings
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
    print(f"Fixed composite figure saved as {filename}.svg/pdf/png")

# 1. Load and Flip Images
ha_img = mpimg.imread('HA.jpg')
hi_img = mpimg.imread('HI.jpg')
ha_img_flipped = np.fliplr(ha_img)
hi_img_flipped = np.fliplr(hi_img)

# 2. Setup Figure Layout
fig = plt.figure(figsize=(10, 7.5)) # Increased height slightly for better spacing
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.45], hspace=0.3, wspace=0.15)

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
# Use ax3.set_title with large padding to avoid overlap
ax3.set_title('c  Summary of Quantified Experimental Data', loc='left', fontweight='bold', pad=10)

# Table Data
table_data = [
    ["Assay Type", "Sample Group", "Observation Description", "Final Titer ($log_2$)"],
    ["HA (Virus)", "Standard Ag", "Complete agglutination observed up to Well 9", "9"],
    ["HI (Serum)", "Positive Blood (PB)", "Complete inhibition observed up to Well 11", "11"],
    ["HI (Serum)", "Group A1", "Complete inhibition observed up to Well 10", "10"],
    ["HI (Serum)", "Group A2", "Complete inhibition observed up to Well 7", "7"],
    ["HI (Serum)", "Group A3", "Complete inhibition observed up to Well 9", "9"]
]

# Create the table
# Position it lower in the axis using bbox [left, bottom, width, height]
the_table = ax3.table(cellText=table_data, loc='center', cellLoc='center', 
                      bbox=[0.05, 0.0, 0.9, 0.85]) 
the_table.auto_set_font_size(False)
the_table.set_fontsize(8.5)

# Header and Cell formatting
for (row, col), cell in the_table.get_celld().items():
    if row == 0:
        cell.set_text_props(fontweight='bold', color='#333333')
        cell.set_facecolor('#F2F2F2')
        cell.set_edgecolor('black')
        cell.set_linewidth(1.0)
    else:
        cell.set_edgecolor('#DDDDDD')
        cell.set_linewidth(0.5)

# Adjust layout
plt.subplots_adjust(top=0.9, bottom=0.1, left=0.08, right=0.92)

save_pub_py(fig, "Scientific_Report_Final_Fixed")
plt.close(fig)
