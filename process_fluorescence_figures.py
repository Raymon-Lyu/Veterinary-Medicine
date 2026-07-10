import cv2
import numpy as np
import os
import argparse

def cv2_imread(file_path):
    try:
        return cv2.imdecode(np.fromfile(file_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None

def cv2_imwrite(file_path, img):
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

def draw_outlined_text(img, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, scale=1.3, thickness=3, color=(255, 255, 255), outline_color=(0, 0, 0)):
    """Draws white text with a black outline for maximum visibility on dark fluorescence images."""
    cv2.putText(img, text, position, font, scale, outline_color, thickness + 4, cv2.LINE_AA)
    cv2.putText(img, text, position, font, scale, color, thickness, cv2.LINE_AA)

def merge_and_enhance(dapi_path, target_path, target_type, target_mult=1.0):
    """Merges DAPI (Blue) and Target (TUNEL/Green or PCNA/Red) channels with custom enhancement factor, preserving scale bars."""
    dapi_img = cv2_imread(dapi_path)
    target_img = cv2_imread(target_path)
    
    if dapi_img is None or target_img is None:
        return None
        
    h, w = dapi_img.shape[:2]
    blue = dapi_img[:, :, 0]
    
    # Mild contrast enhancement for DAPI nuclei
    dapi_val = np.percentile(blue[blue > 0], 99.5) if np.any(blue > 0) else 255
    blue = np.clip(blue, 0, dapi_val)
    blue = (blue / dapi_val * 255).astype(np.uint8)
    
    green = np.zeros((h, w), dtype=np.uint8)
    red = np.zeros((h, w), dtype=np.uint8)
    
    if target_type == "TUNEL":
        raw_g = target_img[:, :, 1]
        green = np.clip(raw_g.astype(np.float32) * target_mult, 0, 255).astype(np.uint8)
    elif target_type == "PCNA":
        raw_r = target_img[:, :, 2]
        red = np.clip(raw_r.astype(np.float32) * target_mult, 0, 255).astype(np.uint8)
        
    merged = cv2.merge([blue, green, red])
    
    # Detect and preserve white pixels (like scale bar & label text in LAS X exports)
    white_mask = (dapi_img[:, :, 0] > 180) & (dapi_img[:, :, 1] > 180) & (dapi_img[:, :, 2] > 180)
    white_mask_target = (target_img[:, :, 0] > 180) & (target_img[:, :, 1] > 180) & (target_img[:, :, 2] > 180)
    merged[white_mask] = [255, 255, 255]
    merged[white_mask_target] = [255, 255, 255]
    
    return merged

def create_2x2_figure(pairs, target_type, output_path, target_mult=1.0, img_size=1000, gap=15):
    images = []
    for path_dapi, path_target, label_letter, label_text in pairs:
        merged = merge_and_enhance(path_dapi, path_target, target_type, target_mult)
        if merged is None:
            return False
            
        img_resized = cv2.resize(merged, (img_size, img_size), interpolation=cv2.INTER_CUBIC)
        draw_outlined_text(img_resized, label_letter, (50, 80), scale=2.0, thickness=4)
        
        text_size = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 1.2, 3)[0]
        text_x = img_size - text_size[0] - 50
        draw_outlined_text(img_resized, label_text, (text_x, 80), scale=1.2, thickness=3)
        
        images.append(img_resized)
        
    grid_size = img_size * 2 + gap
    canvas = np.ones((grid_size, grid_size, 3), dtype=np.uint8) * 255
    
    canvas[0:img_size, 0:img_size] = images[0]
    canvas[0:img_size, img_size + gap:grid_size] = images[1]
    canvas[img_size + gap:grid_size, 0:img_size] = images[2]
    canvas[img_size + gap:grid_size, img_size + gap:grid_size] = images[3]
    
    return cv2_imwrite(output_path, canvas)

if __name__ == "__main__":
    # This script is pre-configured for the short term project but can be run via CLI arguments.
    print("Fluorescence figure processing library written!")
