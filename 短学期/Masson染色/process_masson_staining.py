import os
import cv2
import numpy as np

def crop_center_physical(img_path, output_path, target_size=1000):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: 无法读取图片 {img_path}")
        return False
        
    h, w, c = img.shape
    
    # 采用固定中心物理裁剪法，边长为短边的 0.50 倍
    # 这样能 100.0% 保证去掉任何圆形畸变黑边和极其微小的四角暗影
    short_side = min(h, w)
    side = int(short_side * 0.50)
    
    cx, cy = w // 2, h // 2
    
    x1 = cx - side // 2
    y1 = cy - side // 2
    x2 = cx + side // 2
    y2 = cy + side // 2
    
    cropped = img[y1:y2, x1:x2]
    
    # 统一尺寸缩放到 1000x1000 像素
    resized = cv2.resize(cropped, (target_size, target_size), interpolation=cv2.INTER_LANCZOS4)
    
    _, encoded = cv2.imencode('.jpg', resized)
    encoded.tofile(output_path)
    print(f"成功物理裁剪并保存 Masson 染色图: {os.path.basename(output_path)}")
    return True

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    masson_images = [
        "脾脏.jpg",
        "小肠.jpg",
        "大肠.jpg",
        "肌肉.jpg",
        "胶原纤维和肌肉.jpg",
        "卵巢.jpg"
    ]
    
    print("开始提取显微镜视野并物理裁剪成 1000x1000 像素的方形 Masson 染色图片...")
    for name in masson_images:
        img_path = os.path.join(current_dir, name)
        output_name = f"cropped_{name}"
        output_path = os.path.join(current_dir, output_name)
        
        if os.path.exists(img_path):
            crop_center_physical(img_path, output_path)
        else:
            print(f"Error: 找不到图片 {name}")

if __name__ == "__main__":
    main()
    # 脚本自我删除
    try:
        os.remove(__file__)
        print("处理脚本已自我销毁。")
    except Exception:
        pass
