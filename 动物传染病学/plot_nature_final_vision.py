import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import cv2
import numpy as np
import os

# Ultra-dense Nature style for maximum information density
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",
    "pdf.fonttype": 42,
    "font.size": 7,
    "axes.linewidth": 0.5,
})

def process_gel_full(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None: return None
    # Contrast enhancement without aggressive cropping
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return img

def create_final_vision_figure():
    input_dir = "exp3_zs"
    pcr_files = ["12-5.11.tif", "34-5.11.tif", "56-5.11.tif", "78-5.11.tif"]
    
    # Load and prepare lane-specific crops for Perspective 2
    # Estimation of lane positions based on strip preview
    lanes_oral = []
    lanes_inj = []
    
    fig = plt.figure(figsize=(8, 6), dpi=300)
    gs = GridSpec(2, 1, height_ratios=[1.2, 0.8], hspace=0.4)
    
    # --- Panel A: Two Perspectives of PCR Results ---
    gs_a = gs[0].subgridspec(1, 2, wspace=0.3)
    
    # A1: Perspective 1 - Dose-wise Route Comparison (Original Strips)
    ax_a1_master = fig.add_subplot(gs_a[0])
    ax_a1_master.set_title("a1 | Perspective 1: Dose-wise Comparison", loc='left', fontweight='bold', fontsize=8)
    ax_a1_master.axis('off')
    
    inner_gs1 = gs_a[0].subgridspec(4, 1, hspace=0.1)
    labels = ["Ctrl", "Low", "Mid", "High"]
    for i, (f, label) in enumerate(zip(pcr_files, labels)):
        ax = fig.add_subplot(inner_gs1[i])
        img = process_gel_full(os.path.join(input_dir, f))
        if img is not None:
            # Consistent height for concatenation
            img = cv2.resize(img, (800, 200))
            ax.imshow(img, cmap='magma', aspect='auto')
            # Collect for perspective 2
            w = img.shape[1]
            lanes_oral.append(img[:, :w//2])
            lanes_inj.append(img[:, w//2:])
            
        ax.set_ylabel(label, fontsize=6, rotation=0, ha='right', va='center')
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0.25, 0.1, f"{i*2+1}", transform=ax.transAxes, color='white', ha='center', fontsize=5)
        ax.text(0.75, 0.1, f"{i*2+2}", transform=ax.transAxes, color='white', ha='center', fontsize=5)

    # A2: Perspective 2 - Route-wise Dose Trend (Re-grouped Lanes)
    ax_a2_master = fig.add_subplot(gs_a[1])
    ax_a2_master.set_title("a2 | Perspective 2: Route-wise Trend", loc='left', fontweight='bold', fontsize=8)
    ax_a2_master.axis('off')
    
    inner_gs2 = gs_a[1].subgridspec(2, 1, hspace=0.2)
    # Oral Trend
    ax_oral = fig.add_subplot(inner_gs2[0])
    oral_strip = np.hstack(lanes_oral)
    ax_oral.imshow(oral_strip, cmap='magma', aspect='auto')
    ax_oral.set_ylabel("Oral", fontsize=6, fontweight='bold')
    ax_oral.set_xticks([])
    ax_oral.set_yticks([])
    for i, l in enumerate([1,3,5,7]):
        ax_oral.text((i+0.5)/4, 0.1, f"L{l}", transform=ax_oral.transAxes, color='white', ha='center', fontsize=5)
        
    # Inj Trend
    ax_inj = fig.add_subplot(inner_gs2[1])
    inj_strip = np.hstack(lanes_inj)
    ax_inj.imshow(inj_strip, cmap='magma', aspect='auto')
    ax_inj.set_ylabel("Inj", fontsize=6, fontweight='bold')
    ax_inj.set_xticks([])
    ax_inj.set_yticks([])
    for i, l in enumerate([2,4,6,8]):
        ax_inj.text((i+0.5)/4, 0.1, f"L{l}", transform=ax_inj.transAxes, color='white', ha='center', fontsize=5)

    # --- Panel B: 16S RNA Identification ---
    ax_b = fig.add_subplot(gs[1])
    ax_b.axis('off')
    ax_b.set_title("b | 16S rRNA Sequence & Identification Analysis", loc='left', fontweight='bold', fontsize=8)
    
    seq = (
        "ACAATATGGTTAGCGCCCTCCCGAAGGTTAAGCTACCTACTTCTTTTGCAACCCACTCCCATGGTGTGACGGGCGGTGTGTACAAGGCCCGGGAACGTATTCACCGTGGCATTCTGATCC\n"
        "ACGATTACTAGCGATTCCGACTTCATGGAGTCGAGTTGCAGACTCCAATCCGGACTACGACGCACTTTATGAGGTCCGCTTGCTCTCGCGAGGTCGCTTCTCTTTGTATGCGCCATTGTAG\n"
        "CACGTGTGTAGCCCTGGTCGTAAGGGCCATGATGACTTGACGTCATCCCCACCTTCCTCCAGTTTATCACTGGCAGTCTCCTTTGAGTTCCCGACCTAATCGCTGGCAACAAAGGATAAGG\n"
        "GTTGCGCTCGTTGCGGGACTTAACCCAACATTTCACAACACGAGCTGACGACAGCCATGCAGCACCTGTCTCACAGTTCCCGAAGGCCACAAATCCATCTCTGGATTCTTCTGTGGATGTC\n"
        "AAGACCAGGTAAGGTTCTTCGCGTTGCATCGAATTAAACCACATACTCCACCGCTTGTGCGGGCCCCCGTCAATTCATTTGAGTTTTAACCTTGCGGCCGTACTCCCCAGGCGGTCTACTT\n"
        "AACGCGTTAGCTCCGGAAGCCACGCCTCAAGGGCACAACCTCCAAGTAGACATCGTTTACGGCGTGGACTACCAGGGTATCTAATCCTGTTTGCTCCCCACGCTTTCGCACCTGAGCGTCA\n"
        "GTCTTTGTCCAGGGGGCCGCCTTCGCCACCGGTATTCCTCCAGATCTCTACGCATTTCACCGCTACACCTGGAATTCTACCCCCCTCTACAAGACTCAAGCCTGCCAGTTTCGAATGCAGT\n"
        "TCCCAGGTTGAGCCCGGGGATTTCACATCCGACTTGACAGACCGCCTGCGTGCGCTTTACGCCCAGTAATTCCGATTAACGCTTGCACCCTCCGTATTACCGCGGCTGCTGGCACGGAGTTA\n"
        "GCCGGTGCTTCTTCTGCGGGTAACGTCAATTGCTGCGGTTATTAACCACAACACCTTCCTCCCCGCTGAAAGTACTTTACAACCCGAAGGCCTTCTTCATACACGCGGCATGGCTGCATCA\n"
        "GGCTTGCGCCCATTGTGCAATATTCCCCACTGCTGCCTCCCGTAGGAGTCTGGACCGTGTCTCAGTTCCAGTGTGGCTGGTCATCCTCTCAGACCAGCTAGGGATCGTCGCCTTGGTGAGCC\n"
        "GTTACCTCACCAACAAGCTAATCCCATCTGGGCACATCTGATGGCAAGAGGCCCGAAGGTCCCCCTCTTTGGTCTTGCGACGTTATGCGGTATTAGCCACCGTTTCCAGTAGTTATCCCCC\n"
        "TCCATCAGGCAGTTTCCCAGACATTACTCACCCGTCCGCCACTCGTCAGCAAAGCAGCAAGCTGCTTCCTGTTACCGTTCGACTTGCATGT"
    )
    
    # ID Summary Table in Panel B
    id_results = [
        ("Lane 3 (Oral Low)", "Escherichia coli", "Commensal/Opportunistic"),
        ("Lane 6 (Inj Mid)", "Escherichia coli", "Internal Translocation"),
        ("Lane 8 (Inj High)", "Salmonella enterica", "Confirmed Infection")
    ]
    
    ax_b.text(0, 0.85, "16S Sequence (Partial):", fontweight='bold', fontsize=6)
    ax_b.text(0, 0.45, seq, fontsize=4, fontfamily='monospace', linespacing=1.2)
    
    y_table = 0.35
    ax_b.text(0, y_table, "Sample ID Summary:", fontweight='bold', fontsize=6)
    for sample, hit, note in id_results:
        y_table -= 0.08
        color = '#E64B35FF' if "Salmonella" in hit else '#333333'
        ax_b.text(0.05, y_table, f"{sample}:", fontweight='bold', fontsize=5.5)
        ax_b.text(0.3, y_table, hit, color=color, fontsize=5.5, fontstyle='italic')
        ax_b.text(0.6, y_table, f"({note})", fontsize=5.5, color='#666666')

    output_path = "final_version/Salmonella_Publication_Final_v3"
    os.makedirs("final_version", exist_ok=True)
    fig.savefig(f"{output_path}.png", bbox_inches='tight', dpi=400)
    fig.savefig(f"{output_path}.pdf", bbox_inches='tight')
    
    print(f"Final report v3 saved as {output_path}.png/pdf")

if __name__ == "__main__":
    create_final_vision_figure()
