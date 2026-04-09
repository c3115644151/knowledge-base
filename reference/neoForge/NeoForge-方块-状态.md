# NeoForge-方块-状态

> 版本：1.21.11 / NeoForge 26.1.x
> 源文档：https://docs.neoforged.net/docs/blocks/states

## 概述

Blockstates（方块状态）是一种表示方块不同状态的简单方式。例如，小麦作物有8个生长阶段，为每个阶段创建一个单独的方块会显得很不合理。或者对于台阶方块——底部状态、顶部状态和双台阶状态。这就是 Blockstates 的用武之地。

## Blockstate 属性

Blockstates 使用属性系统。一个方块可以有多种类型的多个属性。例如，末影传送门框架有两个属性：是否有眼（`eye`，2个选项）和朝向（`facing`，4个选项）。因此，末影传送门框架总共有 8（2 × 4）个不同的方块状态：

```
minecraft:end_portal_frame[facing=north,eye=false]
minecraft:end_portal_frame[facing=east,eye=false]
minecraft:end_portal_frame[facing=south,eye=false]
minecraft:end_portal_frame[facing=west,eye=false]
minecraft:end_portal_frame[facing=north,eye=true]
minecraft:end_portal_frame[facing=east,eye=true]
minecraft:end_portal_frame[facing=south,eye=true]
minecraft:end_portal_frame[facing=west,eye=true]
```

`blockid[property1=value1,property2=value,...]` 是以文本形式表示方块状态的标准方式。

如果没有定义任何 blockstate 属性，它仍然有恰好一个方块状态——没有属性的那个。可以表示为 `minecraft:oak_planks[]` 或简写为 `minecraft:oak_planks`。

每个 `BlockState` 在内存中只存在一次。可以使用 `==` 比较。`BlockState` 是 final 类，不能被扩展。**所有功能都放在对应的 Block 类中！**

## 何时使用 Blockstates

### Blockstates vs 分离方块

经验法则：**如果名称不同，就应该是一个单独的方块**。例如椅子方块：椅子的方向应该是属性，而不同类型的木头应该分成不同的方块。

### Blockstates vs Block Entities

规则：**如果是有限数量的状态，使用 blockstate；如果是无限或近乎无限数量的状态，使用 block entity**。Block entity 可以存储任意数量的数据，但比 blockstate 慢。

Blockstates 和 block entity 可以结合使用。例如，箱子使用 blockstate 属性来管理方向、是否含水或成为双箱子，而存储物品栏、是否打开或与漏斗交互则由 block entity 处理。

## API 速查表

### 属性类型

| 类型 | 类 | 创建方法 |
|------|-----|---------|
| 整数属性 | `IntegerProperty` | `IntegerProperty.create(name, min, max)` |
| 布尔属性 | `BooleanProperty` | `BooleanProperty.create(name)` |
| 枚举属性 | `EnumProperty<E>` | `EnumProperty.create(name, EnumClass.class)` |

### Block 方法

| 方法 | 说明 |
|------|------|
| `createBlockStateDefinition(StateDefinition.Builder)` | 重写此方法添加属性 |
| `registerDefaultState(BlockState)` | 设置默认状态 |
| `getStateForPlacement(BlockPlaceContext)` | 设置放置时的状态 |

### BlockState 方法

| 方法 | 说明 |
|------|------|
| `getValue(Property<?>)` | 获取属性值 |
| `setValue(Property<T>, T)` | 设置属性值（返回新的 BlockState） |
| `defaultBlockState()` | 获取默认状态 |

## 代码示例

### 基本实现

```java
public class MyBlock extends Block {
    // 使用 BlockStateProperties 中的共享属性
    public static final EnumProperty<Direction> FACING = BlockStateProperties.FACING;
    public static final BooleanProperty POWERED = BlockStateProperties.POWERED;

    public MyBlock(BlockBehaviour.Properties properties) {
        super(properties);
        // 注册默认状态
        this.registerDefaultState(
            this.stateDefinition.any()
                .setValue(FACING, Direction.NORTH)
                .setValue(POWERED, false)
        );
    }

    @Override
    protected void createBlockStateDefinition(StateDefinition.Builder<Block, BlockState> builder) {
        builder.add(FACING, POWERED);
    }

    @Override
    public BlockState getStateForPlacement(BlockPlaceContext context) {
        // 根据放置方向设置 FACING
        return this.defaultBlockState()
            .setValue(FACING, context.getHorizontalDirection().getOpposite());
    }
}
```

### 使用属性

```java
// 获取属性值
Direction direction = blockState.getValue(MyBlock.FACING);
boolean powered = blockState.getValue(MyBlock.POWERED);

// 设置属性值（BlockState 是不可变的）
BlockState newState = blockState.setValue(MyBlock.POWERED, true);
```

## Level#setBlock 更新标志

```java
// 设置方块状态
level.setBlock(pos, newState, flags);

// 常用标志（可位运算组合）
Block.UPDATE_NEIGHBORS     // 通知邻居方块
Block.UPDATE_CLIENTS        // 同步到客户端
Block.UPDATE_INVISIBLE     // 不在客户端更新
Block.UPDATE_IMMEDIATE      // 立即渲染
Block.UPDATE_NONE          // = UPDATE_INVISIBLE | UPDATE_SKIP_BLOCK_ENTITY_SIDEEFFECTS
Block.UPDATE_ALL           // = UPDATE_NEIGHBORS | UPDATE_CLIENTS
Block.UPDATE_ALL_IMMEDIATE // = UPDATE_NEIGHBORS | UPDATE_CLIENTS | UPDATE_IMMEDIATE

// 便捷方法
level.setBlockAndUpdate(pos, newState); // 等同于 setBlock(pos, newState, Block.UPDATE_ALL)
```

## 注意事项

1. **BlockState 是不可变的**：`setValue()` 不会修改原对象，而是返回一个新对象
2. **每个 BlockState 只存在一次**：可以使用 `==` 比较
3. **功能放在 Block 类中**：不要在 BlockState 中添加逻辑
4. **属性数量限制**：如果需要超过 8-9 位数据（约几百个状态），应使用 BlockEntity

## 关联引用

- [[NeoForge-方块]] - 方块注册与基础
- [[NeoForge-方块实体]] - BlockEntity 创建、数据存储
- [[NeoForge-资源]] - 模型、纹理等资源系统
