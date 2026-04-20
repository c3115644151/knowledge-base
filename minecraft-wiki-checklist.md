# Minecraft Wiki 本地化清单

> **目标**：将中文 Minecraft Wiki (https://zh.minecraft.wiki/) 的核心开发相关内容本地化，转换为适合 AI 查阅的 Markdown 格式，并附带原版材质图片，最终存放在 `reference/minecraft-wiki/` 目录下。

## 目录结构规划
```text
知识库/
└── reference/
    └── minecraft-wiki/
        ├── 机制/            # 附魔、交易、酿造等
        ├── 方块/            # 自然方块、功能方块、红石等
        ├── 物品/            # 武器、工具、消耗品等
        ├── 实体/            # 敌对、中立、友好生物
        ├── 世界生成/        # 群系、结构、维度
        └── assets/          # 存放相关原版材质与图标
```

## 核心条目清单 (Checklist)

由于官方 Wiki 拥有近万个条目，我们将优先提取**对模组开发（NeoForge）最有价值的索引类和核心机制类页面**。

### 1. 基础机制 (Mechanics)
- [x] [附魔](https://zh.minecraft.wiki/w/%E9%99%84%E9%AD%94) (Enchanting) - *已处理*
- [ ] [状态效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C) (Status Effects)
- [ ] [交易](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93) (Trading)
- [ ] [酿造](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0) (Brewing)
- [ ] [伤害类型](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3) (Damage)
- [ ] [红石电路](https://zh.minecraft.wiki/w/%E7%BA%A2%E7%9F%B3%E7%94%B5%E8%B7%AF) (Redstone)

### 2. 世界生成 (World Generation)
- [ ] [生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB) (Biomes)
- [ ] [生成结构](https://zh.minecraft.wiki/w/%E7%94%9F%E6%88%90%E7%BB%93%E6%9E%84) (Structures)
- [ ] [维度](https://zh.minecraft.wiki/w/%E7%BB%B4%E5%BA%A6) (Dimensions - 主世界/下界/末地)

### 3. 方块与物品总览 (Blocks & Items)
*(注：方块和物品的具体条目成百上千，优先抓取总览和分类页面，AI可通过分类页顺藤摸瓜)*
- [ ] [方块总览](https://zh.minecraft.wiki/w/%E6%96%B9%E5%9D%97) (Blocks)
- [ ] [物品总览](https://zh.minecraft.wiki/w/%E7%89%A9%E5%93%81) (Items)
- [ ] [工具](https://zh.minecraft.wiki/w/%E5%B7%A5%E5%85%B7) (Tools)
- [ ] [盔甲](https://zh.minecraft.wiki/w/%E7%9B%94%E7%94%B2) (Armor)
- [ ] [食物](https://zh.minecraft.wiki/w/%E9%A3%9F%E7%89%A9) (Food)

### 4. 实体与生物 (Entities)
- [ ] [生物总览](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9) (Mobs)
- [ ] [实体总览](https://zh.minecraft.wiki/w/%E5%AE%9E%E4%BD%93) (Entities)
- [ ] [怪物分类：敌对/中立/被动](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9#%E5%88%86%E7%B1%BB)

### 5. 模组开发数据向 (Data-Driven)
- [ ] [战利品表](https://zh.minecraft.wiki/w/%E6%88%98%E5%88%A9%E5%93%81%E8%A1%A8) (Loot Tables)
- [ ] [标签](https://zh.minecraft.wiki/w/%E6%A0%87%E7%AD%BE) (Tags)
- [ ] [配方](https://zh.minecraft.wiki/w/%E9%85%8D%E6%96%B9) (Recipes)
- [ ] [进度](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6) (Advancements)

## 执行策略建议
1. **逐类抓取**：使用 `WebFetch` 抓取上述 URL，清洗掉 Wiki 的导航栏、侧边栏等无关 HTML/Markdown，提取纯粹的表格、属性和说明。
2. **材质留存**：提取页面中的核心图标/材质图片链接，将其下载到 `assets/` 目录，并在生成的 MD 文档中使用相对路径引用。
3. **结构对齐**：确保生成的 Markdown 结构与 `neoForge` API 文档的命名和分类习惯一致（如 `Minecraft-实体-生物总览.md`）。