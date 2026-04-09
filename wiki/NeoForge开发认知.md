# NeoForge开发认知

## 当前理解

NeoForge 是 Minecraft 1.20.2+ 的现代模组开发框架，相比旧版 Forge 有重大架构变化。

**版本号规范体系**（重要认知）：

| 类型 | 格式 | 示例 |
|------|------|------|
| 语义版本 | major.minor.patch | 1.2.3 |
| Minecraft | 1.20.2（标准）/ 23w01a（快照）/ 1.20.2-pre1（预发布）/ 1.20.2-rc1（发布候选） | - |
| NeoForge（旧版） | MCminor.MCpatch.NeoForgeVersion | 20.2.59（对应MC 1.20.2） |
| NeoForge（26.1+） | YY.Drop.Hotfix.NeoForgeRelease | 26.1.0.10-beta |
| 模组标准 | major.minor.patch | 1.0.0 |
| 模组扩展-API | major.api.minor.patch | 10.4.5.19 |
| 模组扩展-Hotfix | major.minor.patch.hotfix | 0.5.1f |

**开发阶段标记**：alpha/experimental（不稳定）→ beta（半稳定）→ release/stable（稳定）。规则：`0.x.x` 为开发版，`1.0.0` 为正式版。

**模组发布文件命名规范**：
```
modid-版本号.jar                              # 基本格式
modid-MC版本-版本.jar                         # MC版本在前（更常见）
modid-MC版本-modload-版本.jar                 # 包含加载器
```

**核心版本号知识**：26.1.1.14-beta 表示 Minecraft 26.1.1 对应 NeoForge `26.1.1.14-beta`，Java 25 由 Foojay resolver 自动管理。**移除代码混淆**是重大里程碑：Mojang 移除了代码混淆，官方参数名直接可用，不再需要 Parchment mappings。

**工具链**：Java 25、Gradle 9.1.0+、ModDevGradle 2.0.141 / NeoGradle 7.1.21。

**配置文件架构（构建→运行→入口）**：

```
gradle.properties（构建时）
        ↓ 自动替换
neoforge.mods.toml（运行时）
        ↓ 加载
@Mod 主类（代码入口）
```

**gradle.properties 核心属性**：

| 属性 | 作用 |
|------|------|
| `mod_id` | 模组唯一标识（小写字母、数字、下划线，2-64字符） |
| `mod_name` | 显示名称 |
| `mod_version` | 版本号 |
| `mod_license` | 开源协议（MIT等） |
| `mod_group_id` | Java包名前缀（如 com.example.mymod） |
| `minecraft_version` | MC版本 |
| `neo_version` | NeoForge版本 |

**neoforge.mods.toml 结构**（位于 `src/main/resources/META-INF/`）：

- **非模组特定属性**：modLoader、loaderVersion、license
- **模组特定属性**：[[mods]] 块 - modId、version、displayName、description、logoFile、authors
- **依赖配置**：[[dependencies.modId]] - modId、type、versionRange、ordering、side
- **依赖类型**：required（必须）/ optional（可选）/ incompatible（不兼容）/ discouraged（不推荐）
- **特性配置**：[[features.modId]] - javaVersion 等
- **Mixin配置**：[[mixins]] - config

**@Mod 注解入口**：

```java
@Mod("mymod")  // 必须和 modId 一致
public class MyMod {
    public MyMod(IEventBus modBus, ModContainer container) {
        // 初始化逻辑
    }
}
```

**构造函数参数**（模组加载时自动调用）：

| 参数类型 | 用途 |
|----------|------|
| `IEventBus` | 事件总线，注册事件和内容 |
| `ModContainer` | 模组容器，获取模组信息 |
| `Dist` | 当前运行端（客户端/服务端） |
| `FMLModContainer` | javafml 的模组容器实现 |

**客户端专用类**：

```java
@Mod(value = "mymod", dist = Dist.CLIENT)
public class MyModClient {
    // 只在客户端加载
}
```

**Java基础概念：构造函数**
- **定义**：创建对象时自动执行的特殊方法，用于初始化对象
- **特性**：名字与类名相同、无返回类型、new时自动执行
- **在模组中**：游戏加载模组时自动 new 主类，构造函数执行初始化逻辑

**代码组织规范（Structuring Your Mod）**：

