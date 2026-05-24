import matplotlib as mpl
import matplotlib.pyplot as plt
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
    "axes.linewidth": 0.8,
})

def create_nature_figure(image_path, output_prefix):
    # Load the extracted image (BGRA)
    img_bgr = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGRA2RGBA)
    h, w = img_rgb.shape[:2]
    center = (w // 2, h // 2)

    # Define ROIs (normalized coordinates relative to center/radius)
    # These are estimated based on the previous observation of IMG_4533
    # 肠 (Duodenum) is at the top (~12 o'clock)
    # 肺 (Lung) is at top-right (~2 o'clock)
    
    # Coordinates for zoom (approximate center of the section)
    # x, y, size
    rois = {
        "Duodenum": [w//2, h//4, w//4],
        "Lung": [int(w*0.75), int(h*0.35), w//4]
    }

    # Create figure: 1 main panel (A) and 1 zoom panel (B)
    fig = plt.figure(figsize=(6, 3.5), dpi=300)
    gs = fig.add_gridspec(1, 2, width_ratios=[1.2, 1], wspace=0.15)
    
    # Panel A: Full Plate
    ax_main = fig.add_subplot(gs[0])
    ax_main.imshow(img_rgb)
    ax_main.set_title("A. Full Culture Plate", loc='left', fontweight='bold', fontsize=8)
    ax_main.axis('off')

    # Panel B: Duodenum Zoom
    ax_zoom = fig.add_subplot(gs[1])
    cx, cy, sz = rois["Duodenum"]
    half_sz = sz // 2
    
    # Extract ROI
    roi_img = img_rgb[max(0, cy-half_sz):min(h, cy+half_sz), 
                      max(0, cx-half_sz):min(w, cx+half_sz)]
    
    ax_zoom.imshow(roi_img)
    ax_zoom.set_title("B. Duodenum (High Density)", loc='left', fontweight='bold', fontsize=8)
    ax_zoom.axis('off')
    
    # Add professional border to zoom
    for spine in ax_zoom.spines.values():
        spine.set_visible(True)
        spine.set_edgecolor('#E64B35')
        spine.set_linewidth(1.5)

    # Add indicator box to main panel
    rect = patches.Rectangle(
        (cx-half_sz, cy-half_sz), sz, sz, 
        linewidth=1, edgecolor='#E64B35', facecolor='none', linestyle='--'
    )
    ax_main.add_patch(rect)
    ax_main.text(cx, cy-half_sz-15, "Duodenum", color='#E64B35', 
                 fontsize=7, fontweight='bold', ha='center', va='bottom')

    # Add Connection Arrows/Lines for the "Zoom" effect
    # Connect top-right of ROI to top-left of zoom
    con1 = patches.ConnectionPatch(
        xyA=(cx+half_sz, cy-half_sz), coordsA=ax_main.transData,
        xyB=(0, 1), coordsB=ax_zoom.transAxes,
        arrowstyle="-", color='#E64B35', linewidth=0.8, linestyle='--'
    )
    # Connect bottom-right of ROI to bottom-left of zoom
    con2 = patches.ConnectionPatch(
        xyA=(cx+half_sz, cy+half_sz), coordsA=ax_main.transData,
        xyB=(0, 0), coordsB=ax_zoom.transAxes,
        arrowstyle="-", color='#E64B35', linewidth=0.8, linestyle='--'
    )
    fig.add_artist(con1)
    fig.add_artist(con2)

    # Global adjustments
    plt.tight_layout()
    
    # Save in various formats
    output_prefix = "final_version/Full_Plate_Duodenum_Zoom_Nature"
    fig.savefig(f"{output_prefix}.png", bbox_inches='tight', dpi=300)
    fig.savefig(f"{output_prefix}.pdf", bbox_inches='tight')
    fig.savefig(f"{output_prefix}.svg", bbox_inches='tight')
    
    print(f"Figure saved as {output_prefix}.png/pdf/svg")

if __name__ == "__main__":
    image_path = "exp2_zs/extracted_IMG_4533.png"
    output_prefix = "final_version/Bacterial_Culture_Nature_Figure"
    
    # Ensure output directory exists
    os.makedirs("final_version", exist_ok=True)
    
    create_nature_figure(image_path, output_prefix)
