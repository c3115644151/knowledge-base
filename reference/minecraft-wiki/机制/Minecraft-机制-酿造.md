# Minecraft 机制：酿造 (Brewing)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/酿造](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0)（重定向至“药水酿造”）  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

酿造是将“材料 → 药水/喷溅/滞留”的数据驱动链路，和状态效果、战斗、探索高度耦合。模组开发最常用的扩展方式是：新增药水效果、增加酿造配方、让自定义物品参与酿造流程。

### NeoForge 对照文档

- [NeoForge 状态效果与药水](../../neoForge/NeoForge-物品-状态效果.md)
- [NeoForge 物品数据组件](../../neoForge/NeoForge-物品-数据组件.md)

### 1. 注册表与标识符（药水与效果）
酿造链路至少涉及两类注册对象：
- **状态效果 (Mob Effect)**：决定药水最终给实体施加什么效果（见 [Minecraft-机制-状态效果.md](Minecraft-%E6%9C%BA%E5%88%B6-%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C.md)）
- **药水 (Potion)**：决定“饮用/喷溅/滞留”载体中携带的效果列表与持续时间/等级（不同版本实现细节不同，但通常是“Potion → MobEffectInstance 列表”）

### 2. 高权重扩展点：新增酿造配方
常见需求：
- 让“粗制药水 + 自定义材料”生成“自定义效果药水”
- 为现有药水增加“延长/增强/腐化”的分支

实现策略：
- 若平台提供专用注册入口（常见命名类似 `BrewingRecipeRegistry` / `PotionBrewing` 扩展点），优先使用其公开 API 注册配方。
- 若你希望完全数据驱动，通常需要把玩法迁移到“配方系统/数据包”或通过事件拦截实现（酿造在原版里并非完全由普通配方 JSON 描述）。

### 3. 酿造设备与流程（决定你注入点应该放哪里）
酿造台一次处理 1–3 个瓶子，核心输入由两类槽位决定：
- **材料槽**：决定本次反应发生什么
- **燃料槽**：烈焰粉提供能量（Java/基岩在“何时消耗能量”存在差异）

如果你的模组要做“批量自动化酿造/特殊燃料/特殊容器”，需要重点关注：
- 计时（每次酿造固定用时）
- 能量消耗时机（平台差异）
- 中途取出材料的行为

### 4. 与其它系统的联动（高频玩法）
- **状态效果**：药水的全部价值在于施加 MobEffectInstance
- **区域效果云**：滞留药水与区域云在 PVP/PVE 玩法里非常常用
- **战利品与结构**：药水材料与产出常通过战利品投放
- **命令与测试**：配合 `/give` 与 `/effect` 能快速验证你注册的药水/效果是否生效

---

## 原版 Wiki 快速索引 (Quick Reference)

### 酿造流程与设备
- [酿造药水](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E8%8D%AF%E6%B0%B4)（基础流程、喷溅/滞留转换、时间与燃料）
- [酿造设备](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E8%AE%BE%E5%A4%87)（酿造台/炼药锅/烈焰粉/玻璃瓶/水瓶）

### 材料体系（决定“如何设计配方树”）
- [材料](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E6%9D%90%E6%96%99)
- [基础材料与改性剂](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E5%9F%BA%E7%A1%80%E6%9D%90%E6%96%99%E4%B8%8E%E6%94%B9%E6%80%A7%E5%89%82)（下界疣、红石粉、荧石粉、发酵蛛眼、火药、龙息）
- [影响材料](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E5%BD%B1%E5%93%8D%E6%9D%90%E6%96%99)（决定最终效果：迅捷、力量、抗火等）

### 配方树（超长表格）
- [酿造配方](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E9%85%8D%E6%96%B9)
  - [基础药水](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E5%9F%BA%E7%A1%80%E8%8D%AF%E6%B0%B4)
  - [效果药水](https://zh.minecraft.wiki/w/%E8%8D%AF%E6%B0%B4%E9%85%BF%E9%80%A0#%E6%95%88%E6%9E%9C%E8%8D%AF%E6%B0%B4)

---

### Wiki 全目录（H2/H3/H4）

- [酿造药水](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E8%8D%AF%E6%B0%B4)
- [酿造设备](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E8%AE%BE%E5%A4%87)
- [材料](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E6%9D%90%E6%96%99)
  - [基础材料与改性剂](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%9F%BA%E7%A1%80%E6%9D%90%E6%96%99%E4%B8%8E%E6%94%B9%E6%80%A7%E5%89%82)
  - [影响材料](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%BD%B1%E5%93%8D%E6%9D%90%E6%96%99)
  - [元素](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%85%83%E7%B4%A0)
- [酿造配方](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E9%85%BF%E9%80%A0%E9%85%8D%E6%96%B9)
  - [基础药水](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%9F%BA%E7%A1%80%E8%8D%AF%E6%B0%B4)
  - [效果药水](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E6%95%88%E6%9E%9C%E8%8D%AF%E6%B0%B4)
    - [正面效果](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E6%AD%A3%E9%9D%A2%E6%95%88%E6%9E%9C)
    - [负面效果](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E8%B4%9F%E9%9D%A2%E6%95%88%E6%9E%9C)
    - [混合效果](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E6%B7%B7%E5%90%88%E6%95%88%E6%9E%9C)
  - [药物](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E8%8D%AF%E7%89%A9)
  - [不可酿造的药水](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E4%B8%8D%E5%8F%AF%E9%85%BF%E9%80%A0%E7%9A%84%E8%8D%AF%E6%B0%B4)
- [视频](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E8%A7%86%E9%A2%91)
- [历史](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%8E%86%E5%8F%B2)
- [你知道吗](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%97)
- [画廊](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E7%94%BB%E5%BB%8A)
- [参见](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%8F%82%E8%A7%81)
- [参考](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%8F%82%E8%80%83)
- [外部链接](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%A4%96%E9%83%A8%E9%93%BE%E6%8E%A5)
- [导航](https://zh.minecraft.wiki/w/%E9%85%BF%E9%80%A0#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

酿造体系常用原版资源定位：
- 酿造台贴图：`assets/minecraft/textures/block/brewing_stand.png`（及其相关分层贴图，随版本不同）
- 药水瓶贴图：`assets/minecraft/textures/item/` 下的 potion/splash_potion/lingering_potion 相关资源
- 区域效果云粒子：`assets/minecraft/particles/` 与 `assets/minecraft/textures/particle/`
