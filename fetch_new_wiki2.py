import subprocess
import re
import html

PAGES = [
    ("额外核心组件", "Minecraft-额外-盔甲.md", "盔甲", "https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2"),
    ("额外核心组件", "Minecraft-额外-弹射物.md", "弹射物", "https://zh.minecraft.wiki/w/%E5%BC%B9%E5%B0%84%E7%89%A9"),
    ("额外核心组件", "Minecraft-额外-矿车.md", "矿车", "https://zh.minecraft.wiki/w/%E7%9F%BF%E8%BD%A6"),
    ("额外核心组件", "Minecraft-额外-船.md", "船", "https://zh.minecraft.wiki/w/%E8%88%B9"),
    ("额外核心组件", "Minecraft-额外-创造模式物品栏.md", "创造模式物品栏", "https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F"),
    ("额外核心组件", "Minecraft-额外-统计信息.md", "统计信息", "https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF"),
    ("额外核心组件", "Minecraft-额外-记分板.md", "记分板", "https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF")
]

def fetch_anchors(url):
    try:
        # Some URLs redirect. curl -L handles it.
        result = subprocess.run(
            ['curl', '-L', '-s', '-A', 'Mozilla/5.0', url],
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
    pat = re.compile(r'<h([2-4])[^>]*id="([^"]+)"[^>]*>(.*?)</h\1>', re.S)
    for m in pat.finditer(html_content):
        lvl = int(m.group(1))
        hid = m.group(2)
        inner_html = m.group(3)
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
        f"# Minecraft 机制：{title} ({title})",
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
        
print("All additional files created successfully.")
