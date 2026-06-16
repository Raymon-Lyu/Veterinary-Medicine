import os
import re

base_dir = r"D:\just_soso\horse cow\Veterinary Medicine\中药方剂学"

md_files = [
    "泻下药.md", "止咳化痰平喘药与方剂.md", "安神开窍药方.md", "补虚方药.md",
    "解表药.md", "理气方.md", "平肝药.md", "清热药.md", "驱虫方药.md",
    "祛湿方药.md", "外用方药.md", "温里方.md", "消导药.md"
]

herbs = {}

def add_herb(cat, herb_list_str):
    if cat not in herbs:
        herbs[cat] = []
    # Split by 、, ， or ,
    items = re.split(r'[、，,]', herb_list_str)
    for item in items:
        item = item.strip()
        item = re.sub(r'\[\[(.*?)\]\]', r'\1', item)
        item = re.sub(r'^\s*-\s*', '', item)
        if item:
            herbs[cat].append(item)

for md in md_files:
    path = os.path.join(base_dir, md)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_category = None
    in_herbs = False
    
    # Check headers for fallback category
    file_cat_match = re.match(r'(.*?)(药|方).md', md)
    file_cat = file_cat_match.group(1) + "药" if file_cat_match else md.replace(".md", "")
    
    for line in lines:
        line = line.strip()
        
        # 匹配 `代表药物有...` 或 `常见中药有：...`
        m = re.search(r'(代表药物有|常见中药有：|常见药物有：|常见中药有)(.*?)$', line)
        if m:
            add_herb("泻下相关(自动推断)", m.group(2).replace(">","、"))
            continue
            
        if line.startswith("### 常用中药") or line.startswith("### 中药"):
            in_herbs = True
            continue
        if line.startswith("### 常用方剂") or line.startswith("### 方剂") or line.startswith("### 攻下药与攻下方") or line.startswith("### 润下药"):
            in_herbs = False
            
        # Section with #####
        if in_herbs and line.startswith("##### "):
            current_category = line.replace("##### ", "").strip()
            continue
            
        if in_herbs and line.startswith("- "):
            # Pattern: - 疏风散热：薄荷、牛蒡子、蝉蜕
            if "：" in line:
                parts = line.replace("- ", "").split("：", 1)
                add_herb(parts[0].strip(), parts[1].strip())
            else:
                if current_category:
                    add_herb(current_category, line)
                else:
                    add_herb(file_cat, line)

# Dump to file
preview = []
for cat, items in herbs.items():
    preview.append(f"- **{cat}**: {', '.join(items)}")

with open(os.path.join(base_dir, "preview_herbs.md"), 'w', encoding='utf-8') as out:
    out.write("\n".join(preview))
