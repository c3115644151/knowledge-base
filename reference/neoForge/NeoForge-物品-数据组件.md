# NeoForge 物品数据组件

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/items/datacomponents

## 概述

数据组件（Data Components）是 NeoForge 1.21.x 引入的核心系统，用于在物品堆栈上存储和同步数据。相比旧版 NBT，数据组件提供了更类型安全、更易用的 API。

## API 速查表

### 核心类型

| 类型 | 说明 |
|------|------|
| `DataComponentType<T>` | 数据组件类型 |
| `PatchedDataComponentMap` | 可修改的组件映射 |
| `DataComponentPatch` | 组件补丁 |
| `MutableDataComponentHolder` | 可变组件持有者 |

### 内置组件

| 组件 | 类型 | 说明 |
|------|------|------|
| `CUSTOM_NAME` | `Component` | 自定义名称 |
| `LORE` | `List<Component>` | 物品描述 |
| `ENCHANTMENTS` | `Map<ResourceKey<Enchantment>, Integer>` | 附魔 |
| `DYED_COLOR` | `int` | 染色颜色 |
| `UNBREAKABLE` | `boolean` | 无法破坏 |
| `MAX_DAMAGE` | `int` | 最大耐久 |
| `DAMAGE` | `int` | 当前耐久损伤 |

---

## 代码示例

### 创建自定义数据组件

```java
// 1. 定义数据组件类型
public static final DataComponentType<Integer> MAX_CHARGE = 
    DataComponentType.<Integer>builder()
        .persistent(Codec.INT)
        .build();

// 2. 注册组件
private static final DeferredRegister.DataComponents DATA_COMPONENTS =
    DeferredRegister.createDataComponents(MOD_ID);

public static final DeferredHolder<DataComponentType<?>, 
        DataComponentType<Integer>> MAX_CHARGE = 
    DATA_COMPONENTS.register("max_charge", 
        () -> DataComponentType.<Integer>builder()
            .persistent(Codec.INT)
            .build());

// 3. 在 mod 初始化时注册
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class Registries {
    @SubscribeEvent
    public static void registerDataComponents(
            RegisterDataComponentTypeEvent event) {
        event.register(MAX_CHARGE);
    }
}
```

### 使用数据组件

```java
// 创建带组件的物品
ItemStack stack = new ItemStack(Items.DIAMOND_SWORD);

// 设置组件
stack.set(DataComponents.MAX_CHARGE, 100);

// 获取组件
int charge = stack.get(DataComponents.MAX_CHARGE).orElse(0);

// 检查是否存在
if (stack.has(DataComponents.MAX_CHARGE)) {
    // ...
}

// 移除组件
stack.remove(DataComponents.MAX_CHARGE);

// 带默认值获取
int value = stack.getOrDefault(DataComponents.MAX_DAMAGE, 0);
```

### 组件补丁 (DataComponentPatch)

```java
// 创建组件补丁
DataComponentPatch patch = DataComponentPatch.builder()
    .add(DataComponents.CUSTOM_NAME, 
        Component.literal("§b冰霜之剑")))
    .add(DataComponents.ENCHANTMENTS, 
        Map.of(Enchantments.FIRE_PROTECTION, 2))
    .remove(DataComponents.DYED_COLOR)  // 移除某个组件
    .build();

// 应用补丁到物品
ItemStack result = stack.copy();
result.apply(patch);
```

### 组件变更监听

```java
public class MyItem extends Item {
    @Override
    public void onAttachedToStack(ItemStack stack) {
        // 当物品附加到玩家背包时调用
        stack.onAttachedToEntity(this, entity);
    }
    
    @Override
    public void onDetachedFromStack(ItemStack stack, LivingEntity entity) {
        // 当物品从玩家背包移除时调用
    }
}

// 监听组件变化（需要注册）
@Mod.EventBusSubscriber(modid = MOD_ID, bus = Mod.EventBusSubscriber.Bus.MOD)
public static class listeners {
    @SubscribeEvent
    public static void onDataComponentInit(
            DataComponentInitializedEvent event) {
        // 注册组件变化监听器
    }
}
```

### 可变物品

```java
// 创建可变物品（允许修改组件）
MutableDataComponentHolder holder = stack.asMutable();

// 设置组件
holder.set(DataComponents.CUSTOM_NAME, 
    Component.literal("修改后的名称"));

// 批量更新
holder.update(DataComponents.ENCHANTMENTS, 
    enchantments -> {
        Map<ResourceKey<Enchantment>, Integer> newMap = 
            new HashMap<>(enchantments);
        newMap.put(Enchantments.SHARPNESS, 1);
        return newMap;
    });
```

---

## 内置组件参考

### 消耗品组件

```java
// 食物属性
stack.set(DataComponents.FOOD, 
    new FoodProperties.Builder()
        .nutrition(4)
        .saturationModifier(0.3f)
        .build());

// 可消耗属性
stack.set(DataComponents.CONSUMABLE, Consumable.of()
    .whenConsumed(
        ConsumeEffect.give(ItemStack(Items.EMERALD, 1))
    )
    .build());
```

### 工具属性

```java
// 工具属性
stack.set(DataComponents.TOOL, new Tool(
    Collections.emptyList(),     // 破坏效果
    2.0f                        // 破坏速度
));

// 盔甲属性
stack.set(DataComponents.ARMOR, new Armor(
    ArmorMaterial.DIAMOND,
    ArmorItem.Type.HELMET,
    new DamageAbsorption(0, 0, 0, 0)
));
```

### 附魔效果组件

```java
// 附魔效果（用于附魔徽章等）
stack.set(DataComponents.ENCHANTMENT_GLINT, true);

// 自定义附魔效果
stack.set(DataComponents.ENCHANTMENT_EFFECTS, 
    List.of(
        EnchantmentEffect.create(
            EnchantmentValueEffect.forEnchantment(
                Enchantments.FIRE_PROTECTION),
            EnchantmentEffectTarget.EQUIPMENT
        )
    ));
```

---

## 注意事项

### 版本差异
- NeoForge 1.21.x 完全重写了数据系统
- 旧版 `getOrCreateTag()` / `getTag()` 已弃用
- 使用 `get()` / `set()` / `remove()` 替代

### 性能考虑
- 频繁修改组件会产生性能开销
- 批量操作使用 `DataComponentPatch` 更高效
- 客户端不需要同步的数据使用 `Transient` 组件

### 序列化
- 组件自动处理网络同步
- 持久化数据需要指定 `Codec`
- 临时数据使用 `Transient` 标记

---

## 关联引用

- 物品注册：[NeoForge-物品](./NeoForge-物品.md)
- 物品交互：[NeoForge-物品-交互](./NeoForge-物品-交互.md)
- 附魔系统：[NeoForge-服务端-附魔](./NeoForge-服务端-附魔.md)
