# NeoForge-数据存储-编解码器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/datastorage/codecs

## 概述

编解码器（Codecs）是来自 Mojang DataFixerUpper 的序列化工具，用于描述对象如何在不同格式（如 JSON 和 NBT）之间转换。

## 使用 Codec

```java
// 编码到 JSON
exampleCodec.encodeStart(JsonOps.INSTANCE, exampleObject);

// 解码 JSON
exampleCodec.parse(JsonOps.INSTANCE, exampleJson);

// 编码到 NBT
exampleCodec.encodeStart(NbtOps.INSTANCE, exampleObject);

// 解码 NBT
exampleCodec.parse(NbtOps.INSTANCE, exampleNbt);
```

## 基础 Codec

| Codec | Java 类型 |
|-------|----------|
| `Codec.BOOL` | Boolean |
| `Codec.BYTE` | Byte |
| `Codec.SHORT` | Short |
| `Codec.INT` | Integer |
| `Codec.LONG` | Long |
| `Codec.FLOAT` | Float |
| `Codec.DOUBLE` | Double |
| `Codec.STRING` | String |
| `Codec.EMPTY` | Unit (null) |

### 带限制的 String

```java
Codec.STRING.string(256)  // 最多 256 字符
Codec.STRING.sizeLimitedString(1024)  // 最多 1024 字符
```

## Record Codec

使用 RecordCodecBuilder 创建 Record 的编解码器：

```java
public record SomeObject(String s, int i, boolean b) {
    public static final Codec<SomeObject> CODEC = RecordCodecBuilder.create(instance ->
        instance.group(
            Codec.STRING.fieldOf("s").forGetter(SomeObject::s),
            Codec.INT.optionalFieldOf("i", 0).forGetter(SomeObject::i),
            Codec.BOOL.fieldOf("b").forGetter(SomeObject::b)
        ).apply(instance, SomeObject::new)
    );
}
```

## 转换器

### xmap

```java
public static final Codec<ClassB> B_CODEC = A_CODEC.xmap(
    ClassA::toB,  // A -> B
    ClassB::toA   // B -> A
);
```

### flatXmap

```java
public static final Codec<Integer> INT_CODEC = Codec.STRING.comapFlatMap(
    s -> {
        try {
            return DataResult.success(Integer.valueOf(s));
        } catch (NumberFormatException e) {
            return DataResult.error(s + " is not an integer.");
        }
    },
    Integer::toString
);
```

### Range Codec

```java
Codec.intRange(0, 4)   // 整数范围
Codec.floatRange(0f, 1f)  // 浮点范围
Codec.doubleRange(0.0, 1.0)  // 双精度范围
```

## 集合

### List

```java
Codec.listOf()  // 无限制
Codec.create(primitive, min, max)  // 有限制
```

### Map

```java
Codec.unboundedMap(Codec.STRING, BlockPos.CODEC)
```

### Pair

```java
Codec.pair(Codec.INT.fieldOf("left").codec(), Codec.STRING.fieldOf("right").codec())
```

## Either

```java
Codec.either(Codec.INT, Codec.STRING)  // 尝试第一个，失败则尝试第二个

// Xor - 只能有一个成功
Codec.xor(Codec.INT.fieldOf("number").codec(), Codec.STRING.fieldOf("text").codec());

// Alternative - 主要编码器优先
Codec.withAlternative(BlockPos.CODEC, otherCodec);
```

## 递归

```java
public record RecursiveObject(Optional<RecursiveObject> inner) {}

public static final Codec<RecursiveObject> RECURSIVE_CODEC = Codec.recursive(
    RecursiveObject.class.getSimpleName(),
    recursedCodec -> RecordCodecBuilder.create(instance ->
        instance.group(
            recursedCodec.optionalFieldOf("inner").forGetter(RecursiveObject::inner)
        ).apply(instance, RecursiveObject::new)
    )
);
```

## 调度

用于基于类型的解码：

```java
public static final Codec<ExampleObject> DISPATCH_CODEC = 
    DISPATCH.byNameCodec().dispatch(
        ExampleObject::type,    // 获取类型的 MapCodec
        Function.identity()      // 从注册表获取编解码器
    );
```

## RegistryOps

用于需要注册表条目的编解码：

```java
RegistryOps<JsonElement> ops = RegistryOps.create(JsonOps.INSTANCE, lookupProvider);
exampleCodec.encodeStart(ops, exampleObject);
```

## DynamicOps 格式转换

```java
// NBT 转 JSON
JsonElement converted = NbtOps.INSTANCE.convertTo(JsonOps.INSTANCE, nbtTag);
```

## DataResult

```java
DataResult<ExampleObject> result = exampleCodec.parse(JsonOps.INSTANCE, json);
result.resultOrPartial(error -> /* 处理错误 */)
       .ifPresent(obj -> /* 使用对象 */);
```

## 注意事项

1. **Record 优先**：使用 Record 定义数据结构
2. **不可变集合**：从 Codec 解码的集合是不可变的
3. **Optional 字段**：使用 `optionalFieldOf` 处理可选字段
4. **Registry 引用**：需要注册表时使用 RegistryOps

## 关联引用

- [[NeoForge-数据存储]] - 数据存储总览
- [[NeoForge-网络-流编解码器]] - StreamCodec
- [[NeoForge-数据存储-值IO]] - Value I/O
