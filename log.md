# 知识库操作日志

<!-- 只追加，不删除 -->

## [2026-04-09 13:00] ingest | AI知识库设计

新建话题。记录了对知识库架构的重新设计，借鉴Karpathy方案并优化：
- Skill体系重构，遵循渐进式加载原则
- 补充log.md操作日志机制
- 补充Lint健康检查机制
- 补充查询回写机制

## [2026-04-09 13:33] update | NeoForge开发认知

新建话题，整合历史 TOOLS.md 内容。版本号规则修正为四组件格式（YY.Drop.Hotfix.NeoForgeRelease），新增移除混淆意义、API 变化详情（ItemStackTemplate、GuiGraphicsExtractor、MutableQuad、ChunkPos）、工具链版本（Gradle 9.1.0+/MDG 2.0.141）、迁移策略。


## [2026-04-09 13:50] update | NeoForge开发认知

补充入门流程内容：
- 开发前置要求（Java基础、JDK、IDE、Git）
- 工作区搭建流程（Mod Generator、Gradle项目导入）
- 构建测试命令（gradlew build/runClient/runServer）
- 关键术语表（JDK/IDE/Gradle/JAR/Mod ID/EULA）
- 来源：官方入门文档 https://docs.neoforged.net/docs/gettingstarted/


## [2026-04-09 14:02] update | NeoForge开发认知

深化配置文件架构和模组加载流程：
- 新增配置文件架构图（gradle.properties → neoforge.mods.toml → @Mod 三层关系）
- 补充 gradle.properties 核心属性表
- 补充 neoforge.mods.toml 结构详解（[[mods]]块、依赖配置、特性配置、Mixin配置）
- 补充 @Mod 注解用法、构造函数参数、客户端专用类写法
- 补充 Java 基础：构造函数概念
- 新增关键术语：TOML、Group ID、IEventBus、ModContainer、Entrypoint
- 来源：官方 Mod Files 文档 https://docs.neoforged.net/docs/resources/game-assets/


## [2026-04-09 14:13] update | NeoForge开发认知

补充代码组织规范和AI编程最佳实践：
- 新增包命名规范（顶层包、第二层模组ID）
- 新增子包组织两种方式（按功能 vs 按逻辑）
- 新增类命名规范（类型后缀、Mojang例外）
- 新增特殊包隔离（client/server/data）
- 新增AI编程最佳实践：混合架构设计（registry集中 + feature按逻辑分组）
- 补充AI特点与架构匹配表、核心操作流程
- 来源：官方 Structuring Your Mod 文档

## [2026-04-09 14:17] update | NeoForge开发认知

补充版本号规范体系：
- 语义版本基础（major.minor.patch）
- Minecraft版本格式（标准/快照/预发布/发布候选）
- NeoForge版本新旧版区别（旧版20.2.59 vs 新版26.1.0.10-beta）
- 模组版本号规范（标准/扩展-API/扩展-Hotfix）
- 开发阶段标记（alpha→beta→release）
- 模组发布文件命名规范（基本/MC版本/加载器格式）
- AI编程中版本规范的重要性
- 来源：NeoForge Versioning 文档

## [2026-04-09 14:25] update | NeoForge开发认知

补充注册系统核心知识：
- 注册本质（注册 = 告诉游戏存在）、注册表概念、注册名格式
- DeferredRegister 完整用法（创建注册器/声明注册对象/构造函数注册）
- 常用注册表位置（BLOCKS/ITEMS/ENTITY_TYPES/BLOCK_ENTITY_TYPES）
- 特殊化注册器、获取注册对象方法
- 查询注册表（getValue/getKey/containsKey）
- ⚠️ 警告：注册完成前不要查询
- 自定义注册表（NewRegistryEvent）、数据包注册表（进阶）
- 注册核心术语表
- 来源：官方 Registries 文档 https://docs.neoforged.net/docs/concepts/registries


---

## 2026-04-09 知识库重构

### 结构调整
- 创建 `reference/` 目录：AI 专用参考文档（批量生成）
- 创建 `topics/` 目录：个性化知识（交流沉淀）
- 迁移 53 个 NeoForge 文档到 `reference/neoForge/`
- 迁移 `NeoForge开发认知.md` 到 `topics/`

### 命名规范
- reference/ 下的文档：API 文档风格，结构固定
- topics/ 下的文档：交流沉淀风格，结构灵活

### 清理
- 删除任务临时文件（清单、审查报告）
- 更新 index.md 和 README.md


## [2026-04-12 13:05] sync | 知识库整理与同步

首次完整同步，新增目录：
- agent-growth/ - Agent成长日记（含惯例与日记）
- raw/ - 原料知识（股票入门、视频解析）

索引更新：
- 更新 index.md 结构说明，添加新目录
- 更新 README.md 文件计数（53个NeoForge文档）
