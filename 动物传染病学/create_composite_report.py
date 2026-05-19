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
    print(f"Composite figure saved as {filename}.svg/pdf/png")

# 1. Load and Pre-process Images
# Based on user hint: Left in image is actually Well 12 (Right). 
# So we flip them horizontally to restore Well 1 to the left.
ha_img = mpimg.imread('HA.jpg')
hi_img = mpimg.imread('HI.jpg')

ha_img_flipped = np.fliplr(ha_img)
hi_img_flipped = np.fliplr(hi_img)

# 2. Setup Figure Layout (2 rows: Top for photos, Bottom for table)
fig = plt.figure(figsize=(8.5, 7))
gs = fig.add_gridspec(3, 2, height_ratios=[1, 1, 0.6], hspace=0.35, wspace=0.15)

# --- Panel (a): HA Plate Image ---
ax1 = fig.add_subplot(gs[0, :])
ax1.imshow(ha_img_flipped)
ax1.set_axis_off()
ax1.set_title('a  Original HA Assay Plate (Corrected Orientation)', loc='left', fontweight='bold', pad=10)
# Add Well Labels for clarity
for i in range(12):
    ax1.text(ha_img_flipped.shape[1] * (i + 0.5) / 12, -20, str(i+1), 
             ha='center', fontsize=7, color='red', fontweight='bold')

# --- Panel (b): HI Plate Image ---
ax2 = fig.add_subplot(gs[1, :])
ax2.imshow(hi_img_flipped)
ax2.set_axis_off()
ax2.set_title('b  Original HI Assay Plate (Corrected Orientation)', loc='left', fontweight='bold', pad=10)
# Add Row Labels
rows = ["PB", "A1", "A2", "A3"]
for i, label in enumerate(rows):
    ax2.text(-80, hi_img_flipped.shape[0] * (i + 1.2) / 6.5, label, 
             va='center', ha='right', fontsize=9, fontweight='bold', color='blue')

# --- Panel (c): Results Table ---
ax3 = fig.add_subplot(gs[2, :])
ax3.set_axis_off()
ax3.set_title('c  Quantified HA/HI Assay Results Summary', loc='left', fontweight='bold', pad=5)

# Table Data
table_data = [
    ["Assay Type", "Sample Group", "Observation (Agglutination End)", "Titer ($log_2$)"],
    ["HA (Virus)", "Standard Antigen", "Positive up to Well 9", "9"],
    ["HI (Serum)", "Positive Blood (PB)", "Inhibited up to Well 11", "11"],
    ["HI (Serum)", "Test Group A1", "Inhibited up to Well 10", "10"],
    ["HI (Serum)", "Test Group A2", "Inhibited up to Well 7", "7"],
    ["HI (Serum)", "Test Group A3", "Inhibited up to Well 9", "9"]
]

# Create the table
the_table = ax3.table(cellText=table_data, loc='center', cellLoc='center')
the_table.auto_set_font_size(False)
the_table.set_fontsize(8)
the_table.scale(1.0, 1.8)

# Style the table header
for j in range(len(table_data[0])):
    cell = the_table[0, j]
    cell.set_text_props(fontweight='bold', color='white')
    cell.set_facecolor('#404040')

plt.tight_layout()
save_pub_py(fig, "Plate_Images_and_Data_Report")
plt.close(fig)
