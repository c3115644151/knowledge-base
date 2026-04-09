# NeoForge StreamCodec 系统

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/networking/streamcodecs

## 概述

StreamCodec 用于在网络缓冲区中序列化和反序列化数据。

## API 速查表

### ByteBufCodecs 基础类型

| 方法 | 类型 |
|------|------|
| `BYTE` | `byte` |
| `INT` | `int` |
| `VAR_INT` | 可变 int |
| `LONG` | `long` |
| `VAR_LONG` | 可变 long |
| `FLOAT` | `float` |
| `DOUBLE` | `double` |
| `BOOLEAN` | `boolean` |
| `STRING` | `String` |
| `COMPONENT` | `Component` |

### 复合编解码器

| 方法 | 说明 |
|------|------|
| `StreamCodec.composite()` | 组合多个编解码器 |
| `ByteBufCodecs.list()` | 列表 |
| `ByteBufCodecs.set()` | 集合 |
| `ByteBufCodecs.map()` | Map |
| `ByteBufCodecs.optional()` | Optional |

---

## 代码示例

### 基本用法

```java
// 1. 定义编解码器
public static final StreamCodec<FriendlyByteBuf, MyData> CODEC = 
    StreamCodec.unit(
        new MyData(42, "hello"),
        data -> {
            FriendlyByteBuf buf = new FriendlyByteBuf(Unpooled.buffer());
            buf.writeInt(data.value());
            buf.writeUtf(data.message());
            return buf;
        },
        buf -> new MyData(buf.readInt(), buf.readUtf())
    );

// 2. Record 用法
public record MyData(int value, String message) {
    public static final StreamCodec<FriendlyByteBuf, MyData> CODEC = 
        StreamCodec.composite(
            ByteBufCodecs.VAR_INT, MyData::value,
            ByteBufCodecs.STRING_UTF8, MyData::message,
            MyData::new
        );
}
```

### 复杂类型

```java
// 列表
StreamCodec<FriendlyByteBuf, List<ItemStack>> LIST_CODEC = 
    ByteBufCodecs.list(ItemStack.OPTIONAL_SMALL_NBT);

// Map
StreamCodec<FriendlyByteBuf, Map<String, Integer>> MAP_CODEC = 
    ByteBufCodecs.map(
        HashMap::new,
        ByteBufCodecs.STRING_UTF8, ByteBufCodecs.VAR_INT);

// Optional
StreamCodec<FriendlyByteBuf, Optional<Component>> OPT_CODEC = 
    ByteBufCodecs.optional(ByteBufCodecs.COMPONENT);
```

---

## 注意事项

### 性能考虑
- 使用 `VAR_INT` 代替 `INT` 减少字节数
- 避免频繁创建新对象

### 常见错误
1. **读写不匹配**：`read` 和 `write` 必须对称
2. **缓冲区管理**：正确释放缓冲区

---

## 关联引用

- 网络 Payload：[NeoForge-网络-Payload](./NeoForge-网络-Payload.md)
