# NeoForge 开发认知

> 个人认知文档，用于项目大局规划。技术细节查 `reference/neoForge/`。

---

## 生态定位

NeoForge 是 Minecraft 1.20.2+ 的现代模组框架，从 Forge 分叉而来。

**加载器三强格局（2026年）**：

| 加载器 | 状态 | 特点 |
|--------|------|------|
| **Forge** | 活跃开发 | 最大生态，历史最久，有 1.21.11 版本支持 |
| **NeoForge** | 活跃开发 | 2023年从 Forge 分叉，代码更现代 |
| **Fabric** | 活跃开发 | 轻量性能优先，更新最快 |

**为什么选 NeoForge**：
- 2023年12月 Forge 团队内部分歧，大部分开发团队离开创立 NeoForge
- 代码架构更干净、现代化
- API 设计更一致，文档更新更活跃
- 93% 热门模组已支持 NeoForge

**注意**：Forge 并未停止维护，仍在跟进最新版本。NeoForge 是"现代版 Forge"，不是替代品。

**当前版本**：Minecraft 26.1.1 / NeoForge 26.1.x

---

## 版本认知

**年份制命名**（重要变化）：
- 旧版：1.20.4、1.21 等
- 新版：26.1.1（2026年第一个 Drop 的第一个 Hotfix）

**版本号结构**：`YY.Drop.Hotfix`
- YY：年份（26 = 2026）
- Drop：大版本号
- Hotfix：小版本号

**工具链**：
| 工具 | 作用 |
|------|------|
| Java 25 | 运行环境 |
| Gradle | 构建工具 |
| ModDevGradle | NeoForge 官方插件 |
| IntelliJ IDEA / Claude Code | 开发环境 |

**官方资源**：
- Mod Generator：https://neoforged.net/mod-generator/
- 官方文档：https://docs.neoforged.net
- Discord 社区

---

## 项目架构设计

**这是我需要做的决策：如何组织代码目录。**

### 两种分包方式

| 方式 | 特点 | 适用场景 |
|------|------|----------|
| 按功能 | `blocks/`、`items/`、`entities/` | 小项目、传统项目 |
| 按逻辑 | `feature/ruby/`、`feature/oven/` | 功能独立、模块化项目 |

### AI 编程推荐：混合架构

```
com.example.mymod/
├── registry/         # 注册中心（集中管理所有注册）
├── feature/          # 功能模块（每个功能一个目录）
├── client/           # 客户端专用代码
└── data/             # 数据生成
```

**为什么这样设计**：
- `registry/` 集中：AI 容易找到注册位置，统一添加
- `feature/` 分组：一个功能 = 一个目录，AI 注意力聚焦
- 客户端隔离：防止服务端崩溃

**我的职责**：指定分包策略，决定功能如何划分。

---

## 核心概念认知

### 注册系统

**本质**：不注册 = 游戏不知道这个东西存在。

所有物品、方块、实体都需要注册到游戏的"户口本"里。

**我的认知**：注册是模组开发的基础动作，AI 会处理具体代码，我只需要知道"所有东西都要注册"。

### 配置文件三层

```
gradle.properties    →  构建时配置（版本号、模组ID）
neoforge.mods.toml   →  运行时配置（依赖、显示名）
@Mod 主类            →  代码入口
```

**我的认知**：配置分散在三层，改版本号要去 `gradle.properties`。

### 客户端/服务端分离

**原则**：客户端代码不能在服务端运行，会导致崩溃。

**我的认知**：渲染、GUI、特效属于客户端，逻辑、数据属于服务端。AI 会处理隔离，我需要知道有这个概念。

---

## 发布认知

**文件命名**：`modid-MC版本-版本号.jar`

**发布渠道**：
- CurseForge（主流）
- Modrinth（新兴）
- GitHub Releases（开源）

**版本阶段**：
- alpha/experimental：不稳定，早期测试
- beta：半稳定，功能基本完成
- release：稳定，正式发布

---

## 与 AI 协作的认知

**我负责**：
- 项目方向决策
- 功能需求定义
- 分包策略指定
- 版本规划

**AI 负责**：
- 具体代码实现
- API 查阅和调用
- Bug 修复
- 文档生成

**关键**：我只需要知道"有什么"和"为什么"，"怎么做"交给 AI 查 `reference/neoForge/`。

---

## 实战经验（2026-04-20 更新）

### 丛林神殿是 Legacy 结构

> **踩坑经验**：丛林神殿（`jungle_temple`）和沙漠神殿（`desert_pyramid`）是硬编码 Java 逻辑，**不是 Jigsaw 结构**。
> 无法通过 `data/minecraft/worldgen/processor_list/` JSON 覆盖注入方块。

**Legacy 结构** → 必须使用 **Mixin** 拦截生成逻辑
**Jigsaw 结构**（要塞、末地城、下界堡垒）→ 可使用 **StructureProcessor + processor_list**

### StructureProcessor 正确注册（26.1）

| 错误 | 正确 |
|---|---|
| `Registries.STRUCTURE_PROCESSOR_SERIALIZER` | `Registries.STRUCTURE_PROCESSOR` |
| `processBlock(ServerLevelAccessor level, ...)` | `processBlock(LevelReader level, ...)` |
| `SoundEvents.BRUSH_GENERIC_COMPLETED` | `SoundEvents.BRUSH_GRAVEL_COMPLETED` |
| `registerBlock(name, fn, props)` 三参数 | `register(name, props -> new Block(...))` 双参数 |

完整勘误见：`reference/neoForge/NeoForge-开发实践勘误.md`

---

## 演进历史

| 时间 | 变化 |
|------|------|
| 2026-04-09 | 初始版本，包含版本规范、配置架构、分包策略、注册认知 |
