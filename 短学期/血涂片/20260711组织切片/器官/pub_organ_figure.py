import os
import cv2
import numpy as np
import matplotlib
# 设置非交互式后端
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def main():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 按照心、肝、脾、肺、肾的顺序读取
    organ_names = ["心.jpg", "肝.jpg", "脾.jpg", "肺.jpg", "肾.jpg"]
    labels = ["a", "b", "c", "d", "e"]
    
    imgs = []
    for name in organ_names:
        img_path = os.path.join(current_dir, name)
        if not os.path.exists(img_path):
            print(f"Error: 找不到器官图片 {name}")
            return
            
        img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            print(f"Error: 无法读取图片 {name}")
            return
        imgs.append(img)
        
    # 统一像素比例的核心：计算全局的最大边长以作为缩放比例基准
    max_dim = max(max(img.shape[:2]) for img in imgs)
    
    target_side = 500      # 每一个子图网格的尺寸
    organ_max_size = 440   # 器官占格子最大边长为 440，四周留有优雅白边
    
    # 全局一致的缩放比例，使得最大边长的器官刚好为 440，而小器官等比例缩放
    global_scale = organ_max_size / max_dim
    
    processed_imgs = []
    for img in imgs:
        h, w = img.shape[:2]
        new_w = int(w * global_scale)
        new_h = int(h * global_scale)
        
        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
        
        # 居中贴到 500x500 的纯白画布上
        canvas = np.ones((target_side, target_side, 3), dtype=np.uint8) * 255
        dx = (target_side - new_w) // 2
        dy = (target_side - new_h) // 2
        canvas[dy : dy + new_h, dx : dx + new_w] = resized
        processed_imgs.append(canvas)
        
    # Apply publication styles (nature-figure skill requirement)
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['font.sans-serif'] = ['Arial', 'DejaVu Sans', 'Liberation Sans']
    plt.rcParams['svg.fonttype'] = 'none'   # editable text in SVG
    plt.rcParams['pdf.fonttype'] = 42       # TrueType in PDF
    
    # 创建 matplotlib subplots 绘图板 (1x5横排)
    fig, axes = plt.subplots(1, 5, figsize=(15, 3.2), dpi=300)
    plt.subplots_adjust(wspace=0.08, hspace=0.0) # 子图之间留出细小白边，对应 nature figure gutters
    
    for ax, img, label in zip(axes, processed_imgs, labels):
        # 转换为 RGB 格式以防 matplotlib 变色
        rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        ax.imshow(rgb_img)
        
        # 清除坐标轴和黑边框
        ax.set_xticks([])
        ax.set_yticks([])
        for spine in ax.spines.values():
            spine.set_visible(False)
            
        # 学术风格字母标号
        ax.text(
            0.05, 0.95, label,
            transform=ax.transAxes,
            fontsize=16,
            fontweight='bold',
            color='black',
            ha='left',
            va='top'
        )
        
    # 保存为期刊出版级的三种格式
    fig.savefig(os.path.join(current_dir, "organs_merged_1x5.svg"), bbox_inches='tight')
    fig.savefig(os.path.join(current_dir, "organs_merged_1x5.pdf"), bbox_inches='tight')
    fig.savefig(os.path.join(current_dir, "organs_merged_1x5.jpg"), dpi=300, bbox_inches='tight')
    plt.close(fig)
    
    print("Nature-figure 1x5 器官大图生成成功 (已保存为 SVG/PDF/JPG 格式)！")
    
    # 清除历史遗留临时文件
    legacy_files = [
        "test_organ_crop.py", "test_cropped_heart.jpg",
        "analyze_colors.py", "test_two_step_heart.jpg",
        "test_pure_stats.py", "test_pure_stats_heart.jpg",
        "merge_manual_organs.py"
    ]
    for lf in legacy_files:
        path = os.path.join(current_dir, lf)
        if os.path.exists(path):
            try:
                os.remove(path)
            except Exception:
                pass

if __name__ == "__main__":
    main()
    # 脚本自我删除
    try:
        os.remove(__file__)
        print("排版脚本已自我销毁。")
    except Exception:
        pass
