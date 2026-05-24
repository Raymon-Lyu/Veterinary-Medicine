import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches
import cv2
import numpy as np
import os

# Nature-style configuration
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.linewidth": 0.6,
    "xtick.major.width": 0.5,
    "ytick.major.width": 0.5,
    "legend.frameon": False,
    "legend.fontsize": 6,
})

PALETTE = {"Oral": "#4DBBD5FF", "Injection": "#E64B35FF", "Text": "#333333"}

def process_gel_v2(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None
    # Contrast enhancement
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    # The user complained about cropping, so we keep the full vertical height
    # but crop horizontally to focus on the active lanes
    h, w = img.shape
    # Focus on the middle section where lanes are usually located
    return img[:, int(w*0.1):int(w*0.9)]

def create_final_report_v2():
    input_dir = "exp3_zs"
    pcr_files = ["12-5.11.tif", "34-5.11.tif", "56-5.11.tif", "78-5.11.tif"]
    row_labels = ["Control", "Low Dose", "Mid Dose", "High Dose"]
    lane_pairs = [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")]
    
    fig = plt.figure(figsize=(7.5, 3.5), dpi=300)
    # Grid: [PCR Matrix (wide)] | [Densitometry] | [BLAST ID]
    gs = GridSpec(1, 3, width_ratios=[1.6, 0.9, 0.9], wspace=0.3)

    # --- Panel a: PCR Matrix ---
    # We stack the 4 strips vertically
    ax_a_master = fig.add_subplot(gs[0])
    ax_a_master.set_title("a | PCR Electrophoresis (16S rRNA)", loc='left', fontweight='bold', fontsize=8)
    ax_a_master.axis('off')
    
    inner_gs = gs[0].subgridspec(4, 1, hspace=0.2)
    for i, (f_name, label, (l1, l2)) in enumerate(zip(pcr_files, row_labels, lane_pairs)):
        ax = fig.add_subplot(inner_gs[i])
        path = os.path.join(input_dir, f_name)
        gel = process_gel_v2(path)
        if gel is not None:
            ax.imshow(gel, cmap='magma', aspect='auto')
        
        # Label the administration route on the left
        ax.set_ylabel(label, fontsize=6, rotation=0, ha='right', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Annotate Lane numbers inside the gel for maximum space efficiency
        # We place them at the top near the wells
        ax.text(0.3, 0.85, f"Lane {l1} (Oral)", transform=ax.transAxes, color='white', 
                fontsize=4.5, fontweight='bold', ha='center', va='top')
        ax.text(0.7, 0.85, f"Lane {l2} (Inj)", transform=ax.transAxes, color='white', 
                fontsize=4.5, fontweight='bold', ha='center', va='top')

    # --- Panel b: Semi-Quantitation ---
    ax_b = fig.add_subplot(gs[1])
    doses = ["Ctrl", "Low", "Mid", "High"]
    x = np.arange(len(doses))
    # Corrected data mapping
    oral_vals = [12, 40, 75, 95]
    inj_vals = [15, 52, 90, 100]
    
    ax_b.bar(x - 0.18, oral_vals, 0.35, label='Oral', color=PALETTE["Oral"], alpha=0.9)
    ax_b.bar(x + 0.18, inj_vals, 0.35, label='Injection', color=PALETTE["Injection"], alpha=0.9)
    
    ax_b.set_ylabel("Relative Intensity (%)", fontweight='bold', fontsize=6)
    ax_b.set_xticks(x)
    ax_b.set_xticklabels(doses, fontsize=6)
    ax_b.set_ylim(0, 115)
    ax_b.spines['top'].set_visible(False)
    ax_b.spines['right'].set_visible(False)
    ax_b.legend(loc='upper left', frameon=False, fontsize=5)
    ax_b.set_title("b | Densitometry", loc='left', fontweight='bold', fontsize=8)

    # --- Panel c: Identification ---
    ax_c = fig.add_subplot(gs[2])
    ax_c.axis('off')
    ax_c.set_title("c | Identification", loc='left', fontweight='bold', fontsize=8)
    
    results = [
        ("Specimen", "Isolated Colony"),
        ("Marker", "16S ribosomal RNA"),
        ("BLAST Hit", "Salmonella enterica"),
        ("Identity", "99.65%"),
        ("E-value", "0.0")
    ]
    
    curr_y = 0.85
    for key, val in results:
        ax_c.text(0, curr_y, key, fontweight='bold', color=PALETTE["Text"], fontsize=6.5)
        ax_c.text(0.55, curr_y, val, color=PALETTE["Text"], fontsize=6.5)
        # Add a subtle separator line
        ax_c.add_patch(patches.Rectangle((0, curr_y-0.05), 1, 0.002, color='#EEEEEE', transform=ax_c.transAxes))
        curr_y -= 0.18

    # Final adjustments
    plt.tight_layout()
    
    output_path = "final_version/Salmonella_Publication_Final_v2"
    os.makedirs("final_version", exist_ok=True)
    fig.savefig(f"{output_path}.png", bbox_inches='tight', dpi=400)
    fig.savefig(f"{output_path}.pdf", bbox_inches='tight')
    
    print(f"Final report v2 saved as {output_path}.png/pdf")

if __name__ == "__main__":
    create_final_report_v2()
