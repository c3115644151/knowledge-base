# Minecraft 机制：交易 (Trading)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/交易](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93)  
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+  
> **本地更新时间**：2026-04-20  

---

## 模组开发核心要点 (Modding Priorities)

交易系统通常用于“经济/获取途径/进度门槛”的设计：你可以用村民交易投放模组材料、图纸、附魔书、任务道具等，并通过声望、需求、补货等机制实现稳定的可控产出。

### 1. 交易对象与关键概念
- 交易主要发生在：
  - **村民 (Villager)**：职业 + 等级 + 工作站点方块决定交易池与解锁路线
  - **流浪商人 (Wandering Trader)**：固定/随机池，偏“旅行商店”定位
- 每个交易项本质是一个 **MerchantOffer**（输入 A/B → 输出 C，带次数限制、经验、价格乘数等参数）。

### 2. 高权重扩展点：注入交易与改价格
常见需求：
- 给某职业某等级添加/替换交易项
- 为流浪商人添加交易项
- 根据玩家状态（声望、成就、任务阶段）动态改价格或改库存

实现策略（以 NeoForge/Forge 常见模式为参照，具体事件名以你的环境为准）：
- **静态注入**：监听交易相关事件（常见为 `VillagerTradesEvent` / `WandererTradesEvent`），向对应职业/等级的交易列表追加 `MerchantOffer`。
- **动态价格**：
  - 若只是复用原版“声望/英雄/需求”机制，优先使用原版参数（价格乘数、需求机制）。
  - 若需要更复杂折扣（比如技能树/阵营声望），通常需要在交易生成时或交易打开时进行二次修正（不同平台事件入口不同，建议将逻辑封装为“根据玩家与交易项计算价格”的函数）。

### 3. 需要重点掌握的原版规则（决定平衡性）
- **声望/言论（Java 侧）**：会影响最终价格，并且是“每个村民对每个玩家独立”的。
- **供需关系**：同一交易频繁被使用会涨价，长时间不用会回落。
- **交易次数上限与补货**：交易会被锁定（出现红色 ×），村民在工作站点补货后恢复；这直接决定了可刷取效率。
- **村民等级与经验**：交易推动村民升级解锁更高等级交易；模组若投放“高阶产物”，通常绑定在更高等级以形成进度门槛。

### 4. 与数据驱动系统的联动
交易产出常与以下系统关联（建议只在“高权重”部分描述你要支持的设计，其余用索引回查）：
- **附魔与附魔书**：图书管理员交易是附魔投放核心路径
- **结构探索**：藏宝图等交易可引导玩家去结构
- **战利品表与掉落**：交易与掉落常互为备选获取途径

---

## 极简代码示例 (Minimal Code Examples)

```java
import net.minecraft.world.entity.npc.VillagerProfession;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.common.BasicItemListing;
import net.neoforged.neoforge.event.village.VillagerTradesEvent;

// 监听 NeoForge 总线事件
@SubscribeEvent
public static void onVillagerTrades(VillagerTradesEvent event) {
    if (event.getType() == VillagerProfession.CLERIC) {
        // 在牧师等级 1 时添加交易：1 个绿宝石换 2 个红石
        event.getTrades().get(1).add(new BasicItemListing(
            new ItemStack(Items.EMERALD, 1), // 输入
            new ItemStack(Items.REDSTONE, 2), // 输出
            16, // 最大交易次数
            2,  // 给予村民的经验值
            0.05f // 价格乘数
        ));
    }
}
```

## 原版 Wiki 快速索引 (Quick Reference)

### 机制与规则
- [机制](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9C%BA%E5%88%B6)
- [言论与声望（Java）](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E8%A8%80%E8%AE%BA%E4%B8%8E%E5%A3%B0%E6%9C%9B)
- [供需关系](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BE%9B%E9%9C%80%E5%85%B3%E7%B3%BB)
- [村庄英雄](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9D%91%E5%BA%84%E8%8B%B1%E9%9B%84)
- [新增交易项与补货](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%96%B0%E5%A2%9E%E4%BA%A4%E6%98%93%E9%A1%B9%E4%B8%8E%E8%A1%A5%E8%B4%A7)
- [交易（展示手持物品等细节）](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BA%A4%E6%98%93)

### 职业与具体交易池（超长表格）
- [村民职业与交易选项](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9D%91%E6%B0%91%E8%81%8C%E4%B8%9A%E4%B8%8E%E4%BA%A4%E6%98%93%E9%80%89%E9%A1%B9)
  - 典型高频职业锚点：
    - [图书管理员](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%9B%BE%E4%B9%A6%E7%AE%A1%E7%90%86%E5%91%98)
    - [工具匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%B7%A5%E5%85%B7%E5%8C%A0)
    - [武器匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%AD%A6%E5%99%A8%E5%8C%A0)
