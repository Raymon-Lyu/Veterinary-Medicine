import json
import os
import re

base_dir = os.path.dirname(os.path.abspath(__file__))
json_file = os.path.join(base_dir, 'fangji_data.json')
html_file = os.path.join(base_dir, 'fangji_flashcards.html')

# 1. Load existing formulas
with open(json_file, 'r', encoding='utf-8') as f:
    formulas = json.load(f)

# 2. Define new Herbs data
herbs_data = [
    {"name": "麻黄, 桂枝, 细辛", "大类": "常见中药", "子类": "辛温解表", "notes": "发汗解表，散风寒。麻黄发汗平喘，桂枝解肌和营，细辛温肺化饮。"},
    {"name": "薄荷, 柴胡, 葛根", "大类": "常见中药", "子类": "辛凉解表", "notes": "疏风散热。薄荷发汗最强，柴胡和解退热，葛根升阳止泻。"},
    {"name": "石膏, 知母", "大类": "常见中药", "子类": "清热泻火", "notes": "清热降火，除烦生津。两者常相须为用（白虎汤）。"},
    {"name": "丹皮, 生地", "大类": "常见中药", "子类": "清热凉血", "notes": "清解血分实热。丹皮兼活血退虚热，生地兼滋阴生津。"},
    {"name": "黄连, 黄芩, 黄柏", "大类": "常见中药", "子类": "清热燥湿", "notes": "苦寒燥湿，泻火解毒。黄连主中焦/心胃，黄芩主上焦/肺，黄柏主下焦/肾。"},
    {"name": "金银花, 连翘, 蒲公英", "大类": "常见中药", "子类": "清热解毒", "notes": "连翘为疮家圣药，蒲公英为治疗乳痈要药。"},
    {"name": "大黄, 芒硝", "大类": "常见中药", "子类": "攻下药", "notes": "大黄泻热通便、活血祛瘀；芒硝润燥软坚。两者常相须为用。"},
    {"name": "甘遂, 芫花", "大类": "常见中药", "子类": "峻下逐水药", "notes": "毒性猛烈，排积水。与甘草合用毒性增强（十八反）。甘遂逐水最猛。"},
    {"name": "神曲, 山楂, 麦芽 (焦三仙)", "大类": "常见中药", "子类": "消导药", "notes": "健脾胃，消食化积。神曲消谷食，山楂消肉食，麦芽消面食。"},
    {"name": "半夏, 天南星", "大类": "常见中药", "子类": "温化寒痰", "notes": "半夏为治湿痰要药；天南星温燥强，为治风痰要药。"},
    {"name": "川贝, 浙贝", "大类": "常见中药", "子类": "清化热痰", "notes": "川贝润而甘，主治燥痰久咳；浙贝苦泄散结强，主治热痰及瘰疬。"},
    {"name": "附子, 肉桂, 干姜", "大类": "常见中药", "子类": "温里药", "notes": "附子回阳救逆要药，干姜温中散寒主药，肉桂引火归元。"},
    {"name": "陈皮, 茯苓, 苍术", "大类": "常见中药", "子类": "理气祛湿", "notes": "陈皮行气健脾，茯苓利水渗湿，苍术芳香化湿。"},
    {"name": "人参, 黄芪, 白术", "大类": "常见中药", "子类": "补气药", "notes": "人参大补元气，黄芪补气升阳固表，白术补气健脾燥湿。"},
    {"name": "当归, 熟地", "大类": "常见中药", "子类": "补血药", "notes": "当归补血活血调经，熟地补血滋阴益精填髓。"}
]

# 3. Define Comparisons data
comparisons_data = [
    {"name": "人参 vs 党参", "大类": "中药对比", "子类": "补虚药对比", "notes": "**共性**：均能补脾益肺，生津养血。\n**人参**（重症）：大补元气、复脉固脱，救气虚欲脱危证。\n**党参**（轻症）：药力弱，无固脱之功，不可代人参救急。"},
    {"name": "人参 vs 黄芪", "大类": "中药对比", "子类": "补虚药对比", "notes": "**共性**：均为补气要药。\n**人参**（主内）：补心脾肺，大补元气，治内伤第一要药。\n**黄芪**（主表/升）：补气升阳，固表止汗、托毒生肌、利水退肿。"},
    {"name": "黄芪 vs 白术", "大类": "中药对比", "子类": "补气药对比", "notes": "**共性**：补气利水止汗。\n**黄芪**（升提）：脾肺双补，长于升阳固表。\n**白术**（除湿）：仅补气健脾，长于健脾除湿。"},
    {"name": "生地黄 vs 熟地黄", "大类": "中药对比", "子类": "地黄辨析", "notes": "**共性**：养阴滋阴。\n**生地黄**（寒）：清热凉血，主治热证火证、血热妄行。\n**熟地黄**（温）：补血滋阴，益精填髓，绝对无清热凉血之功。"},
    {"name": "天冬 vs 麦冬", "大类": "中药对比", "子类": "滋阴药对比", "notes": "**共性**：性寒凉，养肺阴。\n**天冬**（偏下）：寒润力强，滋肾阴而清降虚火。\n**麦冬**（偏上）：寒润力弱，养胃生津、润肺清心。"},
    {"name": "杜仲 vs 续断", "大类": "中药对比", "子类": "补阳药对比", "notes": "**共性**：补肝肾，强筋骨，止血安胎。\n**杜仲**：纯补肝肾，可降血压。\n**续断**：补而不滞，兼通筋脉活血，治血脉郁滞之风湿跌打。"},
    {"name": "麝香 vs 冰片", "大类": "中药对比", "子类": "开窍药对比", "notes": "**共性**：味辛气香，开窍醒神。\n**麝香**（温）：开窍力极强，宜寒闭，兼活血通经催产。\n**冰片**（寒）：开窍力较弱，宜热闭，兼清热解毒止痛。"}
]

# Combine all
all_data = formulas + herbs_data + comparisons_data

# Read HTML and replace raw data
with open(html_file, 'r', encoding='utf-8') as f:
    html_content = f.read()

# Replace the array in `const raw = [...]`
import re
pattern = re.compile(r'const raw = \[.*?\];', re.DOTALL)
new_js_var = "const raw = " + json.dumps(all_data, ensure_ascii=False) + ";"

if pattern.search(html_content):
    new_html = pattern.sub(new_js_var, html_content)
else:
    print("Could not find 'const raw = [...]' in HTML.")
    exit(1)

# Write back
with open(html_file, 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Successfully embedded {len(all_data)} items into {html_file}.")