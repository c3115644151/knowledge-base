# Minecraft Wiki 本地化知识库 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将中文 Minecraft Wiki 的核心“介绍/机制/索引”页面批量本地化为 AI 友好的 Markdown 文档，突出 NeoForge 模组开发高权重内容，并为低权重内容提供精确的 Wiki 锚点索引与原版材质定位。

**Architecture:** 以 [minecraft-wiki-checklist.md](file:///workspace/minecraft-wiki-checklist.md) 为单一事实来源，按类别（机制/世界生成/方块/物品/实体/数据驱动）逐页抓取 → 抽取 TOC 生成锚点索引 → 人工（AI）重写开发要点 → 追加 assets 定位与（可选）下载 → 更新索引文件。

**Tech Stack:** Markdown 文档；抓取与下载使用 `curl`；必要的结构化抽取使用 Python 标准库（`html.parser`, `re`, `json`）；不依赖第三方库。

---

## 文件结构（最终形态）

- 新增/维护：
  - [minecraft-wiki-checklist.md](file:///workspace/minecraft-wiki-checklist.md)
  - `reference/minecraft-wiki/index.md`（本地总索引：按主题分组 + 关键词映射）
  - `reference/minecraft-wiki/<分类>/Minecraft-<分类>-<主题>.md`（每页一文档，采用“Mod开发优先”模板）
  - `reference/minecraft-wiki/assets/<slug>/...`（可选：下载并引用的 wiki 图片/图标）
- 可选更新（建议）：
  - [index.md](file:///workspace/index.md)（全局索引补充 minecraft-wiki 入口）
  - [README.md](file:///workspace/README.md)（文档计数补充）

---

## 共用“页面处理”工作流（每页都用）

### Step A：抓取页面并生成“锚点索引”

- [ ] **A1. 下载页面 HTML（便于提取目录标题）**

```bash
PAGE_URL="https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94"
curl -L "$PAGE_URL" -o /tmp/mcwiki-page.html
```

- [ ] **A2. 用 Python 标准库抽取 TOC（h2/h3）作为锚点索引**

```bash
python - <<'PY'
from html.parser import HTMLParser
import re

class P(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_h2 = False
        self.in_h3 = False
        self.curr_id = None
        self.text = []
        self.items = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h2","h3"):
            self.curr_id = attrs.get("id") or None
            self.text = []
            self.in_h2 = tag == "h2"
            self.in_h3 = tag == "h3"
    def handle_endtag(self, tag):
        if tag in ("h2","h3"):
            t = re.sub(r"\s+", " ", "".join(self.text)).strip()
            if t:
                lvl = 2 if self.in_h2 else 3
                self.items.append((lvl, self.curr_id, t))
            self.in_h2 = self.in_h3 = False
            self.curr_id = None
            self.text = []
    def handle_data(self, data):
        if self.in_h2 or self.in_h3:
            self.text.append(data)

html = open("/tmp/mcwiki-page.html", "r", encoding="utf-8", errors="ignore").read()
p = P()
p.feed(html)
for lvl, hid, title in p.items[:60]:
    print(lvl, hid or "", title)
PY
```

- [ ] **A3. 将抽取到的标题整理成“低优先级索引”段落（精确到锚点）**
  - 输出格式：
    - `- [标题](<PAGE_URL>#<anchor>)`
    - 对“超长表格”章节只保留锚点 + 少量常用行示例。

### Step B：重写“Mod 开发核心要点”

- [ ] **B1. 针对该主题列出 3–6 条“开发者需要立刻知道”的事实**
  - 注册表 / ResourceLocation / TagKey / 数据组件 / 关键 JSON 路径
  - 常用事件入口（仅列事件名与触发时机，不写冗长背景）
  - 与战利品/配方/标签/进度/命令等系统的交互点
  - 版本差异（Java/基岩/1.20 vs 1.21+）只保留会影响实现的差异

- [ ] **B2. 只在“高权重”段落详细写**
  - 低权重内容改为“索引链接 + 关键词提示”，不展开叙述。

### Step C：原版材质与图片

- [ ] **C1. 在文档中列出“资产定位”**
  - 优先列：`assets/minecraft/textures/...` 的原版资源路径（你做模组会直接用到）
  - 其次列：Wiki 页面中出现的代表性图片（图标/方块/物品）

- [ ] **C2（可选）. 下载 Wiki 图片到本地 assets/**
  - 从页面中识别文件名（如 `Enchanted_Book.png`），再用 `Special:FilePath` 下载：

```bash
mkdir -p "reference/minecraft-wiki/assets/<slug>"
curl -L "https://zh.minecraft.wiki/w/Special:FilePath/<FileName>" -o "reference/minecraft-wiki/assets/<slug>/<FileName>"
```

---

## Task 1：基础设施与索引入口

**Files:**
- Modify: [minecraft-wiki-checklist.md](file:///workspace/minecraft-wiki-checklist.md)
- Create: `reference/minecraft-wiki/index.md`
- Modify (optional): [index.md](file:///workspace/index.md)
- Modify (optional): [README.md](file:///workspace/README.md)

- [ ] **Step 1: 确认目录存在**

```bash
mkdir -p /workspace/reference/minecraft-wiki/{机制,方块,物品,实体,世界生成,assets}
```

- [ ] **Step 2: 创建本地总索引 `reference/minecraft-wiki/index.md`**
  - 内容：按 checklist 的分类分组列出本地文档链接 + 关键词映射（对齐 [index.md](file:///workspace/index.md) 的风格）

- [ ] **Step 3（可选）: 更新全局索引与 README**
  - 在 [index.md](file:///workspace/index.md) 增加 `reference/minecraft-wiki/` 区块
  - 在 [README.md](file:///workspace/README.md) 增加文档计数

---

## Task 2：机制类页面（优先级：极高/高/中）

**Files:**
- Modify/Create: `reference/minecraft-wiki/机制/*.md`

- [ ] **Step 1: 完成“状态效果”**
  - Wiki：`https://zh.minecraft.wiki/w/状态效果`
  - 输出：`reference/minecraft-wiki/机制/Minecraft-机制-状态效果.md`
  - 高权重点：`MobEffect` 注册、`MobEffectInstance` 生命周期、tick 应用逻辑、免疫与叠加规则、数据驱动/命令关联索引

- [ ] **Step 2: 完成“伤害类型/伤害”**
  - Wiki：`https://zh.minecraft.wiki/w/伤害`
  - 输出：`reference/minecraft-wiki/机制/Minecraft-机制-伤害.md`
  - 高权重点：`damage_type` 数据驱动、标签、`DamageSource` 判定与常见事件拦截入口

- [ ] **Step 3: 完成“交易”**
  - Wiki：`https://zh.minecraft.wiki/w/交易`
  - 输出：`reference/minecraft-wiki/机制/Minecraft-机制-交易.md`
  - 高权重点：交易注入点、价格/折扣、村民等级与职业、战利品/经济系统关联索引

- [ ] **Step 4: 完成“酿造”**
  - Wiki：`https://zh.minecraft.wiki/w/酿造`
  - 输出：`reference/minecraft-wiki/机制/Minecraft-机制-酿造.md`
  - 高权重点：`Potion`/`MobEffect` 关联、配方注入、数据驱动与物品组件关联索引

- [ ] **Step 5: 完成“红石电路”**
  - Wiki：`https://zh.minecraft.wiki/w/红石电路`
  - 输出：`reference/minecraft-wiki/机制/Minecraft-机制-红石电路.md`
  - 高权重点：信号源、方块更新、计划刻/即时更新差异（低权重用索引）

---

## Task 3：数据驱动页面（战利品表/标签/配方）

**Files:**
- Create: `reference/minecraft-wiki/机制/Minecraft-机制-战利品表.md`
- Create: `reference/minecraft-wiki/机制/Minecraft-机制-标签.md`
- Create: `reference/minecraft-wiki/机制/Minecraft-机制-配方.md`

- [ ] **Step 1: 战利品表**
  - Wiki：`https://zh.minecraft.wiki/w/战利品表`
  - 高权重点：JSON 结构、函数/条件、与结构箱子/实体掉落/方块掉落的映射、NeoForge 全局修改器索引

- [ ] **Step 2: 标签**
  - Wiki：`https://zh.minecraft.wiki/w/标签`
  - 高权重点：TagKey 语义、数据包合并/替换、常用标签分类、代码查询入口

- [ ] **Step 3: 配方**
  - Wiki：`https://zh.minecraft.wiki/w/配方`
  - 高权重点：配方 JSON 结构、序列化关键点、配方类型扩展、数据包覆盖规则

---

## Task 4：世界生成（群系/结构/维度）

**Files:**
- Create: `reference/minecraft-wiki/世界生成/*.md`

- [ ] **Step 1: 生物群系**
  - Wiki：`https://zh.minecraft.wiki/w/生物群系`
  - 高权重点：数据包入口、标签与特征、NeoForge Biome Modifiers 对应关系（低权重索引）

- [ ] **Step 2: 生成结构**
  - Wiki：`https://zh.minecraft.wiki/w/生成结构`
  - 高权重点：结构类型与数据文件入口；Jigsaw / template_pool 作为索引重点

- [ ] **Step 3: 维度**
  - Wiki：`https://zh.minecraft.wiki/w/维度`
  - 输出可做“低优先级”：主要提供锚点索引 + 关键数据文件名（dimension/dimension_type）

---

## Task 5：方块/物品/实体总览（索引型为主，但要补“开发关键点”）

**Files:**
- Create: `reference/minecraft-wiki/方块/Minecraft-方块-方块总览.md`
- Create: `reference/minecraft-wiki/物品/Minecraft-物品-物品总览.md`
- Create: `reference/minecraft-wiki/物品/Minecraft-物品-工具.md`
- Create: `reference/minecraft-wiki/物品/Minecraft-物品-食物.md`
- Create: `reference/minecraft-wiki/实体/Minecraft-实体-实体总览.md`
- Create: `reference/minecraft-wiki/实体/Minecraft-实体-生物总览.md`

- [ ] **Step 1: 方块总览（极高）**
  - 高权重点：`BlockState`/属性/形状/方块实体关联/客户端渲染差异（其余分类列表只做锚点索引）

- [ ] **Step 2: 物品总览（极高）**
  - 高权重点：1.21 数据组件体系总览、交互入口、耐久/堆叠/工具提示（分类列表锚点索引）

- [ ] **Step 3: 工具（高）**
  - 高权重点：Tier、挖掘等级/速度、标签、战斗属性（具体工具表格仅索引）

- [ ] **Step 4: 食物（高）**
  - 高权重点：`FoodProperties`、状态效果附加、可食用条件与动画（具体食物列表仅索引）

- [ ] **Step 5: 实体/生物总览（极高/高）**
  - 高权重点：注册、属性、AI Goal、同步数据与渲染器；生物分类表仅索引

---

## Task 6：验收与一致性检查

**Files:**
- Modify: `reference/minecraft-wiki/index.md`
- Modify: [minecraft-wiki-checklist.md](file:///workspace/minecraft-wiki-checklist.md)

- [ ] **Step 1: 每篇文档必须包含**
  - Wiki 源地址
  - 模组开发核心要点（详细）
  - 原版 Wiki 快速索引（锚点）
  - Assets（原版资源路径 + 可选下载的 wiki 图片）

- [ ] **Step 2: 清单勾选与本地索引同步**
  - checklist 对应条目标记为完成
  - `reference/minecraft-wiki/index.md` 的链接指向正确文件

- [ ] **Step 3: 运行简单一致性检查（可选）**

```bash
python - <<'PY'
from pathlib import Path
root = Path("/workspace/reference/minecraft-wiki")
mds = list(root.rglob("*.md"))
missing = []
for p in mds:
    t = p.read_text(encoding="utf-8", errors="ignore")
    for needle in ("Wiki 源地址", "模组开发核心要点", "原版 Wiki 快速索引", "相关资源与材质"):
        if needle not in t:
            missing.append((str(p), needle))
if missing:
    print("MISSING:")
    for p, n in missing:
        print("-", p, "=>", n)
    raise SystemExit(1)
print("OK", len(mds))
PY
```

