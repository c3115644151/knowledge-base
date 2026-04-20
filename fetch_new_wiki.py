import subprocess
import re
import html
import urllib.parse
import os

PAGES = [
    ("客户端与资源", "Minecraft-客户端-粒子.md", "粒子", "https://zh.minecraft.wiki/w/Java%E7%89%88%E7%B2%92%E5%AD%90"),
    ("客户端与资源", "Minecraft-客户端-声音.md", "声音", "https://zh.minecraft.wiki/w/%E5%A3%B0%E9%9F%B3"),
    ("客户端与资源", "Minecraft-客户端-模型.md", "模型", "https://zh.minecraft.wiki/w/%E6%A8%A1%E5%9E%8B"),
    ("高级机制与数据", "Minecraft-数据-进度.md", "进度", "https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6"),
    ("高级机制与数据", "Minecraft-数据-属性.md", "属性", "https://zh.minecraft.wiki/w/%E5%B1%9E%E6%80%A7"),
    ("高级机制与数据", "Minecraft-机制-命令.md", "命令", "https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4"),
    ("方块实体与流体", "Minecraft-方块-方块实体.md", "方块实体", "https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97%E5%AE%9E%E4%BD%93"),
    ("方块实体与流体", "Minecraft-方块-流体.md", "流体", "https://zh.minecraft.wiki/w/%E6%B5%81%E4%BD%93")
]

def fetch_anchors(url):
    try:
        result = subprocess.run(
            ['curl', '-s', '-A', 'Mozilla/5.0', url],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        html_content = result.stdout
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return []
    
    out = []
    # Match <h2 id="Something"><span id="..."></span>Title</h2>
    # The title text might be after the span, or inside, or mixed.
    # Let's extract the whole <hX id="id">...</hX> content
    pat = re.compile(r'<h([2-4])[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
    for m in pat.finditer(html_content):
        lvl = int(m.group(1))
        hid = m.group(2)
        inner_html = m.group(3)
        
        # Remove inner tags from title (e.g. <span>...</span>)
        title = re.sub(r'<[^>]+>', '', inner_html)
        title = html.unescape(re.sub(r'\s+', ' ', title)).strip()
        
        if not title or title in ('目录', '导航菜单'):
            continue
        out.append((lvl, hid, title))
    return out

for folder, filename, title, url in PAGES:
    print(f"Processing {title}...")
    anchors = fetch_anchors(url)
    
    filepath = f"/workspace/reference/minecraft-wiki/{folder}/{filename}"
    
    lines = [
        f"# Minecraft：{title} ({title})",
        "",
        f"> **Wiki 源地址**：[{url}]({url})",
        "> **适用版本**：Java 版 1.21+ / NeoForge 26.1+",
        "> **本地更新时间**：2026-04-20",
        "",
        "---",
        "",
        "## 模组开发核心要点 (Modding Priorities)",
        "",
        "<!-- 代理需要在此处填写 NeoForge 1.21+ 开发相关的核心知识点 -->",
        "",
        "---",
        "",
        "## 极简代码示例 (Minimal Code Examples)",
        "",
        "<!-- 代理需要在此处填写适用于 NeoForge 1.21+ 的极简代码或 JSON 示例 -->",
        "",
        "---",
        "",
        "## 原版 Wiki 快速索引 (Quick Reference)",
        "",
        "对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。",
        "",
        "### Wiki 全目录（H2/H3/H4）",
        ""
    ]
    
    for lvl, hid, txt in anchors:
        indent = "  " * (lvl - 2)
        link = f"{url}#{hid}"
        lines.append(f"{indent}- [{txt}]({link})")
        
    lines.append("")
    lines.append("## 相关资源与材质 (Assets)")
    lines.append("")
    lines.append("*(待补充该机制相关的原版资源路径)*")
    lines.append("")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("\n".join(lines))
        
print("All base files created successfully.")
