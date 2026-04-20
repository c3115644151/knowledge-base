# Minecraft 机制：伤害 (Damage)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

伤害系统是战斗、环境交互、生物 AI、状态效果、战利品的“汇流点”。在 1.20+ 之后，**伤害类型 (Damage Type)** 已数据驱动化，模组开发常见需求（新增伤害类别、绕过护甲、改变死亡信息/来源判定）都应围绕 `damage_type` 注册表与标签体系展开。

### NeoForge 对照文档

- [NeoForge 伤害类型系统](../../neoForge/NeoForge-服务端-伤害类型.md)
- [NeoForge LivingEntity 与生物逻辑](../../neoForge/NeoForge-实体-LivingEntity.md)

### 1. 注册表与数据文件位置
- **注册表名称**：`minecraft:damage_type`
- **数据文件路径**：`data/<namespace>/damage_type/<name>.json`
- **标签路径**：`data/<namespace>/tags/damage_type/<tag>.json`

这些数据决定了：
- 某伤害是否受游戏难度影响（Wiki 的“难度影响”章节）
- 某伤害是否绕过无敌帧/护甲/保护类魔咒/抗性提升等（通过 damage_type 标签描述）
- 死亡消息、击退、着火等附带表现（随版本而变，具体以原版数据字段为准）

### 2. DamageType 与 DamageSource 的关系（实现层面）
- **DamageType**：描述“这是什么伤害”（类别、规则、标签）。
- **DamageSource**：一次具体伤害事件的载体，通常包含：
  - DamageType（通过 `Holder<DamageType>` 或 key 引用）
  - 造成者实体（attacker）
  - 直接伤害实体（direct，例如箭矢/火球）

模组中经常需要回答两个问题：
- “这个伤害是不是某类伤害？”（通过 DamageType/TagKey 判断）
- “这个伤害是谁造成的？”（用于战利品归属、仇恨、统计）

### 3. 高权重扩展点：事件与拦截
常见改造目标与对应入口：
- **改伤害数值**：`LivingHurtEvent`（更早的数值层）、`LivingDamageEvent`（更接近最终结算）
- **取消伤害**：同上事件中根据条件 `cancel`（例如护盾类玩法）
- **自定义死亡处理**：`LivingDeathEvent`（复活、替换掉落、替换死亡原因显示）
- **击退/击退抗性**：常见在伤害事件后或专门的 knockback 事件（不同平台命名不同）

建议的实现策略：
- 优先用数据驱动 DamageType + tag 表达“规则”（是否绕过冷却/护甲等）
- 仅把“复杂逻辑”放进事件（例如基于装备、技能树、连击层数的动态伤害）

### 4. 需要重点关注的原版规则（会影响你写的玩法）
- **受击后伤害免疫（无敌帧）**：影响持续伤害/光环伤害的频率；部分 DamageType 可绕过（Wiki 提到 `minecraft:bypasses_cooldown` 标签）。
- **伤害减免路径**：
  - 护甲值/韧性
  - 保护类魔咒（保护/火焰保护/爆炸保护/弹射物保护/摔落缓冲）
  - 抗性提升
  - 生物自身伤害修正（例如女巫魔法减免）
  - 某些伤害直接绕过上述路径（如虚空、饥饿、/kill 等）

### 5. 与其它系统的联动（模组高频需求）
- **战利品表**：伤害来源影响掉落归属与条件判断（例如“被玩家击杀”“被爆炸击杀”）
- **状态效果**：部分状态效果直接以“魔法伤害”等分类造成伤害（如中毒/凋零等）
- **命令**：`/damage` 用于调试各种 DamageType 的表现（与数据驱动字段是否生效强相关）

---

## 极简代码示例 (Minimal Code Examples)

**1. 注册伤害类型 (JSON: `data/<modid>/damage_type/custom_damage.json`)**
```json
{
  "message_id": "yourmodid.custom_damage",
  "exhaustion": 0.1,
  "scaling": "always"
}
```

**2. 触发与拦截伤害 (Java)**
```java
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceKey;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.world.damagesource.DamageSource;
import net.minecraft.world.entity.Entity;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.entity.living.LivingDamageEvent;

// 造成自定义伤害
public static void dealCustomDamage(Entity target) {
    var registry = target.level().registryAccess().registryOrThrow(Registries.DAMAGE_TYPE);
    var key = ResourceKey.create(Registries.DAMAGE_TYPE, ResourceLocation.fromNamespaceAndPath("yourmodid", "custom_damage"));
    target.hurt(new DamageSource(registry.getHolderOrThrow(key)), 5.0f);
}

// 拦截并修改伤害 (NeoForge 总线)
@SubscribeEvent
public static void onLivingDamage(LivingDamageEvent.Pre event) {
    if (event.getSource().is(net.minecraft.tags.DamageTypeTags.IS_FIRE)) {
        event.setNewDamage(event.getNewDamage() * 0.5f); // 火焰伤害减半
    }
}
```

