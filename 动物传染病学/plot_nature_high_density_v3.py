import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import matplotlib.patches as patches
import cv2
import numpy as np
import os

# Ultra-dense Nature style
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.linewidth": 0.5,
    "xtick.major.width": 0.4,
    "ytick.major.width": 0.4,
    "legend.frameon": False,
})

PALETTE = {"Primary": "#333333", "Highlight": "#E64B35FF", "Text": "#333333"}

def process_gel_v3(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    # Preservation-focused cropping
    h, w = img.shape
    return img[int(h*0.1):int(h*0.9), int(w*0.05):int(w*0.95)]

def create_two_panel_report():
    input_dir = "exp3_zs"
    pcr_files = ["12-5.11.tif", "34-5.11.tif", "56-5.11.tif", "78-5.11.tif"]
    row_labels = ["Control", "Low Dose", "Mid Dose", "High Dose"]
    lane_pairs = [("1", "2"), ("3", "4"), ("5", "6"), ("7", "8")]
    
    # Square-ish layout for high density in a document
    fig = plt.figure(figsize=(6.5, 3.5), dpi=300)
    gs = GridSpec(1, 2, width_ratios=[1.2, 1], wspace=0.3)

    # --- Panel a: PCR Electrophoresis Matrix ---
    ax_a_master = fig.add_subplot(gs[0])
    ax_a_master.set_title("a | PCR Electrophoresis (16S rRNA)", loc='left', fontweight='bold', fontsize=8)
    ax_a_master.axis('off')
    
    inner_gs = gs[0].subgridspec(4, 1, hspace=0.15)
    for i, (f_name, label, (l1, l2)) in enumerate(zip(pcr_files, row_labels, lane_pairs)):
        ax = fig.add_subplot(inner_gs[i])
        path = os.path.join(input_dir, f_name)
        gel = process_gel_v3(path)
        if gel is not None:
            ax.imshow(gel, cmap='magma', aspect='auto')
        
        ax.set_ylabel(label, fontsize=6, rotation=0, ha='right', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        
        # Highlight Lanes 3, 6, 8 as they have results
        c3 = 'yellow' if l1 == "3" else 'white'
        c6 = 'yellow' if l2 == "6" else 'white'
        c8 = 'yellow' if l2 == "8" else 'white'
        
        ax.text(0.3, 0.85, f"L{l1}", transform=ax.transAxes, color=c3 if l1=="3" else 'white', 
                fontsize=5, fontweight='bold', ha='center', va='top')
        ax.text(0.7, 0.85, f"L{l2}", transform=ax.transAxes, color=c6 if l2=="6" or l2=="8" else 'white', 
                fontsize=5, fontweight='bold', ha='center', va='top')

    # --- Panel b: Identification Table ---
    ax_c = fig.add_subplot(gs[1])
    ax_c.axis('off')
    ax_c.set_title("b | Bacterial Identification (BLAST)", loc='left', fontweight='bold', fontsize=8)
    
    results = [
        ("Lane 3 (Oral Low)", "E. coli"),
        ("Lane 6 (Inj Mid)", "E. coli"),
        ("Lane 8 (Inj High)", "Salmonella sp."),
        ("Identity (Avg)", "99.65%"),
        ("Gene Target", "16S ribosomal RNA")
    ]
    
    curr_y = 0.85
    for key, val in results:
        ax_c.text(0, curr_y, key, fontweight='bold', color=PALETTE["Text"], fontsize=6.5)
        # Highlight Salmonella in red as requested by the overall context of the project
        color = '#E64B35FF' if "Salmonella" in val else PALETTE["Text"]
        ax_c.text(0.55, curr_y, val, color=color, fontsize=6.5)
        ax_c.add_patch(patches.Rectangle((0, curr_y-0.05), 1, 0.002, color='#EEEEEE', transform=ax_c.transAxes))
        curr_y -= 0.16

    plt.tight_layout()
    output_path = "final_version/Bacterial_Identification_Summary_TwoPanel"
    fig.savefig(f"{output_path}.png", bbox_inches='tight', dpi=400)
    fig.savefig(f"{output_path}.pdf", bbox_inches='tight')
    
    print(f"Two-panel high-density figure saved as {output_path}.png/pdf")

if __name__ == "__main__":
    os.makedirs("final_version", exist_ok=True)
    create_two_panel_report()
