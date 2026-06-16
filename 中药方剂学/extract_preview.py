import os
import re
import yaml
import json

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
    in_comparisons = False
    
    for line in lines:
        line = line.strip()
        if line.startswith("### 常用中药") or line.startswith("### 中药"):
            in_herbs = True
            in_comparisons = False
            continue
        if line.startswith("### 常用方剂") or line.startswith("### 方剂"):
            in_herbs = False
            in_comparisons = False
            continue
        if "对比" in line and line.startswith("###"):
            in_herbs = False
            in_comparisons = True
            continue
        
        if in_herbs and line.startswith("##### "):
            current_category = line.replace("##### ", "").strip()
            if current_category not in herbs:
                herbs[current_category] = []
        elif in_herbs and line.startswith("- ") and current_category:
            herb = line.replace("- ", "").strip()
            herbs[current_category].append(herb)
        
        if in_comparisons and line.startswith("- **"):
            # Simple heuristic for comparisons if they are in lists
            comparisons.append(line)

# Also parse 方剂库
fangji_dir = os.path.join(base_dir, "方剂库")
if os.path.exists(fangji_dir):
    for f in os.listdir(fangji_dir):
        if f.endswith(".md"):
            with open(os.path.join(fangji_dir, f), 'r', encoding='utf-8') as file:
                content = file.read()
                # extract yaml frontmatter
                m = re.match(r"^---\n(.*?)\n---", content, re.DOTALL)
                if m:
                    try:
                        data = yaml.safe_load(m.group(1))
                        if data and "name" not in data:
                            data["name"] = f.replace(".md", "")
                        formulas.append(data)
                    except:
                        pass

# Format the preview
preview = []
preview.append("### 🌿 常见中药部分 (从13个文件中提取)")
for cat, items in herbs.items():
    preview.append(f"**{cat}**: {', '.join(items)}")

preview.append("\n### ⚖️ 中药对比部分 (启发式提取)")
for comp in comparisons:
    preview.append(comp)

preview.append(f"\n### 💊 方剂库部分 (共提取 {len(formulas)} 个方剂)")
for form in formulas:
    name = form.get("name", "未知")
    dalai = form.get("大类", "")
    preview.append(f"- **{name}** ({dalai})")

with open(os.path.join(base_dir, "preview_summary.md"), 'w', encoding='utf-8') as out:
    out.write("\n".join(preview))

print("Extraction complete. Summary saved to preview_summary.md")
