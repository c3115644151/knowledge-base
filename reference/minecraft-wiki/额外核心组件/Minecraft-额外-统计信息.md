# Minecraft 机制：统计信息 (统计信息)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **统计信息 (Statistics)** 是 Minecraft 中用来记录玩家各项行为数据的系统，分为通用统计（如“跳跃次数”）和物品/方块/实体相关的统计（如“挖掘方块次数”）。
- **核心注册表**：在 NeoForge 1.21+ 中，可以通过 `Registries.CUSTOM_STAT` 注册自定义的通用统计信息标识符（`ResourceLocation`）。
- **格式化器 (StatFormatter)**：原版提供了多种格式化器（如时间、距离、默认数值），注册自定义统计信息时必须通过 `Stats.makeCustomStat` 来指定其显示格式。
- **触发与增加**：在玩家触发相关行为的代码逻辑中（例如右键物品、方块交互），可以通过调用 `ServerPlayer.awardStat(stat)` 或 `ServerPlayer.awardStat(stat, amount)` 来增加玩家的统计信息数值。
- **与记分板联动**：原版的统计信息可以直接作为记分板的准则（Criteria），模组注册的自定义统计信息同样支持这一特性。

---

## 极简代码示例 (Minimal Code Examples)

```java
import net.minecraft.core.registries.Registries;
import net.minecraft.resources.ResourceLocation;
import net.minecraft.stats.StatFormatter;
import net.minecraft.stats.Stats;
import net.minecraft.world.entity.player.Player;
import net.neoforged.bus.api.IEventBus;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.event.lifecycle.FMLCommonSetupEvent;
import net.neoforged.neoforge.registries.DeferredRegister;

public class ModStats {
    // 1. 创建 CUSTOM_STAT 的 DeferredRegister
    public static final DeferredRegister<ResourceLocation> CUSTOM_STATS = 
        DeferredRegister.create(Registries.CUSTOM_STAT, "mymod");

    // 2. 注册自定义统计信息的 ResourceLocation
    public static final java.util.function.Supplier<ResourceLocation> INTERACT_WITH_BLOCK = 
        CUSTOM_STATS.register("interact_with_block", 
            () -> ResourceLocation.fromNamespaceAndPath("mymod", "interact_with_block"));

    public static void register(IEventBus eventBus) {
        CUSTOM_STATS.register(eventBus);
    }

    // 3. 在 CommonSetup 中为其指定格式化器
    @SubscribeEvent
    public static void commonSetup(FMLCommonSetupEvent event) {
        event.enqueueWork(() -> {
            // 使用 DEFAULT 格式化器（直接显示数字）
            Stats.makeCustomStat(INTERACT_WITH_BLOCK.get(), StatFormatter.DEFAULT);
        });
    }

    // 4. 在具体逻辑中触发统计增加
    public static void onPlayerInteract(Player player) {
        if (!player.level().isClientSide()) {
            player.awardStat(INTERACT_WITH_BLOCK.get()); // 默认增加 1
            // 此时对应的本地化键为: stat.mymod.interact_with_block
        }
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [统计界面](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#统计界面)
- [命名空间ID](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#命名空间ID)
  - [统计类型和名称](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#统计类型和名称)
  - [统计信息列表](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#统计信息列表)
- [存储格式](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#存储格式)
- [历史](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#历史)
- [画廊](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#画廊)
- [参考](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#参考)
- [导航](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E7%BB%9F%E8%AE%A1%E4%BF%A1%E6%81%AF#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
