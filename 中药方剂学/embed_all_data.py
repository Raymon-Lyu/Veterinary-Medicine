import json
import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
fangji_dir = os.path.join(base_dir, '方剂库')
json_file = os.path.join(base_dir, 'fangji_data.json')
html_file = os.path.join(base_dir, 'fangji_flashcards.html')

# 1. Dynamically parse all formulas from 方剂库
formulas = []
if os.path.exists(fangji_dir):
    for f_name in os.listdir(fangji_dir):
        if not f_name.endswith('.md'):
            continue
            
        path = os.path.join(fangji_dir, f_name)
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Parse frontmatter
        m = re.match(r'^---\n(.*?)\n---\n(.*)', content, re.DOTALL)
        if not m:
            continue
            
        frontmatter = m.group(1)
        body = m.group(2).strip()
        
        formula = {
            "type": "方剂",
            "name": f_name.replace(".md", ""),
            "notes": body,
            "组成": [], "君药": [], "臣药": [], "佐药": [], "使药": []
        }
        
        # Parse fields from frontmatter
        for line in frontmatter.split('\n'):
            line = line.strip()
            # Simple key-value
            kv = re.match(r'^([^:]+):\s*(.*)', line)
            if kv:
                key = kv.group(1).strip()
                val = kv.group(2).strip()
                if key in ["大类", "子类", "功效"]:
                    formula[key] = val.strip("'\"")
                    
        # Parse list fields (组成, 君药, etc.)
        list_keys = ["组成", "君药", "臣药", "佐药", "使药"]
        for key in list_keys:
            # Match list pattern
            list_m = re.search(fr'{key}:\s*\n((?:\s*-\s+.*\n?)*)', frontmatter)
            if list_m:
                items = re.findall(r'-\s+(.*)', list_m.group(1))
                formula[key] = [item.strip() for item in items if item.strip()]
        
        formulas.append(formula)

# Update json_file as well
with open(json_file, 'w', encoding='utf-8') as f:
    json.dump(formulas, f, ensure_ascii=False, indent=2)

# 2. Define Comprehensive Herbs data based on the latest verified list
herbs_data = [
    # 1. 解表药
    {"name": "辛温解表", "大类": "常见中药", "子类": "解表药", "notes": "麻黄, 桂枝, 细辛, 荆芥, 防风, 紫苏, 白芷, 辛夷, 苍耳子, 生姜, 葱白"},
    {"name": "辛凉解表", "大类": "常见中药", "子类": "解表药", "notes": "薄荷, 牛蒡子, 蝉蜕, 桑叶, 菊花, 柴胡, 升麻, 葛根"},
    # 2. 清热药
    {"name": "清热泻火", "大类": "常见中药", "子类": "清热药", "notes": "石膏, 知母, 栀子"},
    {"name": "清热凉血", "大类": "常见中药", "子类": "清热药", "notes": "丹皮, 地骨皮, 生地, 白头翁, 白茅根, 紫草, 玄参, 水牛角"},
    {"name": "清热燥湿", "大类": "常见中药", "子类": "清热药", "notes": "黄连, 黄芩, 黄柏, 龙胆, 苦参"},
    {"name": "清热解毒", "大类": "常见中药", "子类": "清热药", "notes": "金银花, 连翘, 蒲公英, 紫花地丁, 板蓝根, 大青叶, 青黛, 马勃, 射干, 山豆根"},
    {"name": "清热解暑", "大类": "常见中药", "子类": "清热药", "notes": "香薷, 荷叶, 青蒿"},
    # 3. 泻下药
    {"name": "攻下药", "大类": "常见中药", "子类": "泻下药", "notes": "大黄, 芒硝, 巴豆"},
    {"name": "润下药", "大类": "常见中药", "子类": "泻下药", "notes": "火麻仁, 郁李仁"},
    {"name": "峻下逐水", "大类": "常见中药", "子类": "泻下药", "notes": "芫花, 甘遂, 大戟"},
    # 4. 消导药
    {"name": "消食化积", "大类": "常见中药", "子类": "消导药", "notes": "六(神)曲, 山楂, 麦芽, 谷芽, 莱菔子, 鸡内金"},
    # 5. 温里药
    {"name": "温中/救逆/散寒", "大类": "常见中药", "子类": "温里药", "notes": "附子, 肉桂, 干姜, 小茴香, 吴茱萸, 高良姜, 艾叶, 花椒"},
    # 6. 补虚药
    {"name": "补气", "大类": "常见中药", "子类": "补虚药", "notes": "人参, 党参, 黄芪, 白术"},
    {"name": "补血", "大类": "常见中药", "子类": "补虚药", "notes": "当归, 白芍, 熟地黄, 阿胶"},
    {"name": "滋阴", "大类": "常见中药", "子类": "补虚药", "notes": "天冬, 麦冬, 枸杞子, 黄精"},
    {"name": "补阳", "大类": "常见中药", "子类": "补虚药", "notes": "巴戟天, 肉苁蓉, 淫羊藿, 杜仲, 续断"},
    # 7. 理气药
    {"name": "理气健脾", "大类": "常见中药", "子类": "理气药", "notes": "陈皮, 砂仁, 枳实、枳壳, 丁香, 大腹皮, 莱菔子, 厚朴"},
    {"name": "疏肝解郁", "大类": "常见中药", "子类": "理气药", "notes": "青皮, 香附"},
    {"name": "调理肺气", "大类": "常见中药", "子类": "理气药", "notes": "苏子"},
    # 8. 祛湿药
    {"name": "祛风湿", "大类": "常见中药", "子类": "祛湿药", "notes": "羌活, 独活, 威灵仙, 木瓜, 桑寄生, 秦艽, 马钱子, 乌梢蛇"},
    {"name": "利水渗湿", "大类": "常见中药", "子类": "祛湿药", "notes": "茯苓, 猪苓, 泽泻, 车前子, 金钱草, 海金沙, 石韦"},
    {"name": "芳香化湿", "大类": "常见中药", "子类": "祛湿药", "notes": "藿香, 苍术"},
    # 9. 止咳化痰平喘药
    {"name": "温化寒痰", "大类": "常见中药", "子类": "止咳化痰平喘药", "notes": "半夏, 南星, 旋覆花, 白前"},
    {"name": "清化热痰", "大类": "常见中药", "子类": "止咳化痰平喘药", "notes": "贝母, 瓜蒌, 天花粉, 桔梗, 前胡"},
    {"name": "温性止咳", "大类": "常见中药", "子类": "止咳化痰平喘药", "notes": "杏仁, 百部, 紫菀, 款冬花, 苏子"},
    {"name": "寒性止咳", "大类": "常见中药", "子类": "止咳化痰平喘药", "notes": "马兜铃, 枇杷叶, 桑白皮"},
    {"name": "平喘药", "大类": "常见中药", "子类": "止咳化痰平喘药", "notes": "葶苈子, 白果, 洋金花, 麻黄"},
    # 10. 安神开窍药
    {"name": "安神药", "大类": "常见中药", "子类": "安神开窍药", "notes": "朱砂, 酸枣仁, 远志, 牛黄"},
    # 11. 平肝药
    {"name": "平肝明目", "大类": "常见中药", "子类": "平肝药", "notes": "决明子"},
    {"name": "平肝熄风", "大类": "常见中药", "子类": "平肝药", "notes": "天麻, 钩藤, 天竺黄"},
    # 12. 驱虫药
    {"name": "驱肠虫", "大类": "常见中药", "子类": "驱虫药", "notes": "使君子, 常山"},
    # 13. 外用药
    {"name": "涂敷喷洗", "大类": "常见中药", "子类": "外用药", "notes": "冰片, 炉甘石"}
]

