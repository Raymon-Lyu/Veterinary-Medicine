import os
import cv2
import numpy as np

def crop_microscope_circle(img_path, output_path):
    # 使用 np.fromfile 读取，避免中文路径报错
    img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
    if img is None:
        print(f"Error: 无法读取图片 {img_path}")
        return False
        
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 使用中值滤波或高斯模糊去除噪点
    blurred = cv2.medianBlur(gray, 9)
    
    # 阈值分割得到二值图（因为圆圈内很亮，圆圈外很黑）
    # 设定阈值为 40
    _, thresh = cv2.threshold(blurred, 40, 255, cv2.THRESH_BINARY)
    
    # 寻找轮廓
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if not contours:
        print(f"Error: 在 {img_path} 中未找到任何区域！")
        return False
        
    # 找到面积最大的轮廓，这就是显微镜圆形视野
    max_contour = max(contours, key=cv2.contourArea)
    
    # 拟合外接圆
    (x, y), radius = cv2.minEnclosingCircle(max_contour)
    x, y, r = int(x), int(y), int(radius)
    
    print(f"检测到圆形视野 - 圆心: ({x}, {y}), 半径: {r}")
    
    # 创建纯白背景
    h, w, c = img.shape
    white_bg = np.ones_like(img) * 255
    
    # 创建遮罩 (Mask)，圆内为255，圆外为0
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
    
    # 使用 cv2.imencode 和 tofile 写入，避免中文路径报错
    _, encoded_img = cv2.imencode('.jpg', cropped)
    encoded_img.tofile(output_path)
    print(f"成功保存裁剪后的图片至：{output_path}")
    return True

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    test_img = os.path.join(current_dir, "微信图片_20260713081531_3240_63.jpg")
    out_img = os.path.join(current_dir, "test_cropped_1.jpg")
    crop_microscope_circle(test_img, out_img)