**包命名规范**：
- **顶层包**：使用唯一标识（域名/邮箱/用户名），如 `com.example`
- **第二层**：模组ID，如 `com.example.mymod`
- **目的**：避免不同模组的类冲突

**子包组织两种方式**：
| 方式 | 说明 | 适用场景 |
|------|------|----------|
| **按功能分组** | `block/`、`item/`、`entity/` | Minecraft 官方方式，相关类型集中 |
| **按逻辑分组** | `feature/oven/`、`feature/chest/` | 相关代码在一起，功能完整 |

**类命名规范**：
- 类型后缀：`PowerRingItem`、`NotDirtBlock`、`OvenMenu`
- Mojang例外：实体类不加后缀（`Pig`、`Zombie`）

**特殊包隔离**：
- `client/`：客户端专用代码，防止服务端调用崩溃
- `server/`：服务端专用代码
- `data/`：数据生成代码

**AI编程最佳实践：混合架构**

**设计原则：让 AI 在一个上下文内完成一个功能**

```
com.example.mymod/
│
├── MyMod.java              # 主入口
│
├── registry/               # 注册中心（集中管理）
│   ├── ModItems.java       # 所有物品注册
│   ├── ModBlocks.java      # 所有方块注册
│   └── ModBlockEntities.java
│
├── feature/                # 功能模块（按逻辑组织）
│   ├── ruby/               # 红宝石相关
│   │   ├── RubyOre.java
│   │   ├── RubyBlock.java
│   │   └── RubyItem.java
│   │
│   └── oven/               # 烤箱相关
│       ├── OvenBlock.java
│       ├── OvenBlockEntity.java
│       ├── OvenMenu.java
│       └── OvenScreen.java
│
├── client/                 # 客户端专用
│   └── ClientSetup.java
│
├── data/                   # 数据生成
│   └── DataGenerators.java
│
└── util/                   # 工具类
    └── Helpers.java
```

**AI特点与架构匹配**：

| AI特点 | 架构设计 |
|--------|----------|
| 上下文窗口有限 | 一个功能 = 一个 feature 目录 |
| 注意力机制 | 相关代码集中，关联更强 |
| 渐进式生成 | 按功能模块逐个生成 |
| 依赖搜索 | registry 集中，查找高效 |

**AI操作流程**：
```
"帮我做一个红宝石烤箱"
    ↓
1. 找到 feature/ 目录
2. 创建 feature/ruby_oven/
3. 在这个目录生成所有类
4. 去 registry/ 添加注册
5. 完成
```

**核心原则**：
- 注册集中：AI容易找到、容易添加
- 功能分组：AI的注意力聚焦
- 客户端隔离：防止服务端崩溃

**一致性原则**：
- 同类操作只用一种方法
- 避免混用导致bug

**核心开发规范**：
- 所有注册必须用 DeferredRegister
- 客户端/服务端代码分离
- 数据驱动优先（LootTable、Tags、Recipes 用 JSON）

**注册系统核心**：

NeoForge 使用注册表（Registry）管理系统内容，**不注册 = 不存在**。

| 概念 | 解释 |
|------|------|
| 注册（Register） | 告诉游戏"我的东西存在"，否则游戏不知道这些物品/方块 |
| 注册表（Registry） | 官方的"户口本"，映射注册名到对象 |
| 注册名 | 格式 `命名空间:名字`，如 `minecraft:dirt`、`mymod:ruby` |

**DeferredRegister 用法**（推荐方式）：

```java
// 创建注册器
public static final DeferredRegister<Block> BLOCKS = DeferredRegister.create(
    BuiltInRegistries.BLOCKS,  // 方块注册表
    "mymod"                     // 模组ID
);

// 声明注册对象
public static final DeferredHolder<Block, Block> RUBY_BLOCK = BLOCKS.register(
    "ruby_block",              // 注册名
    () -> new Block(...)       // 创建对象的Supplier
);

// 在构造函数注册
public MyMod(IEventBus modBus) {
    BLOCKS.register(modBus);   // 告诉注册器开始工作
}
```

**常用注册表**：

| 注册表 | 位置 | 注册内容 |
|--------|------|----------|
| 方块 | `BuiltInRegistries.BLOCKS` | 方块 |
| 物品 | `BuiltInRegistries.ITEMS` | 物品 |
| 实体 | `BuiltInRegistries.ENTITY_TYPES` | 生物、矿车等 |
| 方块实体 | `BuiltInRegistries.BLOCK_ENTITY_TYPES` | 箱子、熔炉等 |

