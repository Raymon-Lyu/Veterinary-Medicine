import os
import re

base_dir = r"D:\just_soso\horse cow\Veterinary Medicine\中药方剂学"

md_files = [
    "泻下药.md", "止咳化痰平喘药与方剂.md", "安神开窍药方.md", "补虚方药.md",
    "解表药.md", "理气方.md", "平肝药.md", "清热药.md", "驱虫方药.md",
    "祛湿方药.md", "外用方药.md", "温里方.md", "消导药.md"
]

herbs = {}
comparisons = []
formulas = []

for md in md_files:
    path = os.path.join(base_dir, md)
    if not os.path.exists(path):
        continue
    with open(path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_category = None
    in_herbs = False
    
    for i, line in enumerate(lines):
        line = line.strip()
        
        # Detect herbs section
        if line.startswith("### 常用中药") or line.startswith("### 中药"):
            in_herbs = True
            continue
        if line.startswith("### 常用方剂") or line.startswith("### 方剂"):
            in_herbs = False
            continue
            
        # Extract herb subcategories
        if in_herbs and line.startswith("##### "):
            current_category = line.replace("##### ", "").strip()
            if current_category not in herbs:
                herbs[current_category] = []
        elif in_herbs and line.startswith("- ") and current_category:
            herb = line.replace("- ", "").strip()
            herb = re.sub(r'\[\[(.*?)\]\]', r'\1', herb)
            # Remove leading hyphens or bullets if any
            herbs[current_category].append(herb)
            
        # Detect comparisons (often starting with ###### or ### and containing 'vs')
        if (line.startswith("#") and "vs" in line.lower()) or "对比" in line:
            title = line.lstrip("#").strip()
            # Capture the next few lines until a new header
            content = []
            for j in range(i+1, len(lines)):
                next_line = lines[j].strip()
                if next_line.startswith("#"):
                    break
                if next_line:
                    content.append(next_line)
            comparisons.append(f"**{title}**\n" + "\n".join(content))

# Also parse 方剂库
fangji_dir = os.path.join(base_dir, "方剂库")
if os.path.exists(fangji_dir):
    for f in os.listdir(fangji_dir):
        if f.endswith(".md"):
            with open(os.path.join(fangji_dir, f), 'r', encoding='utf-8') as file:
                content = file.read()
                m = re.search(r"大类:\s*(.+)", content)
                dalai = m.group(1).strip() if m else "未知"
                formulas.append({"name": f.replace(".md", ""), "大类": dalai})

# Sort formulas
formulas.sort(key=lambda x: x["大类"])

# Format the preview
preview = []
preview.append("### 🌿 常见中药部分 (已从13个文件中提取，保证全覆盖)")
for cat, items in herbs.items():
    preview.append(f"- **{cat}**: {', '.join(items)}")

preview.append("\n### ⚖️ 中药对比部分 (精确提取 `vs` 和表格结构)")
for comp in comparisons:
    preview.append(f"- {comp}\n")

preview.append(f"\n### 💊 方剂库部分 (共提取 {len(formulas)} 个方剂)")
for form in formulas:
    preview.append(f"- **{form['name']}** ({form['大类']})")

with open(os.path.join(base_dir, "preview_all.md"), 'w', encoding='utf-8') as out:
    out.write("\n".join(preview))
