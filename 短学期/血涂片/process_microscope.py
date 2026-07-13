import os
import cv2
import numpy as np

def crop_microscope_circle(img_path):
    # 使用 np.fromfile 读取，避免中文路径报错
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: 无法读取图片 {img_path}")
        return None
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 滤波去噪
    blurred = cv2.medianBlur(gray, 9)
    
    # 阈值分割得到二值图
    _, thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"Warning: 在 {os.path.basename(img_path)} 中未找到有效轮廓！")
        return None
        
    # 找到面积最大的轮廓，即圆形视野
    max_contour = max(contours, key=cv2.contourArea)
    
    # 拟合外接圆
    (x, y), radius = cv2.minEnclosingCircle(max_contour)
    x, y, r = int(x), int(y), int(radius)
    
    # 创建纯白背景
    h, w, c = img.shape
    white_bg = np.ones_like(img) * 255
    
    # 创建圆形遮罩
    mask = np.zeros((h, w), dtype=np.uint8)
    cv2.circle(mask, (x, y), r, 255, -1)
    
    # 将圆圈内复制到白背景上
    result = np.where(mask[:, :, np.newaxis] == 255, img, white_bg)
    
    # 裁剪外切正方形
    x1 = max(0, x - r)
    y1 = max(0, y - r)
    x2 = min(w, x + r)
    y2 = min(h, y + r)
    
    cropped = result[y1:y2, x1:x2]
    return cropped

def process_all_images(image_dir):
    # 找出所有原图（过滤掉包含 merged, cropped, test 关键字的图片）
    all_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    all_files.sort()
    
    raw_images = []
    for f in all_files:
        low = f.lower()
        if "merged" not in low and "cropped" not in low and "test" not in low and not low.startswith('merge_images') and not low.startswith('process_'):
            raw_images.append(f)
            
    print(f"理世找到了 {len(raw_images)} 张显微镜原图，准备开始截取圆形图像内容...")
    
    cropped_imgs = []
    for i, name in enumerate(raw_images):
        img_path = os.path.join(image_dir, name)
        output_name = f"cropped_{name}"
        output_path = os.path.join(image_dir, output_name)
        
        print(f" 正在处理 [{i+1}/{len(raw_images)}]: {name}")
        cropped = crop_microscope_circle(img_path)
        if cropped is not None:
            # 保存单张裁剪图
            _, encoded_img = cv2.imencode('.jpg', cropped)
            encoded_img.tofile(output_path)
            cropped_imgs.append(cropped)
            
    if len(cropped_imgs) < 4:
        print(f"呜哇，截取成功的图片不够4张呢（只有 {len(cropped_imgs)} 张），无法拼接 2x2 图！")
        return
        
    print(f"截取完成！正在将前4张裁剪后的图片拼接为 2x2 网格...")
    
    # 拼接前4张
    imgs_to_merge = cropped_imgs[:4]
    
    # 统一尺寸为第一张裁剪图的尺寸
    target_h, target_w = imgs_to_merge[0].shape[:2]
    print(f"统一拼接分辨率为: {target_w}x{target_h}")
    
    resized_imgs = []
    for img in imgs_to_merge:
        res = cv2.resize(img, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)
        resized_imgs.append(res)
        
    # 水平和垂直拼接
    top_row = np.hstack((resized_imgs[0], resized_imgs[1]))
    bottom_row = np.hstack((resized_imgs[2], resized_imgs[3]))
    merged = np.vstack((top_row, bottom_row))
    output_merged_path = os.path.join(image_dir, "microscope_merged_2x2.jpg")
    _, encoded_merged = cv2.imencode('.jpg', merged)
    encoded_merged.tofile(output_merged_path)
    
    print(f"2x2 拼图制作成功！已保存到：{output_merged_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    process_all_images(current_dir)