**特殊化注册器**：
```java
DeferredRegister.Blocks BLOCKS = DeferredRegister.createBlocks("mymod");
DeferredRegister.Items ITEMS = DeferredRegister.createItems("mymod");
```

**查询注册表**：
```java
// 通过名字获取对象
Block dirt = BuiltInRegistries.BLOCKS.getValue(
    Identifier.fromNamespaceAndPath("minecraft", "dirt")
);

// 通过对象获取名字
Identifier name = BuiltInRegistries.BLOCKS.getKey(Blocks.DIRT);

// 检查是否存在
boolean hasItem = BuiltInRegistries.ITEMS.containsKey(
    Identifier.fromNamespaceAndPath("create", "brass_ingot")
);
```

⚠️ **警告：注册完成前不要查询！**

**自定义注册表**（高级）：
为模组提供扩展点，让其他模组能添加内容：
```java
public static final ResourceKey<Registry<Spell>> SPELL_REGISTRY_KEY = 
    ResourceKey.createRegistryKey(Identifier.fromNamespaceAndPath("mymod", "spells"));

// 在 NewRegistryEvent 中注册
@SubscribeEvent
public static void registerRegistries(NewRegistryEvent event) {
    event.register(SPELL_REGISTRY);
}
```

**注册核心术语**：

| 术语 | 解释 |
|------|------|
| Registry | 注册表，存所有已注册对象 |
| Register | 注册，把对象加入注册表 |
| DeferredRegister | 延迟注册器，推荐方式 |
| DeferredHolder | 持有注册对象的容器 |
| BuiltInRegistries | Minecraft 内置注册表位置 |
| Identifier | 标识符/注册名 |

**注册与代码结构的关系**：`registry/` 目录集中管理所有注册，与 DeferredRegister 配合使用，形成统一的注册入口。

**API 重要变化**：
- `ItemStack` → 需要 `ItemStackTemplate`（数据组件相关）
- `GuiGraphics` → `GuiGraphicsExtractor`，大量 GUI 方法重命名（render → extractRenderState 等）
- 新增 `MutableQuad`（可变 BakedQuad 表示）
- `ChunkPos` 构造：`new ChunkPos(pos)` → `ChunkPos.containing(pos)`

**迁移策略**：保持 1.21.11 工作区对照 26.1 工作区，通过对比 Vanilla 用法学习 API 变化。

**入门流程**（开发环境搭建 → 构建测试）：

1. **开发前置要求**：
   - Java 基础：面向对象、泛型、函数式特性
   - JDK：64位 JVM，26.1 需要 Java 25
   - IDE：IntelliJ IDEA / Eclipse（或使用 Claude Code 进行 AI 编程）
   - 版本控制：Git + GitHub（非必需但推荐）

2. **工作区搭建**：
   - 访问 Mod Generator（https://neoforged.net/mod-generator/）
   - 填写模组信息：名称、模组ID、包名、MC版本、Gradle插件
   - 下载解压 ZIP，导入 IDE（Gradle 项目）
   - 首次导入需下载依赖（耗时较长）
   - 核心配置文件：`gradle.properties`（mod_id、mod_name、mod_version、mod_group_id）

3. **构建与测试命令**：
   - 构建：`gradlew build` → 输出到 `build/libs/*.jar`
   - 客户端测试：`gradlew runClient`
   - 服务器测试：`gradlew runServer`（需接受 EULA、关闭正版验证）

**关键术语**：

| 术语 | 解释 |
|------|------|
| JDK | Java 开发工具包 |
| IDE | 集成开发环境（代码编辑器） |
| Gradle | 依赖管理和构建工具 |
| JAR | Java 打包文件格式 |
| Mod ID | 模组唯一标识符 |
| EULA | 最终用户许可协议 |
| TOML | 配置文件格式（类似JSON/YAML） |
| Group ID | Java包名前缀 |
| @Mod | 标记主类的注解 |
| IEventBus | 事件总线 |
| ModContainer | 模组容器 |
| Entrypoint | 入口点 |
| Semver | 语义化版本规范 |

## 演进历史

