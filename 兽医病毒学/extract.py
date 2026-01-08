from pypdf import PdfReader, PdfWriter
import os

def extract_pages(input_path, output_path, start_page, end_page):
    """
    从 PDF 中提取指定页面范围并保存为新文件。
    
    参数:
    input_path (str): 源 PDF 文件路径
    output_path (str): 输出 PDF 文件路径
    start_page (int): 开始页码（也就是你PDF阅读器上看到的页码，从1开始）
    end_page (int): 结束页码（包含这一页）
    """
    
    # 检查文件是否存在
    if not os.path.exists(input_path):
        print(f"错误: 找不到文件 {input_path}")
        return

    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        # 获取总页数
        total_pages = len(reader.pages)
        
        # 边界检查
        if start_page < 1 or end_page > total_pages or start_page > end_page:
            print(f"页码错误! 文件只有 {total_pages} 页，你请求的是 {start_page}-{end_page} 页。")
            return

        # 核心逻辑：循环添加页面
        # 注意：Python索引从0开始，所以 start_page 需要减 1
        # end_page 不需要减，因为 range 函数是“左闭右开”的，
        # 但我们需要包含 end_page，所以 range 的结束参数刚好就是 end_page (对应索引 end_page-1)
        # 举例：提取第 5 页到第 5 页。 range(4, 5) -> 只有索引 4。正确。
        
        print(f"正在提取第 {start_page} 页 到 第 {end_page} 页...")
        
        for i in range(start_page - 1, end_page):
            writer.add_page(reader.pages[i])

        # 保存文件
        with open(output_path, "wb") as f:
            writer.write(f)
            
        print(f"成功! 文件已保存至: {output_path}")

    except Exception as e:
        print(f"发生错误: {e}")

# ==========================================
# 使用示例 (在此处修改你的文件路径)
# ==========================================

# 假设你的兽医病毒学课件在这个路径
source_file = r"D:\just_soso\horse cow\Veterinary Medicine\兽医病毒学\2025-第1-3讲-病毒的复制.pdf" 
target_file = "兽医病毒学_重点章节_Baltimore分类.pdf"

# 提取第 10 页到第 25 页
extract_pages(source_file, target_file, 53, 76)