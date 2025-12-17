import cv2
import numpy as np
import matplotlib.pyplot as plt

def analyze_inhibition_zones(image_path, pixels_per_mm=None):
    """
    检测抑菌圈并计算直径
    :param image_path: 图片路径
    :param pixels_per_mm: 像素与毫米的比例 (例如: 1mm = 15 pixels)。如果为None，则只输出像素值。
    """
    # 1. 读取图片
    img = cv2.imread(image_path)
    if img is None:
        print("Error: 无法读取图片")
        return

    original_img = img.copy()
    
    # 2. 图像预处理
    # 转换为灰度图
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # 高斯模糊，减少噪点和菌苔表面的不均匀纹理
    # (9, 9) 是核大小，可以根据图片清晰度调整
    gray_blurred = cv2.GaussianBlur(gray, (9, 9), 2)
    
    # 3. 霍夫圆检测 (关键步骤)
    # param1: Canny边缘检测的高阈值
    # param2: 圆心检测的累加器阈值 (越小检测到的圆越多，越容易误检；越大越严格)
    # minRadius/maxRadius: 根据实际图片分辨率调整，避免检测到药敏纸片(太小)或培养皿边缘(太大)
    circles = cv2.HoughCircles(
        gray_blurred, 
        cv2.HOUGH_GRADIENT, 
        dp=1, 
        minDist=100,       # 两个圆心之间的最小距离 (防止同心圆检测)
        param1=50,         
        param2=30,         # 重点调整这个参数：如果圈没检测出来，调小它；如果噪点太多，调大它
        minRadius=30,      # 最小半径 (像素)，用于过滤掉中间的小纸片
        maxRadius=150      # 最大半径 (像素)
    )

    # 4. 绘制结果
    output_data = []
    
    if circles is not None:
        circles = np.uint16(np.around(circles))
        print(f"检测到 {len(circles[0, :])} 个潜在抑菌圈。")

        for i in circles[0, :]:
            center_x, center_y, radius = i[0], i[1], i[2]
            diameter_pixels = radius * 2
            
            # 计算物理尺寸
            if pixels_per_mm:
                diameter_mm = diameter_pixels / pixels_per_mm
                label = f"{diameter_mm:.2f} mm"
                print(f"位置({center_x}, {center_y}) - 直径: {diameter_mm:.2f} mm")
            else:
                label = f"{diameter_pixels} px"
                print(f"位置({center_x}, {center_y}) - 直径: {diameter_pixels} px")

            # 绘制外圆 (抑菌圈边界) - 绿色
            cv2.circle(img, (center_x, center_y), radius, (0, 255, 0), 2)
            # 绘制圆心 - 红色
            cv2.circle(img, (center_x, center_y), 2, (0, 0, 255), 3)
            # 添加文字标签
            cv2.putText(img, label, (center_x - 40, center_y - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)
            
            output_data.append(diameter_pixels)
    else:
        print("未检测到明显的圆形抑菌圈，请调整 param2 或 minRadius。")

    # 5. 显示图像 (使用Matplotlib以便在Notebook中查看)
    plt.figure(figsize=(10, 10))
    # OpenCV是BGR，Matplotlib是RGB，需要转换
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title("Inhibition Zone Detection")
    plt.axis("off")
    plt.show()