# 3. Define Comparisons data precisely extracted
comparisons_data = [
    {"name": "人参 vs 党参", "大类": "中药对比", "子类": "补虚药对比", "notes": "**共性**：均能补脾益肺，生津养血。\n**人参**（重症）：独具**大补元气、复脉固脱**之功，用于治气虚欲脱、脉微欲绝的危重证候。兼有益气安神、生血、摄血、壮阳作用。\n**党参**（轻症）：功效类似但药力较弱，**无**大补元气、复脉固脱之功。**虽用大剂量，亦不能代替人参益气固脱**。"},
    {"name": "人参 vs 黄芪", "大类": "中药对比", "子类": "补虚药对比", "notes": "**共性**：均为常用补气要药，同用可相互增强补气之功。\n**人参**（主内）：能补心、脾、肺之气，长于大补元气、安神增智，为**治内伤气虚第一要药**。\n**黄芪**（主表/升）：大补元气不如人参，但**温升之力强过人参**。长于**固表止汗、托毒生肌、利尿退肿**，善补肌表之气（此为人参所无或所不及）。"},
    {"name": "黄芪 vs 白术", "大类": "中药对比", "子类": "补气药对比", "notes": "**共性**：两者均能补气、利水、止汗\n**黄芪**（升提）：**脾、肺双补**，甘温补气力较强。长于**补气升阳**。主治气虚水肿，且**益卫固表、止汗之力优于白术**\n**白术**（除湿）：**仅补气健脾**。长于**健脾除湿**。"},
    {"name": "生地黄 vs 熟地黄", "大类": "中药对比", "子类": "地黄辨析", "notes": "**共性**：均能养阴滋阴。\n**生地黄**（寒）：清热凉血，养阴生津。偏于“清”与“凉”。是清热凉血的要药。\n**熟地黄**（温）：补血滋阴，益精填髓。偏于“补”与“填”。经炮制后性转温，绝对无清热凉血之功。"},
    {"name": "天冬 vs 麦冬", "大类": "中药对比", "子类": "滋阴药对比", "notes": "**共性**：两者药性均寒凉，养肺阴\n**天冬**（偏下）：寒润之力强于麦冬，长于滋肾阴而清降虚火。\n**麦冬**（偏上）：寒润之力较弱，偏于养胃生津、润肺与清心除烦。"},
    {"name": "杜仲 vs 续断", "大类": "中药对比", "子类": "补阳药对比", "notes": "**共性**：均能补肝肾，强筋骨，止血安胎，疗伤续折。\n**杜仲**：以补肝肾为重，侧重于单纯的“补”，可降血压。\n**续断**：为补益肝肾、宣通筋脉之要药，补而不滞、形而不泄，更强调兼顾活血与行滞。"}
]

# Combine all
all_data = formulas + herbs_data + comparisons_data

# Read HTML and replace raw data
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace the array in `const raw = [...]`
pattern = re.compile(r'const raw = \[.*?\];', re.DOTALL)

for item in all_data:
    if "notes" in item and item["notes"]:
        item["notes"] = item["notes"].replace("\n", "<br>")
    if "notes" in item and item["notes"]:
        item["notes"] = item["notes"].replace("\n", "<br>")

new_js_var = "const raw = " + json.dumps(all_data, ensure_ascii=False) + ";"

if pattern.search(html_content):
    new_html = pattern.sub(lambda m: new_js_var, html_content)
else:
    print("Could not find 'const raw = [...]' in HTML.")
    exit(1)

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Successfully embedded {len(formulas)} formulas, {len(herbs_data)} herb categories, and {len(comparisons_data)} comparisons into HTML.")
print(f"Total embedded items: {len(all_data)}.")