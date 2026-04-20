# Minecraft 机制：状态效果 (Status Effect / Mob Effect)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/状态效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

状态效果是模组中最常见的“持续性机制载体”之一：既可以用来做玩家/生物的能力增益，也常用于触发粒子、属性修正、AI 行为变化与战斗系统联动。

### 1. 注册表与标识符
- **注册表名称**：`minecraft:mob_effect`（代码侧通常通过 `Registries.MOB_EFFECT` 访问）
- **标识符形式**：`minecraft:<effect_name>`（例如 `minecraft:speed`）
- **语言键**：通常为 `effect.minecraft.<effect_name>`（用于多语言显示）

### 2. 运行时表示：MobEffect 与 MobEffectInstance
- **MobEffect**：效果的“类型定义”（是否有粒子/图标、颜色、分类、属性修正等）。
- **MobEffectInstance**：效果的“实例”（持续时间、等级 amplifier、是否显示粒子、是否显示图标等）。
  - Wiki 提到的“等级”在内部通常用 `amplifier` 表示：等级 = amplifier + 1。

### 3. 叠加、覆盖与清除规则（影响你写逻辑的地方）
- 同一种效果不能叠加为多个实例：新效果会覆盖旧效果。
- 覆盖规则与版本有关（Java/基岩差异），如果你要实现“更强效果覆盖但保留弱效果在后续恢复”的玩法，需要明确按目标平台实现。
- 清除途径常见有：奶、死亡重生、不死图腾、命令 `/effect clear`。

### 4. Tick 行为与事件入口
你常见的实现需求通常落在两类：
- **效果自身每 tick 产生影响**：例如持续伤害、持续回复、持续修改移动等。优先放进自定义 `MobEffect` 的 tick 逻辑（原版也这么做）。
- **效果作为“状态标记”参与其它系统**：例如当实体有某效果时修改伤害、掉落、交互等。优先在事件中做条件判断。

常用事件入口（以 NeoForge/Forge 体系为参照，实际事件名以你的环境为准）：
- `LivingHurtEvent` / `LivingDamageEvent`：根据效果改变伤害计算结果（例如抗性、脆弱、流血等）
- `LivingHealEvent`：根据效果改变治疗
- `LivingDeathEvent`：根据效果触发额外掉落/复活逻辑
- `PlayerTickEvent` / `LivingTickEvent`：用于“持续检测”的玩法（尽量避免高频重计算）

### 5. 与数据驱动系统的联动点
状态效果经常与以下系统形成闭环（优先在文档/数据包层定义，必要时再用代码补充）：
- **药水/酿造**：通过药水效果把 `MobEffectInstance` 施加到实体
- **食物**：食物可附带效果实例（例如金苹果类）
- **信标/潮涌核心/区域效果云**：批量施加效果实例
- **命令 `/effect`**：调试与测试非常重要

---

## 原版 Wiki 快速索引 (Quick Reference)

低优先级内容不在本地展开，直接给出可精确跳转的 Wiki 章节锚点。

### 监测与显示
- [监测](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E7%9B%91%E6%B5%8B)（HUD/图标显示、闪烁规则、Java/基岩差异）

### 机制与规则
- [机制](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E6%9C%BA%E5%88%B6)（获取途径、覆盖规则、粒子表现）
- [效果等级](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E6%95%88%E6%9E%9C%E7%AD%89%E7%BA%A7)（amplifier 与等级换算、负数处理差异）
- [效果持续时间](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E6%95%88%E6%9E%9C%E6%8C%81%E7%BB%AD%E6%97%B6%E9%97%B4)
- [免疫状态效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E5%85%8D%E7%96%AB%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C)（哪些生物免疫哪些效果）
- [即时生效效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E5%8D%B3%E6%97%B6%E7%94%9F%E6%95%88%E6%95%88%E6%9E%9C)（瞬间治疗/瞬间伤害/饱和）
- [状态效果分类](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C%E5%88%86%E7%B1%BB)（正面/中性/负面）
- [解除效果](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E8%A7%A3%E9%99%A4%E6%95%88%E6%9E%9C)

### 数据字典（超长表格）
- [状态效果列表](https://zh.minecraft.wiki/w/%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C#%E7%8A%B6%E6%80%81%E6%95%88%E6%9E%9C%E5%88%97%E8%A1%A8)
  - 速查：该表提供 `ID`（字符串）与分类/颜色信息；开发侧通常将 `ID` 作为 ResourceLocation 的 path 部分（例如 `speed` → `minecraft:speed`）。

---

## 相关资源与材质 (Assets)

状态效果主要会涉及 GUI 图标与粒子表现。原版资源定位通常包含：
- 物品栏/状态效果图标相关：`assets/minecraft/textures/mob_effect/`（不同版本/资源包可能组织略有差异）
- 药水瓶/喷溅/滞留视觉：`assets/minecraft/textures/item/` 下的药水相关贴图

