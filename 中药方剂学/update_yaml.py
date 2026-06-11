import os
import glob
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    match = re.match(r'^---\n(.*?)\n---\n(.*)', content, flags=re.DOTALL)
    if not match:
        return

    frontmatter = match.group(1)
    body = match.group(2)

    lines = frontmatter.split('\n')
    
    parsed = {}
    order = []
    current_key = None
    
    for line in lines:
        if not line.strip():
            continue
        
        m_key = re.match(r'^([^ ]+?):\s*(.*)$', line)
        if m_key and not line.startswith(' ') and not line.startswith('-'):
            key = m_key.group(1)
            val = m_key.group(2).strip()
            current_key = key
            if current_key not in order:
                order.append(current_key)
            if val:
                parsed[current_key] = val
            else:
                parsed[current_key] = []
        elif (line.startswith('  -') or line.startswith('- ')) and current_key is not None:
            item = line.strip()[1:].strip()
            if item:
                if isinstance(parsed[current_key], str):
                    parsed[current_key] = [parsed[current_key]]
                parsed[current_key].append(item)
    
    ingredients = []
    for k in ['组成', '君药', '臣药', '佐药', '使药', '主要药味']:
        if k in parsed:
            val = parsed[k]
            if isinstance(val, list):
                ingredients.extend(val)
            elif isinstance(val, str) and val:
                ingredients.append(val)
    
    # deduplicate but preserve order
    ingredients = list(dict.fromkeys(ingredients))
    
    new_lines = ['---']
    
    for key in order:
        if key in ['组成', '君药', '臣药', '佐药', '使药', '主要药味']:
            continue
            
        val = parsed[key]
        if isinstance(val, list):
            new_lines.append(f"{key}:")
            for item in val:
                new_lines.append(f"  - {item}")
        else:
            new_lines.append(f"{key}: {val}")
            
    if ingredients:
        new_lines.append("组成:")
        for item in ingredients:
            new_lines.append(f"  - {item}")
            
    for k in ['君药', '臣药', '佐药', '使药']:
        if k in parsed:
            val = parsed[k]
            if isinstance(val, list) and len(val) > 0:
                new_lines.append(f"{k}:")
                for item in val:
                    new_lines.append(f"  - {item}")
            elif isinstance(val, str) and val:
                new_lines.append(f"{k}: {val}")

    new_lines.append('---')
    new_frontmatter = '\n'.join(new_lines)
    
    new_content = new_frontmatter + '\n' + body
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(new_content)

files = glob.glob(r"D:/just_soso/horse cow/Veterinary Medicine/中药方剂学/方剂库/*.md")
for f in files:
    try:
        process_file(f)
    except Exception as e:
        print(f"Failed to process {f}: {e}")
print(f"Processed {len(files)} files.")
