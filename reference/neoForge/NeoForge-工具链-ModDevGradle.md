# NeoForge 工具链 - ModDevGradle

> **来源**：官方文档 https://docs.neoforged.net/toolchain/docs/plugins/mdg/
> **更新时间**：2026-04-20
> **版本**：26.1
> **适用场景**：新项目推荐使用 ModDevGradle，现有项目可继续使用 NeoGradle

---

## 📋 概述

ModDevGradle 是 NeoForge 新一代 Gradle 插件，相比 NeoGradle 有以下优势：

| 特性 | 说明 |
|------|------|
| Gradle 最佳实践 | 兼容 Gradle 8.8+ |
| 配置缓存支持 | 加速重复构建 |
| 自动日志配置 | 开发友好的日志设置 |
| Vanilla 模式 | 支持多加载器项目的纯 Minecraft 子项目 |

---

## 1. 基本配置

### 1.1 gradle.properties

```properties
# 启用 Gradle 配置缓存（可选）
org.gradle.configuration-cache=true
```

### 1.2 settings.gradle

```groovy
plugins {
    // 自动下载 Java 工具链
    id 'org.gradle.toolchains.foojay-resolver-convention' version '0.8.0'
}
```

### 1.3 build.gradle

```groovy
plugins {
    // 最新版本见 https://projects.neoforged.net/neoforged/ModDevGradle
    id 'net.neoforged.moddev' version '1.0.11'
}

neoForge {
    // NeoForge 版本，见 https://projects.neoforged.net/neoforged/neoforge
    version = "21.0.103-beta"
    
    // 验证 Access Transformer 文件（推荐开启）
    validateAccessTransformers = true
    
    runs {
        client {
            client()
        }
        data {
            data()
        }
        server {
            server()
        }
    }
    
    mods {
        testproject {
            sourceSet sourceSets.main
        }
    }
}
```

---

## 2. 运行配置

### 2.1 支持的运行类型

| 类型 | 说明 |
|------|------|
| `client` | 客户端运行 |
| `server` | 服务端运行 |
| `data` | 数据生成 |
| `gameTestServer` | 游戏测试服务器 |

### 2.2 运行配置详解

```groovy
neoForge {
    runs {
        configureEach {
            // 设置日志级别
            systemProperty 'forge.logging.console.level', 'debug'
        }
        
        client {
            client()
            // 工作目录（默认 run/）
            gameDirectory = project.file('runs/client')
            // JVM 参数
            jvmArguments = ["-XX:+AllowEnhancedClassRedefinition"]
            jvmArgument("-XX:+AllowEnhancedClassRedefinition")
            // 程序参数
            programArguments = ["--arg"]
            programArgument("--arg")
            // 系统属性
            systemProperties = ["a.b.c": "xyz"]
            systemProperty("a.b.c", "xyz")
            // 环境变量
            environment = ["FOO_BAR": "123"]
            environment("FOO_BAR", "123")
            // 日志级别
            logLevel = org.slf4j.event.Level.DEBUG
            // IDE 中显示的名称
            ideName = "Run Client"
            // 禁用 IDE 运行配置
            disableIdeRun()
            // 源集（默认 main）
            sourceSet = sourceSets.main
            // 加载的 mod
            loadedMods = [mods.mymod]
            // 启动前执行的任务（会显著减慢启动）
            taskBefore tasks.named("generateSomeCodeTask")
        }
    }
}
```

---

## 3. Vanilla 模式

用于多加载器项目的纯 Minecraft 子项目，不包含任何 Mod 加载器扩展。

```groovy
neoForge {
    // NeoForm 版本，见 https://projects.neoforged.net/neoforged/neoform
    neoFormVersion = "1.21-20240613.152323"
    
    runs {
        client { client() }
        server { server() }
        data { data() }
    }
}
```

**限制**：
- 仅支持 `client`、`server`、`data` 运行类型
- 不包含 Mod 加载器代码
- 仅支持基础资源包和数据包

---

## 4. 禁用反编译/重编译

从 MDG 2.0.124 开始，可以跳过反编译/重编译流程以加速 CI/CD。

**默认行为**：当 `CI` 环境变量为 `true` 时自动启用（GitHub Actions 默认为 true）。

**手动控制**：
```groovy
neoForge {
    enable {
        version = "..."
        disableRecompilation = true
    }
}
```

---

## 5. Jar-in-Jar

### 5.1 外部依赖

