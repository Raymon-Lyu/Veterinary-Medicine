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
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Liquid Flashcards</title>
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.4);
            --glass-border: rgba(255, 255, 255, 0.5);
            --text-main: #1d1d1f;
            --accent: #0071e3;
        }
        
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            color: var(--text-main);
        }

        /* Ambient Background shapes */
        .ambient {
            position: absolute;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, rgba(0,113,227,0.2) 0%, rgba(255,255,255,0) 70%);
            border-radius: 50%;
            z-index: -1;
            filter: blur(50px);
        }
        .a1 { top: 10%; left: 10%; }
        .a2 { bottom: 10%; right: 10%; width: 400px; height: 400px; }

        .app-container {
            width: 90vw;
            height: 80vh;
            max-width: 400px;
            max-height: 650px;
            position: relative;
            perspective: 2000px;
        }

        /* Animation Classes */
        .slide-left {
            transform: translateX(-120%) rotate(-10deg) !important;
            opacity: 0;
        }
        .slide-right {
            transform: translateX(120%) rotate(10deg) !important;
            opacity: 0;
        }
        .slide-in-right {
            animation: slideInRight 0.5s cubic-bezier(0.23, 1, 0.32, 1) forwards;
        }
        .slide-in-left {
            animation: slideInLeft 0.5s cubic-bezier(0.23, 1, 0.32, 1) forwards;
        }

        @keyframes slideInRight {
            from { transform: translateX(100%) rotate(5deg); opacity: 0; }
            to { transform: translateX(0) rotate(0); opacity: 1; }
        }
        @keyframes slideInLeft {
            from { transform: translateX(-100%) rotate(-5deg); opacity: 0; }
            to { transform: translateX(0) rotate(0); opacity: 1; }
        }

        /* Glassmorphism Card */
        .card {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.23, 1, 0.32, 1), opacity 0.5s ease;
            cursor: pointer;
        }

        .card.flipped {
            transform: rotateY(180deg);
        }

        .card-face {
            position: absolute;
            width: 100%;
            height: 100%;
            backface-visibility: hidden;
            border-radius: 30px;
            background: var(--glass-bg);
            backdrop-filter: blur(25px) saturate(180%);
            -webkit-backdrop-filter: blur(25px) saturate(180%);
            border: 1px solid var(--glass-border);
            box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
            display: flex;
            flex-direction: column;
            padding: 40px 30px;
        }

        .card-front {
            justify-content: center;
            align-items: center;
            text-align: center;
        }

        .card-back {
            transform: rotateY(180deg);
            overflow-y: auto;
        }

        /* Typography */
        .name {
            font-size: 2.8rem;
            font-weight: 700;
            letter-spacing: -0.02em;
            margin-bottom: 15px;
            background: linear-gradient(180deg, #1d1d1f 0%, #434344 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .sub-name {
            font-size: 0.95rem;
            font-weight: 500;
            color: rgba(0, 0, 0, 0.5);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .role-group { margin-bottom: 20px; }
        .role-label {
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 6px;
        }
        .role-content {
            font-size: 1.15rem;
            font-weight: 500;
            color: #1d1d1f;
        }

        .notes {
            margin-top: auto;
            font-size: 0.9rem;
            line-height: 1.5;
            color: rgba(0,0,0,0.6);
            padding-top: 20px;
            border-top: 1px solid rgba(0,0,0,0.05);
            font-style: italic;
        }

        /* Minimal Status */
        .status-bar {
            position: absolute;
            bottom: -50px;
            width: 100%;
            display: flex;
            justify-content: center;
            font-size: 0.8rem;
            font-weight: 600;
            color: rgba(0,0,0,0.3);
            letter-spacing: 0.1em;
        }

        /* Hidden controls for swipe feel */
        .nav-trigger {
            position: absolute;
            top: 0;
            height: 100%;
            width: 15%;
            z-index: 100;
        }
        .nav-prev { left: -15%; }
        .nav-next { right: -15%; }

        /* Filter pill */
        .top-pill {
            position: absolute;
            top: -60px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.5);
            backdrop-filter: blur(10px);
            padding: 6px 15px;
            border-radius: 20px;
            border: 1px solid var(--glass-border);
            font-size: 0.75rem;
            display: flex;
            gap: 10px;
            align-items: center;
        }
        select {
            background: transparent;
            border: none;
            outline: none;
            font-size: 0.75rem;
            font-weight: 600;
            color: var(--text-main);
            cursor: pointer;
        }
    </style>
</head>
<body>
    <div class="ambient a1"></div>
    <div class="ambient a2"></div>

    <div class="app-container">
        <div class="top-pill">
            <select id="filter">
                <option value="all">ALL CATEGORIES</option>
            </select>
            <span id="shuffle" style="cursor:pointer">SHUFFLE</span>
        </div>

        <div id="card" class="card">
            <div class="card-face card-front" id="front"></div>
            <div class="card-face card-back" id="back"></div>
        </div>

        <div class="status-bar" id="status">0 / 0</div>
    </div>

    <script>
        const data = """ + json.dumps(all_data, ensure_ascii=False) + """;
        let displayList = [...data];
        let index = 0;

        const card = document.getElementById('card');
        const front = document.getElementById('front');
        const back = document.getElementById('back');
        const status = document.getElementById('status');
        const filter = document.getElementById('filter');
        const shuffle = document.getElementById('shuffle');

        // Init Filter
        const cats = [...new Set(data.map(i => i.大类).filter(Boolean))].sort();
        cats.forEach(c => {
            const el = document.createElement('option');
            el.value = c; el.textContent = c.toUpperCase();
            filter.appendChild(el);
        });

        function render() {
            if (displayList.length === 0) return;
            card.classList.remove('flipped');
            const item = displayList[index];
            
            front.innerHTML = `
                <div class="sub-name">${item.大类 || 'FORMULA'}</div>
                <div class="name">${item.name}</div>
                <div style="font-size:0.7rem; opacity:0.3; margin-top:20px; letter-spacing:0.2em">TAP TO REVEAL</div>
            `;

            let comp = '';
            ['君药', '臣药', '佐药', '使药'].forEach(r => {
                if (item[r] && item[r].length > 0 && item[r][0]) {
                    comp += `<div class="role-group"><div class="role-label">${r}</div><div class="role-content">${item[r].join('、')}</div></div>`;
                }
            });
            if (!comp && item.组成) {
                comp = `<div class="role-group"><div class="role-label">组成</div><div class="role-content">${item.组成.join('、')}</div></div>`;
            }

            back.innerHTML = `
                <div style="font-size:0.8rem; font-weight:700; opacity:0.3; margin-bottom:30px; letter-spacing:0.1em">${item.name.toUpperCase()} DETAILS</div>
                ${comp}
                ${item.notes ? `<div class="notes">${item.notes}</div>` : ''}
            `;

            status.textContent = `${index + 1} / ${displayList.length}`;
        }

        function navigate(dir) {
            if (dir === 'next' && index < displayList.length - 1) {
                card.classList.add('slide-left');
                setTimeout(() => {
                    index++;
                    render();
                    card.classList.remove('slide-left');
                    card.classList.add('slide-in-right');
                    setTimeout(() => card.classList.remove('slide-in-right'), 500);
                }, 300);
            } else if (dir === 'prev' && index > 0) {
                card.classList.add('slide-right');
                setTimeout(() => {
                    index--;
                    render();
                    card.classList.remove('slide-right');
                    card.classList.add('slide-in-left');
                    setTimeout(() => card.classList.remove('slide-in-left'), 500);
                }, 300);
            }
        }

        card.onclick = () => card.classList.toggle('flipped');

        // Gesture handling
        let startX = 0;
        document.addEventListener('touchstart', e => startX = e.touches[0].clientX);
        document.addEventListener('touchend', e => {
            const endX = e.changedTouches[0].clientX;
            const diff = endX - startX;
            if (Math.abs(diff) > 50) {
                if (diff > 0) navigate('prev');
                else if (diff < 0) navigate('next');
            }
        });

        // Desktop keyboard support
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowLeft') navigate('prev');
            if (e.key === 'ArrowRight') navigate('next');
            if (e.key === ' ' || e.key === 'Enter') card.onclick();
        });

        filter.onchange = (e) => {
            displayList = e.target.value === 'all' ? [...data] : data.filter(i => i.大类 === e.target.value);
            index = 0;
            render();
        };

        shuffle.onclick = () => {
            displayList.sort(() => Math.random() - 0.5);
            index = 0;
            render();
        };

        render();
    </script>
</body>
</html>
"""
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    generate()
