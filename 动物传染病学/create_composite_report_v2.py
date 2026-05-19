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
    "font.size": 7.5,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight")
    fig.savefig(f"{filename}.pdf", bbox_inches="tight")
    fig.savefig(f"{filename}.png", dpi=dpi, bbox_inches="tight")
    print(f"Refined composite figure saved as {filename}.svg/pdf/png")

# 1. Load and Flip Images
ha_img = mpimg.imread('HA.jpg')
hi_img = mpimg.imread('HI.jpg')
ha_img_flipped = np.fliplr(ha_img)
hi_img_flipped = np.fliplr(hi_img)

# 2. Setup Figure Layout (Horizontal side-by-side for images)
# 10 inches wide, 6.5 inches tall
fig = plt.figure(figsize=(10, 6.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.35], hspace=0.25, wspace=0.1)

# --- Panel (a): HA Plate (Left) ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(ha_img_flipped)
ax1.set_axis_off()
ax1.set_title('a  Virus HA Assay (Well 1-12)', loc='left', fontweight='bold', pad=12)
# Well labels on HA
for i in range(12):
    ax1.text(ha_img_flipped.shape[1] * (i + 0.5) / 12, -30, str(i+1), 
             ha='center', fontsize=6, color='#E64B35', fontweight='bold')

# --- Panel (b): HI Plate (Right) ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(hi_img_flipped)
ax2.set_axis_off()
ax2.set_title('b  Serum HI Assay (PB, A1-A3)', loc='left', fontweight='bold', pad=12)
# Row labels on HI
rows = ["PB", "A1", "A2", "A3"]
for i, label in enumerate(rows):
    # Adjusting vertical position based on visual observation of the wells in hi_img
    ax2.text(-40, hi_img_flipped.shape[0] * (i + 1.2) / 6.5, label, 
             va='center', ha='right', fontsize=8, fontweight='bold', color='#4DBBD5')

# --- Panel (c): Results Table (Bottom) ---
ax3 = fig.add_subplot(gs[1, :])
ax3.set_axis_off()

# Table Data
table_data = [
    ["Assay Type", "Sample Group", "Observation Description", "Final Titer ($log_2$)"],
    ["HA (Virus)", "Standard Ag", "Complete agglutination observed up to Well 9", "9"],
    ["HI (Serum)", "Positive Blood (PB)", "Complete inhibition observed up to Well 11", "11"],
    ["HI (Serum)", "Group A1", "Complete inhibition observed up to Well 10", "10"],
    ["HI (Serum)", "Group A2", "Complete inhibition observed up to Well 7", "7"],
    ["HI (Serum)", "Group A3", "Complete inhibition observed up to Well 9", "9"]
]

# Create the table with better styling
the_table = ax3.table(cellText=table_data, loc='center', cellLoc='center', edges='horizontal')
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)
the_table.scale(0.95, 2.0)

# Header formatting
for j in range(len(table_data[0])):
    cell = the_table[0, j]
    cell.set_text_props(fontweight='bold', color='#333333')
    cell.set_facecolor('#F0F0F0')
    cell.visible_edges = 'B' # Only bottom line for header

# Add a clean title for the table section
fig.text(0.05, 0.28, 'c  Summary of Quantified Experimental Data', fontweight='bold', fontsize=9)

# Adjust layout manually to prevent overlaps
plt.subplots_adjust(top=0.9, bottom=0.05, left=0.05, right=0.95)

save_pub_py(fig, "Scientific_Report_Refined_Layout")
plt.close(fig)