```groovy
dependencies {
    jarJar(implementation("org.commonmark:commonmark")) {
        version {
            // 兼容的版本范围
            strictly '[0.1, 1.0)'
            // 开发环境使用的版本
            prefer '0.21.0'
        }
    }
}
```

**版本范围格式**：

| 范围 | 含义 |
|------|------|
| `(,1.0]` | x <= 1.0 |
| `1.0` | 软性要求 1.0（允许任何版本）|
| `[1.0]` | 硬性要求 1.0 |
| `[1.2,1.3]` | 1.2 <= x <= 1.3 |
| `[1.0,2.0)` | 1.0 <= x < 2.0 |
| `[1.5,)` | x >= 1.5 |
| `(,1.0],[1.2,)` | x <= 1.0 或 x >= 1.2 |

### 5.2 本地文件

```groovy
sourceSets {
    plugin
}

neoForge {
    mods {
        'plugin' {
            sourceSet sourceSets.plugin
        }
    }
}

def pluginJar = tasks.register("pluginJar", Jar) {
    from(sourceSets.plugin.output)
    archiveClassifier = "plugin"
    manifest {
        attributes(
            'FMLModType': "LIBRARY",
            "Automatic-Module-Name": project.name + "-plugin"
        )
    }
}

dependencies {
    jarJar files(pluginJar)
}
```

### 5.3 子项目

```groovy
dependencies {
    jarJar project(":coremod")
}
```

---

## 6. 单元测试

### 6.1 JUnit 集成

```groovy
dependencies {
    testImplementation 'org.junit.jupiter:junit-jupiter:5.7.1'
    testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
}

test {
    useJUnitPlatform()
}

neoForge {
    unitTest {
        enable()
        testedMod = mods.mymod
    }
}
```

### 6.2 测试服务器

```groovy
dependencies {
    testImplementation "net.neoforged:testframework:<neoforge version>"
}
```

```java
@ExtendWith(EphemeralTestServerProvider.class)
public class TestClass {
    @Test
    public void testMethod(MinecraftServer server) {
        // 使用 server...
    }
}
```

---

## 7. Parchment 映射

使用社区提供的参数名和 Javadoc。

**方式一：gradle.properties**：
```properties
neoForge.parchment.minecraftVersion=1.21
neoForge.parchment.mappingsVersion=2024.06.23
```

**方式二：build.gradle**：
```groovy
neoForge {
    parchment {
        minecraftVersion = "1.20.6"
        mappingsVersion = "2024.05.01"
    }
}
```

---

## 8. Access Transformers

### 8.1 默认位置

放置在 `src/main/resources/META-INF/accesstransformer.cfg`，无需额外配置。

### 8.2 自定义位置

```groovy
neoForge {
    // 添加额外的 AT 文件
    accessTransformers.from "../src/main/resources/META-INF/accesstransformer.cfg"
    
    // 覆盖整个列表（移除默认）
    accessTransformers = ["../src/main/resources/META-INF/accesstransformer.cfg"]
}
```

### 8.3 发布 AT

```groovy
neoForge {
    accessTransformers {
        publish file("src/main/resources/META-INF/accesstransformer.cfg")
    }
}
```

消费发布的 AT：
```groovy
dependencies {
    accessTransformers "<group>:<artifact>:<version>"
}
```

---

## 9. Interface Injection

在开发时向 Minecraft 类添加接口。

**interfaces.json**：
```json
{
    "net/minecraft/world/item/ItemStack": [
        "testproject/FunExtensions"
    ]
}
```

**build.gradle**：
```groovy
neoForge {
    interfaceInjectionData.from "interfaces.json"
}
```

> ⚠️ 此功能仅用于开发时。运行时需要使用 Mixin 或 Coremod。

---

## 10. 常见问题

### 10.1 "Attach Sources" 无效（IntelliJ）

重新加载 Gradle 项目，然后再次点击 "Attach Sources"。

### 10.2 Task `idePostSync` not found

从其他插件迁移时出现此错误：

1. 打开 Gradle 工具窗口
2. 右键点击 Gradle 项目
3. 点击 `Tasks Activation`
4. 选择 `idePostSync` 任务并用 `-` 按钮删除
5. 重新同步 Gradle 项目

---

## 11. 版本对照

| Minecraft | NeoForge | ModDevGradle | Java |
|-----------|----------|--------------|------|
| 1.21.x | 21.0.x | 1.0.x | 21 |
| 26.1 | 26.1.x | 2.0.x | **25** |

---

*文档更新：2026-04-20*
*基于官方 ModDevGradle 文档*
