import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
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
    "axes.linewidth": 0.8,
    "axes.titlesize": 8,
    "axes.titleweight": 'bold',
})

def load_image_rgb(path):
    img_bgr = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    if img_bgr is None:
        raise FileNotFoundError(f"Could not load image: {path}")
    if len(img_bgr.shape) == 3:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    elif img_bgr.shape[2] == 4:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2RGBA)
    else:
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    return img_rgb

def plot_high_density_comparison():
    # Paths
    control_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\extracted_IMG_4533.png"
    po_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\low_po\extracted_IMG_20260428_145240.png"
    output_dir = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\final_version"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load images
    img_ctrl = load_image_rgb(control_path)
    img_po = load_image_rgb(po_path)
    
    # Setup Figure (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.2, 3.8), dpi=300)
    plt.subplots_adjust(wspace=0.15)

    # --- Panel A: Control (Overview + Sterile Inset) ---
    h1, w1 = img_ctrl.shape[:2]
    ax1.imshow(img_ctrl)
    ax1.set_title("A. Control Group (Sterile)", loc='left')
    ax1.axis('off')
    
    # ROI for Duodenum zoom
    cx, cy = int(w1 * 0.5), int(h1 * 0.25)
    sz = int(w1 * 0.28)
    half_sz = sz // 2
    roi_ctrl = img_ctrl[max(0, cy-half_sz):min(h1, cy+half_sz), 
                        max(0, cx-half_sz):min(w1, cx+half_sz)]
    
    rect = patches.Rectangle((cx-half_sz, cy-half_sz), sz, sz, 
                            linewidth=0.8, edgecolor='#333333', facecolor='none', linestyle='--')
    ax1.add_patch(rect)
    
    ax_inset = inset_axes(ax1, width="38%", height="38%", loc='lower right', borderpad=0.2)
    ax_inset.imshow(roi_ctrl)
    ax_inset.set_xticks([]); ax_inset.set_yticks([])
    for spine in ax_inset.spines.values():
        spine.set_visible(True); spine.set_edgecolor('#333333'); spine.set_linewidth(0.8)
    ax_inset.set_title("Growth", fontsize=6, pad=2)

    # --- Panel B: PO Group (Systemic Infection Mapping) ---
    h2, w2 = img_po.shape[:2]
    ax2.imshow(img_po)
    ax2.set_title("B. PO Group (Systemic Infection)", loc='left')
    ax2.axis('off')
    
    # Organ labels based on the 6 sectors
    # Adjusted positions based on the actual physical markings on the plate
    labels = [
        {"name": "Intestine", "pos": (0.5, 0.12)},   # 顶部 (Top center)
        {"name": "Kidney", "pos": (0.85, 0.35)},       # 右上 (Top right) - adjusted outward
        {"name": "Lung", "pos": (0.8, 0.7)},        # 右下 (Bottom right)
        {"name": "Spleen", "pos": (0.5, 0.88)},       # 底部 (Bottom center)
        {"name": "Liver", "pos": (0.2, 0.75)},      # 左下 (Bottom left) - adjusted downward
        {"name": "Heart", "pos": (0.15, 0.35)}      # 左上 (Top left) - fixed spelling and adjusted outward
    ]
    
    for label in labels:
        lx, ly = int(w2 * label["pos"][0]), int(h2 * label["pos"][1])
        ax2.text(lx, ly, label["name"], color='white', fontsize=6, 
                 fontweight='bold', ha='center', va='center',
                 bbox=dict(facecolor='black', alpha=0.5, edgecolor='none', boxstyle='round,pad=0.2'))
    
    # Add annotation for Salmonella morphology
    '''
    ax2.annotate('Typical Salmonella colonies', 
                 xy=(int(w2*0.75), int(h2*0.18)), xytext=(int(w2*1.05), int(h2*0.05)),
                 arrowprops=dict(arrowstyle='->', color='#E64B35', linewidth=1),
                 fontsize=6, color='#E64B35', fontweight='bold', ha='right')
    '''
    # Save
    output_prefix = os.path.join(output_dir, "Salmonella_High_Density_Comparison")
    fig.savefig(f"{output_prefix}.png", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_prefix}.pdf", bbox_inches='tight')
    fig.savefig(f"{output_prefix}.svg", bbox_inches='tight')
    print(f"Success: Figure saved to {output_prefix}.png")

if __name__ == "__main__":
    plot_high_density_comparison()
