import cv2
import numpy as np
import os
import glob
import argparse

def cv2_imread(file_path):
    """Reads an image from a file path (supports Unicode paths on Windows)."""
    try:
        return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def cv2_imwrite(file_path, img):
    """Writes an image to a file path (supports Unicode paths on Windows)."""
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

def detect_eyepiece_field(img):
    """Detects the circular eyepiece field in the image."""
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    
    # Scale down for robust and fast processing
    scale = 500.0 / max(h, w)
    gray_resized = cv2.resize(gray, (0, 0), fx=scale, fy=scale)
    
    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray_resized, (9, 9), 2)
    
    # Otsu thresholding
    _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    
    # Morphological closing to fill holes inside the circle
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
    
    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        return None
        
    largest_contour = max(contours, key=cv2.contourArea)
    
    # Fit minimum enclosing circle
    (cx_scaled, cy_scaled), radius_scaled = cv2.minEnclosingCircle(largest_contour)
    
    # Scale back to original size
    cx = int(cx_scaled / scale)
    cy = int(cy_scaled / scale)
    radius = int(radius_scaled / scale)
    
    return cx, cy, radius

def crop_eyepiece_circle(img, cx, cy, radius, bg_style='black', padding=0):
    """Crops the image to the eyepiece circle with the specified background style."""
    h, w = img.shape[:2]
    
    if bg_style == 'square_roi':
        # Crop the maximum inscribed square to eliminate all black background
        half_side = int(radius * 0.707)
        x1 = max(0, cx - half_side)
        y1 = max(0, cy - half_side)
        x2 = min(w, cx + half_side)
        y2 = min(h, cy + half_side)
        cropped = img[y1:y2, x1:x2]
        return cropped

    # Bounding box of the circle (with padding)
    x1 = max(0, cx - radius - padding)
    y1 = max(0, cy - radius - padding)
    x2 = min(w, cx + radius + padding)
    y2 = min(h, cy + radius + padding)
    
    # Create mask for the circle
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (cx, cy), radius, 255, -1)
    
    if bg_style == 'transparent':
        # Split channels and add Alpha channel
        b, g, r = cv2.split(img)
        alpha = mask
        img_rgba = cv2.merge([b, g, r, alpha])
        cropped = img_rgba[y1:y2, x1:x2]
    elif bg_style == 'white':
        # Create white background
        white_bg = np.ones_like(img) * 255
        # Blend original image and white background using mask
        mask_3ch = cv2.merge([mask, mask, mask])
        blended = np.where(mask_3ch == 255, img, white_bg)
        cropped = blended[y1:y2, x1:x2]
    else:  # 'black'
        # Bitwise-AND mask and original image (default black background)
        result = cv2.bitwise_and(img, img, mask=mask)
        cropped = result[y1:y2, x1:x2]
        
    return cropped

def main():
    parser = argparse.ArgumentParser(description="Extract circular eyepiece fields of view from microscope images.")
    parser.add_argument("--input_dir", type=str, required=True, help="Directory containing microscope images.")
    parser.add_argument("--output_dir", type=str, default=None, help="Directory to save cropped images (default: input_dir/cropped_eyepiece).")
    parser.add_argument("--bg", type=str, choices=['black', 'white', 'transparent', 'square_roi'], default='black', help="Background style: black, white, transparent PNG, or square_roi (crops inscribed square to remove all background).")
    parser.add_argument("--padding", type=int, default=0, help="Extra padding in pixels around the circle.")
    
    args = parser.parse_args()
    
    input_dir = os.path.abspath(args.input_dir)
    if not args.output_dir:
        output_dir = os.path.join(input_dir, f"cropped_eyepiece_{args.bg}")
    else:
        output_dir = os.path.abspath(args.output_dir)
        
    os.makedirs(output_dir, exist_ok=True)
    
    # Support common image formats
    image_types = ('*.jpg', '*.jpeg', '*.png', '*.JPG', '*.JPEG', '*.PNG')
    image_paths = []
    for ext in image_types:
        image_paths.extend(glob.glob(os.path.join(input_dir, ext)))
        
    # Deduplicate image paths
    image_paths = sorted(list(set(os.path.abspath(p) for p in image_paths)))
    
    if not image_paths:
        print(f"No images found in {input_dir}")
        return
        
    print(f"Processing {len(image_paths)} images from: {input_dir}")
    print(f"Output directory: {output_dir}")
    print(f"Background style: {args.bg}")
    print("-" * 50)
    
    success_count = 0
    for path in image_paths:
        name = os.path.basename(path)
        img = cv2_imread(path)
        if img is None:
            print(f"Failed to read: {name}")
            continue
            
        circle = detect_eyepiece_field(img)
        if circle is None:
            print(f"Failed to detect circle in: {name}")
            continue
            
        cx, cy, r = circle
        cropped = crop_eyepiece_circle(img, cx, cy, r, bg_style=args.bg, padding=args.padding)
        
        # Decide output extension based on background style
        base_name, _ = os.path.splitext(name)
        out_ext = ".png" if args.bg == 'transparent' else ".jpg"
        dest_path = os.path.join(output_dir, f"cropped_{base_name}{out_ext}")
        
        if cv2_imwrite(dest_path, cropped):
            print(f"Successfully processed {name} -> saved to {os.path.basename(dest_path)} (Center: ({cx}, {cy}), Radius: {r})")
            success_count += 1
        else:
            print(f"Failed to save cropped image for {name}")
            
    print("-" * 50)
    print(f"Completed! Successfully processed {success_count}/{len(image_paths)} images.")

if __name__ == "__main__":
    main()