- **2026-04-09 14:25**：补充注册系统核心知识：
  - 注册本质（注册 = 告诉游戏存在）、注册表概念、注册名格式
  - DeferredRegister 完整用法（创建注册器、声明注册对象、构造函数注册）
  - 常用注册表位置（BLOCKS/ITEMS/ENTITY_TYPES/BLOCK_ENTITY_TYPES）
  - 特殊化注册器（DeferredRegister.Blocks/Items）
  - 获取注册对象方法（DeferredHolder/Supplier）
  - 查询注册表（getValue/getKey/containsKey）
  - ⚠️ 警告：注册完成前不要查询
  - 自定义注册表（NewRegistryEvent）
  - 数据包注册表（进阶）
  - 注册核心术语表
  - 来源：官方 Registries 文档 https://docs.neoforged.net/docs/concepts/registries
- **2026-04-09 14:13**：补充代码组织规范和AI编程最佳实践：
  - 新增包命名规范（顶层包、第二层模组ID）
  - 新增子包组织两种方式（按功能 vs 按逻辑）
  - 新增类命名规范（类型后缀、Mojang例外）
  - 新增特殊包隔离（client/server/data）
  - 新增AI编程最佳实践：混合架构设计（registry集中 + feature按逻辑分组）
  - 补充AI特点与架构匹配表、核心操作流程
  - 来源：官方 Structuring Your Mod 文档
- **2026-04-09 14:02**：深入配置文件架构和模组加载流程：
  - 新增配置文件架构图（gradle.properties → neoforge.mods.toml → @Mod 三层关系）
  - 补充 gradle.properties 核心属性表（mod_id、mod_name、mod_version、mod_license、mod_group_id 等）
  - 补充 neoforge.mods.toml 结构详解（位置、格式、[[mods]]块、依赖配置、特性配置、Mixin配置）
  - 补充 @Mod 注解用法和构造函数参数说明
  - 补充客户端专用类写法（dist = Dist.CLIENT）
  - 补充 Java 基础：构造函数概念
  - 新增关键术语：TOML、Group ID、@Mod、IEventBus、ModContainer、Entrypoint
- **2026-04-09 13:50**：补充入门流程开发环境搭建（Mod Generator）、构建测试命令（gradlew build/runClient/runServer）、关键术语表；用户使用 Claude Code 进行 AI 编程
- **2026-04-09**：版本号规则深化为四组件格式（YY.Drop.Hotfix.NeoForgeRelease），整合了 26.1 Release Notes 的重要变化：移除代码混淆（无需 Parchment）、工具链更新（Gradle 9.1.0+/MDG 2.0.141）、API 变化（ItemStackTemplate、GuiGraphicsExtractor、MutableQuad、ChunkPos）、迁移策略
- **2026-04-08**：初始认知建立——NeoForge 是 Forge 现代分支（1.20.2+），版本号采用年份制命名（26.1、26.1.1），核心规范包括 DeferredRegister、客户端/服务端分离、数据驱动优先

## 来源追踪

| 时间 | 类型 | 来源 | 核心贡献 |
|------|------|------|----------|
| 2026-04-09 | 官方文档 | https://docs.neoforged.net/docs/gettingstarted/ | 入门流程、工具链配置、构建测试命令 |
| 2026-04-09 | 官方文档 | https://docs.neoforged.net/docs/resources/game-assets/ | Mod Files 文档、neoforge.mods.toml 格式、@Mod 注解 |
| 2026-04-09 | 官方博客 | https://neoforged.net/news/26.1release/ | 四组件版本号、移除混淆、API 变化详情 |
| 2026-04-09 | 官方文档 | https://docs.neoforged.net/ | Structuring Your Mod：包命名规范、子包组织、类命名规范 |
| 2026-04-08 | 内部文档 | ./基础设定/TOOLS.md | 初始认知：NeoForge vs Forge 区别、开发规范 |
| 2026-04-09 | 官方文档 | NeoForge Versioning 文档 | 语义版本、Minecraft版本格式、NeoForge新旧版规则、模组版本号规范、开发阶段标记、文件命名规范 |
| 2026-04-09 | 官方文档 | https://docs.neoforged.net/docs/concepts/registries | 注册系统核心知识：DeferredRegister、注册表查询、自定义注册表、数据包注册表 |

## 关联话题

- 无
