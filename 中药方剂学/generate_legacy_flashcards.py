import os
import json
import re

def parse_legacy_fangji(content):
    blocks = content.split('%')
    data = []
    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if not lines:
            continue
        
        entry = {
            "name": lines[0],
            "大类": "前人的遗物-方剂",
            "子类": lines[1] if len(lines) > 1 else "",
            "组成": [],
            "notes": ""
        }
        
        # Simple extraction for legacy format
        current_section = None
        for line in lines[2:]:
            if "组成" in line or "方剂组成" in line:
                current_section = "composition"
                continue
            elif "主治" in line:
                current_section = "notes"
                entry["notes"] += "【主治】\n"
                continue
            elif "功效" in line:
                current_section = "notes"
                entry["notes"] += "【功效】\n"
                continue
            
            if current_section == "composition":
                entry["组成"].append(line)
            elif current_section == "notes":
                entry["notes"] += line + "\n"
            else:
                entry["notes"] += line + "\n"
        
        data.append(entry)
    return data

def parse_legacy_herbs(content):
    blocks = content.split('%')
    data = []
    for block in blocks:
        lines = [l.strip() for l in block.strip().split('\n') if l.strip()]
        if not lines:
            continue
        
        entry = {
            "name": lines[0],
            "大类": "前人的遗物-常用中药",
            "子类": "中药分类",
            "组成": [],
            "notes": "\n".join(lines[1:])
        }
        data.append(entry)
    return data

