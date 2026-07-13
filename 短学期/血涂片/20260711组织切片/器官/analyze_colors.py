import os
import cv2
import numpy as np

def analyze():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_path = os.path.join(current_dir, "心.jpg")
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    h, w, c = img.shape
    print(f"Image Size: {w}x{h}")
    
    # 转换为灰度
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 打印一些统计数据
    print(f"Min Gray: {np.min(gray)}")
    print(f"Max Gray: {np.max(gray)}")
    print(f"Mean Gray: {np.mean(gray)}")
    
    # 打印中心 200x200 的统计数据
    cx, cy = w // 2, h // 2
    center_roi = gray[cy-100:cy+100, cx-100:cx+100]
    print(f"Center 200x200 ROI - Min Gray: {np.min(center_roi)}, Mean Gray: {np.mean(center_roi)}")
    
    # 找出全图最暗的 1000 个像素的坐标均值，看看是不是在器官中心
    flat_indices = np.argsort(gray.flatten())
    # 前 2000 个最暗的像素
    ys, xs = np.unravel_index(flat_indices[:2000], gray.shape)
    mean_x = int(np.mean(xs))
    mean_y = int(np.mean(ys))
    print(f"Mean coordinate of 2000 darkest pixels: ({mean_x}, {mean_y})")

if __name__ == "__main__":
    analyze()