## 原版 Wiki 快速索引 (Quick Reference)

### 机制与总体规则
- [机制](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%9C%BA%E5%88%B6)
- [受击后伤害免疫](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB)
- [击退](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%87%BB%E9%80%80)
- [造成伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3)

### 伤害来源、类型与分类（开发最常回查的三块）
- [伤害来源](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E6%9D%A5%E6%BA%90)（包含生物/物品等来源拆解）
- [伤害类型](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E7%B1%BB%E5%9E%8B)（对应数据驱动 DamageType 概念）
- [伤害分类](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E5%88%86%E7%B1%BB)
  - [魔法伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%AD%94%E6%B3%95%E4%BC%A4%E5%AE%B3)
  - [火焰伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E7%81%AB%E7%84%B0%E4%BC%A4%E5%AE%B3)
  - [弹射物伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%BC%B9%E5%B0%84%E7%89%A9%E4%BC%A4%E5%AE%B3)
  - [爆炸伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E7%88%86%E7%82%B8%E4%BC%A4%E5%AE%B3)
  - [摔落伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%91%94%E8%90%BD%E4%BC%A4%E5%AE%B3)

### 其它关键段落（按需回查）
- [无懈可击（免疫/无敌）](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%97%A0%E6%87%88%E5%8F%AF%E5%87%BB)
- [伤害值调整](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E5%80%BC%E8%B0%83%E6%95%B4)
- [难度影响](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%9A%BE%E5%BA%A6%E5%BD%B1%E5%93%8D)
- [非生物实体](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%9D%9E%E7%94%9F%E7%89%A9%E5%AE%9E%E4%BD%93)

---

### Wiki 全目录（H2/H3/H4）

- [机制](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%9C%BA%E5%88%B6)
  - [无懈可击](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%97%A0%E6%87%88%E5%8F%AF%E5%87%BB)
  - [伤害值调整](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E5%80%BC%E8%B0%83%E6%95%B4)
  - [难度影响](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%9A%BE%E5%BA%A6%E5%BD%B1%E5%93%8D)
  - [非生物实体](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%9D%9E%E7%94%9F%E7%89%A9%E5%AE%9E%E4%BD%93)
- [受击后伤害免疫](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%8F%97%E5%87%BB%E5%90%8E%E4%BC%A4%E5%AE%B3%E5%85%8D%E7%96%AB)
- [击退](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%87%BB%E9%80%80)
  - [击退抗性](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%87%BB%E9%80%80%E6%8A%97%E6%80%A7)
- [造成伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3)
- [伤害来源](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E6%9D%A5%E6%BA%90)
  - [造成伤害的生物](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3%E7%9A%84%E7%94%9F%E7%89%A9)
  - [造成伤害的物品](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%80%A0%E6%88%90%E4%BC%A4%E5%AE%B3%E7%9A%84%E7%89%A9%E5%93%81)
- [伤害类型](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E7%B1%BB%E5%9E%8B)
- [伤害分类](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BC%A4%E5%AE%B3%E5%88%86%E7%B1%BB)
  - [魔法伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E9%AD%94%E6%B3%95%E4%BC%A4%E5%AE%B3)
  - [火焰伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E7%81%AB%E7%84%B0%E4%BC%A4%E5%AE%B3)
  - [弹射物伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%BC%B9%E5%B0%84%E7%89%A9%E4%BC%A4%E5%AE%B3)
  - [爆炸伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E7%88%86%E7%82%B8%E4%BC%A4%E5%AE%B3)
  - [摔落伤害](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%91%94%E8%90%BD%E4%BC%A4%E5%AE%B3)
- [成就](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E6%88%90%E5%B0%B1)
- [进度](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E8%BF%9B%E5%BA%A6)
- [历史](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%8E%86%E5%8F%B2)
- [你知道吗](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%97)
- [参考](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E4%BC%A4%E5%AE%B3#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

伤害系统本身没有固定“贴图”，但它经常与以下资产相关：
- 火焰/熔岩/爆炸等粒子：`assets/minecraft/particles/` 与 `assets/minecraft/textures/particle/`
- 受伤与状态图标（例如受伤动画、状态效果图标）：更多见于客户端渲染与 GUI 资源
