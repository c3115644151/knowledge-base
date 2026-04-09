# NeoForge 高级 - 可扩展枚举

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/advanced/extensibleenums

## 概述

可扩展枚举是对特定原版枚举的增强，允许添加新条目。这是通过在运行时修改枚举的编译字节码来添加元素的。

## `IExtensibleEnum`

所有可以添加新条目的枚举都实现了 `IExtensibleEnum` 接口。该接口作为一个标记，让 `RuntimeEnumExtender` 启动插件服务知道哪些枚举应该被转换。

> ⚠️ **警告**：你不应该在自己的枚举上实现此接口。根据用例改用 Map 或注册表。

未被修补实现该接口的枚举不能通过 Mixin 或 Coremod 添加该接口，因为转换器运行的顺序问题。

### 创建枚举条目

要创建新的枚举条目，需要创建一个 JSON 文件，并在 `neoforge.mods.toml` 中通过 `[[mods]]` 块的 `enumExtensions` 条目引用它：

```
# In neoforge.mods.toml:
[[mods]]
enumExtensions="META-INF/enumextensions.json"
```

JSON 文件结构：

```json
{
    "entries": [
        {
            "enum": "net/minecraft/world/item/ItemDisplayContext",
            "name": "EXAMPLEMOD_STANDING",
            "constructor": "(ILjava/lang/String;Ljava/lang/String;)V",
            "parameters": [ -1, "examplemod:standing", null ]
        },
        {
            "enum": "net/minecraft/world/item/Rarity",
            "name": "EXAMPLEMOD_CUSTOM",
            "constructor": "(ILjava/lang/String;Ljava/util/function/UnaryOperator;)V",
            "parameters": {
                "class": "example/examplemod/MyEnumParams",
                "field": "CUSTOM_RARITY_ENUM_PROXY"
            }
        },
        {
            "enum": "net/minecraft/world/damagesource/DamageEffects",
            "name": "EXAMPLEMOD_TEST",
            "constructor": "(Ljava/lang/String;Ljava/util/function/Supplier;)V",
            "parameters": {
                "class": "example/examplemod/MyEnumParams",
                "method": "getTestDamageEffectsParameter"
            }
        }
    ]
}
```

参数提供类示例：

```java
public class MyEnumParams {
    public static final EnumProxy<Rarity> CUSTOM_RARITY_ENUM_PROXY = new EnumProxy<>(
            Rarity.class, -1, "examplemod:custom", (UnaryOperator<Style>) style -> style.withItalic(true)
    );

    public static Object getTestDamageEffectsParameter(int idx, Class<?> type) {
        return type.cast(switch (idx) {
            case 0 -> "examplemod:test";
            case 1 -> (Supplier<SoundEvent>) () -> SoundEvents.DONKEY_ANGRY;
            default -> throw new IllegalArgumentException("Unexpected parameter index: " + idx);
        });
    }
}
```

### 构造函数

构造函数必须指定为[方法描述符](https://docs.oracle.com/jase/specs/jvms/se21/html/jvms-4.html#jvms-4.3.2)，且只能包含源代码中可见的参数。

如果构造函数标有 `@ReservedConstructor` 注解，则不能用于 mod 枚举常量。

### 参数传递

参数可以以下三种方式指定：

1. **内联在 JSON 文件中**（仅允许原始值、字符串和 null）
2. **引用 mod 中某个类的 `EnumProxy<TheEnum>` 类型字段**
3. **引用返回 `Object` 的方法**，方法必须有两个参数：`int`（参数索引）和 `Class<?>`（预期类型）

> ⚠️ **警告**：用作参数值来源的字段和/或方法应放在单独的类中，以避免过早加载 mod 类。

### 特殊参数规则

- 如果参数是枚举上 `@IndexedEnum` 注解相关的 int ID 参数，则会被忽略并替换为条目的 ordinal
- 如果参数是枚举上 `@NamedEnum` 注解相关的 String name 参数，则必须使用 `namespace:path` 格式前缀 mod ID

### 获取生成的常量

可以通过 `TheEnum.valueOf(String)` 获取生成的枚举常量。如果使用字段引用提供参数，也可以通过 `EnumProxy#getValue()` 获取。

## 为 NeoForge 贡献

要将新的可扩展枚举添加到 NeoForge，至少需要做两件事：

1. 让枚举实现 `IExtensibleEnum`
2. 添加返回 `ExtensionInfo.nonExtended(TheEnum.class)` 的 `getExtensionInfo` 方法

根据枚举的具体细节，可能需要额外操作：

```java
// 示例枚举
@net.neoforged.fml.common.asm.enumextension.IndexedEnum
@net.neoforged.fml.common.asm.enumextension.NamedEnum(1)
@net.neoforged.fml.common.asm.enumextension.NetworkedEnum(...)
public enum ExampleEnum implements net.neoforged.fml.common.asm.enumextension.IExtensibleEnum {
    VALUE_1(0, "value_1", false),
    VALUE_2(1, "value_2", true),
    VALUE_3(2, "value_3");

    ExampleEnum(int arg1, String arg2, boolean arg3) { /* ... */ }
    ExampleEnum(int arg1, String arg2) { this(arg1, arg2, false); }

    public static net.neoforged.fml.common.asm.enumextension.ExtensionInfo getExtensionInfo() {
        return net.neoforged.fml.common.asm.enumextension.ExtensionInfo.nonExtended(ExampleEnum.class);
    }
}
```

## 关联引用

- [访问转换器](./NeoForge-高级-访问转换器.md)
- [特性标志](./NeoForge-高级-特性标志.md)
