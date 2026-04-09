# NeoForge-数据存储-值IO

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/datastorage/valueio

## 概述

Value I/O（值输入/输出）系统是操作数据的标准化序列化方法，如 NBT 的 CompoundTag。

## 输入和输出

```java
// BlockEntity 保存
@Override
protected void saveAdditional(ValueOutput output) {
    super.saveAdditional(output);
    output.putBoolean("boolValue", true);
    output.putString("stringValue", "Hello!");
}

// BlockEntity 加载
@Override
protected void loadAdditional(ValueInput input) {
    super.loadAdditional(input);
    boolean boolValue = input.getBooleanOr("boolValue", false);
    String stringValue = input.getStringOr("stringValue", "Default");
}

// Entity 保存
@Override
protected void addAdditionalSaveData(ValueOutput output) {
    super.addAdditionalSaveData(output);
}

// Entity 加载
@Override
protected void readAdditionalSaveData(ValueInput input) {
    super.readAdditionalSaveData(input);
}
```

## 基础类型

| 类型 | ValueOutput | ValueInput |
|------|-------------|-----------|
| boolean | `putBoolean(key, value)` | `getBooleanOr(key, default)` |
| byte | `putByte(key, value)` | `getByteOr(key, default)` |
| short | `putShort(key, value)` | `getShortOr(key, default)` |
| int | `putInt(key, value)` | `getIntOr(key, default)` / `getInt(key)` |
| long | `putLong(key, value)` | `getLongOr(key, default)` / `getLong(key)` |
| float | `putFloat(key, value)` | `getFloatOr(key, default)` |
| double | `putDouble(key, value)` | `getDoubleOr(key, default)` |
| String | `putString(key, value)` | `getStringOr(key, default)` / `getString(key)` |
| int[] | `putIntArray(key, value)` | `getIntArray(key)` |

## Codec 使用

```java
// 保存
output.storeNullable("codecValue", Rarity.CODEC, Rarity.EPIC);

// 加载
Optional<Rarity> codecValue = input.read("codecValue", Rarity.CODEC);

// 使用 MapCodec
output.store(SingleFile.MAP_CODEC, new SingleFile(id));
Optional<SingleFile> file = input.read(SingleFile.MAP_CODEC);
```

## 列表

### 子列表

```java
// 保存
ValueOutput.ValueOutputList listValue = output.childrenList("listValue");
ValueOutput child0 = listValue.addChild();
child0.putBoolean("boolChild", false);
ValueOutput child1 = listValue.addChild();
child1.putInt("intChild", 42);

// 加载
for (ValueInput childInput : input.childrenListOrEmpty("listValue")) {
    boolean boolChild = childInput.getBooleanOr("boolChild", false);
}
```

### Typed 列表

```java
// 保存
ValueOutput.TypedInputList<Rarity> listValue = output.list("rarities", Rarity.CODEC);
listValue.add(Rarity.COMMON);
listValue.add(Rarity.EPIC);

// 加载
for (Rarity rarity : input.listOrEmpty("rarities", Rarity.CODEC)) {
    // ...
}
```

## 对象

```java
// 保存
ValueOutput objectValue = output.child("objectValue");
objectValue.putBoolean("boolChild", true);
objectValue.putInt("intChild", 20);

// 加载
ValueInput objectValue = input.childOrEmpty("objectValue");
boolean boolChild = objectValue.getBooleanOr("boolChild", false);
int intChild = objectValue.getIntOr("intChild", 0);
```

## NBT 实现

```java
// 创建输出
TagValueOutput output = TagValueOutput.createWithContext(ProblemReporter.DISCARDING, lookupProvider);
// 写入...
CompoundTag tag = output.buildResult();

// 创建输入
ProblemReporter.Collector reporter = new ProblemReporter.Collector(new RootFieldPathElement("example"));
TagValueInput input = TagValueInput.create(reporter, lookupProvider, tag);
// 读取...
```

## ValueIOSerializable

NeoForge 添加的接口：

```java
public class ExampleObject implements ValueIOSerializable {
    @Override
    public void serialize(ValueOutput output) {
        output.putString("name", "example");
        output.putInt("value", 42);
    }

    @Override
    public void deserialize(ValueInput input) {
        // 读取值
    }
}
```

## 注意事项

1. **调用 super**：保存和加载时先调用父类方法
2. **空列表**：列表为空时不写入，使用 `discard()`
3. **MapCodec 冲突**：注意 MapCodec 可能覆盖现有键
4. **ProblemReporter**：处理编码/解码错误

## 关联引用

- [[NeoForge-数据存储]] - 数据存储总览
- [[NeoForge-数据存储-编解码器]] - Codec 编解码器
- [[NeoForge-方块实体]] - BlockEntity 数据存储
