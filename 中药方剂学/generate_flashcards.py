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
    <title>Liquid Prism Flashcards</title>
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.35);
            --glass-border: rgba(255, 255, 255, 0.4);
            --text-main: #1d1d1f;
            --accent: #0071e3;
        }
        
        * {
            box-sizing: border-box;
            -webkit-tap-highlight-color: transparent;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #e2eafc 0%, #cfdef3 100%);
            margin: 0;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            overflow: hidden;
            color: var(--text-main);
            -webkit-font-smoothing: antialiased;
        }

        /* Ambient Background */
        .ambient {
            position: absolute;
            width: 40vw;
            height: 40vw;
            background: radial-gradient(circle, rgba(0,113,227,0.15) 0%, rgba(255,255,255,0) 70%);
            border-radius: 50%;
            z-index: -1;
            filter: blur(60px);
        }
        .a1 { top: 5%; left: 5%; }
        .a2 { bottom: 5%; right: 5%; width: 50vw; height: 50vw; }

        /* Scene & Cube */
        .scene {
            width: 90vw;
            height: 75vh;
            max-width: 380px;
            max-height: 600px;
            perspective: 2000px;
            position: relative;
        }

        .cube {
            width: 100%;
            height: 100%;
            position: relative;
            transform-style: preserve-3d;
            transition: transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1);
        }

        .face {
            position: absolute;
            width: 100%;
            height: 100%;
            border-radius: 35px;
            background: var(--glass-bg);
            backdrop-filter: blur(20px) saturate(180%);
            -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--glass-border);
            box-shadow: 0 10px 40px rgba(0,0,0,0.06);
            padding: 45px 35px;
            overflow: hidden;
            backface-visibility: hidden;
            -webkit-backface-visibility: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            transform-origin: center center;
        }

        /* Glossy Lighting */
        .face::after {
            content: "";
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: linear-gradient(
                135deg,
                rgba(255, 255, 255, 0) 0%,
                rgba(255, 255, 255, 0.05) 45%,
                rgba(255, 255, 255, 0.3) 50%,
                rgba(255, 255, 255, 0.05) 55%,
                rgba(255, 255, 255, 0) 100%
            );
            transform: rotate(-10deg);
            pointer-events: none;
            z-index: 10;
        }

        /* Face Positioning - Using a "square" prism logic to avoid gaps */
        /* Distance to center = width / 2 */
        .face-front  { transform: rotateY(0deg) translateZ(190px); }
        .face-back   { transform: rotateY(180deg) translateZ(190px); }
        .face-right  { transform: rotateY(90deg) translateZ(190px); }
        .face-left   { transform: rotateY(-90deg) translateZ(190px); }

        /* Typography & Layout */
        .content-front {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            text-align: center;
        }

        .content-back {
            width: 100%;
            height: 100%;
            display: flex;
            flex-direction: column;
            text-align: left;
            overflow-y: auto;
            padding-right: 5px;
        }
        
        /* Custom scrollbar for glass */
        .content-back::-webkit-scrollbar { width: 4px; }
        .content-back::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }

        .name {
            font-size: 2.6rem;
            font-weight: 800;
            line-height: 1.1;
            margin-bottom: 20px;
            color: #1d1d1f;
            letter-spacing: -0.03em;
        }

        .sub-name {
            font-size: 0.9rem;
            font-weight: 600;
            color: rgba(0, 0, 0, 0.4);
            text-transform: uppercase;
            letter-spacing: 0.15em;
            margin-bottom: 8px;
        }

        .reveal-hint {
            font-size: 0.65rem;
            color: rgba(0,0,0,0.2);
            letter-spacing: 0.3em;
            margin-top: 30px;
            text-transform: uppercase;
        }

        .role-group { margin-bottom: 22px; }
        .role-label {
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 0.08em;
            margin-bottom: 5px;
        }
        .role-content { font-size: 1.1rem; font-weight: 500; color: #333; }

        .notes {
            margin-top: auto;
            font-size: 0.85rem;
            line-height: 1.6;
            color: rgba(0,0,0,0.5);
            padding-top: 20px;
            border-top: 1px solid rgba(0,0,0,0.06);
            font-style: italic;
        }

        /* Minimal Controls */
        .top-pill {
            position: absolute;
            top: -70px;
            left: 50%;
            transform: translateX(-50%);
            background: rgba(255,255,255,0.6);
            backdrop-filter: blur(15px);
            padding: 8px 18px;
            border-radius: 25px;
            border: 1px solid var(--glass-border);
            display: flex;
            gap: 15px;
            align-items: center;
            z-index: 100;
            box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
        
        select {
            background: transparent;
            border: none;
            outline: none;
            font-size: 0.7rem;
            font-weight: 700;
            color: var(--text-main);
            text-transform: uppercase;
            cursor: pointer;
        }

        .status {
            position: absolute;
            bottom: -60px;
            width: 100%;
            text-align: center;
            font-size: 0.75rem;
            font-weight: 700;
            color: rgba(0,0,0,0.25);
            letter-spacing: 0.2em;
        }
    </style>
</head>
<body>
    <div class="ambient a1"></div>
    <div class="ambient a2"></div>

    <div class="scene">
        <div class="top-pill">
            <select id="filter">
                <option value="all">COLLECTION</option>
            </select>
            <div id="shuffle" style="cursor:pointer; font-size:0.7rem; font-weight:700; opacity:0.6">SHUFFLE</div>
        </div>

        <div id="cube" class="cube">
            <div id="f-front" class="face face-front"></div>
            <div id="f-back" class="face face-back"></div>
            <div id="f-right" class="face face-right" style="opacity:0"></div>
            <div id="f-left" class="face face-left" style="opacity:0"></div>
        </div>

        <div class="status" id="status">0 / 0</div>
    </div>

    <script>
        const raw = """ + json.dumps(all_data, ensure_ascii=False) + """;
        let list = [...raw];
        let idx = 0;
        let rotation = 0;
        let flipped = false;
        let busy = false;

        const cube = document.getElementById('cube');
        const fFront = document.getElementById('f-front');
        const fBack = document.getElementById('f-back');
        const fRight = document.getElementById('f-right');
        const fLeft = document.getElementById('f-left');
        const status = document.getElementById('status');
        const filter = document.getElementById('filter');
        const shuffle = document.getElementById('shuffle');

        // Populate Filter
        const cats = [...new Set(raw.map(i => i.大类).filter(Boolean))].sort();
        cats.forEach(c => {
            const o = document.createElement('option');
            o.value = c; o.textContent = c;
            filter.appendChild(o);
        });

        function getFront(item) {
            return `
                <div class="content-front">
                    <div class="sub-name">${item.大类 || 'Formula'}</div>
                    <div class="name">${item.name}</div>
                    <div class="reveal-hint">Tap to Open</div>
                </div>
            `;
        }

        function getBack(item) {
            let c = '';
            ['君药', '臣药', '佐药', '使药'].forEach(r => {
                if (item[r] && item[r].length > 0 && item[r][0]) {
                    c += `<div class="role-group"><div class="role-label">${r}</div><div class="role-content">${item[r].join('、')}</div></div>`;
                }
            });
            if (!c && item.组成) c = `<div class="role-group"><div class="role-label">Composition</div><div class="role-content">${item.组成.join('、')}</div></div>`;
            return `
                <div class="content-back">
                    <div style="font-size:0.75rem; font-weight:800; opacity:0.25; margin-bottom:25px; letter-spacing:0.1em; text-transform:uppercase">${item.name} Details</div>
                    ${c}
                    ${item.notes ? `<div class="notes">${item.notes}</div>` : ''}
                </div>
            `;
        }

        function update() {
            if (list.length === 0) return;
            fFront.innerHTML = getFront(list[idx]);
            fBack.innerHTML = getBack(list[idx]);
            status.textContent = `${idx + 1} / ${list.length}`;
        }

        function navigate(step) {
            if (busy || list.length < 2) return;
            const nIdx = (idx + step + list.length) % list.length;
            
            busy = true;
            flipped = false;
            
            // Prepare side face
            const side = step > 0 ? fRight : fLeft;
            side.style.opacity = "1";
            side.innerHTML = getFront(list[nIdx]);

            // Rotate
            rotation -= step * 90;
            cube.style.transform = `rotateY(${rotation}deg)`;

            setTimeout(() => {
                idx = nIdx;
                cube.style.transition = "none";
                rotation = 0;
                cube.style.transform = "rotateY(0deg)";
                update();
                fRight.style.opacity = "0";
                fLeft.style.opacity = "0";
                setTimeout(() => {
                    cube.style.transition = "transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)";
                    busy = false;
                }, 50);
            }, 800);
        }

        function flip() {
            if (busy) return;
            flipped = !flipped;
            rotation += 180;
            cube.style.transform = `rotateY(${rotation}deg)`;
        }

        cube.onclick = flip;

        // Gestures
        let sX = 0;
        document.addEventListener('touchstart', e => sX = e.touches[0].clientX);
        document.addEventListener('touchend', e => {
            const d = e.changedTouches[0].clientX - sX;
            if (Math.abs(d) > 60) navigate(d > 0 ? -1 : 1);
        });

        // Keys
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowLeft') navigate(-1);
            if (e.key === 'ArrowRight') navigate(1);
            if (e.key === ' ' || e.key === 'Enter') flip();
        });

        filter.onchange = e => {
            const v = e.target.value;
            list = v === 'all' ? [...raw] : raw.filter(i => i.大类 === v);
            idx = 0; rotation = 0; flipped = false;
            cube.style.transform = "rotateY(0deg)";
            update();
        };

        shuffle.onclick = () => {
            list.sort(() => Math.random() - 0.5);
            idx = 0; rotation = 0; flipped = false;
            cube.style.transform = "rotateY(0deg)";
            update();
        };

        update();
    </script>
</body>
</html>
"""
    with open(output_html, 'w', encoding='utf-8') as f:
        f.write(html_template)
    print(f"Successfully generated {output_html}")

if __name__ == "__main__":
    generate()
