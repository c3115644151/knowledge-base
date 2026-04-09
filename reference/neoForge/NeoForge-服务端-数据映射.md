# NeoForge-服务端-数据映射

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/resources/server/datamaps/

## 概述

数据映射（Data Maps）是数据驱动的、可重载的对象，可以附加到注册对象。类似于标签（Tags），但数据映射是注册对象到对象的映射，而非布尔值。

## 文件位置

`data/<mapNamespace>/data_maps/<registryNamespace>/<registryPath>/<mapPath>.json`

示例：
- `examplemod/data_maps/item/drop_healing.json` → `examplemod:drop_healing` 用于 `minecraft:item`

## JSON 结构

```json
{
    "replace": false,
    "values": {
        "minecraft:carrot": {
            "amount": 12,
            "chance": 1.0
        },
        "#minecraft:logs": {
            "amount": 1,
            "chance": 0.1
        }
    },
    "remove": ["minecraft:potato"]
}
```

## 创建自定义数据映射

### 定义数据映射条目（Record）

```java
public record ExampleData(float amount, float chance) {
    public static final Codec<ExampleData> CODEC = RecordCodecBuilder.create(instance ->
        instance.group(
            Codec.FLOAT.fieldOf("amount").forGetter(ExampleData::amount),
            Codec.floatRange(0, 1).fieldOf("chance").forGetter(ExampleData::chance)
        ).apply(instance, ExampleData::new)
    );
}
```

### 创建数据映射

```java
public static final DataMapType<Item, ExampleData> EXAMPLE_DATA = DataMapType.builder(
    Identifier.fromNamespaceAndPath("examplemod", "example_data"),
    Registries.ITEM,
    ExampleData.CODEC
).build();
```

### 注册数据映射

```java
@SubscribeEvent
public static void registerDataMapTypes(RegisterDataMapTypesEvent event) {
    event.register(EXAMPLE_DATA);
}
```

## 同步数据映射

```java
public static final DataMapType<Item, ExampleData> EXAMPLE_DATA = DataMapType.builder(...)
    .synced(
        ExampleData.CODEC,  // 同步用的 Codec
        false              // 是否强制同步
    ).build();
```

## 使用数据映射

```java
@SubscribeEvent
public static void itemPickup(ItemEntityPickupEvent.Post event) {
    ItemStack stack = event.getOriginalStack();
    Holder<Item> holder = stack.getItemHolder();
    ExampleData data = holder.getData(EXAMPLE_DATA);
    
    if (data != null) {
        Player player = event.getPlayer();
        if (player.getLevel().getRandom().nextFloat() > data.chance()) {
            player.heal(data.amount());
        }
    }
}
```

## 高级数据映射

### 自定义合并器

```java
public class IntMerger implements DataMapValueMerger<Item, Integer> {
    @Override
    public Integer merge(Registry<Item> registry,
            Either<TagKey<Item>, ResourceKey<Item>> first, Integer firstValue,
            Either<TagKey<Item>, ResourceKey<Item>> second, Integer secondValue) {
        return firstValue + secondValue;
    }
}

// 使用
AdvancedDataMapType<Item, Integer> ADVANCED_MAP = AdvancedDataMapType.builder(...)
    .merger(new IntMerger())
    .build();
```

### 自定义移除器

```java
public record MapRemover(String key) implements DataMapValueRemover<Item, Map<String, String>> {
    public static final Codec<MapRemover> CODEC = Codec.STRING.xmap(MapRemover::new, MapRemover::key);

    @Override
    public Optional<Map<String, String>> remove(Map<String, String> value, Registry<Item> registry,
            Either<TagKey<Item>, ResourceKey<Item>> source, Item object) {
        final Map<String, String> newMap = new HashMap<>(value);
        newMap.remove(key);
        return Optional.of(newMap);
    }
}
```

## 数据生成

```java
public class MyDataMapProvider extends DataMapProvider {
    @Override
    protected void gather() {
        this.builder(EXAMPLE_DATA)
            .replace(true)
            .add(ItemTags.SLABS, new ExampleData(10, 1), false)
            .add(Items.APPLE.builtInRegistryHolder(), new ExampleData(5, 0.2f), false)
            .remove(ItemTags.WOODEN_SLABS)
            .conditions(new ModLoadedCondition("botania"));
    }
}

@SubscribeEvent
public static void gatherData(GatherDataEvent.Client event) {
    event.createProvider(MyDataMapProvider::new);
}
```

## 注意事项

1. **不可变条目**：数据映射条目必须不可变
2. **通过 Holder 查询**：必须通过 `Holder` 查询，不能直接用注册对象
3. **可重载**：支持通过 `/reload` 命令重载
4. **合并行为**：默认合并器会覆盖，低优先级包的值被高优先级包覆盖

## 关联引用

- [[NeoForge-服务端资源]] - 服务端资源总览
- [[NeoForge-服务端-标签]] - 标签系统
- [[NeoForge-数据存储-附件]] - 数据附件系统
