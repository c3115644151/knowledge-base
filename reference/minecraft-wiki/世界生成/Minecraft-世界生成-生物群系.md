# Minecraft 世界生成：生物群系 (Biome)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

在 NeoForge 1.21+ 中，生物群系 (Biome) 的定义与生成完全**数据驱动化 (Data-Driven)**。开发者不应在代码中硬编码生物群系特征，而应使用数据包 (Datapack) 的 JSON 文件和 NeoForge 的修饰器 (Modifiers)。

### NeoForge 对照文档

- [NeoForge 生物群系修改器](../../neoForge/NeoForge-世界生成-生物群系修改器.md)
- [NeoForge 世界生成 - 地物（Features）](../../neoForge/NeoForge-世界生成-地物.md)

### 1. 注册表与标识符
- **注册表名称**：`minecraft:biome` (在代码中通过 `Registries.BIOME` 访问)
- **命名空间**：原版生物群系如 `minecraft:plains`，模组自定义如 `mymod:custom_biome`。
- **数据路径**：`data/<namespace>/worldgen/biome/`

### 2. 数据驱动的生物群系定义 (JSON 结构)
自定义生物群系由 JSON 文件定义，核心字段包括：
- `has_precipitation`: 布尔值，是否允许降水。
- `temperature`: 浮点数，控制气候（如冻结水面）与树叶颜色。
- `downfall`: 浮点数，降水概率或湿度。
- `effects`: **视觉核心**。定义环境颜色与音效。
  - 必须字段：`sky_color`, `fog_color`, `water_color`, `water_fog_color`。
  - 可选字段：`foliage_color` (树叶), `grass_color` (草地), `grass_color_modifier` (如 `dark_forest` 或 `swamp` 的特殊过滤), 音效 (`ambient_sound`, `mood_sound` 等)。
- `spawners`: 控制各类别生物 (如 `monster`, `creature`, `water_creature`) 的生成权重、最小/最大群组数量。
- `carvers`: 地形雕刻器 (如洞穴、峡谷)。
- `features`: 一个按生成阶段 (Generation Step) 排序的数组，包含植物、矿石、结构等地物的引用 (指向 `worldgen/placed_feature`)。

### 3. NeoForge 生物群系修饰器 (Biome Modifiers)
**绝对不要通过直接覆盖原版 JSON 来修改现有生物群系！**
NeoForge 提供了 `BiomeModifier` 系统，通过数据包非破坏性地向现有生物群系添加或移除内容。
- **数据路径**：`data/<namespace>/neoforge/biome_modifier/`
- **常见类型 (Type)**：
  - `neoforge:add_features`: 向匹配的生物群系添加地物 (如自定义矿石)。
  - `neoforge:remove_features`: 移除地物。
  - `neoforge:add_spawns`: 添加生物生成。
  - `neoforge:remove_spawns`: 移除生物生成。
- **目标选择 (Biomes)**：通常使用**生物群系标签 (Biome Tag)** (如 `#minecraft:is_overworld`, `#minecraft:is_forest`) 进行精准匹配。

### 4. 开发避坑指南
- **地表规则 (Surface Rules)**：生物群系 JSON **不再**控制地表方块（如草方块还是沙子）。地表材质由 `worldgen/noise_settings` 中的 `surface_rule` 决定。若要为自定义生物群系设定特殊地表，需利用 NeoForge 的 `SurfaceRuleManager` 或替换维度噪声设置。
- **多重噪声生成 (Multi-Noise)**：主世界和下界的生物群系分布由 6 个气候参数决定：`temperature` (温度), `humidity` (湿度), `continentalness` (大陆性), `erosion` (侵蚀度), `depth` (深度), `weirdness` (怪异度)。必须在 `dimension` 配置文件中分配这些参数，生物群系才会自然生成。

---

## 原版 Wiki 快速索引 (Quick Reference)

### 1. 生物群系种类与特征
- [主世界生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%BB%E4%B8%96%E7%95%8C) *(海洋类、山地类、森林类、平原类、湿地类、干旱类、洞穴类)*
- [下界生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%8B%E7%95%8C) *(绯红森林、诡异森林、灵魂沙峡谷、玄武岩三角洲、下界荒地)*
- [末地生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%9C%AB%E5%9C%B0) *(末地、末地小型岛屿、末地中型岛屿、末地高岛、末地荒地)*

### 2. 气候与环境机制
- [温度系统](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B8%A9%E5%BA%A6) *(影响降雪、冰冻、雪人生成等)*
- [降水与积雪](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E9%99%8D%E6%B0%B4) *(雨、雪的视觉效果与逻辑影响)*
- [气候列表与数值](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B0%94%E5%80%99%E5%88%97%E8%A1%A8) *(各原版群系的温度和降水基础值)*

