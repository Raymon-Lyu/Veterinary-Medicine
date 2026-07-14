import os
import cv2
import numpy as np

def test_physical_circle():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, "软骨.jpg")
    
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    h, w, c = img.shape
    
    # 物理正圆参数设定 (圆心在正中心，半径取短边的 0.43 倍)
    short_side = min(h, w)
    r = int(short_side * 0.43)
    cx, cy = w // 2, h // 2
    
    x1, y1 = cx - r, cy - r
    x2, y2 = cx + r, cy + r
    
    sub_img = img[y1:y2, x1:x2]
    sh, sw, sc = sub_img.shape
    
    # 新坐标系下的圆心就在子图正中央 (r, r)
    sub_cx, sub_cy = r, r
    
    # 创建正圆 Alpha 掩膜
    mask = np.zeros((sh, sw), dtype=np.uint8)
    cv2.circle(mask, (sub_cx, sub_cy), r, 255, -1)
    
    # 高斯模糊做抗锯齿
    mask_blur = cv2.GaussianBlur(mask, (9, 9), 0).astype(np.float32) / 255.0
    mask_blur = np.expand_dims(mask_blur, axis=2)
    
    # 强制白底和黑底生成
    black_bg = (sub_img * mask_blur + 0 * (1 - mask_blur)).astype(np.uint8)
    white_bg = (sub_img * mask_blur + 255 * (1 - mask_blur)).astype(np.uint8)
    
    # 缩放到统一的 1000x1000 高清分辨率
    black_resized = cv2.resize(black_bg, (1000, 1000), interpolation=cv2.INTER_LANCZOS4)
    white_resized = cv2.resize(white_bg, (1000, 1000), interpolation=cv2.INTER_LANCZOS4)
    
    cv2.imencode('.jpg', black_resized)[1].tofile(os.path.join(current_dir, "test_circle_black.jpg"))
    cv2.imencode('.jpg', white_resized)[1].tofile(os.path.join(current_dir, "test_circle_white.jpg"))
    print("Physical circle crop test success!")

if __name__ == "__main__":
    test_physical_circle()
