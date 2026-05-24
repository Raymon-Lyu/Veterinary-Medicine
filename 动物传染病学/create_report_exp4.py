import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

# [nature-figure] Minimalist Publication Polish
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 8.5,
})

# Target directory
target_dir = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp4_zs"
if not os.path.exists(target_dir):
    os.makedirs(target_dir)

def save_pub_py(fig, filename, dpi=600):
    output_path = os.path.join(target_dir, filename)
    fig.savefig(f"{output_path}.svg", bbox_inches="tight")
    fig.savefig(f"{output_path}.pdf", bbox_inches="tight")
    fig.savefig(f"{output_path}.png", dpi=dpi, bbox_inches="tight")
    print(f"Final report saved in exp4_zs as {filename}.svg/pdf/png")

# 1. Load Images from exp4_zs
ha_path = os.path.join(target_dir, 'HA.jpg')
hi_path = os.path.join(target_dir, 'HI.jpg')

ha_img = mpimg.imread(ha_path)
hi_img = mpimg.imread(hi_path)
ha_img_flipped = np.fliplr(ha_img)
hi_img_flipped = np.fliplr(hi_img)

# 2. Setup Figure Layout
fig = plt.figure(figsize=(11, 7.5))
gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.4], hspace=0.1, wspace=0.1)

# --- Panel (a): HA Plate ---
ax1 = fig.add_subplot(gs[0, 0])
ax1.imshow(ha_img_flipped)
ax1.set_axis_off()
ax1.set_title('a  Virus HA Assay', loc='left', fontweight='bold', pad=25)
for i in range(12):
    ax1.text(ha_img_flipped.shape[1] * (i + 0.5) / 12, -35, str(i+1), 
             ha='center', fontsize=7, color='#E64B35', fontweight='bold')

# --- Panel (b): HI Plate ---
ax2 = fig.add_subplot(gs[0, 1])
ax2.imshow(hi_img_flipped)
ax2.set_axis_off()
ax2.set_title('b  Serum HI Assay', loc='left', fontweight='bold', pad=25)
rows = ["PB", "A1", "A2", "A3"]
for i, label in enumerate(rows):
    ax2.text(-50, hi_img_flipped.shape[0] * (i + 1.2) / 6.5, label, 
             va='center', ha='right', fontsize=9, fontweight='bold', color='#4DBBD5')

# --- Panel (c): Results Table ---
ax3 = fig.add_subplot(gs[1, :])
ax3.set_axis_off()
ax3.text(0.0, 0.95, 'c  Summary of Expert-Corrected Experimental Data', fontweight='bold', fontsize=10, color='darkred')

# Expert Corrected Data
table_data = [
    ["Assay Type", "Sample Group", "Expert Observation", "Final Titer ($log_2$)"],
    ["HA (Virus)", "Standard Ag", "Agglutination persists up to Well 10", "10"],
    ["HI (Serum)", "Positive Blood (PB)", "Inhibition persists up to Well 9", "9"],
    ["HI (Serum)", "Test Group A1", "Low/No inhibition detected", "< 2"],
    ["HI (Serum)", "Test Group A2", "Inhibition persists up to Well 2", "2"],
    ["HI (Serum)", "Test Group A3", "Low/No inhibition detected", "< 2"]
]

col_widths = [0.15, 0.20, 0.50, 0.15]
the_table = ax3.table(cellText=table_data, loc='center', cellLoc='center', 
                      bbox=[0.0, 0.05, 1.0, 0.85], colWidths=col_widths) 
the_table.auto_set_font_size(False)
the_table.set_fontsize(9)

# Formatting
for (row, col), cell in the_table.get_celld().items():
    if row == 0:
        cell.set_text_props(fontweight='bold', color='white')
        cell.set_facecolor('#333333')
    else:
        cell.set_edgecolor('#CCCCCC')
        cell.set_linewidth(0.5)
        if row > 2:
            cell.get_text().set_color('red')

plt.subplots_adjust(top=0.9, bottom=0.08, left=0.05, right=0.95)

save_pub_py(fig, "Final_Scientific_Report")
plt.close(fig)
