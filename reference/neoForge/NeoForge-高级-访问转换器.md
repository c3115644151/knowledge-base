# NeoForge 高级 - 访问转换器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/advanced/accesstransformers

## 概述

访问转换器（Access Transformers，简称 AT）允许扩大类、方法和字段的可见性，并修改 `final` 标志。它们使 mod 开发者能够访问和修改外部类的不可访问成员。

详细规范文档：https://github.com/NeoForged/AccessTransformers/blob/main/FMLAT.md

## 添加 AT

将访问转换器添加到 mod 项目非常简单，只需在 `build.gradle` 中添加一行：

### ModDevGradle / NeoGradle

默认无需任何操作！

```
// In build.gradle:minecraft { accessTransformers { file 'src/main/resources/META-INF/accesstransformer.cfg'    }}
```

默认情况下，NeoForge 会搜索 `META-INF/accesstransformer.cfg`。如果 `build.gradle` 指定了其他位置的访问转换器，则需要在 `neoforge.mods.toml` 中定义其位置：

```
# In neoforge.mods.toml:
[[accessTransformers]]
file="META-INF/accesstransformer.cfg"
```

此外，可以指定多个 AT 文件并按顺序应用。

### ModDevGradle

```
// In build.gradle:
neoForge {
    // ModDevGradle 已经默认尝试包含 'src/main/resources/META-INF/accesstransformer.cfg'
    accessTransformers.from 'src/additions/resources/accesstransformer_additions.cfg'
}
```

### NeoGradle

```
// In build.gradle:minecraft { accessTransformers { file 'src/main/resources/META-INF/accesstransformer.cfg' file 'src/additions/resources/accesstransformer_additions.cfg'    }}
```

```
# In neoforge.mods.toml
[[accessTransformers]]
file="accesstransformer.cfg"
[[accessTransformers]]
file="accesstransformer_additions.cfg"
```

> 添加或修改任何访问转换器后，必须刷新 Gradle 项目才能使转换生效。

## 访问转换器规范

### 注释

`#` 后的所有文本直到行尾都被视为注释，不会被解析。

### 访问修饰符

访问修饰符指定给定目标将被转换到的新成员可见性，按可见性递减顺序：

| 修饰符 | 可见性范围 |
|--------|------------|
| `public` | 对包内外的所有类可见 |
| `protected` | 仅对包内和子类可见 |
| `default` | 仅对包内类可见 |
| `private` | 仅对类内部可见 |

特殊修饰符 `+f` 和 `-f` 可以附加到上述修饰符上，分别用于添加或移除 `final` 修饰符。

### 目标与指令

#### 类

```
<访问修饰符> <完全限定类名>
```

内部类通过将外部类的完全限定名与内部类名用 `$` 分隔表示。

#### 字段

```
<访问修饰符> <完全限定类名> <字段名>
```

#### 方法

```
<访问修饰符> <完全限定类名> <方法名>(<参数类型>)<返回类型>
```

### 类型描述符

也称为"描述符"，详见 [Java 虚拟机规范 SE 21 第 4.3.2 和 4.3.3 节](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-4.html#jvms-4.3.2)：

| 字符 | 类型 |
|------|------|
| `B` | byte，有符号字节 |
| `C` | char，UTF-16 中的 Unicode 字符码点 |
| `D` | double，双精度浮点数 |
| `F` | float，单精度浮点数 |
| `I` | int，32 位整数 |
| `J` | long，64 位整数 |
| `S` | short，有符号短整数 |
| `Z` | boolean，true 或 false |
| `[` | 数组类型的一维引用 |
| `L<class>;` | 引用类型（如 `Ljava/lang/String;`） |
| `(` | 方法描述符，参数在此指定 |
| `V` | 方法不返回值 |

### 示例

```
# 使 Crypt 中的 ByteArrayToKeyFunction 接口公开
public net.minecraft.util.Crypt$ByteArrayToKeyFunction

# 使 MinecraftServer 中的 'random' 受保护并移除 final 修饰符
protected-f net.minecraft.server.MinecraftServer random

# 使 Util 中的 'makeExecutor' 方法公开
public net.minecraft.Util makeExecutor(Ljava/lang/String;)Lnet/minecraft/TracingExecutor;

# 使 UUIDUtil 中的 'leastMostToIntArray' 方法公开
public net.minecraft.core.UUIDUtil leastMostToIntArray(JJ)[I
```

## 注意事项

- 指令只修改它直接引用的方法；任何覆写方法都不会被访问转换
- 建议确保转换的方法没有非转换的覆写限制可见性，否则会导致 JVM 抛出错误
- 可以安全转换的方法：`final` 方法（或 `final` 类中的方法）、`static` 方法
- `private` 方法通常也是安全的，但可能导致任何子类型中的非预期覆写

## 关联引用

- [可扩展枚举](./NeoForge-高级-可扩展枚举.md)
- [特性标志](./NeoForge-高级-特性标志.md)
