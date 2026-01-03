import pikepdf
import os
from pathlib import Path

def batch_unlock_pdfs(input_folder, output_folder, open_password=None):
    """
    批量移除文件夹中所有 PDF 的加密限制
    :param input_folder: 源文件夹路径
    :param output_folder: 处理后保存的文件夹路径
    :param open_password: 如果文件有“打开密码”，请在此输入（仅限所有文件密码相同时使用）
    """
    # 创建输出文件夹
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"创建输出目录: {output_folder}")

    # 获取所有 PDF 文件
    files = [f for f in os.listdir(input_folder) if f.lower().endswith('.pdf')]
    print(f"在 {input_folder} 中找到 {len(files)} 个 PDF 文件。\n")

    for filename in files:
        input_path = os.path.join(input_folder, filename)
        output_path = os.path.join(output_folder, f"unlocked_{filename}")
        
        try:
            # 尝试打开 PDF
            # pikepdf 会自动处理权限加密（Owner Password）
            # 如果有打开密码，则使用 open_password
            with pikepdf.open(input_path, password=open_password) as pdf:
                # 保存时 encryption=False 会移除所有加密设置
                pdf.save(output_path)
                print(f"[成功] 已解密: {filename}")
                
        except pikepdf.PasswordError:
            print(f"[跳过] 文件需要打开密码: {filename} (请在代码中提供 password 参数)")
        except Exception as e:
            print(f"[错误] 处理 {filename} 时发生异常: {e}")

# --- 配置路径 ---
# 请修改下方的路径为您电脑上的实际路径
source_dir = r'D:\just_soso\horse cow\Veterinary Medicine\动物免疫学\祖传ppt'      # 原始 PDF 文件夹
target_dir = r'D:\just_soso\horse cow\Veterinary Medicine\动物免疫学\un_locked_pdfs'  # 解密后的保存文件夹

# 如果所有文件都有同一个“打开密码”，请填入引号中；否则保持 None
common_password = '20251201'

# 执行批量处理
batch_unlock_pdfs(source_dir, target_dir, open_password=common_password)