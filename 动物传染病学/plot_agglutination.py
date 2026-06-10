import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

# Nature-figure API specifications
mpl.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "svg.fonttype": "none",     # editable text in SVG
    "pdf.fonttype": 42,         # editable TrueType text in PDF
    "font.size": 7,             
    "axes.spines.right": False,
    "axes.spines.top": False,
    "axes.spines.left": False,
    "axes.spines.bottom": False,
    "axes.linewidth": 0.8,
})

def save_pub_py(fig, filename, dpi=600):
    fig.savefig(f"{filename}.svg", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(f"{filename}.pdf", bbox_inches="tight", pad_inches=0.02)
    fig.savefig(f"{filename}.tiff", dpi=dpi, bbox_inches="tight", pad_inches=0.02)

def main():
    img_path = "ningji.jpg"
    if not os.path.exists(img_path):
        print(f"Error: {img_path} not found.")
        return

    try:
        img = Image.open(img_path)
        img_array = np.array(img)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    h, w, c = img_array.shape

    # Cropping strategy to isolate the drops and remove blank slide margins
    # Adjusting empirically based on typical slide layouts
    top_crop = img_array[int(h*0.02):int(h*0.48), int(w*0.15):int(w*0.85)]
    bottom_crop = img_array[int(h*0.52):int(h*0.95), int(w*0.15):int(w*0.85)]

    # Figure Contract: Single column width (89mm ~ 3.5 inches)
    # Using a 2x1 grid, stacked vertically
    fig, axes = plt.subplots(2, 1, figsize=(3.5, 3.8), dpi=300, gridspec_kw={'hspace': 0.05})

    # Panel A: Positive Reaction
    ax0 = axes[0]
    ax0.imshow(top_crop)
    ax0.set_xticks([])
    ax0.set_yticks([])
    
    # Panel Label A
    ax0.text(0.02, 0.95, "A", transform=ax0.transAxes, fontsize=9, fontweight='bold', 
             va='top', ha='left', color='black', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
    
    # Description Label Positive
    ax0.text(0.02, 0.05, "Positive\n(Antibody + Antigen)", transform=ax0.transAxes, 
             fontsize=7, va='bottom', ha='left', color='black', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

    # Panel B: Negative Reaction
    ax1 = axes[1]
    ax1.imshow(bottom_crop)
    ax1.set_xticks([])
    ax1.set_yticks([])
    
    # Panel Label B
    ax1.text(0.02, 0.95, "B", transform=ax1.transAxes, fontsize=9, fontweight='bold', 
             va='top', ha='left', color='black', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))
    
    # Description Label Negative
    ax1.text(0.02, 0.05, "Negative\n(Serum + Antigen)", transform=ax1.transAxes, 
             fontsize=7, va='bottom', ha='left', color='black', 
             bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))

    # Save outputs
    output_prefix = "Agglutination_Assay_Plate"
    save_pub_py(fig, output_prefix)
    print(f"Success! Saved figures to {output_prefix}.(svg|pdf|tiff)")

if __name__ == "__main__":
    main()
