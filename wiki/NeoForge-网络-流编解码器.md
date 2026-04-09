# NeoForge-网络-流编解码器

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/networking/streamcodecs

## 概述

流编解码器（Stream Codecs）是用于描述对象如何存储和读取流（如缓冲区）的序列化工具。主要用于网络同步。

## 使用流编解码器

```java
// 编码到缓冲区
exampleStreamCodec.encode(buffer, exampleObject);

// 从缓冲区解码
ExampleJavaObject obj = exampleStreamCodec.decode(buffer);
```

## 现有流编解码器

### ByteBufCodecs

| 流编解码器 | Java 类型 |
|-----------|----------|
| `BOOL` | Boolean |
| `BYTE` | Byte |
| `SHORT` | Short |
| `INT` | Integer |
| `LONG` | Long |
| `FLOAT` | Float |
| `DOUBLE` | Double |
| `BYTE_ARRAY` | byte[] |
| `LONG_ARRAY` | long[] |
| `STRING_UTF8` | String |
| `TAG` | Tag |
| `COMPOUND_TAG` | CompoundTag |
| `VECTOR3F` | Vector3fc |
| `QUATERNIONF` | Quaternionfc |

### 可变长度数字

```java
ByteBufCodecs.VAR_INT  // 可变整数（0 到 2^28-1）
ByteBufCodecs.VAR_LONG // 可变长整数（0 到 2^56-1）
```

### 受信任标签

```java
ByteBufCodecs.TRUSTED_TAG        // 无大小限制的标签
ByteBufCodecs.TRUSTED_COMPOUND_TAG // 无大小限制的复合标签
```

## 创建流编解码器

### 成员编码器

```java
public class ExampleObject {
    public ExampleObject(String arg1, int arg2, boolean arg3) {}
    public ExampleObject(ByteBuf buffer) {}  // 解码
    public void encode(ByteBuf buffer) {}     // 编码
}

public static final StreamCodec<ByteBuf, ExampleObject> STREAM_CODEC =
    StreamCodec.ofMember(ExampleObject::encode, ExampleObject::new);
```

### 复合流编解码器

```java
public record SimpleExample(String arg1, int arg2, boolean arg3) {}

public static final StreamCodec<ByteBuf, SimpleExample> SIMPLE_CODEC =
    StreamCodec.composite(
        ByteBufCodecs.STRING_UTF8, SimpleExample::arg1,
        ByteBufCodecs.VAR_INT, SimpleExample::arg2,
        ByteBufCodecs.BOOL, SimpleExample::arg3,
        SimpleExample::new
    );
```

### 单位流编解码器

```java
// 不编码任何信息，提供固定值
public static final StreamCodec<ByteBuf, Item> UNIT_CODEC =
    StreamCodec.unit(Items.AIR);
```

### 集合

```java
public static final StreamCodec<ByteBuf, Set<BlockPos>> SET_CODEC =
    ByteBufCodecs.collection(
        HashSet::new,
        BlockPos.STREAM_CODEC,
        256  // 最大大小
    );

public static final StreamCodec<ByteBuf, List<BlockPos>> LIST_CODEC =
    BlockPos.STREAM_CODEC.apply(ByteBufCodecs.list(256));
```

### Map

```java
public static final StreamCodec<ByteBuf, Map<String, BlockPos>> MAP_CODEC =
    ByteBufCodecs.map(
        HashMap::new,
        ByteBufCodecs.STRING_UTF8,
        BlockPos.STREAM_CODEC,
        256
    );
```

### Optional

```java
public static final StreamCodec<RegistryFriendlyByteBuf, Optional<DataComponentType<?>>> OPTIONAL_CODEC =
    DataComponentType.STREAM_CODEC.apply(ByteBufCodecs::optional);
```

### 注册表对象

```java
// 注册表对象
public static final StreamCodec<RegistryFriendlyByteBuf, Item> VALUE_CODEC =
    ByteBufCodecs.registry(Registries.ITEM);

// Holder
public static final StreamCodec<RegistryFriendlyByteBuf, Holder<Item>> HOLDER_CODEC =
    ByteBufCodecs.holderRegistry(Registries.ITEM);
```

### ID 映射器

```java
public enum ExampleIdObject {
    VALUE1, VALUE2, VALUE3;
    
    public static final IntFunction<ExampleIdObject> BY_ID = 
        ByIdMap.continuous(ExampleIdObject::getId, ExampleIdObject.values(), ByIdMap.OutOfBoundsStrategy.ZERO);
}

public static final StreamCodec<ByteBuf, ExampleIdObject> ID_CODEC =
    ByteBufCodecs.idMapper(ExampleIdObject.BY_ID, ExampleIdObject::getId);
```

### Holder 集合

```java
public static final StreamCodec<RegistryFriendlyByteBuf, HolderSet<Item>> HOLDER_SET_CODEC =
    ByteBufCodecs.holderSet(Registries.ITEM);
```

### 递归

```java
public record RecursiveObject(Optional<RecursiveObject> inner) {}

public static final StreamCodec<ByteBuf, RecursiveObject> RECURSIVE_CODEC = 
    StreamCodec.recursive(recursedStreamCodec ->
        StreamCodec.composite(
            recursedStreamCodec.apply(ByteBufCodecs::optional),
            RecursiveObject::inner,
            RecursiveObject::new
        )
    );
```

## 转换器

```java
// map - 转换值
public static final StreamCodec<ByteBuf, Identifier> IDENTIFIER_CODEC = 
    ByteBufCodecs.STRING_UTF8.map(
        Identifier::new,
        Identifier::toString
    );

// mapStream - 转换缓冲区
public static final StreamCodec<RegistryFriendlyByteBuf, Integer> INT_CODEC =
    ByteBufCodecs.VAR_INT.mapStream(buffer -> (ByteBuf) buffer);
```

## 注意事项

1. **缓冲区类型**：`ByteBuf`、`FriendlyByteBuf`、`RegistryFriendlyByteBuf`
2. **泛型顺序**：泛型 `B` 是缓冲区，`V` 是值
3. **兼容性**：`? super B` 意味着所有三种缓冲区类型都可用
4. **可变编码**：优先使用 `VAR_INT`/`VAR_LONG` 减少带宽

## 关联引用

- [[NeoForge-网络基础]] - 网络通信基础
- [[NeoForge-网络-Payload]] - Payload 注册
- [[NeoForge-数据存储-编解码器]] - Codec 编解码器