def generate():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    legacy_dir = os.path.join(base_dir, '前人的遗物')
    output_html = os.path.join(base_dir, 'legacy_flashcards.html')

    all_data = []
    
    # Process Fangji.txt
    fangji_path = os.path.join(legacy_dir, '方剂.txt')
    if os.path.exists(fangji_path):
        with open(fangji_path, 'r', encoding='utf-8') as f:
            all_data.extend(parse_legacy_fangji(f.read()))
    
    # Process Herbs.txt
    herbs_path = os.path.join(legacy_dir, '常用中药.txt')
    if os.path.exists(herbs_path):
        with open(herbs_path, 'r', encoding='utf-8') as f:
            all_data.extend(parse_legacy_herbs(f.read()))

    # Generate HTML (Liquid Prism Template)
    html_template = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>Legacy Liquid Prism</title>
    <style>
        :root {
            --glass-bg: rgba(255, 255, 255, 0.35);
            --glass-border: rgba(255, 255, 255, 0.4);
            --text-main: #1d1d1f;
            --accent: #d4a373;
        }
        
        * { box-sizing: border-box; -webkit-tap-highlight-color: transparent; }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Icons", "Helvetica Neue", Helvetica, Arial, sans-serif;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            margin: 0; height: 100vh; display: flex; justify-content: center; align-items: center; overflow: hidden; color: var(--text-main);
        }

        .ambient { position: absolute; width: 40vw; height: 40vw; border-radius: 50%; z-index: -1; filter: blur(60px); }
        .a1 { top: 5%; left: 5%; background: radial-gradient(circle, rgba(212,163,115,0.15) 0%, rgba(255,255,255,0) 70%); }
        .a2 { bottom: 5%; right: 5%; background: radial-gradient(circle, rgba(108,117,125,0.1) 0%, rgba(255,255,255,0) 70%); }

        .scene { width: 90vw; height: 75vh; max-width: 380px; max-height: 600px; perspective: 2000px; position: relative; }
        .cube { width: 100%; height: 100%; position: relative; transform-style: preserve-3d; transition: transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1); }

        .face {
            position: absolute; width: 100%; height: 100%; border-radius: 35px;
            background: var(--glass-bg); backdrop-filter: blur(20px) saturate(180%); -webkit-backdrop-filter: blur(20px) saturate(180%);
            border: 1px solid var(--glass-border); box-shadow: 0 10px 40px rgba(0,0,0,0.06); padding: 45px 35px;
            overflow: hidden; backface-visibility: hidden; display: flex; flex-direction: column; align-items: center; justify-content: center;
        }

        .face::after {
            content: ""; position: absolute; top: -50%; left: -50%; width: 200%; height: 200%;
            background: linear-gradient(135deg, rgba(255, 255, 255, 0) 0%, rgba(255, 255, 255, 0.05) 45%, rgba(255, 255, 255, 0.3) 50%, rgba(255, 255, 255, 0.05) 55%, rgba(255, 255, 255, 0) 100%);
            transform: rotate(-10deg); pointer-events: none; z-index: 10;
        }

        .face-front  { transform: rotateY(0deg) translateZ(190px); }
        .face-back   { transform: rotateY(180deg) translateZ(190px); }
        .face-right  { transform: rotateY(90deg) translateZ(190px); }
        .face-left   { transform: rotateY(-90deg) translateZ(190px); }

        .content-front { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100%; text-align: center; }
        .content-back { width: 100%; height: 100%; display: flex; flex-direction: column; text-align: left; overflow-y: auto; }
        
        .content-back::-webkit-scrollbar { width: 4px; }
        .content-back::-webkit-scrollbar-thumb { background: rgba(0,0,0,0.1); border-radius: 10px; }

        .name { font-size: 2.2rem; font-weight: 800; line-height: 1.2; margin-bottom: 20px; color: #1d1d1f; letter-spacing: -0.02em; }
        .sub-name { font-size: 0.85rem; font-weight: 600; color: rgba(0, 0, 0, 0.4); text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 8px; }
        .reveal-hint { font-size: 0.6rem; color: rgba(0,0,0,0.2); letter-spacing: 0.3em; margin-top: 30px; text-transform: uppercase; }

        .role-group { margin-bottom: 15px; }
        .role-label { font-size: 0.7rem; font-weight: 700; color: var(--accent); text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 4px; }
        .role-content { font-size: 1rem; font-weight: 500; color: #333; line-height: 1.4; }
        .notes { margin-top: auto; font-size: 0.85rem; line-height: 1.5; color: rgba(0,0,0,0.6); padding-top: 15px; border-top: 1px solid rgba(0,0,0,0.05); white-space: pre-wrap; }

        .top-pill {
            position: absolute; top: -70px; left: 50%; transform: translateX(-50%);
            background: rgba(255,255,255,0.6); backdrop-filter: blur(15px); padding: 8px 18px; border-radius: 25px;
            border: 1px solid var(--glass-border); display: flex; gap: 15px; align-items: center; z-index: 100; box-shadow: 0 4px 15px rgba(0,0,0,0.03);
        }
        select { background: transparent; border: none; outline: none; font-size: 0.7rem; font-weight: 700; color: var(--text-main); text-transform: uppercase; cursor: pointer; }
        .status { position: absolute; bottom: -60px; width: 100%; text-align: center; font-size: 0.7rem; font-weight: 700; color: rgba(0,0,0,0.25); letter-spacing: 0.15em; }
    </style>
</head>
<body>
    <div class="ambient a1"></div>
    <div class="ambient a2"></div>

    <div class="scene">
        <div class="top-pill">
            <select id="filter"><option value="all">LEGACY VAULT</option></select>
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
        let list = [...raw]; let idx = 0; let rotation = 0; let flipped = false; let busy = false;

        const cube = document.getElementById('cube');
        const fFront = document.getElementById('f-front');
        const fBack = document.getElementById('f-back');
        const fRight = document.getElementById('f-right');
        const fLeft = document.getElementById('f-left');
        const status = document.getElementById('status');
        const filter = document.getElementById('filter');
        const shuffle = document.getElementById('shuffle');

        const cats = [...new Set(raw.map(i => i.大类).filter(Boolean))].sort();
        cats.forEach(c => { const o = document.createElement('option'); o.value = c; o.textContent = c.split('-').pop(); filter.appendChild(o); });

        function getFront(item) {
            return `<div class="content-front"><div class="sub-name">${item.子类 || item.大类.split('-').pop()}</div><div class="name">${item.name}</div><div class="reveal-hint">Tap Legacy</div></div>`;
        }

        function getBack(item) {
            let c = '';
            if (item.组成 && item.组成.length > 0) {
                c = `<div class="role-group"><div class="role-label">Composition</div><div class="role-content">${item.组成.join('、')}</div></div>`;
            }
            return `<div class="content-back"><div style="font-size:0.7rem; font-weight:800; opacity:0.2; margin-bottom:15px; letter-spacing:0.1em; text-transform:uppercase">${item.name} ARCHIVE</div>${c}<div class="notes">${item.notes}</div></div>`;
        }

        function update() {
            if (list.length === 0) return;
            fFront.innerHTML = getFront(list[idx]); fBack.innerHTML = getBack(list[idx]);
            status.textContent = `${idx + 1} / ${list.length}`;
        }

        function navigate(step) {
            if (busy || list.length < 2) return;
            const nIdx = (idx + step + list.length) % list.length;
            busy = true; flipped = false;
            const side = step > 0 ? fRight : fLeft;
            side.style.opacity = "1"; side.innerHTML = getFront(list[nIdx]);
            rotation -= step * 90; cube.style.transform = `rotateY(${rotation}deg)`;
            setTimeout(() => {
                idx = nIdx; cube.style.transition = "none"; rotation = 0; cube.style.transform = "rotateY(0deg)";
                update(); fRight.style.opacity = "0"; fLeft.style.opacity = "0";
                setTimeout(() => { cube.style.transition = "transform 0.8s cubic-bezier(0.2, 0.8, 0.2, 1)"; busy = false; }, 50);
            }, 800);
        }

        function flip() { if (busy) return; flipped = !flipped; rotation += 180; cube.style.transform = `rotateY(${rotation}deg)`; }

        cube.onclick = flip;
        let sX = 0;
        document.addEventListener('touchstart', e => sX = e.touches[0].clientX);
        document.addEventListener('touchend', e => { const d = e.changedTouches[0].clientX - sX; if (Math.abs(d) > 60) navigate(d > 0 ? -1 : 1); });
        document.addEventListener('keydown', e => {
            if (e.key === 'ArrowLeft') navigate(-1);
            if (e.key === 'ArrowRight') navigate(1);
            if (e.key === ' ' || e.key === 'Enter') flip();
        });

        filter.onchange = e => {
            const v = e.target.value; list = v === 'all' ? [...raw] : raw.filter(i => i.大类 === v);
            idx = 0; rotation = 0; flipped = false; cube.style.transform = "rotateY(0deg)"; update();
        };

        shuffle.onclick = () => {
            list.sort(() => Math.random() - 0.5); idx = 0; rotation = 0; flipped = false; cube.style.transform = "rotateY(0deg)"; update();
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
