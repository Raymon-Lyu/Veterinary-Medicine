import cv2
import numpy as np
import os
import argparse

def cv2_imread(file_path):
    """Reads an image from a path (Unicode path support for Windows)."""
    try:
        return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def cv2_imwrite(file_path, img):
    """Writes an image to a path (Unicode path support for Windows)."""
    try:
        ext = os.path.splitext(file_path)[1]
        result, nparr = cv2.imencode(ext, img)
        if result:
            nparr.tofile(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error writing to {file_path}: {e}")
        return False

def draw_outlined_text(img, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1.5, thickness=3, color=(255, 255, 255), outline_color=(0, 0, 0)):
    """Draws text with an outline to make it highly legible on any background."""
    # Draw outline (black)
    cv2.putText(img, text, position, font, scale, outline_color, thickness + 4, cv2.LINE_AA)
    # Draw text (white)
    cv2.putText(img, text, position, font, scale, color, thickness, cv2.LINE_AA)

def create_2x2_grid(img_paths, labels, output_path, img_size=1000, gap=15):
    """Resizes and merges 4 images into a 2x2 grid with white gaps and subfigure labels."""
    if len(img_paths) != 4 or len(labels) != 4:
        print("Error: Exactly 4 images and 4 labels are required.")
        return False
        
    images = []
    for path, (letter, detail) in zip(img_paths, labels):
        img = cv2_imread(path)
        if img is None:
            print(f"Error reading image: {path}")
            return False
        
        # Resize to uniform square size
        img_resized = cv2.resize(img, (img_size, img_size), interpolation=cv2.INTER_CUBIC)
        
        # Draw Subpanel Letter (Top-Left)
        if letter:
            draw_outlined_text(img_resized, letter, (50, 80), scale=2.0, thickness=4)
            
        # Draw Detail/Concentration Label (Top-Right)
        if detail:
            text_size = cv2.getTextSize(detail, cv2.FONT_HERSHEY_SIMPLEX, 1.5, 3)[0]
            text_x = img_size - text_size[0] - 50
            draw_outlined_text(img_resized, detail, (text_x, 80), scale=1.5, thickness=3)
            
        images.append(img_resized)
        
    # Create the canvas with a white gap
    grid_size = img_size * 2 + gap
    canvas = np.ones((grid_size, grid_size, 3), dtype=np.uint8) * 255
    
    # Place images onto the canvas
    # Top-Left (A)
    canvas[0:img_size, 0:img_size] = images[0]
    # Top-Right (B)
    canvas[0:img_size, img_size + gap:grid_size] = images[1]
    # Bottom-Left (C)
    canvas[img_size + gap:grid_size, 0:img_size] = images[2]
    # Bottom-Right (D)
    canvas[img_size + gap:grid_size, img_size + gap:grid_size] = images[3]
    
    # Save the combined image
    success = cv2_imwrite(output_path, canvas)
    if success:
        print(f"Grid saved successfully to: {output_path}")
    else:
        print(f"Failed to save grid to: {output_path}")
    return success

def main():
    parser = argparse.ArgumentParser(description="Combine 4 images into a 2x2 publication-quality figure panel.")
    parser.add_argument("--i1", type=str, required=True, help="Path to Image 1 (Top-Left, 0%)")
    parser.add_argument("--i2", type=str, required=True, help="Path to Image 2 (Top-Right, 5%)")
    parser.add_argument("--i3", type=str, required=True, help="Path to Image 3 (Bottom-Left, 10%)")
    parser.add_argument("--i4", type=str, required=True, help="Path to Image 4 (Bottom-Right, 20%)")
    parser.add_argument("--o", type=str, required=True, help="Path to save the combined image")
    
    parser.add_argument("--l1", type=str, default="0%", help="Label for Image 1")
    parser.add_argument("--l2", type=str, default="5%", help="Label for Image 2")
    parser.add_argument("--l3", type=str, default="10%", help="Label for Image 3")
    parser.add_argument("--l4", type=str, default="20%", help="Label for Image 4")
    
    parser.add_argument("--size", type=int, default=1000, help="Uniform size for each square sub-image (pixels)")
    parser.add_argument("--gap", type=int, default=15, help="White gap width between panels (pixels)")
    
    args = parser.parse_args()
    
    img_paths = [args.i1, args.i2, args.i3, args.i4]
    labels = [
        ("A", args.l1),
        ("B", args.l2),
        ("C", args.l3),
        ("D", args.l4)
    ]
    
    create_2x2_grid(img_paths, labels, args.o, img_size=args.size, gap=args.gap)

if __name__ == "__main__":
    main()
