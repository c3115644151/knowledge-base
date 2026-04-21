# Minecraft 机制：创造模式物品栏 (创造模式物品栏)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **创造模式物品栏 (Creative Mode Tabs)** 是玩家在创造模式下获取物品的主要界面。在 NeoForge 1.21+ 中，自定义物品栏以及向现有物品栏添加物品的机制已经完全数据驱动化和事件化。
- **核心注册类**：使用 `DeferredRegister<CreativeModeTab>`（注册表为 `Registries.CREATIVE_MODE_TAB`）来注册全新的物品栏。
- **构建物品栏**：通过 `CreativeModeTab.builder()` 方法可以设置物品栏的标题（`title`）、图标（`icon`）以及显示内容（`displayItems`）。
- **向现有物品栏添加物品**：不推荐直接修改原版的 `CreativeModeTab` 实例，而是应该订阅 `BuildCreativeModeTabContentsEvent` 事件。这允许模组在构建物品栏内容时，安全地将自己的物品插入到原版（如“战斗”、“红石”）或其他模组的物品栏中。
- **物品排序与可见性**：通过 `displayItems` 传入的 `Output` 接口，可以使用 `accept` 方法添加物品，还可以指定物品的可见性（如仅在操作员拥有特定权限时显示）。

---

## 极简代码示例 (Minimal Code Examples)

```java
import net.minecraft.core.registries.Registries;
import net.minecraft.network.chat.Component;
import net.minecraft.world.item.CreativeModeTab;
import net.minecraft.world.item.CreativeModeTabs;
import net.minecraft.world.item.ItemStack;
import net.minecraft.world.item.Items;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.neoforge.event.BuildCreativeModeTabContentsEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModCreativeTabs {
    // 1. 创建 DeferredRegister
    public static final DeferredRegister<CreativeModeTab> CREATIVE_MODE_TABS = 
        DeferredRegister.create(Registries.CREATIVE_MODE_TAB, "mymod");

    // 2. 注册自定义物品栏
    public static final java.util.function.Supplier<CreativeModeTab> MY_TAB = 
        CREATIVE_MODE_TABS.register("my_tab", () -> CreativeModeTab.builder()
            .title(Component.translatable("itemGroup.mymod.my_tab")) // 本地化标题
            .icon(() -> new ItemStack(Items.DIAMOND)) // 物品栏图标
            .displayItems((parameters, output) -> {
                // 向自定义物品栏添加物品
                output.accept(Items.DIRT); 
                // output.accept(ModItems.MY_CUSTOM_ITEM.get());
            }).build());

    // 3. 将注册表挂载到模组事件总线
    public static void register(IEventBus eventBus) {
        CREATIVE_MODE_TABS.register(eventBus);
    }

    // 4. 向原版物品栏添加物品
    @SubscribeEvent
    public static void buildContents(BuildCreativeModeTabContentsEvent event) {
        // 判断是否为原版的“建筑方块”物品栏
        if (event.getTabKey() == CreativeModeTabs.BUILDING_BLOCKS) {
            // 将物品添加到该物品栏
            // event.accept(ModItems.MY_CUSTOM_BLOCK.get());
        }
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [机制](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#机制)
  - [Java版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#Java版)
    - [搜索物品](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#搜索物品)
    - [已保存的快捷栏](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#已保存的快捷栏)
    - [物品销毁](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#物品销毁)
  - [基岩版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#基岩版)
  - [原主机版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#原主机版)
  - [New Nintendo 3DS版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#New_Nintendo_3DS版)
- [物品列表](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#物品列表)
  - [Java版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#Java版_2)
  - [基岩版](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#基岩版_2)
- [历史](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#历史)
- [参考](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#参考)
- [导航](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E5%88%9B%E9%80%A0%E6%A8%A1%E5%BC%8F%E7%89%A9%E5%93%81%E6%A0%8F#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
