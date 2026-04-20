# NeoForge 入门指南

> **版本对照**：
> - 本文档基准：**1.21.11 / NeoForge 26.1**
> - 官方最新：**26.1**（2026-04 更新）
> - 主要变化：Java 21→25，新增 Gradle 插件选择

---

## 环境配置

### 前置要求

| 项目 | 1.21.11 版本 | 26.1 版本（最新）| 迁移说明 |
|------|-------------|-----------------|----------|
| Java JDK | **Java 21** | **Java 25** | ⚠️ 需升级 JDK |
| JVM | 64-bit | 64-bit（不变）| - |
| IDE | IntelliJ / Eclipse | IntelliJ / Eclipse（不变）| - |
| Git | 推荐 | 推荐（不变）| - |

> **🔄 跨版本迁移**：从 1.21.11 迁移到 26.1，需要：
> 1. 安装 Java 25 JDK（推荐 [Microsoft OpenJDK](https://learn.microsoft.com/en-us/java/openjdk/download#openjdk-25)）
> 2. 更新 `JAVA_HOME` 环境变量
> 3. 重新导入 Gradle 项目

### 项目初始化

1. 访问 [Mod Generator](https://neoforged.net/mod-generator/)
2. 填写信息：
   - Mod 名称（可选 Mod ID）
   - 包名
   - **Minecraft 版本**
   - **Gradle 插件**（新增选择，见下表）
3. 下载 ZIP 并解压
4. 导入 IDE，Gradle 会自动下载依赖

#### Gradle 插件选择（26.1 新增）

| 插件 | 说明 | 推荐场景 |
|------|------|----------|
| **ModDevGradle** | 新一代插件，更快 | ✅ 新项目推荐 |
| **NeoGradle** | 传统插件，稳定 | 现有项目迁移 |

> **🔄 跨版本迁移**：现有 NeoGradle 项目可以继续使用，但新项目推荐 ModDevGradle。

### 构建与测试

```bash
# 构建 mod
gradlew build
# 输出: build/libs/<archivesBaseName>-<version>.jar

# 客户端测试
gradlew runClient

# 服务端测试
gradlew runServer
```

### 服务端测试配置

1. 编辑 `eula.txt` 接受 EULA
2. 编辑 `server.properties` 设置 `online-mode=false`
3. 启动服务器

> 💡 **提示**：始终在专用服务器环境测试 mod，包括 client-only mod。

---

## mod 文件结构

### gradle.properties 核心配置

| 属性 | 说明 | 示例 |
|------|------|------|
| `mod_id` | Mod 唯一标识（小写字母/数字/下划线） | `mod_id=examplemod` |
| `mod_name` | 显示名称 | `mod_name=Example Mod` |
| `mod_version` | 版本号 | `mod_version=1.0.0` |
| `mod_group_id` | 包名 | `mod_group_id=com.example` |

### neoforge.mods.toml

```toml
[[mods]]
modId="examplemod"
version="${file.jarVersion}"
displayName="Example Mod"
description='''描述内容'''

[[dependencies.examplemod]]
modId="neoforge"
type="required"
versionRange="[20.6,)"  # 根据目标版本调整
ordering="NONE"
side="BOTH"
```

### @Mod 注解入口

```java
@Mod("examplemod")
public class ExampleMod {
    public ExampleMod(IEventBus modBus) {
        // 注册 DeferredRegister
        // 注册事件处理器
    }
}

// 客户端专用
@Mod(value = "examplemod", dist = Dist.CLIENT)
public class ExampleModClient {
    public ExampleModClient(IEventBus modBus) {
        // 客户端逻辑
    }
}
```

### 构造函数参数

| 参数类型 | 说明 |
|----------|------|
| `IEventBus` | Mod 事件总线（注册用） |
| `ModContainer` | Mod 元数据容器 |
| `Dist` | 物理端（CLIENT/DEDICATED_SERVER） |

---

## 依赖配置

```toml
[[dependencies.modid]]
modId="其他mod_id"
type="required"           # required/optional/incompatible/discouraged
versionRange="[1.0,2.0)"
ordering="NONE"           # NONE/BEFORE/AFTER
side="BOTH"              # BOTH/CLIENT/SERVER
reason="集成说明"
```

---

## 版本规范

### NeoForge 版本格式
`YY.Drop.Hotfix`（如 26.1.1 = 2026年第1个版本第1个热修）

### Minecraft 版本兼容性

```properties
# 1.21.11 版本配置
minecraft_version=1.21.11
minecraft_version_range=[1.21.10,1.22)
neo_version=26.1.1

# 26.1 版本配置（示例，根据实际调整）
minecraft_version=1.21.x  # 根据官方支持情况
neo_version=26.1.x
```

---

## 目录结构

```
src/main/java/com/example/modid/
    ├── ExampleMod.java           # 主入口类
    ├── init/                     # 注册类
    │   ├── ModBlocks.java
    │   ├── ModItems.java
    │   └── ModEntities.java
    └── ...                       # 其他模块

src/main/resources/
    └── META-INF/
        └── neoforge.mods.toml

src/client/java/                  # 客户端代码（可选）
src/server/java/                  # 服务端代码（可选）
```

---

## 注意事项

- ⚠️ 不要在 `build.gradle` 中编辑基础属性，使用 `gradle.properties`
- ⚠️ 始终在专用服务器上测试 mod
- ⚠️ Mod ID 必须在所有 mod 中唯一
- ⚠️ Mod 应对两个物理端都可用，或显式声明端

---

## 🔄 版本迁移速查表

### 从 1.21.11 迁移到 26.1

| 变更项 | 原配置 | 新配置 | 操作 |
|--------|--------|--------|------|
| Java 版本 | 21 | **25** | 升级 JDK |
| Gradle 插件 | NeoGradle | ModDevGradle / NeoGradle | 可选更新 |
| 首次构建时间 | 较长 | 较长（不变）| - |
| run 目录 | `run/` | `runs/client` `runs/server` | 路径变化 |

### 需要检查的文件

1. **gradle.properties** - 确认版本号
2. **build.gradle** - 如果使用 ModDevGradle，配置语法可能不同
3. **settings.gradle** - 插件声明可能需要更新
4. **JAVA_HOME** - 确保指向 Java 25

---

## 关联文档
- [NeoForge-概念.md](./NeoForge-概念.md) - 核心概念（注册表、事件、Sides）
- [NeoForge-方块.md](./NeoForge-方块.md) - 方块开发
- [NeoForge-物品.md](./NeoForge-物品.md) - 物品开发

---

*文档更新：2026-04-20*
*基于官方文档 Version 26.1*
