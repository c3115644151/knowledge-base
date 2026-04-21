# Minecraft：命令 (命令)

> **Wiki 源地址**：[https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4)
> **适用版本**：Java 版 1.21+ / NeoForge 26.1+
> **本地更新时间**：2026-04-20

---

## 模组开发核心要点 (Modding Priorities)

- **命令注册 (Command Registration)**：在 NeoForge 1.21+ 中，必须通过监听 `RegisterCommandsEvent` 来注册自定义命令。可以通过 `event.getDispatcher()` 获取 Brigadier 命令调度器。
- **上下文构建器 (CommandBuildContext)**：1.21+ 引入了大量基于注册表和数据组件的命令参数。当在注册命令时，如果使用了需要访问注册表或验证组件的参数（如 `ItemArgument`、`BlockStateArgument`、`ResourceArgument`），**必须使用** `event.getBuildContext()` 获取上下文构建器，以确保能够正确解析这些数据。
- **环境隔离 (Environment Selection)**：注册命令时，应通过检查 `event.getCommandSelection()` 来判断当前环境是专用服务器 (`DEDICATED`)、单人游戏 (`INTEGRATED`) 还是全部 (`ALL`)。对于只应在特定环境下运行的命令，此检查能够防止不适当的注册。
- **Brigadier 语法基础**：命令结构由 `Commands.literal`（固定命令字面量，如 `/mymod`）和 `Commands.argument`（动态参数输入，如 `<player>`、`<item>`）层级拼接而成。最终的执行逻辑编写在 `executes(context -> { ... })` 方法中，并要求返回一个 `int` 表示执行结果的状态或影响数量。

---

## 极简代码示例 (Minimal Code Examples)

```java
// 1. 命令注册与 Brigadier 语法 (1.21+)
@SubscribeEvent
public static void onRegisterCommands(RegisterCommandsEvent event) {
    CommandDispatcher<CommandSourceStack> dispatcher = event.getDispatcher();
    // 获取 1.21+ 解析物品、方块等组件/注册表所需的上下文
    CommandBuildContext buildContext = event.getBuildContext();

    dispatcher.register(
        // 根命令：/mymod
        Commands.literal("mymod")
            // 权限检查：需要 OP 权限
            .requires(source -> source.hasPermission(2)) 
            
            // 子命令：/mymod give_magic <item>
            .then(Commands.literal("give_magic")
                // 使用 ItemArgument，必须传入 buildContext 以解析组件
                .then(Commands.argument("item", ItemArgument.item(buildContext))
                    .executes(context -> {
                        // 获取命令源上下文
                        CommandSourceStack source = context.getSource();
                        // 解析物品输入
                        ItemInput itemInput = ItemArgument.getItem(context, "item");
                        
                        try {
                            ServerPlayer player = source.getPlayerOrException();
                            // 创建物品栈（会自动附带由命令输入的数据组件）
                            ItemStack stack = itemInput.createItemStack(1, false);
                            player.getInventory().add(stack);
                            
                            // 发送反馈信息，true 表示广播给其他管理员
                            source.sendSuccess(() -> Component.literal("成功发放了魔法物品！"), true);
                            
                            return 1; // 成功时返回 1（或其他正整数，表示受影响的数量）
                        } catch (CommandSyntaxException e) {
                            return 0; // 失败时返回 0
                        }
                    })
                )
            )
    );
}
```

---

## 原版 Wiki 快速索引 (Quick Reference)

对于原版基础概念、具体数值或冗长表格，请直接通过以下锚点跳转至 Wiki 原文查阅。

### Wiki 全目录（H2/H3/H4）

- [使用](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#使用)
- [命令指引](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#命令指引)
  - [语法表示](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#语法表示)
  - [限制条件](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#限制条件)
    - [作弊](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#作弊)
  - [参数类型](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#参数类型)
  - [解析与执行](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#解析与执行)
    - [输出](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#输出)
    - [结果](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#结果)
- [命令列表及其概述](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#命令列表及其概述)
  - [Java版](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#Java版)
    - [调试命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#调试命令)
  - [基岩版和教育版](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#基岩版和教育版)
    - [隐藏命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#隐藏命令)
  - [已移除的命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#已移除的命令)
    - [基岩版开发者命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#基岩版开发者命令)
    - [智能体命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#智能体命令)
  - [愚人节命令](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#愚人节命令)
- [历史](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#历史)
- [参见](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#参见)
- [参考](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#参考)
- [导航](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#导航)
  - [个人工具](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-personal-label)
  - [associated-pages](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-associated-pages-label)
  - [查看](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-views-label)
  - [导航](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-navigation-label)
  - [社区](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-sidebar-community-label)
  - [游戏及衍生作品](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-sidebar-game-label)
  - [版本](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-version-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-sidebar-usefulminecraftpages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-sidebar-usefuldungeonspages-label)
  - [常用页面](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-sidebar-usefullegendspages-label)
  - [工具](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-tb-label)
  - [其他语言](https://zh.minecraft.wiki/w/%E5%91%BD%E4%BB%A4#p-lang-label)

## 相关资源与材质 (Assets)

*(待补充该机制相关的原版资源路径)*
