# NeoForge 入门指南

## 环境配置

### 前置要求
- Java 21 JDK（推荐 Microsoft OpenJDK）
- IDE（IntelliJ IDEA / Eclipse）
- Git
- 64-bit JVM

### 项目初始化
1. 访问 [Mod Generator](https://neoforged.net/mod-generator/) 下载 MDK
2. 解压 ZIP 并导入 Gradle 项目
3. 首次构建：`gradlew build`（耗时较长）
4. 测试运行：`gradlew runClient` / `gradlew runServer`

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
versionRange="[20.6,)"
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
minecraft_version=1.21.11
minecraft_version_range=[1.21.10,1.22)
neo_version=26.1.1
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

## 关联文档
- [NeoForge-概念.md](./NeoForge-概念.md) - 核心概念（注册表、事件、Sides）
- [NeoForge-方块.md](./NeoForge-方块.md) - 方块开发
- [NeoForge-物品.md](./NeoForge-物品.md) - 物品开发
