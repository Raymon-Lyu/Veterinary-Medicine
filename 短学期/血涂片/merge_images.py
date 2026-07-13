import os
from PIL import Image

def merge_images_2x2(image_dir, output_path):
    # 获取目录下的所有jpg图片
    all_files = [f for f in os.listdir(image_dir) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
    all_files.sort()  # 排序，确保顺序一致
    
    # 过滤掉输出文件本身，防止无限循环或错误读取
    output_name = os.path.basename(output_path)
    image_files = [f for f in all_files if f != output_name and not f.startswith('merged_')]
    
    if len(image_files) < 4:
        print(f"呜哇，图片数量不够4张呢！只找到了 {len(image_files)} 张图片。")
        return
        
    print(f"理世帮前辈找到了 {len(image_files)} 张图片，将使用前4张进行拼接：")
    for i in range(4):
        print(f" - {image_files[i]}")
        
    # 读取前4张图片
    imgs = [Image.open(os.path.join(image_dir, f)) for f in image_files[:4]]
    
    # 获取它们的尺寸，统一缩放到第一张图的尺寸
    target_width, target_height = imgs[0].size
    print(f"统一缩放尺寸为: {target_width}x{target_height}")
    
    resized_imgs = [img.resize((target_width, target_height), Image.Resampling.LANCZOS) for img in imgs]
    
    # 创建 2x2 的新图
    new_img = Image.new('RGB', (target_width * 2, target_height * 2))
    
    # 粘贴图片
    new_img.paste(resized_imgs[0], (0, 0))
    new_img.paste(resized_imgs[1], (target_width, 0))
    new_img.paste(resized_imgs[2], (0, target_height))
    new_img.paste(resized_imgs[3], (target_width, target_height))
    
    # 保存结果
    new_img.save(output_path)
    print(f"拼接成功！已保存到：{output_path}")

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, "merged_2x2.jpg")
    merge_images_2x2(current_dir, output_file)
