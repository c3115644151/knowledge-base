# Minecraft：进度 (进度)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **数据生成器 (Data Generation)**：1.21+ 中极其推荐使用数据生成器（Datagen）来生成进度（Advancement） JSON。开发者需实现 `AdvancementProvider.AdvancementGenerator`，通过流式构建器 `Advancement.Builder.advancement()` 来定义进度。
- **自定义触发器 (Criterion Triggers)**：自定义进度触发条件需继承 `SimpleCriterionTrigger`（或相关类），并通过 `DeferredRegister<CriterionTrigger<?>>`（注册到 `Registries.TRIGGER_TYPE`）进行注册。在满足条件时，调用触发器的 `trigger` 方法以授予玩家进度。
- **数据组件的影响 (Data Components in Criteria)**：在 1.21+ 中，由于移除了 NBT 系统，进度中的物品检查（如 `inventory_changed` 触发器）**不再支持 `nbt` 字段**。取而代之的是使用 `components` 谓词来检查物品的数据组件（如检查是否带有特定的自定义组件）。
- **进度结构 (Advancement Structure)**：主要由四部分构成：`display`（显示在界面的图标、名称、描述和背景）、`parent`（指定父节点，以构建进度树）、`criteria`（达成条件，支持与/或逻辑，通常结合 `requirements`）和 `rewards`（完成奖励，如经验、物品或执行函数）。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 注册自定义触发器
public static final DeferredRegister<CriterionTrigger<?>> TRIGGERS = DeferredRegister.create(Registries.TRIGGER_TYPE, "mymod");
public static final DeferredHolder<CriterionTrigger<?>, MyCustomTrigger> CUSTOM_TRIGGER = TRIGGERS.register("my_trigger", () -> new MyCustomTrigger());

// 2. 进度数据生成 (Datagen 1.21+)
public class MyAdvancementProvider implements AdvancementProvider.AdvancementGenerator {
    @Override
    public void generate(HolderLookup.Provider registries, Consumer<AdvancementHolder> saver, ExistingFileHelper existingFileHelper) {
        AdvancementHolder root = Advancement.Builder.advancement()
            .display(
                MyItems.MAGIC_WAND.get(), // 图标
                Component.translatable("advancement.mymod.root.title"),
                Component.translatable("advancement.mymod.root.desc"),
                ResourceLocation.fromNamespaceAndPath("mymod", "textures/gui/advancements/backgrounds/magic.png"),
                AdvancementType.TASK,
                true, true, false
            )
            .addCriterion("has_wand", InventoryChangeTrigger.TriggerInstance.hasItems(MyItems.MAGIC_WAND.get()))
            .save(saver, ResourceLocation.fromNamespaceAndPath("mymod", "root"), existingFileHelper);
    }
}
```

**JSON 示例：检查包含特定数据组件的物品 (1.21+)**

在 1.21+ 中，如果编写 JSON 来判断物品，应使用 `predicates` 检查组件（取代 NBT）：

```json
{
  "criteria": {
    "has_custom_component_item": {
      "trigger": "minecraft:inventory_changed",
      "conditions": {
        "items": [
          {
            "items": "minecraft:stick",
            "predicates": {
              "minecraft:custom_data": "{my_custom_value: 1b}"
            }
          }
        ]
      }
    }
  }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [获取](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#获取)
- [界面](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#界面)
- [进度列表](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#进度列表)
  - [Minecraft](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#-{zh-cn:Minecraft;zh-tw:Minecraft;zh-hk:Minecraft;}-)
  - [下界](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#-{zh-cn:下界;zh-tw:地獄;zh-hk:地獄;}-)
  - [末地](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#-{zh-cn:末地;zh-tw:終界;zh-hk:終界;}-)
  - [冒险](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#-{zh-cn:冒险;zh-tw:冒險;zh-hk:冒險;}-)
  - [农牧业](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#-{zh-cn:农牧业;zh-tw:農牧;zh-hk:農牧;}-)
- [JSON格式](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#JSON格式)
- [音效](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#音效)
- [历史](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#历史)
- [你知道吗](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#你知道吗)
  - [出处](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#出处)
- [画廊](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#画廊)
  - [统计](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#统计)
- [参见](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#参见)
- [参考](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#参考)
- [导航](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E8%BF%9B%E5%BA%A6#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
