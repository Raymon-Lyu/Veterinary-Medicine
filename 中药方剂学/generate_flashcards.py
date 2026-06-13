import os
import json
import re

def parse_yaml_simple(yaml_str):
    """
    A simple YAML parser for the specific format in the fangji markdown files.
    """
    data = {}
    current_key = None
    lines = yaml_str.split('\n')
    for line in lines:
        if not line.strip():
            continue
        # Check for key: value
        match = re.match(r'^(\w+):\s*(.*)$', line)
        if match:
            current_key = match.group(1)
            value = match.group(2).strip()
            if value == '':
                data[current_key] = []
            else:
                data[current_key] = value
        # Check for list items
        elif line.startswith('  - '):
            item = line[4:].strip()
            if item and current_key in data and isinstance(data[current_key], list):
                data[current_key].append(item)
    return data

def generate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    src_dir = os.path.join(base_dir, '方剂库')
    output_json = os.path.join(base_dir, 'fangji_data.json')
    output_html = os.path.join(base_dir, 'fangji_flashcards.html')

    if not os.path.exists(src_dir):
        print(f"Error: {src_dir} not found.")
        return

    all_data = []
    
    for filename in os.listdir(src_dir):
        if filename.endswith('.md'):
            filepath = os.path.join(src_dir, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split by frontmatter delimiters
            parts = content.split('---')
            if len(parts) >= 3:
                yaml_content = parts[1]
                notes = '---'.join(parts[2:]).strip()
                
                entry = parse_yaml_simple(yaml_content)
                entry['name'] = filename.replace('.md', '')
                entry['notes'] = notes
                all_data.append(entry)

    # Write JSON
    with open(output_json, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, ensure_ascii=False, indent=2)
    print(f"Successfully generated {output_json}")

    # Generate HTML
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <title>中药方剂翻转记忆卡</title>
    <style>
        :root {
            --primary-color: #4a7c59;
            --bg-color: #f4f7f6;
            --card-front-bg: #ffffff;
            --card-back-bg: #e9f5ee;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif, "Microsoft YaHei";
            background-color: var(--bg-color);
            margin: 0;
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        h1 { color: var(--primary-color); }
        .controls {
            margin-bottom: 20px;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        select {
            padding: 8px 12px;
            border-radius: 5px;
            border: 1px solid #ccc;
            font-size: 16px;
        }
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            width: 100%;
            max-width: 1200px;
        }
        .card {
            background-color: transparent;
            width: 100%;
            height: 380px;
            perspective: 1000px;
            cursor: pointer;
        }
        .card-inner {
            position: relative;
            width: 100%;
            height: 100%;
            text-align: center;
            transition: transform 0.6s;
            transform-style: preserve-3d;
            box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
            border-radius: 10px;
        }
        .card.flipped .card-inner {
            transform: rotateY(180deg);
        }
        .card-front, .card-back {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 10px;
            display: flex;
            flex-direction: column;
            padding: 20px;
            box-sizing: border-box;
            overflow-y: auto;
        }
        .card-front {
            background-color: var(--card-front-bg);
            color: black;
            justify-content: center;
        }
        .card-back {
            background-color: var(--card-back-bg);
            color: #333;
            transform: rotateY(180deg);
            text-align: left;
        }
        .card-name { font-size: 24px; font-weight: bold; margin-bottom: 10px; color: var(--primary-color); }
        .card-type { font-size: 14px; color: #666; margin-bottom: 5px; }
        .card-label { font-weight: bold; color: var(--primary-color); margin-top: 10px; border-bottom: 1px solid #ddd; }
        .card-list { margin: 5px 0; padding-left: 20px; font-size: 14px; }
        .card-notes { font-size: 13px; color: #555; margin-top: 15px; font-style: italic; white-space: pre-wrap; border-top: 1px dashed #ccc; padding-top: 10px; }
        
        /* 移动端优化 */
        @media (max-width: 600px) {
            .container { grid-template-columns: 1fr; }
        }
    </style>
</head>
<body>
    <h1>🌿 中药方剂翻转记忆卡</h1>
    
    <div class="controls">
        <label for="category-filter">筛选大类：</label>
        <select id="category-filter">
            <option value="all">全部</option>
        </select>
        <span id="stats"></span>
    </div>

    <div class="container" id="card-container"></div>

    <script>
        const fangjiData = """ + json.dumps(all_data, ensure_ascii=False) + """;

        const container = document.getElementById('card-container');
        const filter = document.getElementById('category-filter');
        const stats = document.getElementById('stats');

        // Populate Filter
        const categories = [...new Set(fangjiData.map(item => item.大类).filter(Boolean))];
        categories.sort().forEach(cat => {
            const opt = document.createElement('option');
            opt.value = cat;
            opt.textContent = cat;
            filter.appendChild(opt);
        });

        function renderCards(data) {
            container.innerHTML = '';
            data.forEach(item => {
                const card = document.createElement('div');
                card.className = 'card';
                card.onclick = () => card.classList.toggle('flipped');

                const inner = document.createElement('div');
                inner.className = 'card-inner';

                // Front
                const front = document.createElement('div');
                front.className = 'card-front';
                front.innerHTML = `
                    <div class="card-name">${item.name}</div>
                    <div class="card-type">${item.大类 || ''} - ${item.子类 || ''}</div>
                    <div style="font-size: 12px; color: #999; margin-top: 20px;">(点击翻面查看组成)</div>
                `;

                // Back
                const back = document.createElement('div');
                back.className = 'card-back';
                
                let compositionHtml = '';
                const roles = ['君药', '臣药', '佐药', '使药'];
                roles.forEach(role => {
                    const drugs = item[role];
                    if (drugs && Array.isArray(drugs) && drugs.length > 0 && drugs[0] !== null && drugs[0] !== '') {
                        compositionHtml += `<div class="card-label">${role}</div><div class="card-list">${drugs.join('、')}</div>`;
                    }
                });

                if (!compositionHtml && item.组成) {
                    compositionHtml += `<div class="card-label">组成</div><div class="card-list">${item.组成.join('、')}</div>`;
                }

                const notesHtml = item.notes ? `<div class="card-notes">${item.notes}</div>` : '';

                back.innerHTML = `
                    <div style="font-weight: bold; font-size: 18px; border-bottom: 2px solid var(--primary-color); padding-bottom: 5px; margin-bottom: 10px;">${item.name}</div>
                    ${compositionHtml}
                    ${notesHtml}
                `;

                inner.appendChild(front);
                inner.appendChild(back);
                card.appendChild(inner);
                container.appendChild(card);
            });
            stats.textContent = `共 ${data.length} 个方剂`;
        }

        filter.onchange = (e) => {
            const val = e.target.value;
            const filtered = val === 'all' ? fangjiData : fangjiData.filter(item => item.大类 === val);
            renderCards(filtered);
        };

        // Initial render
        renderCards(fangjiData);
    </script>
</body>
</html>
"""
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    generate()
