import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.lines import Line2D
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
    # Use np.fromfile to handle non-ASCII paths (like Chinese characters)
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

def plot_comparison_figure():
    # Paths
    control_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\extracted_IMG_4533.png"
    po_path = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\exp2_zs\low_po\extracted_IMG_20260428_145240.png"
    output_dir = r"D:\just_soso\horse cow\Veterinary Medicine\动物传染病学\final_version"
    os.makedirs(output_dir, exist_ok=True)
    
    # Load images
    img_ctrl = load_image_rgb(control_path)
    img_po = load_image_rgb(po_path)
    
    # Setup Figure (2 rows, 2 columns)
    # Row 1: Full plates
    # Row 2: Zooms of Duodenum
    fig = plt.figure(figsize=(6, 5.5), dpi=300)
    gs = fig.add_gridspec(2, 2, height_ratios=[1, 0.8], hspace=0.3, wspace=0.2)
    
    # ROI for Duodenum (Top section)
    # In both images, Duodenum is roughly top-center
    def get_zoom_roi(img, cx_ratio=0.5, cy_ratio=0.25, size_ratio=0.3):
        h, w = img.shape[:2]
        cx, cy = int(w * cx_ratio), int(h * cy_ratio)
        sz = int(w * size_ratio)
        half_sz = sz // 2
        roi = img[max(0, cy-half_sz):min(h, cy+half_sz), 
                  max(0, cx-half_sz):min(w, cx+half_sz)]
        return roi, (cx-half_sz, cy-half_sz, sz, sz)

    # A. Control Full
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.imshow(img_ctrl)
    ax_a.set_title("A. Control Group (Full Plate)", loc='left')
    ax_a.axis('off')
    
    # B. PO Full
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.imshow(img_po)
    ax_b.set_title("B. PO Group (Full Plate)", loc='left')
    ax_b.axis('off')
    
    # C. Control Zoom
    ax_c = fig.add_subplot(gs[1, 0])
    roi_ctrl, box_ctrl = get_zoom_roi(img_ctrl)
    ax_c.imshow(roi_ctrl)
    ax_c.set_title("C. Control (Duodenum ROI)", loc='left')
    ax_c.axis('off')
    
    # D. PO Zoom
    ax_d = fig.add_subplot(gs[1, 1])
    roi_po, box_po = get_zoom_roi(img_po)
    ax_d.imshow(roi_po)
    ax_d.set_title("D. PO (Typical Salmonella Colonies)", loc='left')
    ax_d.axis('off')
    
    # Add Borders and Rectangles
    for ax, box in [(ax_a, box_ctrl), (ax_b, box_po)]:
        rect = patches.Rectangle((box[0], box[1]), box[2], box[3], 
                                linewidth=1, edgecolor='#E64B35', facecolor='none', linestyle='--')
        ax.add_patch(rect)
        ax.text(box[0]+box[2]//2, box[1]-10, "Duodenum", color='#E64B35', fontsize=6, ha='center', fontweight='bold')

    for ax in [ax_c, ax_d]:
        for spine in ax.spines.values():
            spine.set_visible(True)
            spine.set_edgecolor('#E64B35')
            spine.set_linewidth(1.2)
            
    # Add Connection Lines for Zoom Effect (Optional but professional)
    def add_zoom_lines(fig, ax_parent, ax_zoom, box):
        # Top right of box to top left of zoom
        con1 = patches.ConnectionPatch(
            xyA=(box[0]+box[2], box[1]), coordsA=ax_parent.transData,
            xyB=(0, 1), coordsB=ax_zoom.transAxes,
            arrowstyle="-", color='#E64B35', linewidth=0.6, linestyle='--', alpha=0.6
        )
        # Bottom right of box to bottom left of zoom
        con2 = patches.ConnectionPatch(
            xyA=(box[0]+box[2], box[1]+box[3]), coordsA=ax_parent.transData,
            xyB=(0, 0), coordsB=ax_zoom.transAxes,
            arrowstyle="-", color='#E64B35', linewidth=0.6, linestyle='--', alpha=0.6
        )
        fig.add_artist(con1)
        fig.add_artist(con2)

    add_zoom_lines(fig, ax_a, ax_c, box_ctrl)
    add_zoom_lines(fig, ax_b, ax_d, box_po)

    # Save
    output_prefix = os.path.join(output_dir, "Salmonella_Comparison_Nature_Figure")
    fig.savefig(f"{output_prefix}.png", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_prefix}.pdf", bbox_inches='tight')
    fig.savefig(f"{output_prefix}.svg", bbox_inches='tight')
    print(f"Success: Figure saved to {output_prefix}.png")

if __name__ == "__main__":
    plot_comparison_figure()
