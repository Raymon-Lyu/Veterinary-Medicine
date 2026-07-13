import os
import cv2
import numpy as np

def crop_organ(img_path, output_path):
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: 无法读取 {img_path}")
        return False
        
    h, w, c = img.shape
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    print(f"Image shape: {img.shape}")
    # 逆阈值分割：背景白色非常亮(>200)，器官和血迹较暗(<180)
    # 我们认为小于 180 的地方是前景
    _, thresh = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY_INV)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print(f"Total contours found: {len(contours)}")
    if not contours:
        print("未找到任何器官轮廓")
        return False
        
    # 筛选靠中心最近且面积较大的轮廓
    img_center = np.array([w / 2, h / 2])
    best_contour = None
    min_dist = float('inf')
    
    for con in contours:
        area = cv2.contourArea(con)
        if area < 100: # 稍微降低噪声过滤门槛
            continue
            
        # 计算轮廓中心
        M = cv2.moments(con)
        if M["m00"] == 0:
            cx, cy = w/2, h/2
        else:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        
        dist = np.linalg.norm(np.array([cx, cy]) - img_center)
        # 我们希望是面积比较大的或者是中心的
        if dist < min_dist:
            min_dist = dist
            best_contour = con
            
    if best_contour is None:
        best_contour = max(contours, key=cv2.contourArea)
        
    x, y, gw, gh = cv2.boundingRect(best_contour)
    print(f"Best contour bounding box: x={x}, y={y}, w={gw}, h={gh}, area={cv2.contourArea(best_contour)}")
    
    # 转换为正方形裁剪区域并添加 50% 的 padding
    cx, cy = x + gw/2, y + gh/2
    side = max(gw, gh) * 1.5  # 1.5倍长边
    
    # 裁剪边界
    x1 = max(0, int(cx - side/2))
    y1 = max(0, int(cy - side/2))
    x2 = min(w, int(cx + side/2))
    y2 = min(h, int(cy + side/2))
    
    print(f"Crop box: x1={x1}, y1={y1}, x2={x2}, y2={y2}")
    
    # 为了保持纯正方形，我们可以进行切片
    cropped = img[y1:y2, x1:x2]
    
    # 写入
    _, encoded = cv2.imencode('.jpg', cropped)
    encoded.tofile(output_path)
    print(f"成功保存裁剪器官到: {output_path}")
    return True

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    img_in = os.path.join(current_dir, "心.jpg")
    img_out = os.path.join(current_dir, "test_cropped_heart.jpg")
    crop_organ(img_in, img_out)
