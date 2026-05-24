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

def plot_inset_comparison():
    # Paths
    control_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\extracted_IMG_4533.png"
    po_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\low_po\extracted_IMG_20260428_145240.png"
    output_dir = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\final_version"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load images
    img_ctrl = load_image_rgb(control_path)
    img_po = load_image_rgb(po_path)
    
    # Setup Figure (1 row, 2 columns)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.5, 3.2), dpi=300)
    plt.subplots_adjust(wspace=0.1)

    def add_panel_with_inset(ax, img, title, label):
        h, w = img.shape[:2]
        ax.imshow(img)
        ax.set_title(title, loc='left')
        ax.axis('off')
        
        # ROI for Duodenum (Top section)
        cx, cy = int(w * 0.5), int(h * 0.25)
        sz = int(w * 0.28)
        half_sz = sz // 2
        roi = img[max(0, cy-half_sz):min(h, cy+half_sz), 
                  max(0, cx-half_sz):min(w, cx+half_sz)]
        
        # Add ROI indicator box
        rect = patches.Rectangle((cx-half_sz, cy-half_sz), sz, sz, 
                                linewidth=0.8, edgecolor='#E64B35', facecolor='none', linestyle='--')
        ax.add_patch(rect)
        
        # Create Inset
        # Placement: Bottom right corner for Control, Bottom left for PO to balance? 
        # Actually, bottom right is usually safest as it's often empty.
        ax_inset = inset_axes(ax, width="40%", height="40%", loc='lower right', borderpad=0.5)
        ax_inset.imshow(roi)
        ax_inset.axis('off')
        
        # Professional border for inset
        for spine in ax_inset.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('#E64B35')
            spine.set_linewidth(1.0)
            
        ax_inset.set_title("Duodenum ROI", fontsize=6, color='#E64B35', fontweight='bold', pad=2)

    # A. Control
    add_panel_with_inset(ax1, img_ctrl, "A. Control Group", "Duodenum")
    
    # B. PO
    add_panel_with_inset(ax2, img_po, "B. PO Group", "Duodenum")

    # Final adjustments
    plt.tight_layout()
    
    # Save
    output_prefix = os.path.join(output_dir, "Salmonella_Inset_Comparison_Nature")
    fig.savefig(f"{output_prefix}.png", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_prefix}.pdf", bbox_inches='tight')
    fig.savefig(f"{output_prefix}.svg", bbox_inches='tight')
    print(f"Success: Figure saved to {output_prefix}.png")

if __name__ == "__main__":
    plot_inset_comparison()