- [流浪商人交易选项](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%B5%81%E6%B5%AA%E5%95%86%E4%BA%BA%E4%BA%A4%E6%98%93%E9%80%89%E9%A1%B9)

---

### Wiki 全目录（H2/H3/H4）

- [机制](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9C%BA%E5%88%B6)
  - [言论与声望](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E8%A8%80%E8%AE%BA%E4%B8%8E%E5%A3%B0%E6%9C%9B)
  - [供需关系](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BE%9B%E9%9C%80%E5%85%B3%E7%B3%BB)
  - [村庄英雄](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9D%91%E5%BA%84%E8%8B%B1%E9%9B%84)
  - [新增交易项与补货](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%96%B0%E5%A2%9E%E4%BA%A4%E6%98%93%E9%A1%B9%E4%B8%8E%E8%A1%A5%E8%B4%A7)
  - [交易](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BA%A4%E6%98%93)
- [村民职业与交易选项](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%9D%91%E6%B0%91%E8%81%8C%E4%B8%9A%E4%B8%8E%E4%BA%A4%E6%98%93%E9%80%89%E9%A1%B9)
  - [不能进行交易的村民](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%B8%8D%E8%83%BD%E8%BF%9B%E8%A1%8C%E4%BA%A4%E6%98%93%E7%9A%84%E6%9D%91%E6%B0%91)
    - [傻子](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%82%BB%E5%AD%90)
    - [失业](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%A4%B1%E4%B8%9A)
    - [幼年](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%B9%BC%E5%B9%B4)
  - [盔甲匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%9B%94%E7%94%B2%E5%8C%A0)
  - [屠夫](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%B1%A0%E5%A4%AB)
  - [制图师](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%88%B6%E5%9B%BE%E5%B8%88)
  - [牧师](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%89%A7%E5%B8%88)
  - [农民](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%86%9C%E6%B0%91)
  - [渔夫](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%B8%94%E5%A4%AB)
  - [制箭师](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%88%B6%E7%AE%AD%E5%B8%88)
  - [皮匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%9A%AE%E5%8C%A0)
  - [图书管理员](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%9B%BE%E4%B9%A6%E7%AE%A1%E7%90%86%E5%91%98)
  - [石匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%9F%B3%E5%8C%A0)
  - [牧羊人](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%89%A7%E7%BE%8A%E4%BA%BA)
  - [工具匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%B7%A5%E5%85%B7%E5%8C%A0)
  - [武器匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%AD%A6%E5%99%A8%E5%8C%A0)
- [流浪商人交易选项](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%B5%81%E6%B5%AA%E5%95%86%E4%BA%BA%E4%BA%A4%E6%98%93%E9%80%89%E9%A1%B9)
- [交易选项（村民交易的平衡性调整）](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BA%A4%E6%98%93%E9%80%89%E9%A1%B9%EF%BC%88-%7Bzh-cn%3A%E6%9D%91%E6%B0%91%E4%BA%A4%E6%98%93%E7%9A%84%E5%B9%B3%E8%A1%A1%E6%80%A7%E8%B0%83%E6%95%B4%3Bzh-tw%3A%E9%87%8D%E6%96%B0%E5%B9%B3%E8%A1%A1%E6%9D%91%E6%B0%91%E4%BA%A4%E6%98%93%3B%7D-%EF%BC%89)
  - [盔甲匠](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%9B%94%E7%94%B2%E5%8C%A0_2)
  - [图书管理员](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%9B%BE%E4%B9%A6%E7%AE%A1%E7%90%86%E5%91%98_2)
- [成就](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%88%90%E5%B0%B1)
- [进度](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E8%BF%9B%E5%BA%A6)
- [历史](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%8E%86%E5%8F%B2)
- [你知道吗](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E4%BD%A0%E7%9F%A5%E9%81%93%E5%90%97)
- [画廊](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E7%94%BB%E5%BB%8A)
- [注释](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E6%B3%A8%E9%87%8A)
- [参考](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%8F%82%E8%80%83)
- [导航](https://zh.minecraft.wiki/w/%E4%BA%A4%E6%98%93#%E5%AF%BC%E8%88%AA)

## 相关资源与材质 (Assets)

交易系统涉及 UI 与村民相关资源，常见定位：
- 村民职业纹理：`assets/minecraft/textures/entity/villager/`
- 交易 UI 元素：主要为客户端界面资源（位置随版本与资源包而变）