### 3. 视觉与着色 (Coloration)
- [植物颜色系统](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%A4%8D%E7%89%A9%E9%A2%9C%E8%89%B2) *(草方块与树叶如何根据群系变色)*
- [特殊植物颜色](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%89%B9%E6%AE%8A%E6%A4%8D%E7%89%A9%E9%A2%9C%E8%89%B2) *(如沼泽、黑森林的硬编码或修饰器着色)*
- [环境颜色与过渡](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%8E%AF%E5%A2%83%E9%A2%9C%E8%89%B2) *(天空、水、水下雾气的颜色平滑过渡逻辑)*

### 4. 数据与指令相关
- [数据包：生物群系定义格式](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB%E5%AE%9A%E4%B9%89%E6%A0%BC%E5%BC%8F) *(原版完整的 JSON 结构字段级参考)*
- 命令使用：`/locate biome <biome>` 定位生物群系，`/fillbiome` 更改指定区域的生物群系。

---

### Wiki 全目录（H2/H3/H4）

- [种类](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%A7%8D%E7%B1%BB)
  - [主世界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%BB%E4%B8%96%E7%95%8C)
    - [海洋类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B5%B7%E6%B4%8B%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [山地类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%B1%B1%E5%9C%B0%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [森林类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%A3%AE%E6%9E%97%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [湿地类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B9%BF%E5%9C%B0%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [平原类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%B9%B3%E5%8E%9F%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [干旱类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%B9%B2%E6%97%B1%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
    - [洞穴类生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B4%9E%E7%A9%B4%E7%B1%BB%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
  - [下界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%8B%E7%95%8C)
  - [末地](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%9C%AB%E5%9C%B0)
  - [特殊生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%89%B9%E6%AE%8A%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
  - [已移除的生物群系](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%B7%B2%E7%A7%BB%E9%99%A4%E7%9A%84%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB)
- [生成](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%94%9F%E6%88%90)
  - [主世界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%BB%E4%B8%96%E7%95%8C_2)
  - [下界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%8B%E7%95%8C_2)
  - [末地](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%9C%AB%E5%9C%B0_2)
- [气候](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B0%94%E5%80%99)
  - [温度](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B8%A9%E5%BA%A6)
  - [降水](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E9%99%8D%E6%B0%B4)
  - [降水类型](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E9%99%8D%E6%B0%B4%E7%B1%BB%E5%9E%8B)
  - [积雪高度](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%A7%AF%E9%9B%AA%E9%AB%98%E5%BA%A6)
  - [气候列表](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%B0%94%E5%80%99%E5%88%97%E8%A1%A8)
    - [主世界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%BB%E4%B8%96%E7%95%8C_3)
    - [下界](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%B8%8B%E7%95%8C_3)
    - [末地](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%9C%AB%E5%9C%B0_3)
- [着色](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%9D%80%E8%89%B2)
  - [植物颜色](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%A4%8D%E7%89%A9%E9%A2%9C%E8%89%B2)
    - [特殊植物颜色](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%89%B9%E6%AE%8A%E6%A4%8D%E7%89%A9%E9%A2%9C%E8%89%B2)
  - [环境颜色](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%8E%AF%E5%A2%83%E9%A2%9C%E8%89%B2)
  - [颜色过渡](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E9%A2%9C%E8%89%B2%E8%BF%87%E6%B8%A1)
- [数据值](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%95%B0%E6%8D%AE%E5%80%BC)
- [成就](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%88%90%E5%B0%B1)
- [进度](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E8%BF%9B%E5%BA%A6)
- [历史](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%8E%86%E5%8F%B2)
- [你知道吗](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%97)
- [画廊](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E7%94%BB%E5%BB%8A)
  - [日出和日落](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%97%A5%E5%87%BA%E5%92%8C%E6%97%A5%E8%90%BD)
  - [早期开发](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E6%97%A9%E6%9C%9F%E5%BC%80%E5%8F%91)
- [参考](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%8F%82%E8%80%83)
- [参见](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%8F%82%E8%A7%81)
- [导航](https://zh.minecraft.wiki/w/%E7%94%9F%E7%89%A9%E7%BE%A4%E7%B3%BB#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

生物群系的色彩很多时候由基础色谱图和 JSON 共同决定：
- **草地色谱**：`assets/minecraft/textures/colormap/grass.png`
- **树叶色谱**：`assets/minecraft/textures/colormap/foliage.png`
- *(注：JSON 中指定的 `grass_color` 会覆盖色谱图的计算结果)*
