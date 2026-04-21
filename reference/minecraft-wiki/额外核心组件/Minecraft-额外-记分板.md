# Minecraft 机制：记分板 (记分板)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **记分板 (Scoreboard)** 主要由服务器端维护，由目标 (Objectives)、分数 (Scores) 和队伍 (Teams) 组成。在模组开发中，大部分操作应该在服务端（如 Server 级事件）进行。
- **获取记分板实例**：通过 `MinecraftServer.getScoreboard()` 可以获取服务端的记分板实例（`ServerScoreboard`）。
- **自定义记分准则 (Criteria)**：你可以创建自定义的 `ObjectiveCriteria`，让其成为记分项的基础标准（通常使用 `ObjectiveCriteria.registerCustom()` 进行注册，并在对应逻辑中更新分数）。
- **分数操作与更新**：通过获取 `Objective` 并调用 `scoreboard.getOrCreatePlayerScore(playerName, objective)` 来更新玩家的分数。在 NeoForge 中，通常在 `PlayerEvent`（如登录、击杀）或 `ServerTickEvent` 中实时维护模组自己的记分逻辑。
- **持久化数据**：由于记分板是原版自带的保存系统，在部分轻量级场景下，模组可以使用隐藏的记分项目来临时或永久存储玩家的数值数据（替代 `SavedData` 或 `Attachment`，但不建议用于复杂的 NBT 存储）。

---

## 极简代码示例 (Minimal Code Examples)

```java
import net.minecraft.network.chat.Component;
import net.minecraft.server.MinecraftServer;
import net.minecraft.world.scores.Objective;
import net.minecraft.world.scores.Scoreboard;
import net.minecraft.world.scores.criteria.ObjectiveCriteria;
import net.minecraft.world.scores.numbers.FixedFormat;
import net.neoforged.bus.api.SubscribeEvent;
import net.neoforged.fml.common.EventBusSubscriber;
import net.neoforged.neoforge.event.entity.player.PlayerEvent;
import net.neoforged.neoforge.event.server.ServerStartedEvent;

@EventBusSubscriber(modid = "mymod")
public class ModScoreboardEvents {
    
    // 自定义准则：通常为 Dummy (dummy)，表示只由命令或模组代码修改
    public static final ObjectiveCriteria MY_CRITERIA = 
        ObjectiveCriteria.registerCustom("mymod:mana");

    // 1. 在服务器启动后初始化记分项
    @SubscribeEvent
    public static void onServerStarted(ServerStartedEvent event) {
        MinecraftServer server = event.getServer();
        Scoreboard scoreboard = server.getScoreboard();
        
        // 检查是否已经存在该记分项
        if (scoreboard.getObjective("mana_score") == null) {
            // 1.21 新增了对数字格式（NumberFormat）的参数支持
            scoreboard.addObjective(
                "mana_score",
                MY_CRITERIA,
                Component.translatable("objective.mymod.mana"), // 显示名称
                ObjectiveCriteria.RenderType.INTEGER, // 渲染类型：整数
                true, // 是否在列表显示
                null // 数字格式，1.21 新增参数，可传 null 默认，或者使用 new FixedFormat(Component.literal("..."))
            );
        }
    }

    // 2. 在玩家登录时，给予初始分数
    @SubscribeEvent
    public static void onPlayerLoggedIn(PlayerEvent.PlayerLoggedInEvent event) {
        if (!event.getEntity().level().isClientSide()) {
            MinecraftServer server = event.getEntity().getServer();
            Scoreboard scoreboard = server.getScoreboard();
            
            Objective manaObjective = scoreboard.getObjective("mana_score");
            if (manaObjective != null) {
                // 1.20.4+ / 1.21+ 更新分数的方式：Player 实现了 ScoreHolder，返回值是 ScoreAccess
                scoreboard.getOrCreatePlayerScore(event.getEntity(), manaObjective).add(10);
            }
        }
    }
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [记分项](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#记分项)
  - [准则](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#准则)
    - [Java版](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#Java版)
    - [基岩版](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#基岩版)
- [显示位置](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#显示位置)
- [队伍](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#队伍)
- [存储格式](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#存储格式)
- [历史](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#历史)
- [参考](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#参考)
- [导航](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E8%AE%B0%E5%88%86%E6%9D%BF#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
