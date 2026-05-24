import cv2
import numpy as np
import os
from PIL import Image
from pillow_heif import register_heif_opener

# Register HEIF opener with Pillow
register_heif_opener()

def extract_petri_dish(image_path, output_path):
    print(f"Processing {image_path}...")
    
    # Load HEIC image using Pillow and convert to numpy array (OpenCV format)
    try:
        pil_img = Image.open(image_path)
        img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    except Exception as e:
        print(f"Error loading image: {e}")
        return

    # 1. Preprocessing
    # To improve performance and stability, we work on a smaller version for detection
    height, width = img.shape[:2]
    max_dim = 1000
    scale = max_dim / max(height, width)
    resized = cv2.resize(img, None, fx=scale, fy=scale)
    
    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (9, 9), 2)

    # 2. Hough Circle Transform for detecting the petri dish
    # Parameters might need tuning based on the specific images
    circles = cv2.HoughCircles(
        blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1.2, 
        minDist=resized.shape[0] // 2,
        param1=100, 
        param2=30, 
        minRadius=resized.shape[0] // 4, 
        maxRadius=resized.shape[0] // 2
    )

    if circles is not None:
        # Get the largest/strongest circle
        circles = np.uint16(np.around(circles))
        best_circle = circles[0, 0] # [x, y, r]
        
        # Scale coordinates back to original image size
        x, y, r = (best_circle / scale).astype(int)
        
        # Optimization: Shrink radius by 15% to remove the lid/wall edge
        r = int(r * 0.85)
        
        # 3. Create Alpha Channel and Extract
        # Add an alpha channel (BGRA)
        b_channel, g_channel, r_channel = cv2.split(img)
        alpha_channel = np.zeros(b_channel.shape, dtype=b_channel.dtype)
        cv2.circle(alpha_channel, (x, y), r, 255, -1)
        
        # Merge to create BGRA image
        bgra = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))
        
        # Crop to the circle
        x_start, y_start = max(0, x-r), max(0, y-r)
        x_end, y_end = min(width, x+r), min(height, y+r)
        cropped = bgra[y_start:y_end, x_start:x_end]

        # 4. Save result (PNG supports transparency)
        cv2.imwrite(output_path, cropped)
        print(f"Successfully saved extracted dish to {output_path}")
    else:
        print("Could not detect a circular petri dish in the image.")

if __name__ == "__main__":
    input_dir = "exp2_zs"
    files = ["IMG_4532.HEIC", "IMG_4533.HEIC"]
    
    for filename in files:
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(input_dir, f"extracted_{filename.split('.')[0]}.png")
        extract_petri_dish(input_path, output_path)
